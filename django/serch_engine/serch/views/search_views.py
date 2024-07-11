from django.shortcuts import render, redirect, get_object_or_404
from serch.models import (
    search_data,
    Engine_name,
    Detaile_name,
    Search_Keyword_Record_Data,
)
from django.contrib.auth.decorators import login_required
import re

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
    options.add_argument("--start-minimized")
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


@login_required(login_url="common:login")
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
                detail_name = get_object_or_404(Detaile_name, name=detail)
                engine_name = get_object_or_404(Engine_name, name=search_engine_name)
                update_or_create_search_record(
                    search_engine_keyword, engine_name, detail_name, request.user
                )
                record = Search_Keyword_Record_Data.objects.all()
                context = {
                    "list": list,
                    "detail": detail,
                    "keyword": search_engine_keyword,
                    "records": record,
                }
                print(record)
                return render(request, "Search/search.html", context)
            case "daum":
                url = "https://www." + search_engine_name + ".net/"
                browser.get(url)
                time.sleep(interval)
                element = browser.find_element(By.ID, "q")
                element.send_keys(search_engine_keyword)
                element.send_keys(Keys.ENTER)
                time.sleep(interval)
                tab_list = browser.find_elements(By.CLASS_NAME, "tab")
                detail_name = get_object_or_404(Detaile_name, name=detail)
                engine_name = get_object_or_404(Engine_name, name=search_engine_name)
                update_or_create_search_record(
                    search_engine_keyword, engine_name, detail_name, request.user
                )
                record = Search_Keyword_Record_Data.objects.all()
                time.sleep(interval)
                context = {
                    "list": list,
                    "detail": detail,
                    "keyword": search_engine_keyword,
                    "records": record,
                }
                print(record)
                time.sleep(interval)
                return render(request, "Search/search.html", context)
            case "naver":
                list = naver_crawl(
                    request,
                    browser,
                    interval,
                    search_engine_name,
                    search_engine_keyword,
                    detail,
                )
                # 검색 기록 저장 및 업데이트 코드
                detail_name = get_object_or_404(Detaile_name, name=detail)
                engine_name = get_object_or_404(Engine_name, name=search_engine_name)
                update_or_create_search_record(
                    search_engine_keyword, engine_name, detail_name, request.user
                )
                record = Search_Keyword_Record_Data.objects.all()
                context = {
                    "list": list,
                    "detail": detail,
                    "keyword": search_engine_keyword,
                    "records": record,
                }
                print(record)
                time.sleep(interval)
                return render(request, "Search/search.html", context)
    context = {"list": list}
    return render(request, "Search/search.html", context)


def naver_crawl(
    request, browser, interval, search_engine_name, search_engine_keyword, detail
):
    list = []
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
    match i_text:
        case "도서":
            print("도서")
            # book_list > ul > li:nth-child(1) > div > a.bookListItem_info_top__r54Eg.linkAnchor > div.bookListItem_text_area__9Qmyx > div.bookListItem_title__K9pVs > span > span
            titles = soup.select(
                ".bookListItem_title__K9pVs > span.bookListItem_text__SL9m9"
            )
            time.sleep(interval)
            # book_list > ul > li:nth-child(1) > div > a.bookListItem_info_top__r54Eg.linkAnchor > div.bookListItem_text_area__9Qmyx > div.bookListItem_detail__uZOWT > div:nth-child(1) > span.bookListItem_define_data__IUMgt

            users = soup.select(
                ".bookListItem_define_item__Jb5MS > span.bookListItem_define_data__IUMgt"
            )
            time.sleep(interval)
            # book_list > ul > li:nth-child(1) > div > div > div > span.bookPrice_price__OagxI
            prices = soup.select("span.bookPrice_price__OagxI")
            time.sleep(interval)
            # book_list > ul > li:nth-child(1) > div > a.bookListItem_info_top__r54Eg.linkAnchor
            book_urls = soup.select("a.bookListItem_info_top__r54Eg.linkAnchor")
            print()
            for idx in range(min([len(users), len(titles), len(prices)])):
                title = titles[idx].text.strip()
                user = users[idx].text.strip()
                price = prices[idx].text.strip()
                book_url = book_urls[idx]["href"]

                pattern = r"\d{1,3}(,\d{3})?"

                match = re.search(pattern, price)
                if match:
                    # 매칭된 부분에서 쉼표(,)를 제거하고 숫자만 남깁니다.
                    result = match.group().replace(",", "")
                    # print(result)
                else:
                    result = 0

                print(f"유저 : {user}/ 제목 :{title}/ 가격 : {result} ")

                list.append(
                    {
                        "num": idx + 1,
                        "user": user,
                        "title": title,
                        "price": price,
                        "url": book_url,
                    }
                )
                detail_name = get_object_or_404(Detaile_name, name=detail)
                engine_name = get_object_or_404(Engine_name, name=search_engine_name)
                try:
                    Search_data = search_data(
                        title=title,
                        user=user,
                        search_user=request.user,
                        keyword=search_engine_keyword,
                        engine_name=engine_name,
                        detail_name=detail_name,
                        price=result,
                        url=book_url,
                    )
                    Search_data.save()
                except:
                    print("존재하는 데이터 입니다.")

        case "이미지":
            images = browser.find_elements(By.CSS_SELECTOR, ".thumb img")
            # main_pack > section > div.api_subject_bx._fe_image_tab_grid_root.ani_fadein > div > div > div.image_tile._fe_image_tab_grid > div:nth-child(1) > div > a > div.info_title > span
            titles = soup.select("div.info_title > span")
            count = 1
            for img in images:
                try:
                    if count > 20:
                        break
                    img.click()
                    time.sleep(2)

                    # 큰이미지 //*[@id="main_pack"]/section[1]/div/div/div[1]/div[2]/div[1]/img
                    # div.viewer_image img
                    img_url = browser.find_element(
                        By.CSS_SELECTOR, "div.viewer_image img"
                    ).get_attribute("src")
                    title = titles[count - 1].text.strip()
                    print(img_url, title)

                    # urlretrieve("다운로드 받을 파일 경로","저장경로")
                    # urlretrieve(
                    #     img_url,
                    #     "C:\source\Project2\django\serch_engine\static\img\crawl_image\ "
                    #     + search_engine_keyword
                    #     + str(count)
                    #     + ".jpg",
                    # )
                    list.append({"img_url": img_url, "title": title})
                    count += 1
                    print(count)
                except:
                    pass
        case "지식iN":
            # main_pack > section > div.api_subject_bx > ul > li:nth-child(1) > div > div.question_area > div > a
            questions = soup.select(".question_area > div > a")
            time.sleep(interval)
            # main_pack > section > div.api_subject_bx > ul > li:nth-child(1) > div > div.answer_area > div.answer_group > a
            answers = soup.select(".answer_group > a")
            time.sleep(interval)
            # main_pack > section > div.api_subject_bx > ul > li:nth-child(30) > div > div.answer_area > div.profile_group > div > a > span.thumb > img
            imgs = soup.select(".profile_group > div > a > span.thumb > img")
            time.sleep(interval)
            # main_pack > section > div.api_subject_bx > ul > li:nth-child(1) > div > div.answer_area > div.profile_group > div > a > span.name
            answer_names = soup.select(".profile_group > div > a > span.name")
            for idx in range(len(questions)):
                question = questions[idx].text.strip()
                answer = answers[idx].text.strip()
                question_url = questions[idx]["href"]
                answer_img = imgs[idx]["src"]
                answer_name = answer_names[idx].text.strip()

                print(
                    f"답변자 : {answer_name}/답변자 이미지 : {answer_img}/ 답변 :{answer}/ 질문 : {question} / 답변 링크 {question_url}"
                )

                list.append(
                    {
                        "num": idx + 1,
                        "question": question,
                        "answer": answer,
                        "url": question_url,
                        "answer_img": answer_img,
                        "answer_name": answer_name,
                    }
                )

        case "지식백과":
            # main_pack > section > div.api_subject_bx.type_noline > ul > li:nth-child(2) > div > div > div.nkindic_tit > h3 > a
            titles = soup.select(".nkindic_tit > h3")

            # main_pack > section > div.api_subject_bx.type_noline > ul > li:nth-child(1) > div > div > div.nkindic_content > div.content_desc > a
            contents = soup.select(".content_desc > a")
            # main_pack > section > div.api_subject_bx.type_noline > ul > li:nth-child(1) > div > div > div.nkindic_content > div.content_desc > .nkindic_source > a
            users = soup.select(".nkindic_source > a")

            for idx in range(min([len(users), len(titles), len(contents)])):
                title = titles[idx].text.strip()
                content = contents[idx].text.strip()
                user = users[idx].text.strip()
                dict_url = users[idx]["href"]

                list.append(
                    {
                        "num": idx + 1,
                        "user": user,
                        "title": title,
                        "content": content,
                        "url": dict_url,
                    }
                )

        case "인플루언서":
            # _inf_content_root\ _fe_influencer_section > div > div.keyword_challenge_wrap > ul > li:nth-child(1) > div.keyword_box_wrap > div.user_box > div.user_box_inner > div.user_info > div.user_area
            Influencers = soup.select(".user_info > div.user_area")
            # _inf_content_root\ _fe_influencer_section > div > div.keyword_challenge_wrap > ul > li:nth-child(1) > div.keyword_box_wrap > div.detail_box > div.title_area > a
            titles = soup.select(".title_area > a")
            # _inf_content_root\ _fe_influencer_section > div > div.keyword_challenge_wrap > ul > li:nth-child(1) > div.keyword_box_wrap > div.detail_box > div.dsc_area > a
            contents = soup.select(".dsc_area > a")
            # _inf_content_root\ _fe_influencer_section > div > div.keyword_challenge_wrap > ul > li:nth-child(1) > div.keyword_box_wrap > div.user_box > div.user_box_inner > a > div > img
            thumb_imgs = soup.select(".user_box_inner > a > div > img")
            for idx in range(
                min([len(Influencers), len(titles), len(contents), len(thumb_imgs)])
            ):
                title = titles[idx].text.strip()
                content = contents[idx].text.strip()
                user = Influencers[idx].text.strip()
                influencer_url = titles[idx]["href"]
                thumb_img = thumb_imgs[idx]["src"]
                print(user, title, content)
                list.append(
                    {
                        "num": idx + 1,
                        "user": user,
                        "title": title,
                        "content": content,
                        "url": influencer_url,
                        "thumb_img": thumb_img,
                    }
                )

        case "동영상":
            contents = browser.find_elements(By.CLASS_NAME, "video_item")
        case "뉴스":
            contents = browser.find_elements(By.CLASS_NAME, "group_news")
        case "쇼핑":
            # content > div.style_content__xWg5l > div.basicList_list_basis__uNBZx > div > div:nth-child(1) > div > div > div.product_info_area__xxCTi > div.product_title__Mmw2K > a
            titles = soup.select(".product_title__Mmw2K > a")
            time.sleep(interval)
            # content > div.style_content__xWg5l > div.basicList_list_basis__uNBZx > div > div:nth-child(1) > div > div > div.product_mall_area___f3wo > div.product_mall_title__Xer1m > a.product_mall__hPiEH.linkAnchor
            # content > div.style_content__xWg5l > div.basicList_list_basis__uNBZx > div > div:nth-child(1) > div > div > div.product_mall_area___f3wo > div.product_mall_title__Xer1m > a.product_mall__hPiEH.linkAnchor > img
            users = soup.select("a.product_mall__hPiEH ")
            time.sleep(interval)
            # b#content > div.style_content__xWg5l > div.basicList_list_basis__uNBZx > div > div:nth-child(1) > div > div > div.product_info_area__xxCTi > div.product_price_area__eTg7I > strong > span.price > span
            prices = soup.select(".price > span")
            time.sleep(interval)
            for idx in range(min([len(users), len(titles), len(prices)])):
                title = titles[idx].text.strip()
                if users[idx].select_one("img") is not None:
                    user = users[idx].select_one("img")["alt"]
                else:
                    user = users[idx].text.strip()
                shop_url = titles[idx]["href"]
                price = prices[idx].text.strip()

                pattern = r"\d{1,3}(,\d{3})?"

                match = re.search(pattern, price)
                if match:
                    # 매칭된 부분에서 쉼표(,)를 제거하고 숫자만 남깁니다.
                    result = match.group().replace(",", "")
                    print(result)
                else:
                    result = 0

                print(f"유저 : {user}/ 제목 :{title}/ 가격 : {result} ")

                list.append(
                    {
                        "num": idx + 1,
                        "user": user,
                        "title": title,
                        "price": price,
                        "url": shop_url,
                    }
                )
                detail_name = get_object_or_404(Detaile_name, name=detail)
                engine_name = get_object_or_404(Engine_name, name=search_engine_name)
                Search_data = search_data(
                    title=title,
                    user=user,
                    search_user=request.user,
                    keyword=search_engine_keyword,
                    engine_name=engine_name,
                    detail_name=detail_name,
                    price=result,
                    url=shop_url,
                )
                Search_data.save()
        # 수정 봐야함  어학 사전
        case "어학사전":
            soup = BeautifulSoup(browser.page_source, "html.parser")
            # print(soup)
            # contents > div:nth-child(2)
            sections = soup.select("#contents > .section")
            print(sections)
            for idx in range(len(sections)):
                section = sections[idx]
                list.append({"source": section.prettify()})
        case "학술정보":
            contents = browser.find_elements(By.CLASS_NAME, "ui_listing_list")
        case "지도":
            contents = browser.current_url
        # 블로그 카페
        case _:
            users = soup.select(".user_box_inner > div > a")
            time.sleep(1)

            contents = soup.select(".title_area > a")
            time.sleep(1)

            # imgs = soup.select(".mod_ugc_thumb_area > a > img")
            # time.sleep(2)

            # img_url_list = []
            # print("들어가기전 ", len(users))
            for idx in range(min([len(users), len(contents)])):
                user = users[idx].text.strip()
                title = contents[idx].text.strip()
                content_url = contents[idx]["href"]
                # img = imgs[idx]["src"]
                print(f"유저 : {user}/ 제목 :{title}/ 링크 : {content_url} ")
                list.append(
                    {
                        "num": idx + 1,
                        "user": user,
                        "title": title,
                        "url": content_url,
                    }
                )
                detail_name = get_object_or_404(Detaile_name, name=detail)
                engine_name = get_object_or_404(Engine_name, name=search_engine_name)
                Search_data = search_data(
                    title=title,
                    user=user,
                    search_user=request.user,
                    keyword=search_engine_keyword,
                    engine_name=engine_name,
                    detail_name=detail_name,
                    url=content_url,
                )
                Search_data.save()
            # print("들어간후 ", len(list))
    return list


def daum_crawl():
    pass


def google_crawl():
    pass


def update_or_create_search_record(keyword, engine_name, detail_name, search_user):
    # 같은 정보가 이미 있는지 확인
    record, created = Search_Keyword_Record_Data.objects.get_or_create(
        keyword=keyword,
        engine_name=engine_name,
        detail_name=detail_name,
        search_user=search_user,
    )

    if not created:
        # 이미 존재하는 경우 count를 +1 증가시킴
        record.count += 1
        record.save()

    return record
