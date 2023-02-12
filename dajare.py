from time import sleep
import os
import math
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import pandas as pd

driver_path = "chromedriver"
options = Options()
options.add_argument('--headless')#バックグラウンドで
driver = webdriver.Chrome(executable_path=driver_path, options=options)

url = "https://dajare.jp/search/"

driver.get(url)
sleep(1)

key=['id','dajare','score']
while True:
    dajare_list=[]
    sleep(1)
    #ページをスクロールするjavascript
    while True:
        # スクロール速度をミリ秒で指定
        scroll_speed = 500
        # スクロールする
        driver.execute_script("window.scrollBy(0, 200);", 500)
        #残スクロールの高さ
        hiddenHeight = driver.execute_script(
            "return document.documentElement.scrollHeight - document.documentElement.clientHeight;")
        #まだスクロール量
        scrollPx = driver.execute_script(
            "return document.documentElement.scrollTop;")
        if math.floor(scrollPx/hiddenHeight*100) == 100:
            break
        # 指定の速度で待機
        sleep(scroll_speed / 1000)

    trs = driver.find_elements(By.CLASS_NAME, 'ListStripe')
    for tr in trs:
        id = (tr.find_element(By.CLASS_NAME,'ListWorkNumber').text)
        dajare = (tr.find_element(By.CLASS_NAME,'ListWorkBody').text)
        score = (tr.find_element(By.CLASS_NAME,'ListWorkScore').text)
        value = [id,dajare,score]
        dajare_list.append(dict(zip(key,value)))

    df = pd.DataFrame(dajare_list)
    if os.path.isfile('dajare.csv'):
        df.to_csv('dajare.csv',index=False,mode='a',header=False)
    else:
        df.to_csv('dajare.csv',index=False)
    # break#テスト用(最初の100件のみcsvにする。コメント化で全件取得に変わる)
    try:
        driver.find_element(By.CLASS_NAME,'LabelAnchorIconNext').click()
    except:
        break

# print(df.head())
driver.quit()
