# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request

class TigerImagePipeline(ImagesPipeline):

    # Function xử lý ảnh: Gửi request đến từng image_url đã scrap
    def get_media_requests(self, item, info):
        for image_url in item.get('image_url', []):  # Duyệt qua từng link ảnh
            yield Request(image_url)  # Gửi request đến image_url -> Scrapy tự biết làm phần còn lại (download it!)

    # Function đặt tên file ảnh sau khi tải về
    def file_path(self, request, response=None, info=None, *, item=None):
        # Đổi tên ảnh = tên sản phẩm, thay khoảng trắng bằng '_' và loại bỏ ký tự '/' để tránh lỗi khi lưu file
        name = item['name'].replace(' ', '_').replace('/', '_')
        return f'{name}.jpg'  # Trả về tên file ảnh sẽ được lưu (ví dụ: My_Product.jpg)

