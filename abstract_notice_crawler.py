from abc import *

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