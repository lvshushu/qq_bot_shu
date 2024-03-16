import cv2

def picture_synthesis(mother_img='1.jpg', son_img='0.jpg', save_img='result.jpg', coordinate=None,x=980,y=100):
    # 读取母图和子图
    M_Img = cv2.imread(mother_img)
    S_Img = cv2.imread(son_img)

    # 缩放子图
    factor = 10
    S_Img = cv2.resize(S_Img, (int(S_Img.shape[1] / factor), int(S_Img.shape[0] / factor)))

    # 获取母图和子图的尺寸
    M_Img_h, M_Img_w, _ = M_Img.shape
    S_Img_h, S_Img_w, _ = S_Img.shape

    # 防止子图尺寸大于母图
    if S_Img_w > M_Img_w:
        S_Img_w = M_Img_w
    if S_Img_h > M_Img_h:
        S_Img_h = M_Img_h

    # 计算粘贴位置
    if coordinate is None or coordinate == "":
        coordinate = (x, y)
    else:
        print("已经指定坐标")

    # 将子图粘贴到母图的指定位置
    M_Img[coordinate[1]:coordinate[1]+S_Img_h, coordinate[0]:coordinate[0]+S_Img_w] = S_Img

    # 保存图片
    cv2.imwrite(save_img, M_Img)
#def mouse_callback(event, x, y, flags, param):
    #if event == cv2.EVENT_LBUTTONDOWN:
        #print("鼠标左键点击坐标：", x, y)
# 调用函数进行图片合成
#picture_synthesis("1.jpg", "0.jpg", "result.jpg")
'''
picture_synthesis(mother_img='3.jpg', son_img='0.jpg', save_img='result.jpg', coordinate=None,x=1054,y=300)
S = cv2.imread('result.jpg')
cv2.namedWindow('图片')
#cv2.setMouseCallback('图片', mouse_callback)

# 显示图片
cv2.imshow('图片', S)

# 等待按键，然后关闭窗口
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
