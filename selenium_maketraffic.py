# Selenium으로 자동 웹 트래픽 생성.
# urls 내의 사이트들에 접속하고 스크롤을 내리거나 클릭하는 등의 액션을 수행하면서 네트워크 로그를 생성.
# 이후 실시간으로 HTTP 요청 및 응답, 패킷 크기, IP 주소, 브라우저 트래픽을 tshark 또는 scapy로 수집.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import os
from stem.control import Controller
from stem import Signal
#TOR_CONTROL_PORT=os.getenv("TOR_CONTROL_PORT")
#TOR_PROXY=os.getenv("TOR_PROXY")
CRAWLING_DURATION=int(os.getenv("CRAWLING_DURATION"))
WEBSITES=os.getenv("WEBSITES", "").split(",")

'''
# 새로운 IP 요청 함수
def renew_tor_ip():
    with Controller.from_port(port=int(TOR_CONTROL_PORT)) as controller:
        #controller.authenticate(password=TOR_PASSWORD)
        controller.signal(Signal.NEWNYM)
    print("새로운 Tor IP 요청 완료!")'
'''

# 크롬 드라이버 설정 (using Tor)
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
#options.add_argument(f"--proxy-server={TOR_PROXY}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)

start_time = time.time()

search_keywords = ["machine learning", "AI news", "latest technology", "best programming languages", "open source projects"]

for url in WEBSITES:
    driver.get(url)
    time.sleep(3)  # 페이지 로딩 대기
    # 구글 검색 자동화
    if "google.com" in url:
        try:
            search_box = driver.find_element(By.NAME, "q")
            search_box.send_keys(random.choice(search_keywords))  # 랜덤 검색어 입력
            search_box.send_keys(Keys.RETURN)
            print("구글에서 검색 수행")
            time.sleep(random.uniform(3, 6))
        except:
            print("구글 검색 실패")
    # 위키백과 랜덤 문서 방문
    elif "wikipedia.org" in url:
        try:
            driver.get("https://en.wikipedia.org/wiki/Special:Random")  # 랜덤 문서
            print("랜덤 위키백과 문서 방문")
            time.sleep(random.uniform(3, 6))
        except:
            print("위키백과 랜덤 문서 방문 실패")
    # 깃허브에서 인기 저장소 방문
    elif "github.com" in url:
        try:
            driver.get("https://github.com/trending")  # 인기 저장소 페이지
            print("깃허브 인기 저장소 방문")
            time.sleep(random.uniform(5, 8))
        except:
            print("깃허브 인기 저장소 방문 실패")
    # 트위터에서 로그인 페이지 이동 (로그인 시도 X)
    elif "twitter.com" in url:
        try:
            driver.get("https://twitter.com/login")  # 로그인 페이지 방문
            print("트위터 로그인 페이지 방문")
            time.sleep(random.uniform(5, 8))
        except:
            print("트위터 방문 실패")
    
    '''
    # Tor IP 변경 요청
    if random.random() < 0.3:  # 30% 확률로 IP 변경
        renew_tor_ip()
        time.sleep(5)  # Tor 네트워크 갱신 대기 시간
    '''

    # 스크롤 액션 추가 (모든 사이트 공통)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 스크롤 내리기
    time.sleep(random.uniform(2,4))

    if time.time() - start_time > CRAWLING_DURATION:
        break

driver.quit()