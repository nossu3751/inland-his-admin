import os

flask_env = os.getenv("INLAND_HIS_ENV")

if flask_env == "development":
    from dotenv import load_dotenv
    load_dotenv()
    url = '0.0.0.0'
    port = 5001
else:
    url = '0.0.0.0'
    port = 5001

class Config(object):
    SQLALCHEMY_DATABASE_URI = f'postgresql://{os.getenv("POSTGRES_USERNAME")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_SERVER_DEV")}/{os.getenv("POSTGRES_DBNAME")}'

