from sqlalchemy.orm import Session
from app.tables.models.cv_model import CV
from uuid import UUID

class CVRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self, user_id: UUID):
        return self.db.query(CV).filter(CV.user_id == user_id).first()

    def save_cv(
        self,
        user_id: UUID,
        file_path: str,
        file_url: str,
        file_name: str,
        name: str = None,
        phone: str = None,
        graduation_year: str = None,
        education: str = None,
        technical_skills: list = None,
        experience: str = None,
        summary: str = None,
    ):
        cv = CV(
            user_id=user_id,
            file_path=file_path,
            file_url=file_url,
            file_name=file_name,
            name=name,
            phone=phone,
            graduation_year=graduation_year,
            education=education,
            technical_skills=technical_skills,
            experience=experience,
            summary=summary,
        )
        self.db.add(cv)
        self.db.commit()
        self.db.refresh(cv)
        return cv

    def update_cv(
        self,
        cv: CV,
        file_path: str,
        file_url: str,
        file_name: str,
        name: str = None,
        phone: str = None,
        graduation_year: str = None,
        education: str = None,
        technical_skills: list = None,
        experience: str = None,
        summary: str = None,
    ):
        cv.file_path = file_path
        cv.file_url = file_url
        cv.file_name = file_name
        cv.name = name
        cv.phone = phone
        cv.graduation_year = graduation_year
        cv.education = education
        cv.technical_skills = technical_skills
        cv.experience = experience
        cv.summary = summary
        self.db.commit()
        self.db.refresh(cv)
        return cv

    def delete_cv(self, cv: CV):
        self.db.delete(cv)
        self.db.commit()