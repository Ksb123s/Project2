from django.shortcuts import render, redirect
from serch.models import search_data

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
    return render(request, "Search/analyze.html")
