# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 00:38:00 2024

@author: ASUS
"""
#123123
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import traceback
import os
shin_error='新光 程式完美'
data=''
try:
    # 新光影城電影介紹網站
    url1 = "https://www.skcinemas.com/films"
    # 新光影城電影時刻表網站
    url2 = "https://www.skcinemas.com/sessions"

    # 依順序儲存資料的list
    l_move_title = ["英文片名", "中文片名", "上映日", "簡介", "電影院名稱", "日期", "廳位", "時刻表",'宣傳照']
    l_move_img = []
    l_move_Eng = []
    l_move_Chr = []
    l_move_release_date = []
    l_move_introduction = []
    l_move_cinema_name = []
    l_move_date = []
    l_move_hall = []
    l_move_timetable = []
    l_move_img_1 = []
    l_move_Eng_1 = []
    l_move_Chr_1 = []
    l_move_release_date_1 = []
    l_move_introduction_1 = []
    youtube=[]
    time_links=[]
    l_moves_rule = []
    cinema_group=[]
    #------------------------------------------------------------------------------------------------------------
    # 使用動態抓取,並用隱性等待資訊完整抓取資料
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless") #無頭模式
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    # driver=webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=chrome_options)
    from selenium.webdriver.chrome.service import Service
    service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url1)
    driver.implicitly_wait(10)
    # 顯性等待最多10秒，每0.5秒尋找一次，於等待時間內尋找特定的字串出现。
    WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, "section-container")))
    # 切割期將上映前'poster-image'的數量
    move_cut_html = driver.page_source.split("即將上映")[0]
    move_cut_soup = BeautifulSoup(move_cut_html, "html.parser")
    move_cut = move_cut_soup.select('div.poster-image')
    # 尋找CLASS點擊進入電影名稱內網站
    move_names = driver.find_elements(By.CLASS_NAME,'poster-image')
    # 依序進入內容選取資訊
    for move_num in range(len(move_cut)):
        # print('點擊電影照進入頁面')
        move_names[move_num].click() #點擊電影照進入頁面
        # 顯性等待最多10秒，每0.5秒尋找一次，於等待時間內尋找特定的字串出现。
        WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, "into-content")))
        this_move = driver.page_source #取得本頁面資訊
        this_move_soup = BeautifulSoup(this_move, "html.parser") # 轉換當頁訊息成網頁語言
        poster_img = this_move_soup.select('img.poster-image') #尋找電影宣傳照
        move_Chr = this_move_soup.select('div.film-title') #尋找電影中文名稱
        move_Eng = this_move_soup.select('div.film-title-alt') #尋找影英文名稱
        release_date = this_move_soup.select('div.open-date') #尋找上映日期
        introduction = this_move_soup.select('div.into-content') #尋找電影簡介
        try:
            youtube_link=this_move_soup.find('iframe').get('src')
            print('我抓到了youtube')
            print(youtube_link)
        except AttributeError:
            print('我沒抓到youtube')
            youtube_link=''
        for i,img in enumerate(poster_img):
            # print('save img')
            l_move_img_1.append(img.get("src"))
            l_move_Eng_1.append(move_Eng[i].text)
            l_move_Chr_1.append(move_Chr[i].text)
            l_move_release_date_1.append(release_date[i].text.split(": ")[1])
            l_move_introduction_1.append(introduction[i].text)
        driver.back()
        WebDriverWait(driver, 10, 0.5).until(EC.element_to_be_clickable((By.CLASS_NAME,'poster-image')))
        move_names = driver.find_elements(By.CLASS_NAME,'poster-image')
    #------------------------------------------------------------------------------------------------------------
    driver.get(url2)
    # 等待所有時刻表出現(10秒)
    WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, "all-sessions-view")))
    cinema_html = driver.page_source #取得本頁面資訊
    cinema_soup = BeautifulSoup(cinema_html, "html.parser") # 轉換當頁訊息成網頁語言
    cinema_n = cinema_soup.select('div.item-container > div.title') #尋找電影院名稱
    # print(f'line 97 要跑{len(cinema_n)}')
    for num,c_n in enumerate(cinema_n):
        # 尋找CLASS點擊進入電影名稱內網站
        # print('line 97')
        cinema_name = driver.find_elements(By.CLASS_NAME, "item-container")[num].click()
        WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, "movie-sessions-view")))
        move_html = driver.page_source #取得本頁面資訊
        move_soup = BeautifulSoup(move_html, "html.parser") # 轉換當頁訊息成網頁語言
        
        move_n = move_soup.select('div.movie-sessions-view') #尋找本頁電影播放欄
        # print(f'line 103 要跑{len(move_n)}')
        for m_num , m in enumerate(move_n):
            # print('line 103')
            m_n = m.select('div.film-name') #尋找本欄電影名字
            m_dates = m.select('div.day-sessions') #尋找本欄電影播放日期欄
            # print(f'line 108 要跑{len(m_dates)}')
            for ds in m_dates:
                # print('line 108')
                m_date = ds.select('div.business-date') #尋找本欄電影播放日期
                m_time = ds.select('div.session') #尋找本欄電影播放時間
                # print(f'line 111 要跑{len(m_date)}')
                for d in m_date:
                    # print('line 111')
                    # print(f'line 112 要跑{len(m_time)}')
                    for t in m_time:
                        # print('line 112')
                        # print('l_move_Chr_1',l_move_Chr_1)
                        # print(m_n[0].text)
                        if m_n[0].text in l_move_Eng_1:
                            # print('line 114')
                            r_n = l_move_Eng_1.index(m_n[0].text) #對應於電影名稱中的排序位置
                            # 依序儲存每一筆資訊至list
                            l_move_img.append(l_move_img_1[r_n])
                            l_move_Eng.append(l_move_Eng_1[r_n])
                            l_move_Chr.append(l_move_Chr_1[r_n])
                            l_move_release_date.append(l_move_release_date_1[r_n])
                            l_move_introduction.append(l_move_introduction_1[r_n])
                            if 'Taichung' in c_n.text:
                                cinema_chinese_name='新光影城台中中港'
                            elif 'Taipei' in c_n.text:
                                cinema_chinese_name='新光影城台北獅子林'
                            elif 'Tianmu' in c_n.text:
                                cinema_chinese_name='新光影城台北天母'
                            elif 'Taoyuan' in c_n.text:
                                cinema_chinese_name='新光影城桃園青埔'
                            elif 'Tainan' in c_n.text:
                                cinema_chinese_name='新光影城台南西門'
                            else:
                                cinema_chinese_name=c_n.text
                            l_move_cinema_name.append(cinema_chinese_name)
                            l_move_date.append(d.text)
                            l_move_timetable.append(t.text)
                            youtube.append(youtube_link)
                            time_links.append('https://www.skcinemas.com/films')
                            cinema_group.append('星光影城')
    # finally:
        # driver.quit()
        
        
    # print('start making DataFrame')
    data = pd.DataFrame({ 
                        l_move_title[0] : l_move_Eng,
                        l_move_title[1] : l_move_Chr,
                        l_move_title[2] : l_move_release_date,
                        l_move_title[3] : l_move_introduction,
                        l_move_title[4] : l_move_cinema_name,
                        l_move_title[5] : l_move_date,
                        l_move_title[7] : l_move_timetable,
                        l_move_title[8] : l_move_img,
                        'youtube': youtube,
                        'time_link':time_links,
                        '影城':cinema_group
                        }) 
    # print('DataFrame done')
    shin_count=f'新光總共{len(data)}筆資料'
    # print(shin_count)
    shin_type=f'data is {type(data)}'
    # print(shin_type)
    # che=set(l_move_Chr)
    # data.to_csv("新光電影清單.csv",encoding="big5",index=False,errors="replace")
except Exception as e:
    # print(e)
    tb = traceback.extract_tb(e.__traceback__)
    shin_error='新光 錯誤報告\n'
    for frame in tb:
        shin_error+=f"文件：{frame.filename}, 行號：{frame.lineno}, 錯誤類型：{e.__class__.__name__}, 錯誤信息：{e}\n"
    
    print(shin_error)