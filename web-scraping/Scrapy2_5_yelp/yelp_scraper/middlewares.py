# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class YelpScraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class YelpScraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

#================================================================================
# Thêm UserAgent thật của PC làm header mặc định
DEFAULT_REQUEST_HEADERS = {
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
}
# Tạo middleware 'RotateUserAgentMiddleware' để xoay vòng User-Agent
import random

class RotateUserAgentMiddleware:
    def __init__(self, user_agents): # Hàm __init__ là constructor, nhận vào một danh sách user_agents.
        self.user_agents = user_agents # Gán danh sách này cho biến self.user_agents để sử dụng sau.

    @classmethod # Cho phép định nghĩa một hàm class-level.
    def from_crawler(cls, crawler): # Hàm đặc biệt trong Scrapy, dùng để lấy cấu hình từ settings.py
        return cls(crawler.settings.getlist('USER_AGENT_LIST')) # khởi tạo class 'RotateUserAgentMiddleware' với danh sách USER_AGENT_LIST đã cấu hình sẵn trong settings.py

    def process_request(self, request, spider): # Hàm mà Scrapy sẽ gọi tự động cho mỗi lần nó gửi request
        request.headers['User-Agent'] = random.choice(self.user_agents) # Chọn ngẫu nhiên 1 user agent từ danh sách
        # -> gán user agent này vào request.headers['User-Agent'] để giả mạo trình duyệt mỗi lần gửi request.
        # -> Mỗi lần Scrapy gửi một request mới, middleware này sẽ tự động thay đổi User-Agent trong phần header, giúp giảm nguy cơ bị chặn.

#================================================================================
'''
# Tạo middlewares 'RotateProxyMiddleware' để xoay vòng Proxy (cách làm tương tự 'RotateUserAgentMiddleware')
class RotateProxyMiddleware:
    def __init__(self, proxy_list):
        self.proxy_list = proxy_list

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            proxy_list=crawler.settings.get('PROXY_LIST') # Cấu hình PROXY_LIST trong setting.py
        )

    def process_request(self, request, spider):
        request.meta['proxy'] = random.choice(self.proxy_list)
'''
#================================================================================
# Tích hợp ScrapingBee API vào Scrapy để bypass bảo mật của Yelp
# Yelp rất khó cào nếu không có stealth proxy, vì họ có reCAPTCHA, JS check, bot blocking cực mạnh
# Bạn đang scrape Yelp – cực kỳ khó chịu với bot → stealth_proxy là gần như bắt buộc!
# middlewares.py
import urllib.parse
from scrapy import Request

class ScrapingBeeMiddleware:
    def __init__(self, api_key):
        self.api_key = api_key

    @classmethod
    def from_crawler(cls, crawler):
        return cls(api_key=crawler.settings.get('SCRAPINGBEE_API_KEY'))

    def process_request(self, request, spider):
        original_url = request.url
        encoded_url = urllib.parse.quote(original_url, safe='')

        # Gửi request thông qua ScrapingBee với stealth_proxy
        api_url = (
            f"https://app.scrapingbee.com/api/v1/"
            f"?api_key={self.api_key}"
            f"&url={encoded_url}"
            f"&stealth_proxy=true"          # Bắt buộc với Yelp!
            f"&render_js=true"              # Load JS động nếu có
            f"&block_resources=false"       # Không chặn ảnh/css
        )

        return Request(
            url=api_url,
            callback=request.callback,
            errback=request.errback,
            meta=request.meta,
            headers=request.headers,
            dont_filter=True  # Cho phép lặp lại request
        )



