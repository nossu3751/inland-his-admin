import traceback
from app.models.app_patch import AppPatch
from app.extensions import db
from sqlalchemy import select



class AppPatchService:
    
    
    @staticmethod
    def get_all_app_patches():
        try:
            stmt = select(AppPatch).order_by(AppPatch.id.desc())
            return db.session.execute(stmt).scalars()
        except Exception:
            return None
    
    @staticmethod
    def create_app_patch(data):
        try:
            new_patch = AppPatch(**data)
            db.session.add(new_patch)
            db.session.commit()

            return new_patch
        except Exception:
            db.session.rollback()
            raise Exception("discussion create failed")
        