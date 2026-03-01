from sqlalchemy.orm import Session
from app.tables.models.video_model import Video, VideoChunk, UserVideo
from uuid import UUID

class VideoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_video_by_youtube_id(self, youtube_video_id: str):
        return self.db.query(Video).filter(
            Video.youtube_video_id == youtube_video_id
        ).first()

    def save_video(
        self,
        youtube_video_id: str,
        video_url: str,
        title: str,
        description: str = None,
        duration: int = 0,
        topic: str = None,
    ):
        video = Video(
            youtube_video_id=youtube_video_id,
            video_url=video_url,
            title=title,
            description=description,
            duration=duration,
            topic=topic,
        )
        self.db.add(video)
        self.db.commit()
        self.db.refresh(video)
        return video

    def save_user_video(self, user_id: UUID, video_id: UUID):
        # Check if user already saved this video
        existing = self.db.query(UserVideo).filter(
            UserVideo.user_id == user_id,
            UserVideo.video_id == video_id
        ).first()
        if existing:
            return existing

        user_video = UserVideo(user_id=user_id, video_id=video_id)
        self.db.add(user_video)
        self.db.commit()
        self.db.refresh(user_video)
        return user_video

    def save_chunks(self, video_id: UUID, chunks: list[str], embeddings: list):
        total = len(chunks)
        for i, (content, embedding) in enumerate(zip(chunks, embeddings)):
            chunk = VideoChunk(
                video_id=video_id,
                content=content,
                chunk_num=i + 1,
                total_chunks=total,
                chunk_embedding=embedding
            )
            self.db.add(chunk)
        self.db.commit()


    def get_user_videos(self, user_id: UUID):
        return self.db.query(Video).join(UserVideo).filter(
            UserVideo.user_id == user_id
        ).order_by(UserVideo.created_at.desc()).all()

    def get_video_by_id(self, video_id: UUID):
        return self.db.query(Video).filter(Video.id == video_id).first()

    def get_chunk_by_id(self, chunk_id: UUID):
       return self.db.query(VideoChunk).filter(VideoChunk.id == chunk_id).first()

    def delete_user_video(self, video_id: UUID, user_id: UUID):
        user_video = self.db.query(UserVideo).filter(
            UserVideo.video_id == video_id,
            UserVideo.user_id == user_id
        ).first()
        if user_video:
            self.db.delete(user_video)
            self.db.commit()
            return True
        return False
