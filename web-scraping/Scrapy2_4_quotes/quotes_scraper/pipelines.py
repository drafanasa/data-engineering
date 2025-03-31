# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import openpyxl
# Tại sao không cần from quotespider import item?
# Vì Spider là nơi tạo ra item (kiểu QuoteItem)
# Còn Pipeline chỉ nhận item như input và xử lý nó
# Do không tạo mới item nào trong pipeline, nên không cần import


class ExcelPipeline:

    # Dùng thư viện openpyxl để tạo ra một file Excel trắng với các sheet và header name tùy chỉnh
    def open_spider(self, spider):
        self.workbook = openpyxl.Workbook()
        self.sheet = self.workbook.active
        self.sheet.title = 'Quotes'
        self.sheet.append(["quote", "author", "tags"]) # Khai báo header trong bảng Excel

    # Lấy data đang được lưu trong danh sách item (sau khi đã scrap thành công) để append vào file Excel vừa tạo)
    def process_item(self, item, spider):
        self.sheet.append([
            item.get('quote'),
            item.get('author'),
            item.get('tags')
        ])
        return item # Dùng return item để gửi item qua pipeline tiếp theo (nếu có nhiều pipeline).

    # Xuất data ra file Excel và đặt tên là 'quotes.xlsx'
    def close_spider(self, spider):
        self.workbook.save('quotes.xlsx')

# NEXT STEP:
    # sau khi code xong Pipeline -> tiến hành kích hoạt pipeline trong settings.py
    # thêm vào cuối file: ITEM_PIPELINES = {'<tên project>.pipelines.ExcelPipeline': 300,}