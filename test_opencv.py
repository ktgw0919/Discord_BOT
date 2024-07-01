import cv2
import matplotlib.pyplot as plt
import conversion_path

def convert_image(image_path):
    img = cv2.imread(image_path)
    img = img[300:510, 1200:1900]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(img, 190, 255, cv2.THRESH_BINARY)[1]
    img = cv2.bitwise_not(img)
    
    cv2.imwrite('tmp_img/sub_op.png', img)
    tmp_path = conversion_path.to_absolute_path('tmp_img/sub_op.png')
    return tmp_path


# name = "img_1"

# img = cv2.imread(name + ".png")

# # グレースケール化
# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imwrite(f"1_{name}_gray.png", img)

# # 二値化
# th = 200
# img = cv2.threshold(img, th, 255, cv2.THRESH_BINARY)[1]
# # cv2.imwrite(f"2_{name}_threshold.png",img)

# # 白黒反転
# img = cv2.bitwise_not(img)
# # cv2.imwrite(f"3_{name}_bitwise.png",img)

# # トリミング_聖遺物レベル
# img_level = img[110:200, 1150:1300]
# # cv2.imwrite(name + "_level.png",img_level)

# # トリミング_メインオプ
# img_level = img[230:280, 1150:1900]
# cv2.imwrite(name + "_main_op.png", img_level)

# # トリミング_サブオプ
# img_level = img[300:510, 1200:1900]
# cv2.imwrite(name + "_sub_op.png", img_level)
