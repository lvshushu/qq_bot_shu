import sys
import os
from PIL import Image
def img2gif(img_path="D:\23208\邓姐头像.png",
            savename="1"):


    '''png转透明背景gif:author: Lian:param img_path: 图片路径:param savename: 保存名称(可选):return:'''



    if not os.path.isfile(img_path):
        print("wrong file name")
        exit()

    import sys
    img = Image.open(img_path)
    img.putalpha(255)
    if not savename: savename = "{}.gif".format(
        os.path.splitext(img_path)[0])  # img.show()img.save(savename, transparency = 0, disposal = 2, loop = 0)
if __name__ == "__main__":

    if (sys.argv.__len__() < 2):
        print("need arguments")
        exit()
    img2gif(*tuple(sys.argv[1:]))
