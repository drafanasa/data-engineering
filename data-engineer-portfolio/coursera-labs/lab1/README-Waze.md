
# Waze Lab - Dự đoán Churn Người Dùng

# Giới thiệu
Lab thuộc khóa "Google Advanced Data Analytics Professional Certificate" trên Coursera. 
Mục tiêu là phân tích dữ liệu và phát triển mô hình machine learning dự đoán churn người dùng trên ứng dụng Waze.

# Mục tiêu Dự án
- Phân tích dữ liệu để xác định yếu tố liên quan đến churn.
- Xây dựng mô hình machine learning dự đoán churn.
- Đề xuất chiến lược giảm churn và tăng trưởng người dùng.

# Công nghệ Sử dụng
- Python (Pandas, NumPy, Matplotlib, Scikit-learn)
- Jupyter Notebook
- PACE Workflow (Plan, Analyze, Construct, Execute)

# Dataset
**Lưu ý:** Dataset dùng cho mục đích học tập, bảo mật bởi Coursera và không chia sẻ ra bên ngoài.
- 14,999 dòng, 13 biến.
- Một số cột chính:
  - `ID`: Định danh người dùng.
  - `label`: Mục tiêu ("retained" hoặc "churned").
  - `sessions`: Số lần mở app trong tháng.
  - `drives`: Số lần lái xe trên 1km trong tháng.
  - `device`: Loại thiết bị.
  - `driven_km_drives`: Tổng km đã lái trong tháng.
  - `duration_minutes_drives`: Tổng thời gian lái trong tháng.


# Quy trình Thực hiện
1. **Plan:** Xây dựng proposal, xác định milestones và stakeholders.
2. **Analyze:** Thực hiện EDA, thống kê mô tả, trực quan hóa dữ liệu, kiểm tra giả thuyết.
3. **Construct:** Xây dựng và tối ưu mô hình machine learning.
4. **Execute:** Đánh giá mô hình, báo cáo kết quả và đề xuất chiến lược.

# Cách Chạy Lab
```bash
# Clone repository
git clone https://github.com/drafanasa/data-engineer-portfolio.git

# Cài đặt thư viện
pip install pandas numpy matplotlib scikit-learn

# Mở Jupyter Notebook
jupyter notebook Waze.ipynb
```

# Ghi chú
- Dataset đã chỉnh sửa cho mục đích học tập.
- Dự án mang tính giả định, không đại diện cho tổ chức hoặc cá nhân nào.

# Liên hệ
- Mọi góp ý vui lòng tạo Issues hoặc Pull Request.
