from flask import session
from flask_login import UserMixin  # 引入用户基类
from werkzeug.security import generate_password_hash,check_password_hash
from .. import db,login,app_tools
import datetime,json

_ = app_tools.BabelGetText

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

Common = "common"
SaleAdmin = "sale_admin"
StayAdmin = "stay_admin"
SuperAdmin = "super_admin"

class User(UserMixin,db.Model):
    # __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    role_choices = (
        (Common, _("顾客")),
        (SaleAdmin, _("售药人员")),
        (StayAdmin, _("进货人员")),
        (SuperAdmin, _("超级管理员")),
    )
    role = db.Column(db.String(128),default="common")

    info = db.relationship("UserDetails", uselist=False, backref="own")
    good_user = db.relationship('GoodUser', backref='user',
                                lazy='dynamic')

    def __init__(self, username):
        self.username = username

    @property
    def get_role_display(self):
        try:
            rc = dict(list(self.role_choices))
        except Exception as e :
            print("E: ", e)
        return rc.get(self.role,"common")
    def is_role(self,name):
        rc = dict(list(self.role_choices))
        return name in rc

    @property
    def is_common(self):
        if not self :
            return False
        if self.role == Common :
            return True
    @property
    def is_stay_admin(self):
        if not self :
            return False
        if self.role == StayAdmin :
            return True
    @property
    def is_sale_admin(self):
        if not self :
            return False
        if self.role == SaleAdmin :
            return True
    @property
    def is_super_admin(self):
        if not self :
            return False
        if self.role == SuperAdmin :
            return True

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.id

    @staticmethod
    def get(user_id):
        if not user_id:
            return None
        return None

    @property
    def get_pic(self):
        if not self.info :
            return "/statics/assets/avatars/profile-pic.jpg"
        else :
            return f"/statics/user_img_thumb/{self.info.pic}"

class UserDetails(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    stu_id = db.Column(db.Integer, db.ForeignKey(User.id), comment="外键")

    pic = db.Column(db.String(255),default="")

    name = db.Column(db.String(255),default="")
    phone = db.Column(db.String(255),default="")
    address = db.Column(db.String(255),default="")

    age = db.Column(db.Integer,default=0)
    sex_choice = [
        ("no",_("未填写")),
        ("male",_("男性")),
        ("female", _("女性")),
    ]
    sex = db.Column(db.String(12),default="no")

    price = db.Column(db.DECIMAL(10, 2),default=0)

class Goods(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    name_cn = db.Column(db.String(255),default="")
    name_en = db.Column(db.String(255),default="")

    details_cn = db.Column(db.Text,default="")
    details_en = db.Column(db.Text,default="")

    mpic = db.Column(db.String(255),default="")
    cpic = db.Column(db.Text,default="[]")

    count = db.Column(db.Integer,default=0)
    price = db.Column(db.DECIMAL(10, 2), default=0)

    ctime = db.Column(db.DateTime, default=datetime.datetime.now)

    good_user = db.relationship('GoodUser', backref='good',
                                lazy='dynamic')

    @property
    def get_mpic(self):
        if not self.mpic :
            return "/statics/assets/avatars/profile-pic.jpg"
        else :
            return f"/statics/pics/{self.mpic}"

    @property
    def get_cpic(self):
        if not self.cpic:
            return []
        else:
            cpic = json.loads(self.cpic)
            cpic_list = []
            for cc in cpic :
                cpic_list.append(f"/statics/child_pics/{cc}")
            return cpic_list

    @property
    def get_name(self):
        lanaguae = session.get('lang', 'en')
        return self.name_en if lanaguae == "en" else self.name_cn

    @property
    def get_details(self):
        lanaguae = session.get('lang', 'en')
        return self.details_en if lanaguae == "en" else self.details_cn

class GoodUser(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    good_id = db.Column(db.Integer, db.ForeignKey('goods.id'))
    count = db.Column(db.Integer,default=1)
    is_add = db.Column(db.Boolean,default=False)
    ctime = db.Column(db.DateTime, default=datetime.datetime.now)

class TeachBuild(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer,default=0,unique=True)
    to_class = db.relationship('TeachClass', backref='to_build',
                                lazy='dynamic')

class TeachClass(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    build_id = db.Column(db.ForeignKey("teach_build.id",ondelete="CASCADE"))
    name = db.Column(db.Integer,default=0,unique=True)

class Collage(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer,default="",unique=True)
class Specialize(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer,default="",unique=True)
class Classes(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer,default="",unique=True)
class Teacher(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer,default="",unique=True)
class CourseDetail(db.Model) :
    id = db.Column(db.Integer, primary_key=True)

    collage_id = db.Column(db.ForeignKey("collage.id",ondelete="CASCADE"))
    specialize_id = db.Column(db.ForeignKey("specialize.id",ondelete="CASCADE"))
    classes_id = db.Column(db.ForeignKey("classes.id",ondelete="CASCADE"))
    teacher_id = db.Column(db.ForeignKey("teacher.id",ondelete="CASCADE"))

    build_id = db.Column(db.ForeignKey("teach_build.id",ondelete="CASCADE"))
    tclass_id = db.Column(db.ForeignKey("teach_class.id",ondelete="CASCADE"))

    to_collage = db.relationship('Collage', backref='to_course',uselist=False)
    to_specialize = db.relationship('Specialize', backref='to_course',uselist=False)
    to_classes = db.relationship('Classes', backref='to_course',uselist=False)
    to_teacher = db.relationship('Teacher', backref='to_course',uselist=False)

    count = db.Column(db.Integer,default=0)

class ClassDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ctime = db.Column(db.String(255),default="")

    classes = db.Column(db.String(255),default="")
    teacher = db.Column(db.String(255),default="")
    phone = db.Column(db.String(255),default="")
    collage = db.Column(db.String(255),default="")

    need_count = db.Column(db.Integer,default=0)
    now_count = db.Column(db.Integer,default=0)
    no_count = db.Column(db.Integer,default=0)
    later_count = db.Column(db.Integer,default=0)
    mor_count = db.Column(db.Integer,default=0)

    stu_names01 = db.Column(db.Text,default="")
    stu_names02 = db.Column(db.Text,default="")
    stu_names03 = db.Column(db.Text,default="")
    stu_names04 = db.Column(db.Text,default="")

    video_url = db.Column(db.String(255),default="")

    @property
    def get_video(self):
        if self.video_url :
            return f"/{self.video_url.strip('/app')}"
        return ""

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pic = db.Column(db.String(255),default="")
    name = db.Column(db.String(255),default="")
    number = db.Column(db.String(255),default="")

    @property
    def get_pic(self):
        return f"/statics/upload_pic/{self.pic}"