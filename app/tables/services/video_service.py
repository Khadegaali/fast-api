from fastapi import UploadFile
from uuid import UUID
import asyncio
import tempfile
import subprocess
import os
from app.tables.repositories.video_repository import VideoRepository
from app.client.llm_client.cohere_client import CohereClient
from app.client.llm_client.storage_client import VideoStorageClient
from sqlalchemy.orm import Session
from pytubefix import YouTube
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

CHUNK_DURATION_SECONDS = 120

class VideoService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = VideoRepository(db)
        self.storage = VideoStorageClient()
        self.cohere = CohereClient()

    async def upload_video_url(self, user_id: UUID, video_url: str):
        info = await asyncio.to_thread(self._get_youtube_info, video_url)

        youtube_video_id = info["youtube_video_id"]
        title = info["title"] or "Untitled Video"
        duration = info["duration"]
        transcript_segments = info["segments"]
        transcript_text = info["transcript"]
        description = info["description"]

        # Check if video already exists by youtube_video_id
        video = self.repo.get_video_by_youtube_id(youtube_video_id)

        if not video:
            # New video — process and save
            topic = self.cohere.generate_topic(transcript_text) if transcript_text else None

            video = self.repo.save_video(
                youtube_video_id=youtube_video_id,
                video_url=video_url,
                title=title,
                description=description,
                duration=duration,
                topic=topic,
            )

            # Save chunks with embeddings
            if transcript_segments:
                chunks = self._split_transcript_into_chunks(transcript_segments)
            elif transcript_text:
                chunks = self._split_transcript_into_chunks_from_text(transcript_text)
            else:
                chunks = []

            if chunks:
                embeddings = [
                    self.cohere.get_embedding(chunk, input_type="search_document")
                    for chunk in chunks
                ]
                self.repo.save_chunks(video.id, chunks, embeddings)

        # Always link user to video
        self.repo.save_user_video(user_id=user_id, video_id=video.id)
        self.db.refresh(video)
        _ = video.chunks
        return video

    async def upload_video_file(self, user_id: UUID, file: UploadFile,
                                youtube_url: str = None):
        video_content = await file.read()
        duration = await asyncio.to_thread(self._get_video_duration_from_file, video_content)

        upload_result = await asyncio.to_thread(
            self.storage.upload_video,
            user_id=str(user_id),
            file_content=video_content,
            filename=file.filename
        )
        video_url = upload_result["url"]

        transcript_text = ""
        segments = []
        youtube_video_id = None

        if youtube_url:
            info = await asyncio.to_thread(self._get_youtube_info, youtube_url)
            transcript_text = info["transcript"]
            segments = info["segments"]
            youtube_video_id = info["youtube_video_id"]

        title = self.cohere.generate_title(transcript_text) if transcript_text else file.filename
        description = self.cohere.generate_description(transcript_text) if transcript_text else None
        topic = self.cohere.generate_topic(transcript_text) if transcript_text else None

        video = self.repo.save_video(
            youtube_video_id=youtube_video_id or video_url,
            video_url=video_url,
            title=title,
            description=description,
            duration=duration,
            topic=topic,
        )

        if segments:
            chunks = self._split_transcript_into_chunks(segments)
        elif transcript_text:
            chunks = self._split_transcript_into_chunks_from_text(transcript_text)
        else:
            chunks = []

        if chunks:
            embeddings = [
                self.cohere.get_embedding(chunk, input_type="search_document")
                for chunk in chunks
            ]
            self.repo.save_chunks(video.id, chunks, embeddings)

        self.repo.save_user_video(user_id=user_id, video_id=video.id)

        return video

    def _get_youtube_info(self, video_url: str) -> dict:
        result = {
            "youtube_video_id": None,
            "title": None,
            "duration": 0,
            "transcript": "",
            "description": None,
            "segments": []
        }

        if "youtube.com" not in video_url and "youtu.be" not in video_url:
            return result

        try:
            yt = YouTube(video_url)
            result["youtube_video_id"] = yt.video_id
            result["title"] = yt.title
            result["duration"] = yt.length or 0
            result["description"] = yt.description
        except Exception as e:
            print(f" YouTube info error: {e}")

        try:
            ytt = YouTubeTranscriptApi()
            transcript_segments = ytt.fetch(result["youtube_video_id"])
            result["segments"] = transcript_segments
            result["transcript"] = " ".join([t.text for t in transcript_segments])
        except (TranscriptsDisabled, NoTranscriptFound):
            pass
        except Exception as e:
            print(f" Transcript error: {e}")

        return result

    def _split_transcript_into_chunks(self, transcript_segments: list, chunk_duration: int = CHUNK_DURATION_SECONDS) -> list[str]:
        if not transcript_segments:
            return []

        sorted_segments = sorted(transcript_segments, key=lambda s: s.start if hasattr(s, 'start') else s['start'])

        chunks = []
        current_chunk = []
        chunk_start_time = 0

        for segment in sorted_segments:
            seg_start = segment.start if hasattr(segment, 'start') else segment['start']
            seg_text = segment.text if hasattr(segment, 'text') else segment['text']

            if seg_start - chunk_start_time >= chunk_duration and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                chunk_start_time = seg_start

            current_chunk.append(seg_text)

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def _split_transcript_into_chunks_from_text(self, text: str, words_per_chunk: int = 300) -> list[str]:
        words = text.split()
        return [" ".join(words[i:i+words_per_chunk]) for i in range(0, len(words), words_per_chunk)]

    def _get_video_duration_from_file(self, video_content: bytes) -> int:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                tmp.write(video_content)
                tmp_path = tmp.name
            result = subprocess.run(
                ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                 '-of', 'default=noprint_wrappers=1:nokey=1', tmp_path],
                capture_output=True, text=True
            )
            os.unlink(tmp_path)
            return int(float(result.stdout.strip()))
        except:
            return 0