# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import time

from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.utils.python import to_bytes
from urllib.parse import urlparse

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains

SOCIALBLADE_DOMAIN = 'socialblade.com'
YOUTUBE_DOMAIN = 'youtube.com'
MELON_DOMAIN = 'xn--o39an51b2re.com'
YOUTUBE_ROBOT = "https://youtube.com/robots.txt"
MELON_ROBOT = "https://xn--o39an51b2re.com/robots.txt"
SOCIALBLADE_ROBOT = "https://socialblade.com/robots.txt"
WEVERSE_ROBOT = "https://www.weverse.io/robots.txt"
CROWDTANGLE_ROBOT = "https://apps.crowdtangle.com/robots.txt"

class ScrapyAppSpiderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

def driver_setting():
    s = Service(ChromeDriverManager().install())
    chrome_options = Options()
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2,
            'plugins': 2,
            'popups': 2,
            'geolocation': 2,
            'notifications': 2,
            'auto_select_certificate': 2,
            'fullscreen': 2,
            'mouselock': 2,
            'mixed_script': 2,
            'media_stream': 2,
            'media_stream_mic': 2,
            'media_stream_camera': 2,
            'protocol_handlers': 2,
            'ppapi_broker': 2,
            'automatic_downloads': 2,
            'midi_sysex': 2,
            'push_messaging': 2,
            'ssl_cert_decisions': 2,
            'metro_switch_to_desktop': 2,
            'protected_media_identifier': 2,
            'app_banner': 2,
            'site_engagement': 2,
            'durable_storage': 2
        }
    }
    chrome_options.add_argument("--headless")                                            # Headless Mode
    chrome_options.add_argument("--no-sandbox")                                          # Bypass OS security model
    chrome_options.add_argument("--disable-gpu")                                         # 그래픽 카드 작동해제 => 성능 향상
    chrome_options.add_experimental_option("useAutomationExtension", False)              # disabling infobars
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')                             # user-agent 값 삽입 -> 봇 감지 방지
    chrome_options.add_argument("--start-maximized")                                    # open browser in maximized mode
    chrome_options.add_argument('lang=ko_KR')                                           # language setting at plug-in
    chrome_options.add_argument('--disable-extensions')                                 # disabling extensions
    chrome_options.add_experimental_option('prefs', prefs)                              # custom settings, disable = 2
    chrome_options.add_argument('log-level=3')
    chrome_options.add_argument('--disable-dev-shm-usage')                              # overcome limited resource problems
    driver = webdriver.Chrome(service=s, options=chrome_options)
    return driver

class NoLoginDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        self.driver.get(request.url)
        domain = urlparse(request.url).netloc
        print('crawling url : {}'.format(request.url))

        #Socialblade Case
        if(domain == SOCIALBLADE_DOMAIN):
            if(request.url != SOCIALBLADE_ROBOT):
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located(
                        (By.ID, 'YouTubeUserTopInfoWrap')
                    )
                )
        #Youtube Channel Case
        elif(domain == YOUTUBE_DOMAIN):
            if( request.url != YOUTUBE_ROBOT ):
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located(
                        (By.ID, 'right-column')
                    )
                )
        #Melon Channel Case
        elif(domain == MELON_DOMAIN):
            if( request.url != MELON_ROBOT ):
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, 'list-style-none')
                    )
                )

        body = to_bytes(text=self.driver.page_source)
        return HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        self.driver = driver_setting()

class LoginDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def spider_opened(self, spider):
        self.driver = driver_setting()
        self.login_process(spider)
        spider.logger.info('Spider opened: %s' % spider.name)

    def login_process(self, spider):
        if spider.name == 'weverse':
            self.driver.get('https://www.weverse.io/')
            self.driver.implicitly_wait(time_to_wait=5)
            self.driver.find_element(By.CLASS_NAME, 'sc-AxjAm.dhTrPj').click()
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.implicitly_wait(time_to_wait=5)
            self.driver.find_element(By.NAME, 'username').send_keys('sunrinkingh2160@gmail.com')
            self.driver.find_element(By.NAME, 'password').send_keys('!eogksalsrnr123')
            self.driver.find_element(By.CLASS_NAME, 'sc-Axmtr.hwYQYk.gtm-login-button').click()
            self.driver.switch_to.window(self.driver.window_handles[0])
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'sc-pjHjD.CNlcm'))
            )
        else:
            self.driver.get('https://apps.crowdtangle.com')
            self.driver.implicitly_wait(time_to_wait=5)
            self.driver.find_element(By.CLASS_NAME, 'facebookLoginButton__authButton--lof0c').click()
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.implicitly_wait(time_to_wait=5)
            self.driver.find_element(By.ID, 'email').send_keys('jaewon@ygmail.net')
            self.driver.find_element(By.ID, 'pass').send_keys('Ygfamily1234@')
            self.driver.find_element(By.ID, 'loginbutton').click()
            self.driver.switch_to.window(self.driver.window_handles[0])
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'app-container'))
            )

    def spider_closed(self, spider):
        self.driver.close()

    def process_request(self, request, spider):
        self.driver.get(request.url)
        print('crawling url : {}'.format(request.url))

        if spider.name == 'weverse':
            if request.url != WEVERSE_ROBOT:
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'sc-pcxhi.kMxZOc'))
                )
        else:
            if request.url != CROWDTANGLE_ROBOT:
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'report-top-level-metrics'))
                )
        body = to_bytes(text=self.driver.page_source)
        return HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass
