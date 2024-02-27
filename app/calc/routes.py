from flask import render_template,redirect,jsonify,request,session,url_for
from flask import Flask
from params_req import BaseResponseParams
from datetime import datetime
import time,os
# import serial

app = Flask(
    __name__,
)

app.secret_key = "a new web"
app.jinja_env.auto_reload = True
app.config["JSONIFY_PRETTYPRINT_REGULAR"]=False

@app.route("/",methods=["GET"])
def home():
    requests = BaseResponseParams(request)

    params = {
        "requests":requests,
    }

    return render_template("index.html",**params)

@app.route("/upload",methods=["POST"])
def upload():
    print("upload .....")
    try:
        mode = request.args.get("mode","")
        print("mode: ", mode)
        file = request.files.get("file")
        save_path = "./upload"
        os.makedirs(save_path,exist_ok=True)
        str_time = str(int((time.time()*1000)))
        file_save_name = str_time+".mp4"
        file_path = os.path.join(save_path,file_save_name)
        file.save(file_path)

        file_path = os.path.abspath(file_path)
        file_save_path = f"./static/video/{str_time}"
        os.makedirs(file_save_path,exist_ok=True)
        file_save_path = os.path.abspath(file_save_path)

        from run import run_detect,run_predict
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
                out_path = os.path.join("/static/video", str_time, file_save_name, "new.mp4")
                abs_path = os.path.abspath(os.path.join("static/video", str_time, file_save_name, file_save_name))
                abs_path2 = os.path.abspath(os.path.join("static/video", str_time, file_save_name, "new.mp4"))
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

if __name__ == "__main__":
    app.run(debug=True)