# image から聖遺物スコアを計算する
import cv2

import calc_artifact_score
import test_opencv
import test_ocr

img_path = 'artifact_02.png' # 画像のパス
img_path = test_opencv.convert_image(img_path) # 画像の前処理
# img_path = 'F:\_programming\Python\画像認識/bgr2gray_2sub_op.png'
sub_op = test_ocr.render_doc_text(img_path) # OCRでサブオプを取得

artifact = calc_artifact_score.Artifact()
calc_artifact_score.assign_values(artifact, sub_op) # 聖遺物クラスにサブオプを代入
score = artifact.calc_score() # スコア計算
print(f'{score=}')