from app import create_app
import os 
from config import url, port
os.umask(0o002)


app = create_app()

if __name__ == '__main__':
    app.run(host=url, port=port)