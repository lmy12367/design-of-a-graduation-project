from app import app as apps,db

# import sys
# print(sys.path)
# from app.user.models import *

# db.init_app(app)
db.create_all()

if __name__ == "__main__":
    apps.run(port="8000")