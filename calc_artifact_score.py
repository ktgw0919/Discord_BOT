import is_noise

class Artifact:
    def __init__(self):
        self.ATK_flat = 0
        self.ATK_per = 0.0
        self.DEF_flat = 0
        self.DEF_per = 0.0
        self.HP_flat = 0
        self.HP_per = 0.0
        self.Elemental = 0
        self.Recharge = 0.0
        self.CRIT_Rate = 0.0
        self.CRIT_DMG = 0.0
        self.sub_op_name = []
        self.sub_op = []
        self.count_sub_op = 0
    
    ATK_WEIGHT = 1
    CRIT_DMG_WEIGHT = 1
    CRIT_RATE_WEIGHT = 2
    def calc_score(self):
        score = (self.ATK_per * Artifact.ATK_WEIGHT + 
                 self.CRIT_DMG * Artifact.CRIT_DMG_WEIGHT + 
                 self.CRIT_Rate * Artifact.CRIT_RATE_WEIGHT)
        return score    

def assign_values(Artifact, sub_op):
    # サブオプを聖遺物クラスに代入
    sub_op_len = len(sub_op)
    i = 0
    while i < sub_op_len:
        if is_noise.is_noise(sub_op[i]): # ノイズの場合はスキップ
            i += 1
            continue
        key = is_noise.find_closest_match(sub_op[i]) # キーを取得
        # print(f"{sub_op[i]=},{key=}")
        # HP,DEF,ATK は実数値とパーセントがあるので、それぞれの値を取得する
        if key == "HP": # HPの場合
            j = i
            while True:
                j = j + 1
                if j >= sub_op_len | is_noise.is_key(sub_op[j]): # ステータスの前にキーが見つかった場合は異常終了
                    print('warning:artifact status is not found.')
                    break
                if is_noise.is_per(sub_op[j]): # パーセントの場合
                    Artifact.HP_per = float(is_noise.per_value(sub_op[j]))
                    Artifact.sub_op_name.append("HPパーセント")
                    Artifact.sub_op.append(Artifact.HP_per)
                    Artifact.count_sub_op += 1
                    break
                elif is_noise.is_flat(sub_op[j]): # 実数値の場合
                    Artifact.HP_flat = int(is_noise.flat_value(sub_op[j]))
                    Artifact.sub_op_name.append("HP実数値")
                    Artifact.sub_op.append(Artifact.HP_flat)
                    Artifact.count_sub_op += 1
                    break
        if key == "攻撃力":
            j = i
            while True:
                j = j + 1
                if j >= sub_op_len | is_noise.is_key(sub_op[j]): # ステータスの前にキーが見つかった場合は異常終了
                    print('warning:artifact status is not found.')
                    break
                if is_noise.is_per(sub_op[j]):
                    Artifact.ATK_per = float(is_noise.per_value(sub_op[j]))
                    Artifact.sub_op_name.append("攻撃力パーセント")
                    Artifact.sub_op.append(Artifact.ATK_per)
                    Artifact.count_sub_op += 1
                    break
                elif is_noise.is_flat(sub_op[j]):
                    Artifact.ATK_flat = int(is_noise.flat_value(sub_op[j]))
                    Artifact.sub_op_name.append("攻撃力実数値")
                    Artifact.sub_op.append(Artifact.ATK_flat)
                    Artifact.count_sub_op += 1
                    break
        if key == "防御力":
            j = i
            while True:
                j = j + 1
                if j >= sub_op_len | is_noise.is_key(sub_op[j]): # ステータスの前にキーが見つかった場合は異常終了
                    print('warning:artifact status is not found.')
                    break
                if is_noise.is_per(sub_op[j]):
                    Artifact.DEF_per = float(is_noise.per_value(sub_op[j]))
                    Artifact.sub_op_name.append("防御力パーセント")
                    Artifact.sub_op.append(Artifact.DEF_per)
                    Artifact.count_sub_op += 1
                    break
                elif is_noise.is_flat(sub_op[j]):
                    Artifact.DEF_flat = int(is_noise.flat_value(sub_op[j]))
                    Artifact.sub_op_name.append("防御力実数値")
                    Artifact.sub_op.append(Artifact.DEF_flat)
                    Artifact.count_sub_op += 1
                    break
        # 元素熟知を取得(整数のみ)
        if key == "元素熟知":
            j = i
            while True:
                j = j + 1
                if j >= sub_op_len | is_noise.is_key(sub_op[j]): # ステータスの前にキーが見つかった場合は異常終了
                    print('warning:artifact status is not found.')
                    break
                if is_noise.is_flat(sub_op[j]):
                    Artifact.Elemental = int(is_noise.flat_value(sub_op[j]))
                    Artifact.sub_op_name.append("元素熟知")
                    Artifact.sub_op.append(Artifact.Elemental)
                    Artifact.count_sub_op += 1
                    break
        # パーセントのみのステータスを取得
        if key == "元素チャージ効率":
            j = i
            while True:
                j = j + 1
                if j >= sub_op_len | is_noise.is_key(sub_op[j]): # ステータスの前にキーが見つかった場合は異常終了
                    print('warning:artifact status is not found.')
                    break
                if is_noise.is_per(sub_op[j]):
                    Artifact.Recharge = float(is_noise.per_value(sub_op[j]))
                    Artifact.sub_op_name.append("元素チャージ効率")
                    Artifact.sub_op.append(Artifact.Recharge)
                    Artifact.count_sub_op += 1
                    break
        if key == "会心率":
            j = i
            while True:
                j = j + 1
                if j >= sub_op_len | is_noise.is_key(sub_op[j]):
                    print('warning:artifact status is not found.')
                    break
                if is_noise.is_per(sub_op[j]):
                    Artifact.CRIT_Rate = float(is_noise.per_value(sub_op[j]))
                    Artifact.sub_op_name.append("会心率")
                    Artifact.sub_op.append(Artifact.CRIT_Rate)
                    Artifact.count_sub_op += 1
                    break
        if key == "会心ダメージ":
            j = i
            while True:
                j = j + 1
                if j >= sub_op_len | is_noise.is_key(sub_op[j]):
                    print('warning:artifact status is not found.')
                    break
                if is_noise.is_per(sub_op[j]):
                    Artifact.CRIT_DMG = float(is_noise.per_value(sub_op[j]))
                    Artifact.sub_op_name.append("会心ダメージ")
                    Artifact.sub_op.append(Artifact.CRIT_DMG)
                    Artifact.count_sub_op += 1
                    break
        i += 1

# sub_ops_in_game = [
#     "攻撃力",
#     "防御力",
#     "HP",
#     "元素熟知",
#     "元素チャージ効率",
#     "会心率",
#     "会心ダメージ",
# ]

# ATK_flat = 0
# ATK_per = 0.0
# DEF_flat = 0
# DEF_per = 0.0
# HP_flat = 0
# HP_per = 0.0
# Elemental = 0
# Recharge = 0.0
# CRIT_Rate = 0.0
# CRIT_DMG = 0.0

# artifact = Artifact()

# sub_op = [
#     "HP",
#     "538",
#     "元素チャージ効率",
#     "-",
#     "17%",
#     "会心率",
#     "、6.2%",
#     "防御力",
#     "13.9%",
# ]

# # 関数を実行してデータを変数に代入
# assign_values(artifact,sub_op)
# print(f"{artifact.ATK_flat=}\n {artifact.ATK_per=}\n {artifact.DEF_flat=}\n {artifact.DEF_per=}\n {artifact.HP_flat=}\n {artifact.HP_per=}\n {artifact.Elemental=}\n {artifact.Recharge=}\n {artifact.CRIT_Rate=}\n {artifact.CRIT_DMG=}")
# print(f'{artifact.calc_score()=}')

