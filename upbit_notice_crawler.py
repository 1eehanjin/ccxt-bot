
import pprint
import requests
import re
from abstract_notice_crawler import AbstractNoticeCrawler
from notice import Notice
class UpbitNoticeCrawler(AbstractNoticeCrawler): 
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
        self.page_url = 'https://api-manager.upbit.com/api/v1/notices?page=1&per_page=20&thread_name=general'
        self.past_notices = {}
        self.init_past_notices()
    
    def crawl_new_listing_symbols(self, notices):
        try:
            notices = self.crawl_notices()
            return self.find_new_listing_symbols(notices)
        except Exception as e:
            print("예외 발생:", e)
            return []
        
    def find_new_listing_symbols(self, notices):
        latest_notice = notices[0]

        if not self.is_new_notice(latest_notice):
            return []
        self.append_past_notice(latest_notice)
        print("새로운 공지 추가 감지됨 : "+ latest_notice.title)
        if not self.is_listing_notice(latest_notice):
            return []
        symbols = self.extract_symbol(latest_notice)
        return symbols


    def crawl_notices(self): 
        #TODO: 프록시 등의 방법으로 딜레이 없이 계속 긁을 수 있도록 함수 바꿔야 함
        response = requests.get(self.page_url, headers=self.headers)
        upbit_notices = response.json()
        upbit_notices = upbit_notices['data']['list']
        notices = []
        for upbit_notice in upbit_notices:
            notice = Notice(str(upbit_notice['id']), upbit_notice['title'])
            notices.append(notice)
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