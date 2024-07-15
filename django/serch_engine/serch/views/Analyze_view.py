from django.shortcuts import render, get_object_or_404
from serch.models import (
    search_data,
    Engine_name,
    Detaile_name,
    Search_Keyword_Record_Data,
)
import json
from django.db.models import Q

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup

import time

import sys

import chromedriver_autoinstaller

# 그래프에 retina display 적용
# %config InlineBackend.figure_format = 'retina'

# 한글 폰트 설정
import koreanize_matplotlib


# 버전 변경에 따른 알림 메세지 무시하기
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)


def analyze(request):

    if request.POST:
        site = request.POST.get("site").strip()
        keyword = request.POST.get("keyword").strip()
        detail = request.POST.get("detail").strip()
        topic = request.POST.get("topic").strip()
        print(site, keyword, detail, topic)

        # detail_name과 engine_name을 Q 객체를 사용하여 필터링
        filters = Q(search_user=request.user)
        if detail:
            filters &= Q(detail_name__name=detail)
        if site:
            filters &= Q(engine_name__name=site)
        if keyword:
            filters &= Q(keyword=keyword)
        # print(filters)
        datas = search_data.objects.filter(filters)
        # print(datas)
        datas_list = list(datas.values())
        # print(f"1 변환전 : {datas_list} \n")
        for data in datas_list:
            data["created_at"] = data["created_at"].strftime(
                "%Y-%m-%d %H:%M:%S"
            )  # 날짜를 원하는 포맷의 문자열로 변환
            data["modified_at"] = data["modified_at"].strftime(
                "%Y-%m-%d %H:%M:%S"
            )  # 날짜를 원하는 포맷의 문자열로 변환
            data["engine_name_id"] = Engine_name.objects.get(
                id=data["engine_name_id"]
            ).name
            data["detail_name_id"] = Detaile_name.objects.get(
                id=data["detail_name_id"]
            ).name

        datas_json = json.dumps(datas_list)  # QuerySet을 JSON 문자열로 변환
        keyword_all = Search_Keyword_Record_Data.objects.filter(
            search_user=request.user
        )
        detail_all = Detaile_name.objects.all()
        context = {
            "datas": datas_json,
            "detail": detail_all,
            "keyword": keyword_all,
            "topic": topic,
        }
        return render(request, "Search/analyze.html", context)

    else:
        datas = search_data.objects.filter(search_user=request.user)
        keyword = Search_Keyword_Record_Data.objects.filter(search_user=request.user)
        detail = Detaile_name.objects.all()

        # 직렬화 전 데이터 처리
        datas_list = list(datas.values())
        # print(f"1 변환전 : {datas_list} \n")
        for data in datas_list:
            data["created_at"] = data["created_at"].strftime(
                "%Y-%m-%d %H:%M:%S"
            )  # 날짜를 원하는 포맷의 문자열로 변환
            data["modified_at"] = data["modified_at"].strftime(
                "%Y-%m-%d %H:%M:%S"
            )  # 날짜를 원하는 포맷의 문자열로 변환
            data["engine_name_id"] = Engine_name.objects.get(
                id=data["engine_name_id"]
            ).name
            data["detail_name_id"] = Detaile_name.objects.get(
                id=data["detail_name_id"]
            ).name

        datas_json = json.dumps(datas_list)  # QuerySet을 JSON 문자열로 변환
        # print(f"1 변환후 : {datas_json} \n")
        context = {"datas": datas_json, "detail": detail, "keyword": keyword}
    return render(request, "Search/analyze.html", context)
