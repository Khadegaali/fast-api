from fastapi import UploadFile
from uuid import UUID
import asyncio
import pdfplumber
import io
from app.tables.repositories.cv_repository import CVRepository
from app.client.llm_client.cohere_client import CohereClient
from app.client.llm_client.storage_client import CVStorageClient
from sqlalchemy.orm import Session

class CVService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = CVRepository(db)
        self.storage = CVStorageClient()
        self.cohere = CohereClient()

    async def upload_cv(self, user_id: UUID, file: UploadFile):
        file_content = await file.read()

        cv_text = await asyncio.to_thread(self._extract_text_from_pdf, file_content)
        analysis = self.cohere.analyze_cv(cv_text)
        existing_cv = self.repo.get_by_user_id(user_id)

        if existing_cv:
            await asyncio.to_thread(self.storage.delete_cv, existing_cv.file_path)
            upload_result = await asyncio.to_thread(
                self.storage.upload_cv,
                user_id=str(user_id),
                file_content=file_content,
                filename=file.filename
            )
            return self.repo.update_cv(
                cv=existing_cv,
                file_path=upload_result["file_path"],
                file_url=upload_result["file_url"],
                file_name=upload_result["file_name"],
                graduation_year=analysis.get("graduation_year"),
                education=analysis.get("education"),
                technical_skills=analysis.get("technical_skills"),
                experience=analysis.get("experience"),      # 👈
                summary=analysis.get("summary"),
            )
        else:
            upload_result = await asyncio.to_thread(
                self.storage.upload_cv,
                user_id=str(user_id),
                file_content=file_content,
                filename=file.filename
            )
            return self.repo.save_cv(
                user_id=user_id,
                file_path=upload_result["file_path"],
                file_url=upload_result["file_url"],
                file_name=upload_result["file_name"],
                graduation_year=analysis.get("graduation_year"),
                education=analysis.get("education"),
                technical_skills=analysis.get("technical_skills"),
                experience=analysis.get("experience"),      # 👈
                summary=analysis.get("summary"),
            )

    async def get_my_cv(self, user_id: UUID):
        cv = self.repo.get_by_user_id(user_id)
        if not cv:
            return None
        cv.file_url = await asyncio.to_thread(
            self.storage.get_signed_url, cv.file_path
        )
        return cv

    def _extract_text_from_pdf(self, file_content: bytes) -> str:
        try:
            with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                return " ".join([page.extract_text() or "" for page in pdf.pages])
        except Exception:
            return ""