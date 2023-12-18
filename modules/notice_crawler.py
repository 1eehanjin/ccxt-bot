from abc import *
from bs4 import BeautifulSoup
import requests
import re
from modules.notice import Notice


class AbstractNoticeCrawler(metaclass = ABCMeta):
    past_notices = {}

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
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ko",
            "Cache-Control": "max-age=0",
            "Cookie": "_ga_Q3CHT9RS7Z=GS1.1.1702539871.1.0.1702539871.60.0.0; _ga_V9QC8ZLCKS=GS1.1.1702539871.1.0.1702539871.0.0.0; _ga=GA1.2.2007189640.1702539872; _gid=GA1.2.651186856.1702539872; _dc_gtm_UA-46635015-21=1; _gat_gtag_UA_46635015_2=1; ak_bmsc=B822061DEB952B6817AD21C1A3D96627~000000000000000000000000000000~YAAQg3pGaKlpIlqMAQAAU8dIZxZmcAcxy6JmBS5ivr7njOvzjTfaWQ7QnVsWx3YxPEUPhbYWewwpH4S94LVsbDCMq0FyC9u+Tt2+7f/kiAgTTm7Ix6WwxjhVirGL8RYQ6NeV5qW2oQvAGe1vOR4zsmi/ufjgidf6RrGx/H7y5RnfQMXLh3pWzBctO45AaHDh0v/9bz9Bzm4vh5auT87nVJvUyrv1Mq2h5tvRUxckTiWoLBax4xjsp9NlWtupWA5LI3nDbvqUSrGUwbssot9rDNpKBM11HhXaVjsorpb53iblzAml13/JeTq1yL00Rwkr3VMRF686cLMzNge28jCfqb4yySm6WUWqE3TB6NyHAWMoBFQsYpYAdpRFvy/C2beyiZwWC09aHCVLXv3Az8x7EFfqGMptB72e8gG8UPn1cuoxpYYXNI9GCO0RVNARLOCRCytbjdBp+idxpJ5KBx78YoUjYdtWniOqFefL7y50G3kSX9ZIKJlKcJtA/ovjNPtS",
            "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "macOS",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.page_url = "https://cafe.bithumb.com/view/boards/43"
        self.init_past_notices()

    def crawl_new_listing_symbols(self):
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
        response = requests.get(self.page_url, headers=self.headers)
        soup=BeautifulSoup(response.content,'lxml')
        rank=soup.findAll(class_="invisible-mobile small-size")
        rank2=soup.findAll(class_="one-line")
        notices = []
        if len(rank):
            for i in range(0,30):
                notice_id=rank[i].text
                notice_title=rank2[i].text
                notice = Notice(notice_id, notice_title)
                if self.is_pinned_notice(notice):
                    continue
                notices.append(notice)
        return notices
    
    def is_pinned_notice(self, notice):
        return notice.id == '■'

    def is_listing_notice(self, notice):
        return notice.id != '■' and '[마켓 추가]' in notice.title

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