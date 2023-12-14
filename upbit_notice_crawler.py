
import requests
import re

class UpbitNoticeCrawler(): 
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
        self.page_url = 'https://api-manager.upbit.com/api/v1/notices?page=1&per_page=20&thread_name=general'
        upbit_notices = self.get_upbit_notices()
        latest_notice_title = self.extract_latest_notice_title(upbit_notices)
        self.set_latest_notice(latest_notice_title)
        self.test_count = 0

    def get_upbit_notices(self): 
        #TODO: 프록시 등의 방법으로 딜레이 없이 계속 긁을 수 있도록 함수 바꿔야 함
        response = requests.get(self.page_url, headers=self.headers)
        upbit_notices = response.json()
        return upbit_notices
    
    def get_upbit_notices_for_test(self):
        if self.test_count < 5:
            self.test_count += 1
            return self.get_upbit_notices()
        else:
            dumynotice = {"success":True,"data":{"total_count":3418,"total_pages":171,"list":[{"created_at":"2023-12-07T14:05:02+09:00","updated_at":"2023-12-08T16:41:40+09:00","id":3911,"title":"[거래] BTC 마켓 디지털 자산 추가 (AAVE)","view_count":100340},{"created_at":"2023-12-06T14:13:27+09:00","updated_at":"2023-12-08T16:41:40+09:00","id":3910,"title":"[입출금] 코스모스(ATOM) 네트워크 업그레이드에 따른 입출금 일시 중단 안내 (12/13 18:00 ~)","view_count":976548},{"created_at":"2023-12-06T11:27:09+09:00","updated_at":"2023-12-08T16:40:37+09:00","id":3909,"title":"[NFT 드롭스] 현대 민화의 대표 작가 김근중 \u0026 목탄으로 그린 어둠의 미학 이재삼 ","view_count":269323},{"created_at":"2023-12-05T23:05:21+09:00","updated_at":"2023-12-08T16:40:37+09:00","id":3908,"title":"[안내] 엔케이엔(NKN) 입출금 일시 중단 안내","view_count":290295},{"created_at":"2023-12-05T17:41:59+09:00","updated_at":"2023-12-08T16:41:40+09:00","id":3907,"title":"[NFT 드롭스] 전은숙, 피페팅 - 골라먹는 미미(美味) ","view_count":207855},{"created_at":"2023-12-05T16:29:26+09:00","updated_at":"2023-12-08T16:40:37+09:00","id":3906,"title":"[안내] 유통량 계획표 변경 안내 : 오리진프로토콜(OGN)","view_count":119483},{"created_at":"2023-12-05T16:18:25+09:00","updated_at":"2023-12-08T16:40:37+09:00","id":3905,"title":"[안내] 유통량 계획표 신규 안내 : 아이오타(IOTA)","view_count":37327},{"created_at":"2023-12-05T13:55:20+09:00","updated_at":"2023-12-08T16:40:37+09:00","id":3904,"title":"[입출금] 파일코인(FIL) 네트워크 업그레이드에 따른 입출금 일시 중단 안내 (12/12 18:00 ~)","view_count":224992},{"created_at":"2023-12-04T18:05:03+09:00","updated_at":"2023-12-08T16:40:37+09:00","id":3902,"title":"[안내] 가상자산 실명계정 운영지침 적용에 따른 원화 입출금 관련 변동사항 안내 (1/1 적용 예정)","view_count":401568},{"created_at":"2023-12-04T14:37:30+09:00","updated_at":"2023-12-08T16:41:40+09:00","id":3901,"title":"[디지털 자산] 11월 5주차 GAS, VTHO 지급 안내","view_count":278391},{"created_at":"2023-12-02T02:29:55+09:00","updated_at":"2023-12-08T16:40:37+09:00","id":3900,"title":"[안내] 코스모스(ATOM) 입출금 일시 중단 안내 (완료)","view_count":601439},{"created_at":"2023-12-01T23:10:19+09:00","updated_at":"2023-12-08T16:40:37+09:00","id":3899,"title":"[안내] 코스모스(ATOM) 입출금 일시 지연 안내","view_count":31944},{"created_at":"2023-12-01T17:32:21+09:00","updated_at":"2023-12-08T16:41:40+09:00","id":3898,"title":"[NFT] 생물다양성 보전 '시드볼트 NFT 컬렉션' 프로젝트 요원 모집을 위한 드롭스 및 SNS 인증 이벤트 안내","view_count":248663},{"created_at":"2023-12-01T16:48:43+09:00","updated_at":"2023-12-08T16:40:37+09:00","id":3897,"title":"[안내] 유통량 정보 제공 목적 및 유통량 이슈 제보 채널 개설 안내","view_count":96127},{"created_at":"2023-12-01T11:07:35+09:00","updated_at":"2023-12-08T16:40:37+09:00","id":3896,"title":"[안내] 유통량 계획표 변경 안내 : 아이큐(IQ)","view_count":493034},{"created_at":"2023-12-01T03:34:42+09:00","updated_at":"2023-12-08T16:40:37+09:00","id":3895,"title":"[안내] 수이(SUI) 입출금 일시 중단 안내 (완료)","view_count":229856},{"created_at":"2023-11-30T18:40:31+09:00","updated_at":"2023-12-08T16:40:37+09:00","id":3894,"title":"[NFT] KBO 공식 NFT 크볼렉트(KBOLLECT) 프로젝트 변동 사항 안내","view_count":139889},{"created_at":"2023-11-30T17:34:41+09:00","updated_at":"2023-12-08T16:41:40+09:00","id":3893,"title":"[입출금] ICX, ZIL, XLM 입출금 일시 중단 안내 (완료)","view_count":129124},{"created_at":"2023-11-30T17:30:48+09:00","updated_at":"2023-12-08T16:40:37+09:00","id":3892,"title":"[안내] 두나무앤파트너스 디지털 자산 보유수량 안내 (2023년 11월)","view_count":39345},{"created_at":"2023-11-30T14:00:00+09:00","updated_at":"2023-12-08T16:40:37+09:00","id":3891,"title":"[거래] BTC 마켓 디지털 자산 추가 (ID)","view_count":352827}],"fixed_notices":[{"created_at":"2023-10-10T08:00:00+09:00","updated_at":"2023-12-08T16:40:37+09:00","id":3772,"title":"[안내] 착오전송 디지털 자산 찾아가기 캠페인 및 착오전송 디지털 자산 복구 서비스 무료 지원 안내","view_count":276922},{"created_at":"2023-04-13T16:56:42+09:00","updated_at":"2023-12-08T16:40:37+09:00","id":3453,"title":"[안내] 특정 코인을 통한 투자 손실 보존 유도 및 업비트 임직원 사칭 주의 안내","view_count":2905318},{"created_at":"2022-08-25T20:00:02+09:00","updated_at":"2023-12-08T16:40:37+09:00","id":2895,"title":"[중요] 특정금융정보법에 따른 미신고 가상자산사업자와의 입출금 제한 및 유의사항 (2023.07.19 추가)","view_count":629565},{"created_at":"2022-05-20T12:28:19+09:00","updated_at":"2023-12-08T16:41:39+09:00","id":2677,"title":"[공지] 가상자산 거래에 관한 위험 고지","view_count":6292273},{"created_at":"2022-05-18T22:10:10+09:00","updated_at":"2023-12-08T16:40:37+09:00","id":2672,"title":"[안내] 알고리즘 스테이블 코인 연관 디지털 자산 투자 주의 안내 (업데이트)","view_count":303066},{"created_at":"2022-03-29T19:45:41+09:00","updated_at":"2023-12-08T16:40:36+09:00","id":2553,"title":"[중요] 트래블룰 관련 입출금 유의사항 안내","view_count":167999},{"created_at":"2022-01-20T14:48:56+09:00","updated_at":"2023-12-08T16:40:36+09:00","id":2397,"title":"[안내] 디지털 자산 오입금 관련 유의사항 안내","view_count":2451443}]}}
            print("더미 상장 공지 리턴")
            return dumynotice
    
    def extract_latest_notice_title(self, upbit_notices):
        latest_notice = upbit_notices['data']['list'][0]['title']
        return latest_notice
    
    def is_new_notice(self, upbit_notice_title):
        if self.latest_notice != upbit_notice_title:
            return True
        return False

    def set_latest_notice(self, upbit_notice_title):
        print("최신 공지 갱신: "+ upbit_notice_title)
        self.latest_notice = upbit_notice_title

    def is_listing_notice(self, upbit_notice_title):
        if "디지털 자산 추가" in upbit_notice_title:
            return True
        return False
    
    
    def extract_symbol_from_listing_notice(self, upbit_notice_title):
        pattern = r'\((.*?)\)' # 괄호로 둘러싸인 문자열을 찾는 패턴
        match = re.search(pattern, upbit_notice_title)
        symbol_str =  match.group(1)
        symbols = symbol_str.split(', ')
        return symbols
    
    def crawl_listing_symbol(self):
        #TODO: 테스트 함수에서 실제 함수로 바꿔야 함, 이런거 테스트 어떻게 하는지...
        upbit_notices = self.get_upbit_notices_for_test()
        crawled_notice_title = self.extract_latest_notice_title(upbit_notices)
        if not self.is_new_notice(crawled_notice_title):
            return []
        self.set_latest_notice(crawled_notice_title)
        if not self.is_listing_notice(crawled_notice_title):
            return []
        symbols = self.extract_symbol_from_listing_notice(crawled_notice_title)
        return symbols
        
        
        
