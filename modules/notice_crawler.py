from abc import *
import json
import pprint
from bs4 import BeautifulSoup
import requests
import re
from modules.message_sender import send_telegram_message
from modules.notice import Notice
from requests.auth import HTTPProxyAuth
import datetime

class AbstractNoticeCrawler(metaclass = ABCMeta):
    past_notices = {}
    with open('./secrets.json') as f:
        secret_data = json.load(f)
        proxies = secret_data['proxies']
        proxy_count = 0

    def init_past_notices(self): 
        notices = self.crawl_notices()
        for notice in notices:
            self.append_past_notice(notice)

    def is_new_notice(self, notice):
        return notice.id not in self.past_notices

    def append_past_notice(self, notice):
        self.past_notices[notice.id] = notice.title

    @abstractmethod
    def crawl_notices(self):
        pass

    @abstractmethod
    def is_listing_notice(self, notice_title):
        pass

    @abstractmethod
    def extract_symbol(self, listing_notice_title):
        pass

    @abstractmethod
    def crawl_new_listing_symbols(self):
        pass

    @abstractmethod
    def find_new_listing_symbols(self, notices):
        pass




class BithumbNoticeCrawler(AbstractNoticeCrawler) : 
    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "max-age=0",
            "Cookie": "bm_mi=E963DC0E906D505AD62ED42C770D1977~YAAQHnkyF5phtvOMAQAAbaafMRbu1sTkTrvaNtMfGPHAXwFNTkBpQo52KYDz70XwxPEudMrUydNluZ/BFP07MSUWZ0m5hoKveafrIanf0XjI1Pada/jgLRZlm04sI2yCY8nXOHKh66HcsF9mhDj66TIlmOqGAgDW4lP1cU/JWJczoXXZ9J1TcABkbXSY4AoY8z7Tatt2ok0QsaV0qVBe1K4rDBAE/amHPJfI1VUtHmtFUl4YJkrqWsEICVrhkqU3EbZpk/2vcd01POb/MNRR2XJfinzYzuYI2RiFy3VnpzAgviudN21zb8dUKd1Zve/FsTN+GKE=~1; bt_react=Y; bm_sz=D651494C3B11BCDDD9DAF56FDECF359D~YAAQHnkyF8BhtvOMAQAAfKqfMRbkQgcscdGZeh/wAUQPiFJN3z/thYV9UGHXlEJzS+lJUTR1NUV6aMsTdT9ZTf0BT00BmefZJEVEvqpxmhuh6MwkgHjMf5yu6vRhuQbj57XezSqZOXCUWKSjR06Q3uxBE06dY14ca8kdxPr2RgX6uBLNsNUCpfklIzjq0WB6GsKaCZK73kKvNc+zLVv6HUR7hYnFepbG/JUtc/GHTUQOpg1+0OSCYAmj7SEDfavl7U38DyE1qMUoWrZhQgEC68fI4pELFtoaQJ2YMURsMC0LtuFg6tIxHmI85PpJGEmBFRNEhA2Ir8CiZlIItyZYye4=~3556931~4604208; bm_sv=868E642E30078B545354F135E205DCB1~YAAQHnkyF8dhtvOMAQAAaaufMRamTYx89eDbQTZXXW8JKHsA/AwBZtVMWUGwBHqhal4uLijQGiYKKXIHy8kceZT/IeQxo97p6Qe7taS/Ctf1xb9GJDtdDB6f88yWnlhGzjsk6NqGNWQ8qKgWqmEAJQ8Mf0+uKba+kPG2cL7QU26T2LBbzmrgsiFDq6ZVPtPuMiAAUD49h3Hnqc78QaKvD6aZBOAxWGfnBglrLQi9HMJ3D5Ooitl9x4qoVDfjr6zAJQ==~1; _abck=3CF57AA484235310E5575F309FC1049A~0~YAAQHnkyF9JhtvOMAQAAxayfMQspmqLr98Zq94ZYvibxcemTqplJU8M9U+Y3DZYzPIrIcFghw8Jo7r3q1aSoy1kXIZULWXgLo9E4P9+Vlg8/JdYYTVWUrspNhd675NnzSGx9J5pgIfBedD/TpKNdx44ptxLl4zA+PVW4HmPWfQLC4G7h7VtrTsyo6tyY0xkzYnyLrcxCCwOApk3JxeVorqIuJmfM/0SdnQ3ZBOyRvExs2dcdvViEFPm8twPX5I759QdBt56kEevNgl13YdGDQlrBTjWGnHk9dO8jY3a751aI9mlaVlLlduMQtRS8HKBCcl6/akDLmzvdGkJW/pJgXZlhmeF9Q9dhITh1R7FgEHE3RWPTfvUtzPZTPNDljeWYj6tqi0sqF+WE2KDR5Jzx7Lyj26XJ2Wt1QA==~-1~-1~-1; _ga=GA1.2.2008935891.1705934565; _gid=GA1.2.1346499537.1705934565; ak_bmsc=C3801E00968007E62C735469AC9D462C~000000000000000000000000000000~YAAQHnkyF9VhtvOMAQAAIK6fMRZGU6hqvEs83vW+Yukcn7KS0NHk6qJUK1/8+NVMz+9wM1iIBIWkkmtNQQ60eOt8t8iJvu3wI+VnlfTmJFcnPT8eFmSf8cobNQYiBebyVzd7IAP8buxbKpu7YwfAnVfowUH+vEXs6Wp07kKzNplmjfhX6hzlc7x/L1jxaGHeJzvg0bqq+grqVLtVQFrOjMwVohcJUOvmgEj/NB89US5PV8MphsRg4wuFAio3z7mfowQZ1NjHrm8jh+0hKrjlHS6DE1wocLqQQhK6usAMyeYVpM04BP2xjIQiCip88hMsBrVZRjJQZukCiUb8zSuiI++qQZWfY6KnW7ZzYNTWZyfKuC6yPUWPxxq6YyMqyXU5maOy3rCPULpD5GsT1jrZ14Om9DblkWzpx/eUjR+tCR1FKHL8/q/HWocH/73zUVupsXai12Ex/lApSXVRix7lRxpzWCb/0EJ1yjCekEmvuy3LNzy1TSlEvf/kHEVG6Eo3BPw16my7TowpIfJqadp6IayVjug7WOZ2HypV; RT=\"z=1&dm=bithumb.com&si=988fdcb8-ccee-4592-b37e-dff711699261&ss=lrp1e4zo&sl=1&tt=te&bcn=%2F%2F684d0d4a.akstat.io%2F&ld=2r9&nu=2k8bnwg7&cl=41k\"; _ga_V9QC8ZLCKS=GS1.1.1705934565.1.0.1705934568.0.0.0",
            "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.page_url = "https://feed.bithumb.com/notice"
        # self.page_url2 = "https://cafe.bithumb.com/view/boards/43"
        self.init_past_notices()

    def crawl_new_listing_symbols(self):
        try:
            notices = self.crawl_notices()
            return self.find_new_listing_symbols(notices)
        except Exception as e:
            now = datetime.datetime.now()
            formatted_time = f"현재 시간: {now:%Y-%m-%d %H:%M:%S}"
            print(formatted_time + "| 예외 발생:", e)

            return []

    # def crawl_new_listing_symbols2(self):
    #     try:
    #         notices = self.crawl_notices2()
    #         return self.find_new_listing_symbols(notices)
    #     except Exception as e:
    #         now = datetime.datetime.now()
    #         formatted_time = f"현재 시간: {now:%Y-%m-%d %H:%M:%S}"
    #         print(formatted_time + "| 예외 발생:", e)

    #         return []

    def find_new_listing_symbols(self, notices):
        latest_notice = notices[0]
        
        if not self.is_new_notice(latest_notice):
            return []
        self.append_past_notice(latest_notice)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{current_time}에 새로운 공지 추가 감지됨: {latest_notice.title}")
        if not self.is_listing_notice(latest_notice):
            return []
        symbols = self.extract_symbol(latest_notice)
        return symbols



    def crawl_notices(self): 
        # self.proxy_count +=1
        # self.proxy_count %= len(self.proxies)
        # response = requests.get(self.page_url, headers=self.headers, proxies=self.proxies[self.proxy_count])
        response = requests.get(self.page_url, headers=self.headers)
        soup=BeautifulSoup(response.content,'lxml')
        
        string_data = soup.find(id="__NEXT_DATA__").string
        parsed_data = json.loads(string_data)
        bithumb_notices = parsed_data['props']['pageProps']['noticeList']
        notices = []
        for bithumb_notice in bithumb_notices:
            if bithumb_notice['topFixYn'] == 'Y':
                continue
            title = f"[{bithumb_notice['categoryName1']}]{bithumb_notice['title']}"
            notice = Notice(str(bithumb_notice['id']), title)
            notices.append(notice)
        if not notices:
            raise ValueError("빗썸 공지를 읽어오지 못했습니다.")
        return notices
    
    # def crawl_notices2(self): 
    #     response = requests.get(self.page_url2, headers=self.headers)
    #     soup=BeautifulSoup(response.content,'lxml')
    #     rank=soup.findAll(class_="invisible-mobile small-size")
    #     rank2=soup.findAll(class_="one-line")
    #     notices = []
    #     if len(rank):
    #         for i in range(0,30):
    #             notice_id=rank[i].text
    #             notice_title=rank2[i].text
    #             notice = Notice(notice_id, notice_title)
    #             if self.is_pinned_notice(notice):
    #                 continue
    #             notices.append(notice)
    #     return notices
    
    # def is_pinned_notice(self, notice):
    #     return notice.id == '■'

    def is_listing_notice(self, notice):
        return '[마켓 추가]' in notice.title

    def extract_symbol(self, notice):
        pattern = r'\(([A-Za-z0-9]+)\)'
        matches = re.findall(pattern, notice.title)
        return matches
    
class UpbitNoticeCrawler(AbstractNoticeCrawler): 
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
        self.page_url = 'https://api-manager.upbit.com/api/v1/notices?page=1&per_page=20&thread_name=general'
        self.past_notices = {}
        self.init_past_notices()
        
    
    def crawl_new_listing_symbols(self):
        try:
            notices = self.crawl_notices()
            return self.find_new_listing_symbols(notices)
        except Exception as e:
            now = datetime.datetime.now()
            formatted_time = f"현재 시간: {now:%Y-%m-%d %H:%M:%S}"
            print(formatted_time + "| 예외 발생:", e)
            return []


    def find_new_listing_symbols(self, notices):
        latest_notice = notices[0]
        
        if not self.is_new_notice(latest_notice):
            return []
        self.append_past_notice(latest_notice)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{current_time}에 새로운 공지 추가 감지됨: {latest_notice.title}")
        if not self.is_listing_notice(latest_notice):
            return []
        symbols = self.extract_symbol(latest_notice)
        return symbols



    def crawl_notices(self): 
        self.proxy_count +=1
        self.proxy_count %= len(self.proxies)
        response = requests.get(self.page_url, headers=self.headers, proxies=self.proxies[self.proxy_count])
        upbit_notices = response.json()
        upbit_notices = upbit_notices['data']['list']
        notices = []
        for upbit_notice in upbit_notices:
            notice = Notice(str(upbit_notice['id']), upbit_notice['title'])
            notices.append(notice)
        if not notices:
            raise ValueError("업비트 공지를 읽어오지 못했습니다.")
        return notices
    


    def is_listing_notice(self, notice):
        if "디지털 자산 추가" in notice.title:
            return True
        return False
    
    def extract_symbol(self, notice):
        pattern = r'\((.*?)\)' # 괄호로 둘러싸인 문자열을 찾는 패턴
        matches = re.findall(pattern, notice.title)
        if not matches:
            return []
        matches = matches[0]
        matches = matches.split(', ')
        symbols = []
        pattern = r'^[a-zA-Z0-9]+$'
        for str in matches:
            if re.match(pattern,str):
                symbols.append(str)
        return symbols