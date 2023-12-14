
from bs4 import BeautifulSoup
import requests
import re
from abstract_notice_crawler import AbstractNoticeCrawler
from notice import Notice

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
    
