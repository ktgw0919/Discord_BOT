from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import urllib
import os

import paths

def get_twitter_content(twitter_url):
    #path
    tmp_img = paths.tmp_img # 画像の一時保管用フォルダ
    
    #XPath
    xpath_close_NOTIFICATIONSON_window = paths.xpath_close_NOTIFICATIONSON_window
    xpath_icon = paths.xpath_icon
    xpath_account_name = paths.xpath_account_name
    xpath_user_name = paths.xpath_user_name
    xpath_user_link = paths.xpath_user_link
    xpath_content = paths.xpath_content

    #headlessモードにする
    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Chrome()

    #特定のURLへ移動
    driver.get(twitter_url)
    sleep(5)

    #最大待機時間を5秒にセット
    driver.implicitly_wait(5)

    #「通知をオンにする」ウィンドウを閉じる
    try:
        button_close_notify_window = driver.find_element(By.XPATH, xpath_close_NOTIFICATIONSON_window)
        button_close_notify_window.click()
    except:
        print('error:No button exist')
    sleep(1)

    # ツイ主のアイコンを取得
    element_icon = driver.find_element(By.XPATH, xpath_icon)
    # print(element_profile_picture.get_attribute("outerHTML"))
    # print(element_profile_picture.get_attribute("src"))
    url_icon = element_icon.get_attribute("src")
    # アイコン画像を画像URLからバイナリで読み込む
    with urllib.request.urlopen(url_icon)as rf:
        icon_data = rf.read()
    # アイコンの保存用フォルダを作成
    try:
        os.mkdir(tmp_img)
    except FileExistsError:
        pass
    # アイコンのバイナリデータをpng形式で書き出す
    with open(f"{tmp_img}/icon.png", mode="wb")as wf:
        wf.write(icon_data)
    sleep(0.1)

    # ツイ主のアカウント名を取得
    element_account_name = driver.find_element(By.XPATH, xpath_account_name)
    # print(element_account_name.get_attribute("outerHTML"))    # デバッグ用
    account_name = element_account_name.text
    print(account_name)
    sleep(0.1)

    # ツイ主のユーザー名(@hogehoge)を取得
    element_user_name = driver.find_element(By.XPATH, xpath_user_name)
    user_name = element_user_name.text
    print(user_name)
    sleep(0.1)

    # ツイ主のプロフリンクを取得
    element_user_url = driver.find_element(By.XPATH, xpath_user_link)
    user_url = element_user_url.get_attribute("href")
    print(user_url)
    sleep(0.1)

    # 内容を取得
    element_content = driver.find_element(By.XPATH, xpath_content)
    content = element_content.text
    print(content)
    sleep(0.1)
    return(account_name, user_name, user_url, content)
    
    
def send_twitter_content(twitter_url):
    get_twitter_content(twitter_url)
    