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
from pydub import audio_segment
import requests
from bs4 import BeautifulSoup

playbot=1011929691566903306




# よくわからん。おまじない
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#トークン取得
token_text = open('../token.txt', 'r', encoding='UTF-8')
token = token_text.readline()
token_text.close


#音楽の長さを取得する
def getTime(musicpath):
    sound = AudioSegment.from_file(musicpath, "m4a")    # 情報の取得
    time = sound.duration_seconds # 再生時間(秒)、注意：float型
    return time


#メッセージを送る関数
async def sendMessage():
    print("send")
    botRoom = client.get_channel(playbot)   # botが投稿するチャンネルのID
    await botRoom.send("!play")

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
            MusicPathList = glob.glob('../music/*'+nextmusic+'*')
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





# 起動時処理
@client.event
async def on_ready():
    botRoom = client.get_channel(playbot)   # botが投稿するチャンネルのID
    await botRoom.send("BOTが起動しました!")
    print(f'ファイル位置：{__file__}')
    #サーバーにあるチャンネル情報の取得
    for channel in client.get_all_channels():
        print("----------")
        print("チャンネル名:" + str(channel.name))
        print("チャンネルID:" + str(channel.id))
        print("----------")
    # BOT情報の出力
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

   


# メッセージが送られた時の処理
@client.event
async def on_message(message):

    # 送信者がBOTの場合反応しない
    #if message.author.bot:
        #return

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




    # 入力を監視する対象のテキストチャンネル
    ReadingoutloudCannelIds = [1009332840120451113,1009329150928093224]
    #メッセージが送られたチャンネルを取得
    chid=message.channel.id
    if chid in ReadingoutloudCannelIds:
        print(0)




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
            musiclist = glob.glob('../music/*.m4a')
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
    if message.content == "!endlessplay":
        endless = True
        await playmusic(message)

    global nextmusic
    if message.content.startswith("!nextplay:"):
        if endless == False:
            await message.channel.send("連続再生中ではありません。")
        else:
            localnextmusic = message.content[10:]
            musiclist = glob.glob('../music/*'+localnextmusic+'*')
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





# チャンネル入退室時の通知処理
@client.event
async def on_voice_state_update(member, before, after):

    # チャンネルへの入室ステータスが変更されたとき（ミュートON、OFFに反応しないように分岐）
    if before.channel != after.channel:
        # 通知メッセージを書き込むテキストチャンネル（チャンネルIDを指定）
        botRoom = client.get_channel(1009335677881696276)

        # 入退室を監視する対象のボイスチャンネル（チャンネルIDを指定）
        announceChannelIds = [948454275955183630, 1009119186221539328]

        # 退室通知
        if before.channel is not None and before.channel.id in announceChannelIds:
            if not member.bot:
                await botRoom.send("**" + member.name + "** が、*" + before.channel.name + "*から現実に戻りました！")
        # 入室通知&BOT入室
        if after.channel is not None and after.channel.id in announceChannelIds:
            if not member.bot:
                await botRoom.send("**" + member.name + "**が 、*" + after.channel.name + "*に現実逃避に来ました！")
                #await member.voice.channel.connect()

            

client.run(token)