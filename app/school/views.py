from flask import render_template,redirect,url_for,request,flash,jsonify,make_response,session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from .. import app,pm,db,app_tools
import os,time
_ = app_tools.BabelGetText
from ..user import models
from .. import settings
from ..tools.pager import PageInfo
from ..tools.params_req import BaseResponseParams
from ..tools.json_params import JsonBaseResponse
from ..tools.excel_src import ExcelDeal
import serial


view = pm.get_blue_app(__name__)
save_base = "./upload"
save_base_pic = "./app/statics/upload_pic"

@view.route("/upload_school",methods=["GET","POST"],endpoint="add_school")
def add_school() :
    req_params = BaseResponseParams(request)

    os.makedirs(save_base,exist_ok=True)
    file = request.files.get("file")
    if file and file.filename:
        file_path = os.path.join(save_base, file.filename)
        file.save(file_path)
        req_params.heads = _("上传成功 ！")

        excel = ExcelDeal(file_path)
        headers = []
        models.TeachBuild.query.delete()
        models.TeachClass.query.delete()
        db.session.commit()

        obj_list = []
        for ci,cargo in enumerate(excel.read_row(start_row=1, choose_attr=[], show_stats="str")):
            if ci == 0 :
                headers = cargo
                obj_list.extend(
                    [
                        models.TeachBuild(id=j,name=j) for i,j in enumerate(headers)
                    ]
                )
                continue

            for i,j in dict(zip(headers,cargo)).items() :
                obj_list.append(models.TeachClass(id=j,build_id=i,name=j))
        db.session.add_all(obj_list)
        db.session.commit()

    return render_template("school/upload_school.html",
                           req_params = req_params,
                           )

@view.route("/")
@view.route("/show_school",methods=["GET"])
def show_school() :
    req_params = BaseResponseParams(request)

    course_details = models.CourseDetail.query.filter()
    teach_builds = models.TeachBuild.query.filter()

    cls_list = []
    for c in course_details :
        cls_list.append(c.tclass_id)

    return render_template("school/show_school.html",
                           req_params = req_params,
                           teach_builds = teach_builds,
                           cls_list = cls_list,
                           )

@view.route("/upload_class",methods=["GET","POST"],endpoint="add_tclass")
def add_tclass() :
    req_params = BaseResponseParams(request)

    os.makedirs(save_base,exist_ok=True)
    file = request.files.get("file")
    if file and file.filename:
        file_path = os.path.join(save_base, file.filename)
        file.save(file_path)
        req_params.heads = _("上传成功 ！")

        excel = ExcelDeal(file_path)

        headers = []
        obj_list = []

        collage_details = {}
        specialize_details = {}
        classes_details = {}
        teacher_details = {}

        models.Collage.query.delete()
        models.Specialize.query.delete()
        models.Classes.query.delete()
        models.Teacher.query.delete()
        models.CourseDetail.query.delete()
        db.session.commit()

        for ci,cargo in enumerate(excel.read_row(start_row=2, choose_attr=[], show_stats="str")):
            nid,collage,specialize,classes,teacher,count,build,tclass = cargo
            collage_details[collage] = models.Collage(name=collage)
            specialize_details[specialize] = models.Specialize(name=specialize)
            classes_details[classes] = models.Classes(name=classes)
            teacher_details[teacher] = models.Teacher(name=teacher)

        add_list = []
        for obj in [collage_details,specialize_details,classes_details,teacher_details] :
            add_list.extend(list(obj.values()))
        db.session.add_all(add_list)
        db.session.commit()

        res = []
        for ci,cargo in enumerate(excel.read_row(start_row=2, choose_attr=[], show_stats="str")):
            nid,collage,specialize,classes,teacher,count,build,tclass = cargo
            res.append(
                models.CourseDetail(
                    collage_id=collage_details[collage].id,
                    specialize_id=specialize_details[specialize].id,
                    classes_id=classes_details[classes].id,
                    teacher_id=teacher_details[teacher].id,
                    build_id=build,
                    tclass_id=tclass,
                    count = count,
                )
            )
        db.session.add_all(res)
        db.session.commit()

    return render_template("school/upload_school.html",
                           req_params = req_params,
                           )

@view.route("/show_class",methods=["GET"])
def show_class() :
    req_params = BaseResponseParams(request)

    course_details = models.CourseDetail.query.filter()
    print(course_details.all())

    return render_template("school/show_course.html",
                           req_params = req_params,
                           course_details = course_details,
                           )

@view.route("/upload_classdetails",methods=["GET","POST"])
def upload_classdetails() :
    req_params = BaseResponseParams(request)

    os.makedirs(save_base,exist_ok=True)
    file = request.files.get("file")
    if file and file.filename:
        file_path = os.path.join(save_base, file.filename)
        file.save(file_path)
        req_params.heads = _("上传成功 ！")

        excel = ExcelDeal(file_path)

        objs = []
        models.ClassDetail.query.delete()
        db.session.commit()
        for ci,cargo in enumerate(excel.read_row(start_row=2, choose_attr=[], show_stats="str")):
            objs.append(
                models.ClassDetail(
                    classes=cargo[1],
                    ctime=cargo[2],
                    teacher=cargo[3],
                    collage=cargo[5],

                    phone = cargo[4],

                    need_count=cargo[6],
                    now_count=cargo[7],
                    no_count=cargo[8],
                    later_count=cargo[9],
                    mor_count=cargo[10],

                    stu_names01=cargo[11],
                    stu_names02=cargo[12],
                    stu_names03=cargo[13],
                    stu_names04=cargo[14],
                )
            )
        db.session.add_all(objs)
        db.session.commit()

    return render_template("school/upload_school.html",
                           req_params = req_params,
                           )

@view.route("/show_classdetails",methods=["GET"])
def show_classdetails() :
    req_params = BaseResponseParams(request)

    class_details = models.ClassDetail.query.filter()

    return render_template("school/show_class_details.html",
                           req_params = req_params,
                           class_details = class_details,
                           )

@view.route("/show_classdetails/<nid>",methods=["GET"])
def show_classdetail_nid(nid) :
    obj = models.ClassDetail.query.get(nid)

    return render_template(
        "school/show_classdetail_nid.html",
        vendor = obj,
    )

@view.route("/upload_user",methods=["GET","POST"])
def upload_user() :
    req_params = BaseResponseParams(request)

    os.makedirs(save_base_pic,exist_ok=True)
    file = request.files.get("file")

    name = req_params.name
    number = req_params.number

    if name and number :

        if file and file.filename:
            req_params.heads = _("上传成功 ！")

            t = str(int(time.time() * 1000))
            t_name = f"{t}.jpg"
            file_path = os.path.join(save_base_pic,t_name)
            file.save(file_path)

            obj = models.Students(
                pic = t_name,
                name = name,
                number = number
            )
            db.session.add(obj)
            db.session.commit()

    return render_template("school/upload_user.html",
                           req_params = req_params,
                           )
@view.route("/show_student",methods=["GET"])
def show_student() :
    req_params = BaseResponseParams(request)

    students = models.Students.query.filter()

    return render_template("school/show_students.html",
                           req_params = req_params,
                           students = students,
                           )

@view.route("/home",methods=["GET"])
def home():
    req_params = BaseResponseParams(request)

    params = {
        "req_params":req_params,
    }

    return render_template("school/upload_home.html",**params)

def add_video(video) :

    for obj in models.ClassDetail.query.filter() :
        if obj.get_video :
            continue
        print("============>>>>>>>>>>>>>: ", obj)
        models.ClassDetail.query.get(obj.id).video_url = video
        break

    db.session.commit()

@view.route("/upload",methods=["POST"])
def upload():
    print("upload .....")
    try:
        mode = request.args.get("mode","")
        print("mode: ", mode)
        file = request.files.get("file")
        save_path = "app/statics/upload"
        os.makedirs(save_path,exist_ok=True)
        str_time = str(int((time.time()*1000)))
        file_save_name = str_time+".mp4"
        file_path = os.path.join(save_path,file_save_name)
        file.save(file_path)

        file_path = os.path.abspath(file_path)
        file_save_path = f"app/statics/video/{str_time}"
        os.makedirs(file_save_path,exist_ok=True)
        file_save_path = os.path.abspath(file_save_path)

        from ..tools.run import run_detect,run_predict
        import ffmpy
        try:

            if mode == "upload01":
                try:
                    # 打开串口，并且获得串口对象
                    SCI1 = serial.Serial("com4", 115200, timeout=50)
                    # 判断是否打开成功
                    if (SCI1.isOpen() == True):
                        print("串口已经打开！")
                except Exception as exc:
                    print("串口打开异常:", exc)
                commandFromECU = 1
                SCI1.write(str(commandFromECU).encode("utf-8"))
                time.sleep(1)
                commandFromECU = 7
                SCI1.write(str(commandFromECU).encode("utf-8"))
                run_detect(file_path,file_save_path,file_save_name)
                out_path = os.path.join("/statics/video", str_time, file_save_name, "new.mp4")
                abs_path = os.path.abspath(os.path.join("app/statics/video", str_time, file_save_name, file_save_name))
                ph = os.path.join("app/statics/video", str_time, file_save_name, "new.mp4")
                abs_path2 = os.path.abspath(os.path.join("app/statics/video", str_time, file_save_name, "new.mp4"))

                add_video(ph)

                commandFromECU = 1
                SCI1.write(str(commandFromECU).encode("utf-8"))
                time.sleep(1)
                commandFromECU = 8
                SCI1.write(str(commandFromECU).encode("utf-8"))
                SCI1.close()  # 关闭端口

            else :
                # try:
                #     # 打开串口，并且获得串口对象
                #     SCI1 = serial.Serial("com4", 115200, timeout=50)
                #     # 判断是否打开成功
                #     if (SCI1.isOpen() == True):
                #         print("串口已经打开！")
                # except Exception as exc:
                #     print("串口打开异常:", exc)
                # commandFromECU = 1
                # SCI1.write(str(commandFromECU).encode("utf-8"))
                # time.sleep(1)
                # commandFromECU = 7
                # SCI1.write(str(commandFromECU).encode("utf-8"))
                run_predict(file_path,file_save_path,file_save_name)
                out_path = os.path.join("/static/video", str_time, "new.mp4")
                abs_path = os.path.abspath(os.path.join("static/video", str_time, file_save_name))
                abs_path2 = os.path.abspath(os.path.join("static/video", str_time, "new.mp4"))
                print(out_path," ap: ",abs_path, "ab2: ",abs_path2)
                # commandFromECU = 1
                # SCI1.write(str(commandFromECU).encode("utf-8"))
                # time.sleep(1)
                # commandFromECU = 8
                # SCI1.write(str(commandFromECU).encode("utf-8"))
                # SCI1.close()  # 关闭端口
            ff = ffmpy.FFmpeg(
                inputs={abs_path: None},
                outputs={abs_path2: None})
            ff.run()

        except Exception as e :
            print("E: ", e)
            out_path = r"/static/imgs/1647569462569.mp4"

        return jsonify({
            "code":200,
            "msg": "upload success",
            "out_path" : out_path,
            "res" : "",
        })
    except Exception as e:
        return jsonify({
            "code" : 101,
            "msg": "upload failed"
        })
