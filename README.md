# Population ETL Pipeline

Dự án thực hành **Data Engineering** bằng Python: thu thập dữ liệu dân số từ [API Ninjas – Population API](https://api-ninjas.com/api/population), xử lý dữ liệu theo nhiều tầng và nạp kết quả vào **Google BigQuery** để truy vấn bằng SQL.

> **Phạm vi:** Mini project phục vụ học tập và xây dựng portfolio. Đây chưa phải hệ thống production. Các tính năng như kiểm thử tự động, kiểm soát schema chặt chẽ và cơ chế cập nhật bằng `MERGE` là hướng nâng cấp.

## 1. Mục tiêu

- Thực hành quy trình **Extract – Transform – Load (ETL)** từ REST API đến data warehouse.
- Tách biệt trách nhiệm giữa các module Python để dễ bảo trì và mở rộng.
- Tổ chức dữ liệu theo các tầng `raw`, `staging`, `final`.
- Bổ sung thông tin quốc gia (`country`) để xác định nguồn gốc của từng bản ghi.
- Tích hợp Google BigQuery và bước đầu tự động hóa bằng `cron` trên Ubuntu.
- Làm quen với logging, xử lý ngoại lệ, quản lý biến môi trường và Git.

## 2. Kiến trúc dữ liệu

```text
API Ninjas – Population API
            |
            v
       Python Extract
            |
            v
    data/raw/ (JSON)
            |
            v
   Parse / Transform
            |
            v
  data/staging/ (CSV)
            |
            v
   Thêm cột country
            |
            v
   data/final/ (CSV)
            |
            v
  BigQuery Load Job
            |
            v
  Google BigQuery (SQL)
```

**Vai trò các tầng:**

| Tầng | Mục đích |
| --- | --- |
| `raw` | Lưu phản hồi JSON từ API để có thể kiểm tra hoặc xử lý lại. |
| `staging` | Lưu dữ liệu đã chuyển từ JSON sang dạng bảng CSV. |
| `final` | Lưu CSV đã bổ sung `country`, chuẩn bị cho bước nạp vào BigQuery. |
| BigQuery | Lưu trữ và truy vấn dữ liệu bằng SQL. |

## 3. Công nghệ sử dụng

| Công nghệ | Vai trò |
| --- | --- |
| Python | Ngôn ngữ triển khai pipeline |
| Requests | Gửi HTTP request tới API (nếu được sử dụng trong `api_client.py`) |
| Pandas | Đọc, biến đổi và ghi CSV |
| Google Cloud BigQuery | Data warehouse và truy vấn SQL |
| Google Cloud CLI / ADC | Cấu hình project và xác thực ứng dụng cục bộ |
| Ubuntu / cron | Môi trường chạy và lập lịch |
| Git / GitHub | Quản lý mã nguồn |

Phiên bản thư viện được ghi trong `requirements.txt`.

## 4. Cấu trúc thư mục

Cấu trúc dưới đây được đối chiếu với ảnh VS Code của dự án:

```text
population/
├── .venv/                 # Virtual environment (không đưa lên Git)
├── data/
│   ├── raw/               # JSON từ API
│   ├── staging/           # CSV sau bước parse
│   └── final/             # CSV đã thêm country
├── log/
│   └── pipeline.log       # Log chạy pipeline
├── src/
│   ├── __init__.py
│   ├── api_client.py       # Gọi API
│   ├── arg_parser.py       # Xử lý tham số dòng lệnh
│   ├── bq_loader.py        # Nạp CSV vào BigQuery
│   ├── config.py           # Cấu hình chung
│   ├── logging_setup.py    # Thiết lập logging
│   ├── parse_data.py       # Parse/chuẩn hóa dữ liệu
│   └── storage.py          # Đọc/ghi dữ liệu cục bộ
├── .env                   # Biến môi trường, không commit
├── .gitignore
├── main.py                # Điểm khởi chạy pipeline
├── requirements.txt
└── README.md
```

## 5. Cài đặt

### 5.1. Clone repository

```bash
git clone <URL_REPOSITORY_CUA_BAN>
cd population
```

### 5.2. Tạo môi trường Python

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 5.3. Cấu hình API key

Tạo file `.env` tại thư mục gốc và đặt API key theo tên biến được sử dụng trong `src/config.py`:

```dotenv
API_NINJAS_KEY=your_api_key_here
```

**Không commit `.env` hoặc API key lên GitHub.** Nếu code sử dụng tên biến khác, hãy sửa ví dụ cho đúng trước khi chạy.

### 5.4. Thiết lập BigQuery (khi dùng bước Load)

1. Tạo hoặc chọn một Google Cloud Project và bật BigQuery API.
2. Tạo dataset `population_lab` (hoặc cập nhật tên dataset trong `src/bq_loader.py`).
3. Đăng nhập Google Cloud CLI và thiết lập Application Default Credentials:

```bash
gcloud auth application-default login
```

4. Đảm bảo tài khoản có quyền tạo BigQuery Load Job và ghi vào dataset.
5. **Location của Load Job phải khớp với location của dataset.** Dataset được dùng trong quá trình thực hành hiện đặt tại `US`.

> Lưu ý: Không đưa token hoặc file khóa service account vào repository.

## 6. Cách chạy pipeline

Tại thư mục gốc dự án, kích hoạt `.venv` rồi chạy:

```bash
python main.py vietnam
```

Có thể thay quốc gia tùy theo dữ liệu API hỗ trợ và cách `arg_parser.py` xử lý tên quốc gia:

```bash
python main.py italia
```

**Kết quả mong đợi:** Pipeline lấy dữ liệu, tạo các file trung gian, bổ sung cột `country` ở tầng final và nạp lên BigQuery nếu bước Load đã được bật trong `main.py`.

Kiểm tra đầu ra cục bộ:

```bash
ls data/raw/ data/staging/ data/final/
head -n 5 data/final/vietnam.csv
```

Kiểm tra log:

```bash
tail -n 50 log/pipeline.log
```

## 7. Mô hình dữ liệu

Một số trường trong dữ liệu Population API:

| Cột | Ý nghĩa |
| --- | --- |
| `country` | Quốc gia, được bổ sung ở tầng final |
| `year` | Năm thống kê |
| `population` | Quy mô dân số |
| `yearly_change_percentage` | Tỷ lệ thay đổi dân số theo năm |
| `yearly_change` | Mức thay đổi dân số theo năm |
| `migrants` | Giá trị liên quan đến di cư |
| `median_age` | Tuổi trung vị |
| `fertility_rate` | Tỷ suất sinh |
| `density` | Mật độ dân số |
| `urban_population_pct` | Tỷ lệ dân số đô thị |
| `urban_population` | Dân số đô thị |
| `percentage` | Tỷ trọng dân số theo nguồn API |
| `rank` | Thứ hạng theo nguồn API |

**Grain dự kiến:** một bản ghi cho mỗi cặp `(country, year)`. Cần kiểm tra tính duy nhất trước khi dùng cặp này làm khóa logic.

## 8. BigQuery và ví dụ SQL

Trong giai đoạn thực hành, mỗi quốc gia có thể được nạp vào một bảng riêng như `population_lab.vietnam`. Thay `PROJECT_ID` bằng ID project của bạn.

```sql
SELECT country, year, population
FROM `PROJECT_ID.population_lab.vietnam`
ORDER BY year DESC
LIMIT 10;
```

Kiểm tra số bản ghi trùng theo năm:

```sql
SELECT country, year, COUNT(*) AS total_rows
FROM `PROJECT_ID.population_lab.vietnam`
GROUP BY country, year
HAVING COUNT(*) > 1;
```

Kiểm tra giá trị thiếu:

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNTIF(country IS NULL) AS missing_country,
  COUNTIF(year IS NULL) AS missing_year,
  COUNTIF(population IS NULL) AS missing_population
FROM `PROJECT_ID.population_lab.vietnam`;
```

## 9. Chiến lược nạp dữ liệu và chạy lại

Trong quá trình phát triển đã thử nghiệm các chế độ ghi:

- `WRITE_APPEND`: thêm bản ghi vào bảng; chạy lại có thể tạo dữ liệu trùng.
- `WRITE_TRUNCATE`: thay thế dữ liệu bảng đích khi Load Job thành công; thích hợp với cách nạp lại **toàn bộ dữ liệu của từng quốc gia vào bảng riêng**, nhưng sẽ thay thế dữ liệu cũ trong bảng đó.

**Trạng thái cần kiểm tra trong mã nguồn:** chế độ ghi thực tế nằm ở `src/bq_loader.py`. Không mặc định rằng pipeline đã có cơ chế `MERGE` hoặc lưu lịch sử thay đổi.

Hướng nâng cấp: nạp vào bảng staging trên BigQuery, kiểm tra khóa `(country, year)`, sau đó dùng `MERGE` để cập nhật bảng chung mà không tạo duplicate.

## 10. Logging và xử lý lỗi

Pipeline có module `src/logging_setup.py` và file `log/pipeline.log` để theo dõi các bước xử lý.

Các lỗi cần quan sát khi vận hành:

- API trả về dữ liệu rỗng hoặc HTTP error.
- JSON thiếu trường hoặc dữ liệu không hợp lệ.
- File đầu vào không tồn tại.
- Xác thực hoặc quyền truy cập BigQuery không hợp lệ.
- Schema CSV khác với schema bảng BigQuery.
- Location của BigQuery Load Job không khớp dataset.

Nên dùng `logging.exception(...)` khi bắt lỗi để lưu đầy đủ traceback và trả mã thoát khác `0` khi pipeline thất bại.

## 11. Tự động hóa bằng cron (Ubuntu)

Ví dụ chạy hằng ngày lúc **08:00 theo múi giờ của máy Ubuntu**:

```cron
0 8 * * * cd /home/waytodata/projects/population && /home/waytodata/projects/population/.venv/bin/python main.py vietnam >> /home/waytodata/projects/population/cron.log 2>&1
```

Xem lịch:

```bash
crontab -l
```

**Điều kiện vận hành:** Ubuntu và dịch vụ cron phải đang chạy; Python phải có thể đọc `.env` và thông tin xác thực Google Cloud trong ngữ cảnh cron. Nếu dùng WSL/máy cá nhân, tắt máy có thể khiến job không chạy.

> Chỉ bật lịch tự động sau khi xác nhận pipeline chạy lại an toàn, không làm trùng hoặc mất dữ liệu ngoài ý muốn.

## 12. Bảo mật repository

Khuyến nghị `.gitignore`:

```gitignore
.venv/
__pycache__/
*.py[cod]
.env
.env.*
!.env.example
*.log
log/
cron.log
```

Nếu dữ liệu thu thập lớn hoặc không muốn công khai file dữ liệu, có thể bỏ qua thêm `data/raw/`, `data/staging/`, `data/final/`. Nếu cần giữ thư mục trống trên GitHub, sử dụng `.gitkeep`.

## 13. Hướng phát triển

- [ ] Viết data contracts và kiểm tra chất lượng dữ liệu tự động.
- [ ] Xây dựng bảng BigQuery chung cho nhiều quốc gia.
- [ ] Dùng staging table + `MERGE` để cập nhật idempotent.
- [ ] Viết unit tests bằng `pytest`.
- [ ] Bổ sung kiểm tra schema drift và dữ liệu đến muộn.
- [ ] Tạo dashboard hoặc analytics mart để so sánh dân số giữa các quốc gia.
- [ ] Tích hợp CI/CD và lịch chạy trên Cloud khi phù hợp.

## 14. Ghi chú

Dự án được xây dựng nhằm rèn luyện tư duy thiết kế ETL, phân chia module, làm việc với dữ liệu thực tế và sử dụng BigQuery. Các thông số triển khai như tên bảng, cách parse dữ liệu, xử lý lỗi và chế độ ghi cần được đối chiếu với mã nguồn mới nhất trước khi sử dụng trong môi trường khác.
