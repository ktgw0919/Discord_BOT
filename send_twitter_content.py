from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import urllib
import os

import paths

def get_twitter_content(twitter_url):
    # path
    tmp_img = paths.tmp_img # 画像の一時保管用フォルダ
    
    # XPath
    xpath_close_NOTIFICATIONSON_window = paths.xpath_close_NOTIFICATIONSON_window
    xpath_icon = paths.xpath_icon
    xpath_account_name = paths.xpath_account_name
    xpath_user_name = paths.xpath_user_name
    xpath_user_link = paths.xpath_user_link
    xpath_content = paths.xpath_content
    
    xpath_no_page_exist = paths.xpath_no_page_exist

    # headlessモードにする
    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Chrome()

    #特定のURLへ移動
    driver.get(twitter_url)
    sleep(0.2)

    # 各処理の最大待機時間を5秒にセット
    driver.implicitly_wait(5)
    
    # リンクが存在しないページ(シャドウバン等含む)だった場合の処理
    try:
        exists_page = driver.find_element(By.XPATH, xpath_no_page_exist)
        # print(exists_page.get_attribute("outerHTML"))
    except:
        pass
    else:
        print('error:Faild to access twitter.')
        return False
    
    #「通知をオンにする」ウィンドウを閉じる
    try:
        button_close_notify_window = driver.find_element(By.XPATH, xpath_close_NOTIFICATIONSON_window)
        button_close_notify_window.click()
    except:
        print('Caution:No notify button exist')
        
    sleep(0.1)

    # ツイ主のアイコンを取得
    try:
        element_icon = driver.find_element(By.XPATH, xpath_icon)
    except:
        print('error:Faild to get user icon.')
        return False
    # print(element_profile_picture.get_attribute("outerHTML"))
    # print(element_profile_picture.get_attribute("src"))
    icon_url = element_icon.get_attribute("src")
    # アイコン画像を画像URLからバイナリで読み込む
    # with urllib.request.urlopen(icon_url)as rf:
    #     icon_data = rf.read()
    # # アイコンの保存用フォルダを作成
    # try:
    #     os.mkdir(tmp_img)
    # except FileExistsError:
    #     pass
    # # アイコンのバイナリデータをpng形式で書き出す
    # with open(f"{tmp_img}/icon.png", mode="wb")as wf:
    #     wf.write(icon_data)
    sleep(0.1)

    # ツイ主のアカウント名を取得
    try:
        element_account_name = driver.find_element(By.XPATH, xpath_account_name)
    except:
        print('error:Faild to get account name.')
        return False
    # print(element_account_name.get_attribute("outerHTML"))    # デバッグ用
    account_name = element_account_name.text
    # print(account_name)
    sleep(0.1)

    # ツイ主のユーザー名(@hogehoge)を取得
    try:
        element_user_name = driver.find_element(By.XPATH, xpath_user_name)
    except:
        print('error:Faild to get user name.')
        return False
    user_name = element_user_name.text
    # print(user_name)
    sleep(0.1)

    # ツイ主のプロフリンクを取得
    try:
        element_user_url = driver.find_element(By.XPATH, xpath_user_link)
    except:
        print('error:Faild to get user url.')
        return False
    user_url = element_user_url.get_attribute("href")
    # print(user_url)
    sleep(0.1)

    # 内容を取得
    try:
        element_content = driver.find_element(By.XPATH, xpath_content)
    except:
        print('error:Faild to get content.')
        return False
    content = element_content.text
    # print(content)
    sleep(0.1)
    
    # 画像を取得
    # xpath_pcture_parent = paths.xpath_picture_parent
    # picture_count = 0
    # try:
    #     picture_parent_element = driver.find_element(By.XPATH, xpath_pcture_parent)
    # except:
    #     pass
    # else:
    #     picture_element = picture_parent_element.find_elements(By.TAG_NAME, 'img')
    #     picture_count = len(picture_element)
    # print(f'This tweet contain {picture_count} picture')
    # picture_url = []
    # for i in range(4):
    #     print((f'{twitter_url}/photo/{i + 1}'))
    #     driver.get(f'{twitter_url}/photo/{i + 1}')
    #     sleep(0.2)
    #     if driver.current_url == twitter_url:
    #         break
    #     else:
    #         picture_count += 1
            
            
    
    return [account_name, user_name, user_url, icon_url, content]
    
    
# def send_twitter_content(twitter_url):
#     account_name, user_name, user_url, content = get_twitter_content(twitter_url)
    