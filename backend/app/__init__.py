import os
from flask import Flask
from flask_cors import CORS
from config import Config
from app.api.v1.routers.bulletin import bulletins_blueprint
from app.api.v1.routers.small_group_discussion import small_group_discussions_blueprint
from app.api.v1.routers.app_patch import app_patch_blueprint
from app.api.v1.routers.new_comer import new_comers_blueprint
from .extensions import db, s3_wrapper
from dotenv import load_dotenv

flask_env = os.getenv("INLAND_HIS_ENV")

if flask_env == "development":
    origins = ["*"]
else:
    origins = [
        "https://admin.inlandhis.com",
        "http://localhost:8501"
    ]

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    
    CORS(app, origins=origins, supports_credentials=True)
    
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(bulletins_blueprint)
    app.register_blueprint(small_group_discussions_blueprint)
    app.register_blueprint(app_patch_blueprint)
    app.register_blueprint(new_comers_blueprint)
    # app.register_blueprint(events_blueprint)
    # app.register_blueprint(bible_challenges_blueprint)

    s3_wrapper.init(
        access_key=os.getenv('AWS_S3_ACCESS_KEY'),
        secret_key=os.getenv('AWS_S3_SECRET_KEY'),
        region='us-west-1',
        bucket_name=os.getenv('AWS_S3_BUCKET_NAME')
    )

    with app.app_context():
        db.create_all()
        
    return app