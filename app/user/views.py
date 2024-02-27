from flask import render_template,redirect,url_for,request,flash,jsonify,make_response,session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from .. import app,pm,db,app_tools
import os,time
_ = app_tools.BabelGetText
from . import models
from .. import settings
from ..tools.pager import PageInfo
from ..tools.params_req import BaseResponseParams
from ..tools.json_params import JsonBaseResponse
from ..tools.role_sign import sign_user_role

view = pm.get_blue_app(__name__)

@view.route("/")
def index():
    return render_template("index.html")

@view.route("/set_language")
def set_language() :
    lanaguae = session.get('lang', 'en') #request.accept_languages.best_match(app_tools.LANGUAGES.keys())
    change_language = "en" if lanaguae == "zh" else "zh"
    print("language: ",lanaguae,change_language)

    # response.headers.add("Accept-Language", change_language)
    # response.headers["Accept-Language"] = change_language
    session['lang'] = change_language

    req_params = BaseResponseParams(request)
    print(req_params.next_url)
    return redirect(req_params.next_url)

@view.route('/login', methods=['GET', 'POST'],endpoint="user_login")
def login():
    req_params = BaseResponseParams(request)

    if req_params.POST:
        json_params = JsonBaseResponse()

        if current_user.is_authenticated:
            logout_user()
        if req_params.username and req_params.password:
            pass
        else:
            return json_params.toJson(code=303,message="Invalid username or password")

        user = models.User.query.filter_by(username=req_params.username).first()
        # if user is None or not user.check_password(""):
        #     return redirect(url_for('login'))
        if user and user.verify_password(req_params.password):
            login_user(user)
        else:
            return json_params.toJson(code=503, message="Invalid password")

        next_page = request.args.get('next',"")
        print("next_page: ", next_page)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = pm.blue_url_for(settings.LOGIN_INDEX) if settings.LOGIN_INDEX else "/"
        print("next_page: ", next_page)
        return json_params.toJson(data={"next_page":next_page})
    return render_template('user/login.html',req_params=req_params)

@view.route('/register', methods=['GET', 'POST'],endpoint="user_register")
def register():
    req_params = BaseResponseParams(request)
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    if req_params.POST:
        json_params = JsonBaseResponse()
        if req_params.username and req_params.password and req_params.password == req_params.repassword:
            try:
                user = models.User(username=req_params.username)
                user.set_password(req_params.password)
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                json_params.set_msg(301,"database errors .....")
        else:
            json_params.set_msg(302, "register params losts....")
        return json_params.toJson()
    return render_template('user/register.html',req_params=req_params,status="register")
    # return render_template('base.html',req_params=req_params,status="register")

@view.route('/logout',endpoint="user_logout")
@login_required
def logout():
    logout_user()
    return redirect(pm.blue_url_for("user_login"))

@view.route("/show_all_users")
# @login_required
@sign_user_role(models.SuperAdmin)
def show_all_users() :
    req_params = BaseResponseParams(request)

    search = req_params.search
    if search :
        users = models.User.query.filter(
            models.User.username.like("%" + search + "%")
        )
    else :
        users = models.User.query.filter()

    page_info = PageInfo(request.args.get('page', None), users.count(), perItems=10,
                         path=f'{request.path}?search={search}&',
                         ormObjs=users, open_id=False,
                         )
    admins = page_info.page_objs

    return render_template("user/show_all_users.html",admins=admins,page_info=page_info,req_params=req_params)

@view.route("/change_user",methods=["POST"])
@sign_user_role(models.SuperAdmin)
def change_user() :
    req_params = BaseResponseParams(request)
    json_params = JsonBaseResponse()

    print("params: ", req_params)

    if request.method == "GET" :
        return json_params.toJson(code="207",message=_("数据请求失败！"))

    nid = req_params.nid
    try:
        obj = models.User.query.get(nid)
    except Exception as e :
        return json_params.toJson(code=201,message=_("用户不存在！"))

    try:
        assert req_params.data
    except Exception as e :
        return json_params.toJson(code=205,message=_("输入信息不能为空！"))

    try:
        data = {}
        if req_params.symbol == "username" :
            obj.username = req_params.data
        if req_params.symbol == "password" :
            obj.set_password(req_params.data)
        if req_params.symbol == "role" :
            print("req_params.data: ", req_params.data)
            if not obj.is_role(req_params.data) :
                return json_params.toJson(code=202,message=_("角色不存在"))
            obj.role = req_params.data
            data["role"] = obj.get_role_display
        db.session.commit()
        return json_params.toJson(code=200,data=data)
    except Exception as e :
        return json_params.toJson(code=203,message=_("异常报错"))

@view.route("/user_details")
@sign_user_role(models.SuperAdmin)
def user_details() :
    req_params = BaseResponseParams(request)
    return render_template("user/user_details.html",
                           req_params = req_params ,
           )

@view.route("/user_thumb_upload",methods=["POST"])
@sign_user_role(models.SuperAdmin)
def user_thumb_upload() :
    print("user_thumb_upload: ", user_thumb_upload)
    file = request.files.get("file")
    if not file :
        return jsonify({"code":101})
    print("file: ", file)
    save_path = "./app/statics/user_img_thumb"
    os.makedirs(save_path, exist_ok=True)

    pic = str((time.time() * 1000)) + ".jpg"

    file.save(os.path.join(save_path, pic))

    pic_path = f"/statics/user_img_thumb/{pic}"

    try :
        assert current_user.info
        models.UserDetails.query.filter(models.UserDetails.stu_id == current_user.id).update(
            {
                "pic" : pic,
            }
        )
    except Exception as e :
        current_user.info = models.UserDetails(pic = pic)
    db.session.commit()

    return jsonify({"code":200,"pic":pic_path})

@view.route("/change_user_details",methods=["GET","POST"])
@sign_user_role(models.SuperAdmin)
def change_user_details() :
    req_params = BaseResponseParams(request)
    sex_choice = models.UserDetails.sex_choice

    if request.method == "POST" :
        userDetails = {
            "name" : req_params.name,
            "phone": req_params.phone,
            "address": req_params.address,
            "age": req_params.age,
            "sex": req_params.sex,
        }
        try:
            assert current_user.info
            models.UserDetails.query.filter(models.UserDetails.stu_id==current_user.id).update(userDetails)
        except Exception as e :
            current_user.info = models.UserDetails(**userDetails)
            # db.session.add(user_detail)
        # current_user.info.name = req_params.name
        db.session.commit()
    else :
        req_params.get_obj_params(current_user.info)

    return render_template("user/change_user_details.html",
                           req_params = req_params,
                           sex_choice = sex_choice,
                           )