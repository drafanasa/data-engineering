# Scrapy settings for yelp_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "yelp_scraper"

SPIDER_MODULES = ["yelp_scraper.spiders"]
NEWSPIDER_MODULE = "yelp_scraper.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "yelp_scraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False # ->  Yelp sử dụng robots.txt nghiêm ngặt → có thể cần tắt ROBOTSTXT_OBEY trong settings.py nếu chỉ học tập.

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "yelp_scraper.middlewares.YelpScraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "yelp_scraper.middlewares.YelpScraperDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "yelp_scraper.pipelines.YelpScraperPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

#================================================================================
# Cấu hình USER_AGENT_LIST cho middleware 'RotateUserAgentMiddleware' vừa tạo bên middlewares.py
DOWNLOADER_MIDDLEWARES = {
    'yelp_scraper.middlewares.RotateUserAgentMiddleware': 543,
}
# Dùng https://iplogger.org/useragents/ để gen một số User Agent ngẫu nhiên
USER_AGENT_LIST = [
    'Mozilla/5.0 (iPod; CPU iPod OS 11_9_2; like Mac OS X) AppleWebKit/600.4 (KHTML, like Gecko)  Chrome/55.0.2234.220 Mobile Safari/600.6',
    'Mozilla/5.0 (Linux i541 x86_64; en-US) Gecko/20130401 Firefox/59.8',
    'Mozilla/5.0 (iPod; CPU iPod OS 10_8_2; like Mac OS X) AppleWebKit/603.40 (KHTML, like Gecko)  Chrome/48.0.3126.355 Mobile Safari/603.0',
    'Mozilla/5.0 (Linux; U; Linux i581 ; en-US) AppleWebKit/603.1 (KHTML, like Gecko) Chrome/54.0.1685.109 Safari/601',
    'Mozilla/5.0 (Linux; Android 4.3.1; Samsung Galaxy SIV Mega GT-I9200 Build/JDQ39) AppleWebKit/602.1 (KHTML, like Gecko)  Chrome/55.0.2834.382 Mobile Safari/601.6',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 8_2_2; en-US) AppleWebKit/602.5 (KHTML, like Gecko) Chrome/47.0.2136.225 Safari/536',
    'Mozilla/5.0 (Windows NT 6.0; Win64; x64; en-US) Gecko/20130401 Firefox/69.3',
    'Mozilla/5.0 (Linux; U; Linux x86_64; en-US) Gecko/20100101 Firefox/54.4',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 7_5_1; en-US) AppleWebKit/533.17 (KHTML, like Gecko) Chrome/51.0.1360.154 Safari/602'
]

#================================================================================
'''
# CẤU HÌNH PROXY_LIST cho middleware 'RotateProxyMiddleware' vừa tạo bên middlewares.py
DOWNLOADER_MIDDLEWARES.update({
    'yelp_scraper.middlewares.RotateProxyMiddleware': 544,
})

PROXY_LIST = [
    # Proxy bình thường: http://<ip>:<port>
    'http://113.160.148.71',

    # Proxy có authenticate: http://<username>:<password>@<ip>:<port>
    #'http://username:password@123.456.789.000:8080',
]
'''
#================================================================================
# CẤU HÌNH THỜI GIAN DELAY & RETRY GIỮA MỖI LẦN REQUEST
DOWNLOAD_DELAY = 2         # Delay giữa các request (giảm tải server)
RETRY_ENABLED = True       # Bật tính năng tự động retry nếu request fail
RETRY_TIMES = 3            # Retry tối đa 3 lần nếu gặp lỗi như timeout, 500, 403,...
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429] #  Cấu hình thêm những mã lỗi nào sẽ được retry

#================================================================================
# CẤU HÌNH SCRAPINGBEE API ĐỂ BYPASS BẢO MẬT CỦA YELP
# ✅ API Key của tôi:
SCRAPINGBEE_API_KEY = '1VR97WT3DWF0BPXN52OPW9IXYRKQIE5Q81YEOFCVXHNZ5YD0PU739011W0VDMZ518BIBYNRQ21NR1B9V'

# ✅ Bật middleware ScrapingBee
DOWNLOADER_MIDDLEWARES = {
    'yelp_scraper.middlewares.ScrapingBeeMiddleware': 543,
}
