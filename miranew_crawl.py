# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 17:51:48 2024

@author: ASUS
"""

from selenium import webdriver
# from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.common.exceptions import ElementClickInterceptedException
# from selenium.common.exceptions import StaleElementReferenceException
# from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import requests as rq
from bs4 import BeautifulSoup as bs
from werkzeug.utils import secure_filename
import pandas as pd
from miranew_crawl_detail import detail_result
import traceback
import os
# import time
miranew_error='美麗新城 程式完美'
miranew_data=''
try:
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
    driver.get(r'https://www.miranewcinemas.com/Booking/Timetable')
    driver.implicitly_wait(10)
    visible_texts=['美麗新台茂影城 Tai-Mall Cinema','美麗新淡海影城 Dan-Hai Cinema','美麗新宏匯影城 Hon-Hui Cinema','美麗新大直皇家影城 Da-Zhi Royal Cinema']
    locater=(By.ID,'sel_cinema')
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locater))
    select_element = driver.find_element(By.ID,'sel_cinema')
    select = Select(select_element)
    chinese_name=[]
    eng_name=[]
    versions=[]
    dates_data_list=[]
    time_data_list=[]
    release_dates=[]
    genre=[]
    director=[]
    actor=[]
    description=[]
    data_cinema=[]
    l_move_img = []
    time_links=[]
    cinema_group=[]
    for visible_text in visible_texts:
        try:
            select.select_by_visible_text(visible_text)
        except NoSuchElementException:
            continue
        r=driver.page_source
        soup=bs(r,'html.parser')
        titles=soup.find_all(class_='MovieCName')
        titles_en=soup.find_all(class_='MovieEName')
        durations=soup.find_all(class_='MovieDuration')
        date_bars=driver.find_elements(By.CLASS_NAME,'ShowDateList')
        img_rs=soup.select('div.movie_post.col.movie_post_pc>img')
        # print(visible_text)
        n=0
        i=0
        for title,title_en,duration,date_bar,img_r in zip(titles,titles_en,durations,date_bars,img_rs):
            # print(title.text)
            # print(title_en.text)
            # print(duration.text)
            dates=date_bar.find_elements(By.CLASS_NAME,'movie_date')
            img=img_r.get('src')
            sess=rq.Session()
            res_img=sess.get(img,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'})
            filename = secure_filename(f'{title_en.text}.jpg')
            with open(filename,'wb') as file:
                file.write(res_img.content)
            for date in dates:
                date.click()
                r2=driver.page_source
                # r2=r2.split(title.text)[1]
                soup2=bs(r2,'html.parser')
                show_date=soup2.find_all(class_='movie_date')[i]
                # print(show_date.text)
                movie_times=soup2.find_all(class_='movie_list row')
                cinema_types=movie_times[n].find_all(class_='movie_time row')
                movie_times=movie_times[n].find(class_='ShowTimeList').find_all(class_='a_st')
                for cinema_type in cinema_types:
                    # print(cinema_type.find(class_='MovieHallCht col').text)
                    for movie_time in cinema_type.find_all(class_='a_st'):
                        eng_name.append(title_en.text)
                        chinese_name.append(title.text)
                        release_dates.append(detail_result[title.text][1])
                        genre.append(detail_result[title.text][2])
                        director.append(detail_result[title.text][3])
                        actor.append(detail_result[title.text][4])
                        description.append(detail_result[title.text][5])
                        time_data_list.append(movie_time.text)
                        dates_data_list.append(show_date.text.strip())
                        versions.append(cinema_type.find(class_='MovieHallCht col').text)
                        data_cinema.append(visible_text)
                        l_move_img.append(img)
                        time_links.append(r'https://www.miranewcinemas.com/Booking/Timetable')
                        cinema_group.append('美麗新影城')
                        # print(movie_time.text)
                i+=1
            n+=1
                # print(soup2.select('div')[1].text)
                # print(soup2.select('div')[2].text)
                # movie_times=soup2.find_all(class_='movie_time row')
                # for movie_time in movie_times:
                #     print(movie_time.text)
            
    driver.quit()
    miranew_data=pd.DataFrame({'中文片名':chinese_name,'英文片名':eng_name,'廳位':versions,
                            '日期':dates_data_list,'時刻表':time_data_list,'電影院名稱': data_cinema,'上映日':release_dates,'類型':genre,
                            '導演':director,'演員':actor,'簡介':description,'宣傳照':l_move_img,'time_link':time_links,'影城':cinema_group})
except Exception as e:
    tb = traceback.extract_tb(e.__traceback__)
    miranew_error='美麗新城錯誤報告\n'
    for frame in tb:
        miranew_error+=f"文件：{frame.filename}, 行號：{frame.lineno}, 錯誤類型：{e.__class__.__name__}, 錯誤信息：{e}\n"