from PIL import Image
import pyocr
import pyocr.builders
import cv2
import numpy as np
import re

def render_doc_text(file_path):

    # ツール取得
    pyocr.tesseract.TESSERACT_CMD = 'F:/_programming/Tesseract-OCR/tesseract.exe'
    tools = pyocr.get_available_tools()
    tool = tools[0]

    # 画像取得
    # img = cv2.imread(file_path, 0)
    # img = Image.fromarray(img)
    
    # 画像の読み込み
    img = Image.open(file_path)

    # OCR
    builder = pyocr.builders.TextBuilder(tesseract_layout=6)
    result = tool.image_to_string(img, lang="jpn", builder=builder)
    print(f'{result=}')

    # 結果から空白文字削除
    # data_list = [text for text in result.split('\n') if text.strip()]
    # 正規表現を使用して連続する空白文字列を一つのカンマに置き換える
    processed_result = re.sub(r'\s+', ',', result)

    # 結果から空白文字を除去し、カンマで分割してリストに格納する
    data_list = [line for line in processed_result.split(',') if line.strip()]
    print(data_list)

    return data_list

# OCR検知
# data_list = render_doc_text('F:\_programming\Python\画像認識/bgr2gray_2sub_op.png')
# print(data_list)
# print(','.join(data_list))