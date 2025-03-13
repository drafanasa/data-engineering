# Milestone 2 - Compile Summary Information 
- Data team của Waze đang phát triển dự án phân tích dữ liệu nhằm giảm monthly churned để thúc đẩy tăng trưởng.
- Report này tóm tắt dữ liệu sơ bộ, trạng thái dự án và các insight từ Milestone 2, ảnh hưởng đến định hướng phát triển trong tương lai.

## Mục tiêu: 
- Phân tích dữ liệu người dùng để xác định mối quan hệ quan trọng giữa các biến.

## Phương pháp:
- Xây dựng dataframe dựa trên .csv dataset.
- Thu thập thống kê sơ bộ.
- Phân tích hành vi người dùng.

## Tác động:
- Xác định các mối quan hệ quan trọng giữa các biến, làm cơ sở cho phân tích dữ liệu sâu hơn.
- Khuyến khích thu thập thêm dữ liệu về super-drivers, vì nhu cầu của họ có thể khác với người dùng thông thường và Waze chưa đáp ứng được.
- Next steps là là thực hiện EDA chi tiết và phát triển visualizations để làm rõ câu chuyện dữ liệu và hỗ trợ quyết định cho dự án.

## Insight:
- Dataset có 82% retained users và 18% churned users, 12 variables gồm các data types như object, float và integer. 
- Cột ‘label’ có 700 giá trị null.
- Nhóm churned users trung bình thực hiện nhiều hơn ~3 chuyến đi trong tháng cuối so với nhóm retained.
- Số ngày nhóm retained user dùng app nhiều gấp 2 so với nhóm churned (thường xuyên hơn).
- Churned users lái xe trung bình nhiều hơn ~200 km và 2.5 giờ so với retained users.
- Churned users có nhiều chuyến đi hơn trong ít ngày hơn, với quãng đường và thời gian dài hơn. 
- Trung bình, mỗi ngày lái xe, nhóm churned user di chuyển 698 km, gấp 240% so với nhóm retained.

## Kết luận: 
-> Manh mối về một tệp user có nhu cầu đặc biệt, cần tiếp tục khám phá. 
-> Data cho thấy tệp user này có xu hướng lái xe đường dài, và có thể họ không đại diện cho nhóm tài xế phổ thông.