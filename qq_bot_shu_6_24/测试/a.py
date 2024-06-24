import subprocess
from  moudles.common_funcation import *
def aaaaaa(folder):
    # 要执行的cmd命令
    #cmd = '.\\ffmpeg -i D:\\23208\\qq_bot_shu\\0.gif -vf "split[original][copy];[copy]palettegen[p];[original][p]paletteuse" output.png'
    cmd="cd D:\\23208\\qq_bot_shu"
    delete_file(folder+"/out_put_apng.png")
    subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    cmd = '.\\ffmpeg -i '+folder+'"/frame_%03d.png" -f apng -plays 0 "'+folder+'/out_put_apng.png"'
    # 使用subprocess.run()执行命令
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # 输出命令执行结果
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)
