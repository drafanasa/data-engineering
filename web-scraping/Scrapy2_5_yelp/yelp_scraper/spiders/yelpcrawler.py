from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import YelpItem

class YelpcrawlerSpider(CrawlSpider):
    name = "yelpcrawler"
    allowed_domains = ["yelp.com"]
    start_urls = ["https://www.yelp.com/search?find_desc=Gyms&find_loc=Berlin%2C+Germany"] # Lọc các phòng Gym ở Berlin - Đức

    rules = (
        # Rule 1: Cho phép duyệt phân trang (chỉ follow, không gọi function nào hết)
        Rule(LinkExtractor(allow=r"desc=Gyms.*start="), follow=True), # allow=r"desc=Gyms.*start=" là regex dùng để lọc các URL có chứa chuỗi desc=Gyms và start= - Ví dụ Page 5 là: https://www.yelp.com/search?find_desc=Gyms&find_loc=Berlin%2C+Gyms&start=50

        # Rule 2: Cho phép truy cập từng trang cụ thể của mỗi phòng gym (vừa follow vùa gọi function parse_item để cào dữ liệu)
        Rule(
            LinkExtractor(allow=r"biz/.*osq=Gyms", deny='hrid'), # allow=r"biz/.*osq=Gyms" cũng là regex để lọc URL có chứa chuỗi biz/ và osq=Gyms - - Ví dụ: https://www.yelp.com/biz/ride-bln-berlin-6?osq=Gyms
            callback="parse_item",
            follow=True
        ),
    )

    def parse_item(self, response):
        item = YelpItem()

        item['name'] = response.xpath('//h1[@class="y-css-olzveb"]/text()').get() or 'No info'
        item['url'] = response.url

        # Website
        item['website_link'] = response.xpath(
            '//p[text()="Business website"]/following-sibling::p[1]/a/@href'
        ).get() or 'No info'

        # Số điện thoại
        item['phone'] = response.xpath(
            '//p[text()="Phone number"]/following-sibling::p[1]/text()'
        ).get() or 'No info'

        # Địa chỉ
        item['address'] = response.xpath(
            '//a[text()="Get Directions"]/../following-sibling::p[1]/text()'
        ).get() or 'No info'

        # Rating (sao đánh giá)
        # contains giúp lọc những <div> có thuộc tính aria-label chứa cụm "star rating"
        # -> Ví dụ: HTML <div class="y-css-f0t6x4" role="img" aria-label="3 star rating"> -> Output: "3 star rating"
        rating = response.xpath(
            '//div[contains(@aria-label, "star rating")]/@aria-label'
        ).get()

        rating_no = rating.split(' ')[0] if rating else 'No info'
        item['rating'] = rating_no

        # Số lượng đánh giá
        review_count = response.xpath(
            '//span[contains(text(), "review")]/text()'
        ).get() # Output ví dụ: "24 reviews"

        review_count_no = review_count.split(' ')[0] if review_count else 'No info'
        item['review_count'] = review_count_no

        yield item
