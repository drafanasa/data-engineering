import scrapy
from ..items import QuoteItem


class QuotespiderSpider(scrapy.Spider):
    name = "quotespider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        quotes = response.xpath('//div[@class="quote"]') # quotes là một selector dạng list, chứa HTML nên không dùng .getall()

        # Tạo vòng lặp scraping data:
        for quote in quotes:
            item = QuoteItem() # gọi class QuoteItem() dể định nghĩa cho danh sách 'item'

            # Lưu ý:
            # -> quote là một block nhỏ được tách từ respons quotes
            # -> dùng XPath tương đối (.//) thay vì tuyệt đối (//) để tránh lấy nhầm phần tử từ toàn trang
            # -> nếu không có dữ liệu, .get() sẽ trả về 'None' nên không cần dùng try-except để tránh lỗi missing value

            item['quote'] = quote.xpath('.//span[@class="text"]/text()').get()
            item['author'] = quote.xpath('.//span/small[@class="author"]/text()').get()
            tags = quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').getall()
            item['tags'] = ', '.join(tags)  # Gộp tag thành 1 string phân tách bằng dấu phẩy

            yield item # Trả về danh sách item mà không làm ngưng vòng lặp

        # Sau khi scraping date trên page xong thì follow nút next để qua trang tiếp theo -> chạy lại class parse từ đầu để tiếp tục scrap!
        next_page = response.xpath('//ul[@class="pager"]/li[@class="next"]/a/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

# NEXT STEP: chạy Terminal để scraping data và lưu kết quả vào file JSON - CSV - EXCEL:
    # scrapy crawl quotespider -o quotes.json
    # scrapy crawl quotespider -o quotes.csv
    # Scrapy không hỗ trợ .xlsx trực tiếp
        # -> cần code một Pipeline xuất Excel trong 'pipelines.py'
        # -> sau đó kích hoạt Pipeline xuất Excel mới tạo này ở trong 'settings.py'
        # -> scrapy crawl quotespider