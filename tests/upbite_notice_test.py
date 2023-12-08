import unittest
import requests
import pprint

class UpbitNoticeCrawlerTests(unittest.TestCase): 
    def setUp(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
        self.page_url = 'https://api-manager.upbit.com/api/v1/notices?page=1&per_page=20&thread_name=general'
        self.query_url = 'https://upbit.com/service_center/notice?id='
    def test_get_upbit_notices(self):
        response = requests.get(self.page_url, headers=self.headers)
        upbit_notice = response.json()
        pprint.pprint(upbit_notice)

if __name__ == '__main__':  
    suite = unittest.TestSuite()
    suite.addTest(UpbitNoticeCrawlerTests('test_get_upbit_notices'))  # 실행할 테스트 추가
    # suite.addTest(MyTestCase('test_two'))  # 다른 테스트 추가

    # 테스트 실행
    runner = unittest.TextTestRunner()
    runner.run(suite)