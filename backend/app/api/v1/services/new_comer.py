import os
from datetime import datetime
import traceback
from app.api.v1.exceptions.new_comer import *
from app.models.new_comer import NewComer
from app.extensions import db
from sqlalchemy import select


class NewComerService:

    @staticmethod
    def get_all_new_comers():
        stmt = select(NewComer).order_by(NewComer.registered_at)
        return db.session.execute(stmt).scalars()
    
    @staticmethod
    def get_new_comer_by_id(id):
        stmt = select(NewComer).where(NewComer.id == id)
        return db.session.execute(stmt).scalar_one_or_none()
    
    @staticmethod
    def delete_new_comer_by_id(id):
        new_comer = NewComerService.get_new_comer_by_id(id)
        try:
            db.session.delete(new_comer)
            db.session.commit()
        except Exception:
            traceback.print_exc()
            db.session.rollback()
            raise NewComerNotDeletedException("Couldn't delete new comer")
    
    @staticmethod
    def update_new_comer(id, update_data):
        try:
            # Step 2: Retrieve the SmallGroupNote object by its ID
            new_comer = NewComerService.get_new_comer_by_id(id)

            if new_comer is None:
                return None
            
            # Step 3: Update the desired fields of the object
            for field, value in update_data.items():
                if hasattr(new_comer, field):
                    setattr(new_comer, field, value)

            db.session.commit()

            return new_comer
        
        except Exception:
            db.session.rollback()
            raise NewComerNotModifiedException()
        
 
