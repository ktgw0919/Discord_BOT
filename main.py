# 使用するライブラリのインポート
import discord  #discord.py
import re       #正規表現
import random   #ランダム
import ffmpeg   #音楽再生
import os
import subprocess
import glob     #条件に一致するファイルを取得
import time
import asyncio
from discord.ext import commands,tasks
from pydub import AudioSegment
import requests
import threading
from bs4 import BeautifulSoup
from discord.utils import get
import aiohttp
import cv2
import matplotlib.pyplot as plt
import unicodedata

import send_twitter_content
import paths
import calc_artifact_score
import test_opencv
import test_ocr

# bot用チャンネル
playbot_channel_name = "botとの戯れ"
notify_channel_name = "アーニャからのお知らせ"

# よくわからん。おまじない
intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)

#トークン取得
token_text = open(paths.token_path, 'r', encoding='UTF-8')
token = token_text.readline()
token_text.close


#音楽の長さを取得する
def getTime(musicpath):
    sound = AudioSegment.from_file(musicpath, "m4a")    # 情報の取得
    time = sound.duration_seconds # 再生時間(秒)、注意：float型
    return time

#スクレイピング用
def extract_post_counts(text):
    pattern = r'(\d+)件のイラスト'
    match = re.search(pattern, text)
    if match:
        count = int(match.group(1))
        return count
    else:
        return None

def get_pixiv_tag_post_count(tag):
    url = f'https://www.pixiv.net/tags/{tag}/artworks'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}

    response = requests.get(url, headers=headers)
    print(f'status_code:{response.status_code}')
    soup = BeautifulSoup(response.content, 'html.parser')

    post_count_element = soup.find('meta', {'property': 'og:description'})
    if post_count_element:
        #return int(post_count_element.get_text(strip=True).replace(',', ''))
        count = extract_post_counts(post_count_element.get('content'))
        if count is not None:
            return (count)
        else:
            return None
    else:
        return None


#無限再生用
endless = False
preMusic = None
nextmusic = "m4a"
#音楽を無限に再生する関数
async def playmusic(message):
    global endless
    global nextmusic
    if message.guild.voice_client is None:
        await message.channel.send("接続していません。")
    elif message.guild.voice_client.is_playing():
        await message.channel.send("再生中です。")
    else:

        global preMusic
        music = None

        #再生する曲をランダムで選択
        for i in range(100):
            MusicPathList = glob.glob(paths.music_path + '/*'+nextmusic+'*')
            print(i)
            print(preMusic)
            music = random.choice(MusicPathList)
            #前回流れた曲と同じ曲が選ばれたら再抽選(100回まで)
            if music != preMusic:
                preMusic=music
                print(preMusic)
                break

        nextmusic='m4a'
        musiclength = getTime(music)

        music1 = os.path.split(music)[1]
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(music), volume=0.1)
        message.guild.voice_client.play(source)
        await message.channel.send("”"+music1+"”を再生します。")
        print(music1)
        print(musiclength)

        await asyncio.sleep(int(musiclength)+2)
        print("wake up")
        if(endless == True):
            await playmusic(message)
        #if(endless == False):
            #await message.channel.send("再生を終了しました。")
            
def send_messages_from_terminal(channel):
    while True:
        # サーバーのリストを表示
        print("\nAvailable Servers:")
        for i, guild in enumerate(client.guilds):
            print(f"{i+1}. {guild.name}")

        # ユーザーにサーバーの選択を求める
        server_choice = int(input("Choose a server (by number) or type '0' to quit: ")) - 1
        if server_choice == -1:
            print("Exiting terminal input mode...")
            break
        chosen_guild = client.guilds[server_choice]

        # 選択されたサーバーのチャンネルをリスト表示
        print("\nAvailable Channels in " + chosen_guild.name + ":")
        text_channels = [channel for channel in chosen_guild.channels if isinstance(channel, discord.TextChannel)]
        for i, channel in enumerate(text_channels):
            print(f"{i+1}. {channel.name}")

        # ユーザーにチャンネルの選択を求める
        channel_choice = int(input("Choose a channel (by number): ")) - 1
        chosen_channel = text_channels[channel_choice]

        # メッセージの入力を求める
        print("Enter your message to send. Type '_END_' on a new line to finish input or 'exit' to stop:")
        lines = []
        while True:
            line = input()
            if line.lower() == "_end_":
                break
            elif line.lower() == "exit":
                print("Exiting terminal input mode...")
                return
            else:
                lines.append(line)

        message_to_send = "\n".join(lines)

        # 選択されたチャンネルにメッセージを送信
        asyncio.run_coroutine_threadsafe(chosen_channel.send(message_to_send), client.loop)

game_channel_names=[
    "Apex",
    "Valorant",
    "LoL",
    "崩壊：スターレイル",
    "原神",
    "学園アイドルマスター",
    "ブルーアーカイブ",
    "バンドリ"
]

# 起動時処理
@client.event
async def on_ready():
    for guild in client.guilds:
        exist_channel = False
        # await guild.me.edit(nick=None)
        for channel in guild.channels:
            if channel.name == playbot_channel_name:
                await channel.send("BOTが起動しました!")
                exist_channel = True
        if not exist_channel:
            print(f"{guild.name} (ID: {guild.id}) では、{playbot_channel_name} という名前のチャンネルが見つかりませんでした。")

    print(f'ファイル位置：{__file__}')
    
    #サーバーにあるチャンネル情報の取得
    print(f'{client.user} としてログインしました。\n')

    for guild in client.guilds:
        print(f"サーバー名: {guild.name}")
        print(f"サーバーID: {guild.id}")
        print("チャンネル情報:")
        for channel in guild.channels:
            print(f"  チャンネル名: {channel.name}")
            print(f"  チャンネルID: {channel.id}")
            print("  ----------")
        print("====================================")
    # BOT情報の出力
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
    # メッセージ送信
    # threading.Thread(target=send_messages_from_terminal, args=(channel,)).start()


# メッセージが送られた時の処理
@client.event
async def on_message(message):

    # 送信者がBOTの場合反応しない
    #if message.author.bot:
        #return

    if not message.author.bot:
        print(f'{message.author=}')
        print(f'{message.author.name=}')
        print(f'{message.author.id=}')
        print(f'{message.author.nick=}')
        print(f'{message.author.display_name=}')
    
    # 挨拶機能
    if not message.author.bot:
        if message.content.startswith("おはよう"):  # メッセージが「おはよう」で始まるか調べる
            m = "おはようございます " + message.author.name + " さん！"  # 返信の内容
            await message.channel.send(m)# メッセージが送られてきたチャンネルへメッセージを送る
    
    
    # 猫語会話機能
    # メッセージリスト（以下のどれかを返信）
    NyanList = [
        "にゃ～～～～～ん",
        "にゃ～ん",
        "にゃ～ん？",
        "にゃん",
        "にゃん？"
        ]
    n=len(NyanList)
    # メッセージに"にゃ"が含まれているか調べる
    pattern=u'にゃ'
    content = message.content
    repattern = re.compile(pattern)
    result=repattern.search(content)
    if result != None:
        if client.user != message.author:
            nyan = NyanList[random.randint(0,n-1)]    # 返信内容をランダムで決定
            await message.channel.send(nyan)    # メッセージが送られてきたチャンネルへメッセージを送る


    # 読み上げ機能
    # 全BOT入退出
    if message.content == "!join":
        if message.author.voice is None:
            await message.channel.send("あなたはボイスチャンネルに接続していません。")
        # BOTがボイスチャンネルに接続する
        else:
            await message.author.voice.channel.connect()
            await message.channel.send("**" + message.author.voice.channel.name + "** に、*BOT*  が入室しました！")
    elif message.content == "!leave":
        if message.guild.voice_client is None:
            await message.channel.send("BOTはボイスチャンネルに接続していません。")
        else:
            # 切断する
            await message.guild.voice_client.disconnect()
            await message.channel.send("*BOT* が退出しました！")


    # BOT入退出
    if message.content == "!musicjoin":
        if message.author.voice is None:
            await message.channel.send("あなたはボイスチャンネルに接続していません。")
        # BOTがボイスチャンネルに接続する
        else:
            await message.author.voice.channel.connect()
            await message.channel.send("**" + message.author.voice.channel.name + "** に、*BOT*  が入室しました！")
    elif message.content == "!musicleave":
        if message.guild.voice_client is None:
            await message.channel.send("BOTはボイスチャンネルに接続していません。")
        else:
            # 切断する
            await message.guild.voice_client.disconnect()
            await message.channel.send("*BOT* が退出しました！")

    #音楽再生
    global endless
    #再生処理
    if message.content == "!play":
        if message.guild.voice_client is None:
            await message.channel.send("接続していません。")
        elif message.guild.voice_client.is_playing():
            await message.channel.send("再生中です。")
        else:
            #再生する曲をランダムで選択
            musiclist = glob.glob(paths.music_path + '/*.m4a')
            music = random.choice(musiclist)

            musiclength = getTime(music)

            music1 = os.path.split(music)[1]
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(music), volume=0.1)
            message.guild.voice_client.play(source)
            await message.channel.send("”"+music1+"”を再生します。")
            print(music1)
            print(musiclength)    
            

            
    #選択再生処理
    if message.content.startswith("!play:"):
        if message.guild.voice_client is None:
            await message.channel.send("接続していません。")
        elif message.guild.voice_client.is_playing():
            await message.channel.send("再生中です。")
        else:
            musicname=message.content[6:]
            print(musicname)
            musiclist = glob.glob('../music/*'+musicname+'*')
            if not musiclist:
                await message.channel.send("” "+musicname+"” は存在しません。")
            else:
                music = random.choice(musiclist)

                musiclength = getTime(music)

                music1 = os.path.split(music)[1]
                source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(music), volume=0.1)
                message.guild.voice_client.play(source)
                await message.channel.send("”"+music1+"”を再生します。")
                print(music1)
                print(musiclength) 


    #停止処理
    elif message.content == "!stop":
        if message.guild.voice_client is None:
            await message.channel.send("接続していません。")

        # 再生中ではない場合は実行しない
        elif not message.guild.voice_client.is_playing():
            await message.channel.send("再生していません。")
        else:
            message.guild.voice_client.stop()
            endless = False
            await message.channel.send("ストップしました。")

            
    #停止処理2
    elif message.content == "!lastplay":
        if message.guild.voice_client is None:
            await message.channel.send("接続していません。")

        # 再生中ではない場合は実行しない
        elif not message.guild.voice_client.is_playing():
            await message.channel.send("再生していません。")
        else:
            endless = False
            await message.channel.send("この曲で終了します。")


        
    #無限再生処理
    # if message.content == "!endlessplay":
    #     endless = True
    #     await playmusic(message)

    global nextmusic
    if message.content.startswith("!nextplay:"):
        if endless == False:
            await message.channel.send("連続再生中ではありません。")
        else:
            localnextmusic = message.content[10:]
            musiclist = glob.glob(paths.music_path + '/*' + localnextmusic+'*')
            if not musiclist:
                await message.channel.send("” "+localnextmusic+"” は存在しません。")
            else:
                nextmusic = message.content[10:]
                await message.channel.send("曲指定に成功しました。")
    
    #スクレイピング
    if message.content.startswith("!pixiv:"):
        tag = message.content[7:]
        print(tag)
        post_image_count = get_pixiv_tag_post_count(tag)

        if post_image_count is not None:
            print(f'{tag}の投稿数: {post_image_count}')
            await message.channel.send(f'pixivでの\'#{tag}\'のイラスト・漫画の投稿数は{post_image_count}件です！')
        else:
            print('投稿数を取得できませんでした。')
            await message.channel.send(f'{tag}の投稿数を取得できませんでした(＞＜)')
            
    # ツイート内容取得
    # メッセージのコンテンツがTwitterのURL形式に一致するかチェック
    twitter_url_pattern = r"https?://(?:www\.)?(twitter|x)\.com/\w+/status/\d+"
    twitter_reg = re.search(twitter_url_pattern, message.content)
    if twitter_reg and message.content.startswith("!"):
        twitter_url = twitter_reg.group()
        print(f'\nget contet of \'{twitter_url}\'')
        tweet_content = send_twitter_content.get_twitter_content(twitter_url)
        if tweet_content is False:
            await message.channel.send('ツイートの取得に失敗しました．ログインしないと見ることができないツイートかもしれません．')
        else:
            account_name, user_name, user_url, icon_url, content = tweet_content
            # print(f'{account_name},{user_name},{user_url},{content}')
            embed_twitter = discord.Embed(
                # title = "Twitter",
                color = 0x1da1f2,
                description = content,
                url = twitter_url 
            )
            embed_twitter.set_author(
                name = f'{account_name} ({user_name})',
                url = twitter_url,
                icon_url = icon_url
            )
            
            # 作成者
            # fname = "ktgw_icon.jpg "
            # file = discord.File(fp = paths.ktgw_icon_path, filename = fname, spoiler = False)
            # embed_twitter.set_image(url=f"attachment://{fname}")
            embed_twitter.set_footer(
                text = 'This Embed is made by ktgw.',
            )
            await message.channel.send(embed = embed_twitter)
            
    # 四則計算
    if message.content.startswith("="):
        print("calc:"+message.content)
        try:
            await message.reply(eval(message.content[1:], {'__builtins__': None}))
        except:
            print("error")
            
    # 画像が送信されている場合
    if len(message.attachments)>0:
        file_count =  len(message.attachments)
        print(f"{file_count} fails have been sent.")
        for attachment in message.attachments:
            print(attachment.content_type)
            if attachment.content_type == "image/png":
                # await attachment.save(paths.image_path + "/image.png")
                # img_path = paths.image_path + "/image.png" # 画像のパス
                # 画像を取得して保存
                async with aiohttp.ClientSession() as session:
                    async with session.get(attachment.url) as response:
                        if response.status == 200:
                            with open(os.path.join(paths.tmp_img,"artifact.png"), 'wb') as f:
                                f.write(await response.read())
                            # print(f'path={os.path.join(paths.tmp_img,"artifact.png")}')
                
                img_path = os.path.join(paths.tmp_img,"artifact.png") # 画像のパス
                img = cv2.imread(img_path)
                print(f'{img.shape=}')
                # if img.shape[0] != 1080 or img.shape[1] != 1920:
                #     print("FHDではない画像")
                #     continue
                tmp_img_path = test_opencv.convert_image(img_path) # 画像の前処理
                sub_op = test_ocr.render_doc_text(tmp_img_path) # OCRでサブオプを取得

                artifact = calc_artifact_score.Artifact()
                calc_artifact_score.assign_values(artifact, sub_op) # 聖遺物クラスにサブオプを代入
                score = artifact.calc_score() # スコア計算
                artifact.count_sub_op_increase() # サブオプの増加数をカウント
                if score == 0:
                    continue
                print(f'{score=}')
                score_str = ""
                for i in range(len(artifact.sub_op_names)):
                    score_str += f'{artifact.sub_op_names[i]:　<10}：{artifact.sub_ops[i]}'
                    if artifact.sub_op_increases[i] != 0:
                        score_str += f'   (+{artifact.sub_op_increases[i]}かも)'
                    score_str += f'\n'
                await message.reply(score_str+"----------------------------------\n"+f'聖遺物スコア：{score}')
            
        return
    
    # print(f'{message.author.global_name=}')

# チャンネル入退室時の通知処理
@client.event
async def on_voice_state_update(member, before, after):
    if not member.bot:
        #入室通知
        if before.channel is None and after.channel is not None:
            notifyChannel = get(member.guild.channels, name = '入退出通知')
            if notifyChannel is not None:
                await notifyChannel.send(f'{member.display_name} が 、 {after.channel.name} チャンネルに現実逃避に来ました！')       
            guild = member.guild
            print(f'{guild.name}に{member.name}が入室')
        #退室通知
        if before.channel is not None and after.channel is None:
            notifyChannel = get(member.guild.channels, name = '入退出通知')
            if notifyChannel is not None:
                await notifyChannel.send(f'{member.display_name} が 、 {before.channel.name}  チャンネルから現実に戻ってしまいました...')       
            guild = member.guild
            print(f'{guild.name}から{member.name}が退室')

client.run(token)
