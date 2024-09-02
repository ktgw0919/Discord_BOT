import is_noise

class Artifact:
    def __init__(self):
        # サブオプの数値
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
        
        # サブオプの上昇回数
        self.ATK_flat_count = 0
        self.ATK_per_count = 0
        self.DEF_flat_count = 0
        self.DEF_per_count = 0
        self.HP_flat_count = 0
        self.HP_per_count = 0
        self.Elemental_count = 0
        self.Recharge_count = 0
        self.CRIT_Rate_count = 0
        self.CRIT_DMG_count = 0
        
        self.sub_op_names = []   # サブオプの名前を格納
        self.sub_ops = []    # サブオプの値を格納
        self.sub_op_increases = []   # サブオプの伸びた回数を格納
        self.count_sub_op = 0   # サブオプションの数
        
    # サブオプの伸び幅の候補
    ATK_flat_glowth_oprions = [14,16,18,19]
    ATK_per_glowth_oprions = [4.1,4.7,5.3,5.8]
    DEF_flat_glowth_oprions = [16,19,21,23]
    DEF_per_glowth_oprions = [5.1,5.8,6.6,7.3]
    HP_flat_glowth_oprions = [209,239,269,299]
    HP_per_glowth_oprions = [4.1,4.7,5.3,5.8]
    Elemental_glowth_oprions = [16,19,21,23]
    Recharge_glowth_oprions = [4.5,5.2,5.8,6.5]
    CRIT_Rate_glowth_oprions = [2.7,3.1,3.5,3.9]
    CRIT_DMG_glowth_oprions = [5.4,6.2,7.0,7.8]
    
    # スコア計算に利用する係数
    ATK_WEIGHT = 1
    CRIT_DMG_WEIGHT = 1
    CRIT_RATE_WEIGHT = 2
    
    # スコアを計算する関数
    def calc_score(self):
        # 誤差を防止するために10倍の値を計算してから10で割る
        score = (self.ATK_per*10 * Artifact.ATK_WEIGHT + 
                 self.CRIT_DMG*10 * Artifact.CRIT_DMG_WEIGHT + 
                 self.CRIT_Rate*10 * Artifact.CRIT_RATE_WEIGHT) / 10
        return score
    
    '''
    # サブオプの伸びた回数をカウントする関数
    def count_sub_op_increase(self):
        for i in range(len(self.sub_op_names)):
            if self.sub_op_names[i] == "攻撃力実数値":
                self.ATK_flat_count = int(min(self.ATK_flat//self.ATK_flat_glowth_oprions[0],6) - 1)
                self.sub_op_increases.append(self.ATK_flat_count)
            if self.sub_op_names[i] == "攻撃力％":
                self.ATK_per_count = int(min(self.ATK_per//self.ATK_per_glowth_oprions[0],6) - 1)
                self.sub_op_increases.append(self.ATK_per_count)
            if self.sub_op_names[i] == "防御力実数値":
                self.DEF_flat_count = int(min(self.DEF_flat//self.DEF_flat_glowth_oprions[0],6) - 1)
                self.sub_op_increases.append(self.DEF_flat_count)
            if self.sub_op_names[i] == "防御力％":
                self.DEF_per_count = int(min(self.DEF_per//self.DEF_per_glowth_oprions[0],6) - 1)
                self.sub_op_increases.append(self.DEF_per_count)
            if self.sub_op_names[i] == "ＨＰ実数値":
                self.HP_flat_count = int(min(self.HP_flat//self.HP_flat_glowth_oprions[0],6) - 1)
                self.sub_op_increases.append(self.HP_flat_count)
            if self.sub_op_names[i] == "ＨＰ％":
                self.HP_per_count = int(min(self.HP_per//self.HP_per_glowth_oprions[0],6) - 1)
                self.sub_op_increases.append(self.HP_per_count)
            if self.sub_op_names[i] == "元素熟知":
                self.Elemental_count = int(min(self.Elemental//self.Elemental_glowth_oprions[0],6) - 1)
                self.sub_op_increases.append(self.Elemental_count)
            if self.sub_op_names[i] == "元素チャージ効率":
                self.Recharge_count = int(min(self.Recharge//self.Recharge_glowth_oprions[0],6) - 1)
                self.sub_op_increases.append(self.Recharge_count)
            if self.sub_op_names[i] == "会心率":
                self.CRIT_Rate_count = int(min(self.CRIT_Rate//self.CRIT_Rate_glowth_oprions[0],6) - 1)
                self.sub_op_increases.append(self.CRIT_Rate_count)
            if self.sub_op_names[i] == "会心ダメージ":
                self.CRIT_DMG_count = int(min(self.CRIT_DMG//self.CRIT_DMG_glowth_oprions[0],6) - 1)
                self.sub_op_increases.append(self.CRIT_DMG_count)
                '''
                
    # サブオプの伸びた回数をカウントする関数
    def count_sub_op_increase(self):
        for i in range(len(self.sub_op_names)):
            if self.sub_op_names[i] == "攻撃力実数値":
                self.ATK_flat_count = int(round(self.ATK_flat/(self.ATK_flat_glowth_oprions[1]+self.ATK_flat_glowth_oprions[2])*2 - 1.0))
                self.sub_op_increases.append(self.ATK_flat_count)
            if self.sub_op_names[i] == "攻撃力％":
                self.ATK_per_count = int(round(self.ATK_per/(self.ATK_per_glowth_oprions[1]+self.ATK_per_glowth_oprions[2])*2 - 1.0))
                self.sub_op_increases.append(self.ATK_per_count)
            if self.sub_op_names[i] == "防御力実数値":
                self.DEF_flat_count = int(round(self.DEF_flat/(self.DEF_flat_glowth_oprions[1]+self.DEF_flat_glowth_oprions[2])*2 - 1.0))
                self.sub_op_increases.append(self.DEF_flat_count)
            if self.sub_op_names[i] == "防御力％":
                self.DEF_per_count = int(round(self.DEF_per/(self.DEF_per_glowth_oprions[1]+self.DEF_per_glowth_oprions[2])*2 - 1.0))
                self.sub_op_increases.append(self.DEF_per_count)
            if self.sub_op_names[i] == "ＨＰ実数値":
                self.HP_flat_count = int(round(self.HP_flat/(self.HP_flat_glowth_oprions[1]+self.HP_flat_glowth_oprions[2])*2 - 1.0))
                self.sub_op_increases.append(self.HP_flat_count)
            if self.sub_op_names[i] == "ＨＰ％":
                self.HP_per_count = int(round(self.HP_per/(self.HP_per_glowth_oprions[1]+self.HP_per_glowth_oprions[2])*2 - 1.0))
                self.sub_op_increases.append(self.HP_per_count)
            if self.sub_op_names[i] == "元素熟知":
                self.Elemental_count = int(round(self.Elemental/(self.Elemental_glowth_oprions[1]+self.Elemental_glowth_oprions[2])*2 - 1.0))
                self.sub_op_increases.append(self.Elemental_count)
            if self.sub_op_names[i] == "元素チャージ効率":
                self.Recharge_count = int(round(self.Recharge/(self.Recharge_glowth_oprions[1]+self.Recharge_glowth_oprions[2])*2 - 1.0))
                self.sub_op_increases.append(self.Recharge_count)
            if self.sub_op_names[i] == "会心率":
                self.CRIT_Rate_count = int(round(self.CRIT_Rate/(self.CRIT_Rate_glowth_oprions[1]+self.CRIT_Rate_glowth_oprions[2])*2 - 1.0))
                self.sub_op_increases.append(self.CRIT_Rate_count)
            if self.sub_op_names[i] == "会心ダメージ":
                self.CRIT_DMG_count = int(round(self.CRIT_DMG/(self.CRIT_DMG_glowth_oprions[1]+self.CRIT_DMG_glowth_oprions[2])*2 - 1.0))
                self.sub_op_increases.append(self.CRIT_DMG_count)
                

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
                    Artifact.sub_op_names.append("ＨＰ％")
                    Artifact.sub_ops.append(Artifact.HP_per)
                    Artifact.count_sub_op += 1
                    break
                elif is_noise.is_flat(sub_op[j]): # 実数値の場合
                    Artifact.HP_flat = int(is_noise.flat_value(sub_op[j]))
                    Artifact.sub_op_names.append("ＨＰ実数値")
                    Artifact.sub_ops.append(Artifact.HP_flat)
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
                    Artifact.sub_op_names.append("攻撃力％")
                    Artifact.sub_ops.append(Artifact.ATK_per)
                    Artifact.count_sub_op += 1
                    break
                elif is_noise.is_flat(sub_op[j]):
                    Artifact.ATK_flat = int(is_noise.flat_value(sub_op[j]))
                    Artifact.sub_op_names.append("攻撃力実数値")
                    Artifact.sub_ops.append(Artifact.ATK_flat)
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
                    Artifact.sub_op_names.append("防御力％")
                    Artifact.sub_ops.append(Artifact.DEF_per)
                    Artifact.count_sub_op += 1
                    break
                elif is_noise.is_flat(sub_op[j]):
                    Artifact.DEF_flat = int(is_noise.flat_value(sub_op[j]))
                    Artifact.sub_op_names.append("防御力実数値")
                    Artifact.sub_ops.append(Artifact.DEF_flat)
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
                    Artifact.sub_op_names.append("元素熟知")
                    Artifact.sub_ops.append(Artifact.Elemental)
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
                    Artifact.sub_op_names.append("元素チャージ効率")
                    Artifact.sub_ops.append(Artifact.Recharge)
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
                    Artifact.sub_op_names.append("会心率")
                    Artifact.sub_ops.append(Artifact.CRIT_Rate)
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
                    Artifact.sub_op_names.append("会心ダメージ")
                    Artifact.sub_ops.append(Artifact.CRIT_DMG)
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

