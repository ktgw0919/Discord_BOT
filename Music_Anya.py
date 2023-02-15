# �g�p���郉�C�u�����̃C���|�[�g
import discord  #discord.py
import re       #���K�\��
import random   #�����_��
import ffmpeg   #���y�Đ�
import os
import subprocess
import glob     #�����Ɉ�v����t�@�C�����擾
import time
import asyncio
from discord.ext import commands,tasks

from pydub import AudioSegment

playbot=1011929691566903306




# �悭�킩���B���܂��Ȃ�
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#�g�[�N���擾
token_text = open('token.txt', 'r', encoding='UTF-8')
token = token_text.readline()
token_text.close
# Bot�̃g�[�N�����w��i�f�x���b�p�[�T�C�g�Ŋm�F�\�j
client.run(token)


#���y�̒������擾����
def getTime(musicpath):
    sound = AudioSegment.from_file(musicpath, "m4a")    # ���̎擾
    time = sound.duration_seconds # �Đ�����(�b)�A���ӁFfloat�^
    return time


#���b�Z�[�W�𑗂�֐�
async def sendMessage():
    print("send")
    botRoom = client.get_channel(playbot)   # bot�����e����`�����l����ID
    await botRoom.send("!play")




#�����Đ��p
endless = False
preMusic = None
nextmusic = "m4a"
#���y�𖳌��ɍĐ�����֐�
async def playmusic(message):
    global endless
    global nextmusic
    if message.guild.voice_client is None:
        await message.channel.send("�ڑ����Ă��܂���B")
    elif message.guild.voice_client.is_playing():
        await message.channel.send("�Đ����ł��B")
    else:

        global preMusic
        music = None

        #�Đ�����Ȃ������_���őI��
        for i in range(100):
            MusicPathList = glob.glob('music/*'+nextmusic+'*')
            print(i)
            print(preMusic)
            music = random.choice(MusicPathList)
            #�O�񗬂ꂽ�ȂƓ����Ȃ��I�΂ꂽ��Ē��I(100��܂�)
            if music != preMusic:
                preMusic=music
                print(preMusic)
                break

        nextmusic='m4a'
        musiclength = getTime(music)

        music1 = os.path.split(music)[1]
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(music), volume=0.1)
        message.guild.voice_client.play(source)
        await message.channel.send("�h"+music1+"�h���Đ����܂��B")
        print(music1)
        print(musiclength)

        await asyncio.sleep(int(musiclength)+2)
        print("wake up")
        if(endless == True):
            await playmusic(message)
        #if(endless == False):
            #await message.channel.send("�Đ����I�����܂����B")





# �N��������
@client.event
async def on_ready():
    botRoom = client.get_channel(playbot)   # bot�����e����`�����l����ID
    await botRoom.send("BOT���N�����܂���!")
    #�T�[�o�[�ɂ���`�����l�����̎擾
    for channel in client.get_all_channels():
        print("----------")
        print("�`�����l����:" + str(channel.name))
        print("�`�����l��ID:" + str(channel.id))
        print("----------")
    # BOT���̏o��
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

   


# ���b�Z�[�W������ꂽ���̏���
@client.event
async def on_message(message):


    # ���M�҂�BOT�̏ꍇ�������Ȃ�
    #if message.author.bot:
        #return

    # ���A�@�\
    if not message.author.bot:
        if message.content.startswith("���͂悤"):  # ���b�Z�[�W���u���͂悤�v�Ŏn�܂邩���ׂ�
            m = "���͂悤�������܂� " + message.author.name + " ����I"  # �ԐM�̓��e
            await message.channel.send(m)# ���b�Z�[�W�������Ă����`�����l���փ��b�Z�[�W�𑗂�
    
    
    # �L���b�@�\
    # ���b�Z�[�W���X�g�i�ȉ��̂ǂꂩ��ԐM�j
    NyanList = [
        "�ɂ�`�`�`�`�`��",
        "�ɂ�`��",
        "�ɂ�`��H",
        "�ɂ��",
        "�ɂ��H"
        ]
    n=len(NyanList)
    # ���b�Z�[�W��"�ɂ�"���܂܂�Ă��邩���ׂ�
    pattern=u'�ɂ�'
    content = message.content
    repattern = re.compile(pattern)
    result=repattern.search(content)
    if result != None:
        if client.user != message.author:
            nyan = NyanList[random.randint(0,n-1)]    # �ԐM���e�������_���Ō���
            await message.channel.send(nyan)    # ���b�Z�[�W�������Ă����`�����l���փ��b�Z�[�W�𑗂�


    # �ǂݏグ�@�\
    # �SBOT���ޏo
    if message.content == "!join":
        if message.author.voice is None:
            await message.channel.send("���Ȃ��̓{�C�X�`�����l���ɐڑ����Ă��܂���B")
        # BOT���{�C�X�`�����l���ɐڑ�����
        else:
            await message.author.voice.channel.connect()
            await message.channel.send("**" + message.author.voice.channel.name + "** �ɁA*BOT*  ���������܂����I")
    elif message.content == "!leave":
        if message.guild.voice_client is None:
            await message.channel.send("BOT�̓{�C�X�`�����l���ɐڑ����Ă��܂���B")
        else:
            # �ؒf����
            await message.guild.voice_client.disconnect()
            await message.channel.send("*BOT* ���ޏo���܂����I")


    # BOT���ޏo
    if message.content == "!musicjoin":
        if message.author.voice is None:
            await message.channel.send("���Ȃ��̓{�C�X�`�����l���ɐڑ����Ă��܂���B")
        # BOT���{�C�X�`�����l���ɐڑ�����
        else:
            await message.author.voice.channel.connect()
            await message.channel.send("**" + message.author.voice.channel.name + "** �ɁA*BOT*  ���������܂����I")
    elif message.content == "!musicleave":
        if message.guild.voice_client is None:
            await message.channel.send("BOT�̓{�C�X�`�����l���ɐڑ����Ă��܂���B")
        else:
            # �ؒf����
            await message.guild.voice_client.disconnect()
            await message.channel.send("*BOT* ���ޏo���܂����I")




    # ���͂��Ď�����Ώۂ̃e�L�X�g�`�����l��
    ReadingoutloudCannelIds = [1009332840120451113,1009329150928093224]
    #���b�Z�[�W������ꂽ�`�����l�����擾
    chid=message.channel.id
    if chid in ReadingoutloudCannelIds:
        print(0)




    #���y�Đ�
    global endless
    #�Đ�����
    if message.content == "!play":
        if message.guild.voice_client is None:
            await message.channel.send("�ڑ����Ă��܂���B")
        elif message.guild.voice_client.is_playing():
            await message.channel.send("�Đ����ł��B")
        else:
            #�Đ�����Ȃ������_���őI��
            musiclist = glob.glob('../million/*.m4a')
            music = random.choice(musiclist)

            musiclength = getTime(music)

            music1 = os.path.split(music)[1]
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(music), volume=0.1)
            message.guild.voice_client.play(source)
            await message.channel.send("�h"+music1+"�h���Đ����܂��B")
            print(music1)
            print(musiclength)    
            

            
    #�I���Đ�����
    if message.content.startswith("!play:"):
        if message.guild.voice_client is None:
            await message.channel.send("�ڑ����Ă��܂���B")
        elif message.guild.voice_client.is_playing():
            await message.channel.send("�Đ����ł��B")
        else:
            musicname=message.content[6:]
            print(musicname)
            musiclist = glob.glob('../million/*'+musicname+'*')
            if not musiclist:
                await message.channel.send("�h "+musicname+"�h �͑��݂��܂���B")
            else:
                music = random.choice(musiclist)

                musiclength = getTime(music)

                music1 = os.path.split(music)[1]
                source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(music), volume=0.1)
                message.guild.voice_client.play(source)
                await message.channel.send("�h"+music1+"�h���Đ����܂��B")
                print(music1)
                print(musiclength) 


    #��~����
    elif message.content == "!stop":
        if message.guild.voice_client is None:
            await message.channel.send("�ڑ����Ă��܂���B")

        # �Đ����ł͂Ȃ��ꍇ�͎��s���Ȃ�
        elif not message.guild.voice_client.is_playing():
            await message.channel.send("�Đ����Ă��܂���B")
        else:
            message.guild.voice_client.stop()
            endless = False
            await message.channel.send("�X�g�b�v���܂����B")

            
    #��~����2
    elif message.content == "!lastplay":
        if message.guild.voice_client is None:
            await message.channel.send("�ڑ����Ă��܂���B")

        # �Đ����ł͂Ȃ��ꍇ�͎��s���Ȃ�
        elif not message.guild.voice_client.is_playing():
            await message.channel.send("�Đ����Ă��܂���B")
        else:
            endless = False
            await message.channel.send("���̋ȂŏI�����܂��B")


        
    #�����Đ�����
    if message.content == "!endlessplay":
        endless = True
        await playmusic(message)

    global nextmusic
    if message.content.startswith("!nextplay:"):
        if endless == False:
            await message.channel.send("�A���Đ����ł͂���܂���B")
        else:
            localnextmusic = message.content[10:]
            musiclist = glob.glob('../million/*'+localnextmusic+'*')
            if not musiclist:
                await message.channel.send("�h "+localnextmusic+"�h �͑��݂��܂���B")
            else:
                nextmusic = message.content[10:]
                await message.channel.send("�Ȏw��ɐ������܂����B")





# �`�����l�����ގ����̒ʒm����
@client.event
async def on_voice_state_update(member, before, after):

    # �`�����l���ւ̓����X�e�[�^�X���ύX���ꂽ�Ƃ��i�~���[�gON�AOFF�ɔ������Ȃ��悤�ɕ���j
    if before.channel != after.channel:
        # �ʒm���b�Z�[�W���������ރe�L�X�g�`�����l���i�`�����l��ID���w��j
        botRoom = client.get_channel(1009335677881696276)

        # ���ގ����Ď�����Ώۂ̃{�C�X�`�����l���i�`�����l��ID���w��j
        announceChannelIds = [948454275955183630, 1009119186221539328]

        # �ގ��ʒm
        if before.channel is not None and before.channel.id in announceChannelIds:
            if not member.bot:
                await botRoom.send("**" + member.name + "** ���A*" + before.channel.name + "*���猻���ɖ߂�܂����I")
        # �����ʒm&BOT����
        if after.channel is not None and after.channel.id in announceChannelIds:
            if not member.bot:
                await botRoom.send("**" + member.name + "**�� �A*" + after.channel.name + "*�Ɍ��������ɗ��܂����I")
                #await member.voice.channel.connect()

            
