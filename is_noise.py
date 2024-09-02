import re
import difflib

# キーの一覧
keys = [
    "HP",
    "攻撃力",
    "防御力",
    "元素熟知",
    "元素チャージ効率",
    "会心率",
    "会心ダメージ",
    # 誤認識対策
    "会必率",
    "会必ダメージ",
]

# 渡された単語に類似度が高いキーを取得
def find_closest_match(sub_op):
    closest_key = difflib.get_close_matches(sub_op, keys, n=1, cutoff=0.5)
    if not closest_key:
        return None
    key = closest_key[0]
    if key == "会必率":
        key = "会心率"
    if key == "会必ダメージ":
        key = "会心ダメージ"
    return key

def is_noise(sub_op):
    # 類似度が高いキーが見つかった場合はノイズではないと判定
    if find_closest_match(sub_op) != None:
        # print(f'{sub_op}=key')
        return False
    # パーセントの場合はノイズではないと判定
    if re.search(r"[\d]+(\.[\d]+)?%", sub_op):
        # print(f'{sub_op}=per')
        return False
    # 整数(実数値)の場合はノイズではないと判定
    if re.search(r"[\d]+", sub_op):
        # print(f'{sub_op}=flat')
        return False
    # そのほかの場合はノイズと判定
    else:
        # print(f'{sub_op}=noise')
        return True

def is_key(sub_op):
    # 類似度が高いキーが見つかった場合はキーと判定
    if find_closest_match(sub_op) != None:
        return True
    else:
        return False
    
def is_per(sub_op):
    # 小数(パーセント)の場合はパーセントと判定
    if re.search(r"[\d]+(\.[\d]+)?%", sub_op):
        return True
    else:
        return False
    
def is_flat(sub_op):
    # 整数(実数値)の場合は実数値と判定
    if re.search(r"[\d]+", sub_op):
        return True
    else:
        return False
    
def per_value(sub_op):
    # パーセントの値を取得する
    if is_per(sub_op) == False:
        return None
    match = re.search(r"[\d]+(\.[\d]+)?", sub_op)
    # print(f"per_value={match.group()}")
    value = float(match.group())
    if value > 39:
        value = value / 10
    return value

def flat_value(sub_op):
    # 実数値の値を取得する
    if is_flat(sub_op) == False:
        return None
    match = re.search(r"[\d]+", sub_op)
    return int(match.group())

sub_op = [
    "HP",
    "538",
    "元素チャージ効率",
    "-",
    "17%",
    "会心率",
    "、6.2%",
    "防御力",
    "13.9%",
]

for i in range(len(sub_op)):
    if is_noise(sub_op[i]):
        # print(f'is_noise=True')
        continue
    if is_key(sub_op[i]):
        # print(f'is_key=True')
        continue
    if is_per(sub_op[i]):
        # print(f'is_per=True:{sub_op[i]}={per_value(sub_op[i])}')
        per_value(sub_op[i])
        continue
    if is_flat(sub_op[i]):
        # print(f'is_flat=True:{sub_op[i]}={flat_value(sub_op[i])}')
        flat_value(sub_op[i])
        continue
