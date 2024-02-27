from ..calc.detect import run,parse_opt,main
from ..calc.predict import run_predict as rp

import os

def run_detect(source,out_path,out_name):
    opt = parse_opt(source,out_path,out_name)
    main(opt)

def run_predict(source,out_path,out_name):
    rp(source,os.path.join(out_path,out_name))

def run_mp4():
    import ffmpy
    # 需要转换格式的视频文件，文件真实存在
    source_file = r"D:\code\python\yolov5-count\static\video\1647573776265\1647573776265.mp4\1647573776265.mp4"
    # 转换成功后的视频文件，文件夹真实存在，不会自动创建
    sink_file = r"D:\code\python\yolov5-count\static\video\1647573776265\kk.mp4"

    ff = ffmpy.FFmpeg(
        inputs={source_file: None},
        outputs={sink_file: None})
    ff.run()

if __name__ == "__main__" :
    source = r"data/video/back2.mp4"
    out_path = r"runs/detect"
    out_name = r"kk"

    # run_detect(source,out_path,out_name)
    # run_mp4()

    video_path      = "D:\\code\\python\\yolov5-count3\\data\\video\\x1.mp4"
    video_save_path = "D:\\code\\python\\yolov5-count3\\img_out\\x11.mp4"
    run_predict(video_path,"D:\\code\\python\\yolov5-count3\\img_out\\","x12.mp4")