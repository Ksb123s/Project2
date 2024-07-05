from django.shortcuts import render, redirect
from serch.models import search_data

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains
from urllib.request import urlretrieve
import requests
import pandas as pd
from bs4 import BeautifulSoup


def set_chrome_driver():
    options = ChromeOptions()
    # options.add_argument("headless")
    # options.add_argument("--start-maximized")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    return driver


def scroll_all(browser, interval):
    prev_height = browser.execute_script("return document.documentElement.scrollHeight")

    while True:
        browser.execute_script(
            "window.scrollTo(0, document.documentElement.scrollHeight)"
        )

        time.sleep(interval)

        cur_height = browser.execute_script(
            "return document.documentElement.scrollHeight"
        )

        if cur_height == prev_height:

            break

        prev_height = cur_height

    browser.execute_script("window.scrollTo(0,0)")


# Create your views here.


def search(request):
    list = []
    interval = 2
    url = ""
    if request.POST:
        search_engine_name = request.POST.get("site")
        detail = request.POST.get("detail")
        search_engine_keyword = request.POST.get("search")
        print(search_engine_name, detail, search_engine_keyword)

        browser = set_chrome_driver()

        match search_engine_name:
            case "google":
                url = "https://www." + search_engine_name + ".com/"
                browser.get(url)
                time.sleep(2)
                element = browser.find_element(By.NAME, "q")
                element.send_keys(search_engine_keyword)
                element.send_keys(Keys.ENTER)
                time.sleep(interval)
                return redirect("search")
            case "daum":
                url = "https://www." + search_engine_name + ".net/"
                browser.get(url)
                time.sleep(interval)
                element = browser.find_element(By.ID, "q")
                element.send_keys(search_engine_keyword)
                element.send_keys(Keys.ENTER)
                time.sleep(interval)
                tab_list = browser.find_elements(By.CLASS_NAME, "tab")
                print(tab_list)
                time.sleep(interval)
                return redirect("search")
            case "naver":
                url = "https://www." + search_engine_name + ".com/"
                browser.get(url)
                time.sleep(interval)
                element = browser.find_element(By.ID, "query")
                element.send_keys(search_engine_keyword)
                element.send_keys(Keys.ENTER)
                time.sleep(interval)
                naver_list = browser.find_elements(By.CLASS_NAME, "tab")
                for link in naver_list:
                    a_link = link.get_attribute("href")
                    i_text = link.text.strip()
                    # print(i_text, a_link)
                    if i_text == detail:
                        browser.get(a_link)
                        break
                time.sleep(interval)
                scroll_all(browser, interval)
                soup = BeautifulSoup(browser.page_source, "lxml")
                match search_engine_name:
                    case "도서":
                        # book_list > ul > li:nth-child(1) > div > a.bookListItem_info_top__r54Eg.linkAnchor > div.bookListItem_text_area__9Qmyx > div.bookListItem_title__K9pVs
                        titles = soup.select(".bookListItem_title__K9pVs")
                        time.sleep(interval)
                        # book_list > ul > li:nth-child(1) > div > a.bookListItem_info_top__r54Eg.linkAnchor > div.bookListItem_text_area__9Qmyx > div.bookListItem_detail__uZOWT > div:nth-child(1) > span.bookListItem_define_data__IUMgt
                        users = soup.select("span.bookListItem_define_data__IUMgt")
                        time.sleep(interval)
                        # book_list > ul > li:nth-child(1) > div > div > div > span
                        prices = soup.select("span.bookPrice_price__OagxI")
                        time.sleep(interval)
                        for idx in range(len(users)):
                            title = titles[idx].text.strip()
                            user = users[idx].text.strip()
                            price = prices[idx].text.strip()

                            print(f"유저 : {user}/ 제목 :{title}/ 가격 : {price} ")

                            list.append(
                                {
                                    "num": idx + 1,
                                    "user": user,
                                    "title": title,
                                    "url": price,
                                }
                            )

                    case "이미지":
                        contents = browser.find_elements(By.CLASS_NAME, "image_wrap")
                    case "지식iN":
                        contents = browser.find_elements(By.CLASS_NAME, "lst_nkin")
                    case "지식백과":
                        contents = browser.find_elements(By.CLASS_NAME, "lst_nkindic")
                    case "인플루언서":
                        contents = browser.find_elements(
                            By.CLASS_NAME, "keyword_challenge_wrap"
                        )
                    case "동영상":
                        contents = browser.find_elements(By.CLASS_NAME, "video_item")
                    case "뉴스":
                        contents = browser.find_elements(By.CLASS_NAME, "group_news")
                    case "쇼핑":
                        contents = browser.find_elements(
                            By.CLASS_NAME, "basicList_list_basis__uNBZx"
                        )
                    case "어학사전":
                        contents = browser.find_elements(By.ID, "contents")
                    case "학술정보":
                        contents = browser.find_elements(
                            By.CLASS_NAME, "ui_listing_list"
                        )
                    case "지도":
                        contents = browser.current_url

                    case _:
                        users = soup.select(".user_box_inner > div > a")
                        time.sleep(1)

                        contents = soup.select(".title_area > a")
                        time.sleep(1)

                        # imgs = soup.select(".mod_ugc_thumb_area > a > img")
                        # time.sleep(2)

                        # img_url_list = []
                        # print("들어가기전 ", len(users))
                        for idx in range(len(users)):
                            user = users[idx].text.strip()
                            title = contents[idx].text.strip()
                            content_url = contents[idx]["href"]
                            # img = imgs[idx]["src"]
                            print(
                                f"유저 : {user}/ 제목 :{title}/ 링크 : {content_url} "
                            )
                            list.append(
                                {
                                    "num": idx + 1,
                                    "user": user,
                                    "title": title,
                                    "url": content_url,
                                }
                            )
                        # print("들어간후 ", len(list))

                context = {"list": list}
                time.sleep(interval)
                return render(request, "Search/search.html", context)
    context = {"list": list}
    return render(request, "Search/search.html", context)
