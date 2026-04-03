
# Sơ đồ cây chức năng

```
- Hệ thống tự động điền thông minh
  - Quản lý xác thực người dùng (Authentication)
    - Đăng nhập (`/api/auth/login`)
      - Xác thực tên người dùng và mật khẩu.
      - Tạo phiên (session) và trả về session ID.
    - Đăng ký (`/api/auth/signup`)
      - Đăng ký người dùng mới với tên, email và mật khẩu.
  - Dịch vụ gợi ý (Suggestion Service)
    - Lấy gợi ý cho trường dữ liệu (`/api/suggestions`)
      - Dựa trên lịch sử nhập liệu của người dùng cho một trường cụ thể.
      - Trả về danh sách các giá trị đã nhập trước đó, sắp xếp theo tần suất và thời gian.
  - Xử lý tài liệu (Word/Document Processing)
    - Tải lên và phân tích tài liệu (`/api/word/upload`)
      - Hỗ trợ các định dạng: .docx, .pdf, .xlsx, .xls, .csv, .txt.
      - Phân tích tài liệu để trích xuất các trường (fields).
      - Lưu mẫu tài liệu (template) vào cơ sở dữ liệu.
  - Dịch vụ thay thế biểu mẫu (Form Replacement Service)
    - Tải lên và phát hiện cấu trúc biểu mẫu thông minh (`/api/form-replacement/upload-with-intelligent-detection`)
      - Chỉ hỗ trợ file .docx.
      - Tự động phát hiện tiêu đề, nhãn và các trường có thể điền.
      - Giữ nguyên cấu trúc và bố cục của tài liệu gốc.
      - Tạo ra một biểu mẫu HTML có thể điền được.
  - Xử lý file Excel (Excel Processing)
    - Tải lên và phân tích file Excel (`/api/excel/upload`)
      - Đọc dữ liệu từ các file .xlsx hoặc .xls.
      - Tự động phát hiện các hàng tiêu đề và kiểu dữ liệu của cột.
      - Chuẩn hóa tên trường và xử lý các định dạng dữ liệu khác nhau.
      - Lưu trữ dữ liệu đã phân tích để sử dụng trong các biểu mẫu.
  - Soạn thảo tài liệu với AI (AI Composer)
    - Quản lý tài liệu
      - Tạo tài liệu mới (`/api/composer/documents`).
      - Cập nhật tài liệu hiện có (`/api/composer/documents/{doc_id}`).
      - Lấy danh sách tài liệu (`/api/composer/documents`).
    - Gợi ý nội dung AI
      - Yêu cầu gợi ý dựa trên ngữ cảnh (`/api/composer/suggestions`).
    - Theo dõi lịch sử soạn thảo
      - Ghi lại các hành động của người dùng (chỉnh sửa, chấp nhận gợi ý) (`/api/composer/actions`).
```

# Mô tả chi tiết các chức năng

## 1. Quản lý xác thực người dùng (Authentication)

- **Mục đích**: Cung cấp cơ chế đăng nhập và đăng ký an toàn cho người dùng.
- **Chi tiết**:
  - **Đăng nhập (`/api/auth/login`)**:
    - **Đầu vào**: Tên người dùng (username) và mật khẩu (password).
    - **Xử lý**:
      - Kiểm tra thông tin đăng nhập so với cơ sở dữ liệu người dùng (hiện tại là một đối tượng trong bộ nhớ).
      - Nếu hợp lệ, một `session_id` duy nhất được tạo và lưu trữ.
      - `session_id` được gửi lại cho người dùng thông qua cookie, duy trì trạng thái đăng nhập.
    - **Đầu ra**: Thông báo thành công cùng với thông tin người dùng và cookie chứa `session_id`.
  - **Đăng ký (`/api/auth/signup`)**:
    - **Đầu vào**: Tên người dùng, email, và mật khẩu.
    - **Xử lý**:
      - Xác thực đầu vào để đảm bảo tất cả các trường đều được điền.
      - Kiểm tra xem tên người dùng đã tồn tại hay chưa.
      - Nếu hợp lệ, người dùng mới sẽ được thêm vào cơ sở dữ liệu.
    - **Đầu ra**: Thông báo đăng ký thành công.

## 2. Dịch vụ gợi ý (Suggestion Service)

- **Mục đích**: Cung cấp các gợi ý thông minh cho các trường trong biểu mẫu, dựa trên lịch sử nhập liệu của người dùng.
- **Chi tiết**:
  - **Lấy gợi ý (`/api/suggestions`)**:
    - **Đầu vào**: `user_id`, `field_id`, và `top_k` (số lượng gợi ý mong muốn).
    - **Xử lý**:
      - Truy vấn cơ sở dữ liệu để lấy tất cả các `entries` (dữ liệu đã nhập) trước đó cho `user_id` và `field_id` cụ thể.
      - Nếu có đủ dữ liệu (ít nhất 1 entry), hệ thống sẽ phân tích tần suất xuất hiện và thời gian nhập gần nhất của mỗi giá trị.
      - Các gợi ý được xếp hạng dựa trên một thuật toán kết hợp tần suất và sự gần đây.
    - **Đầu ra**: Một danh sách các gợi ý được xếp hạng, cùng với số lượng entry đã có.

## 3. Xử lý tài liệu (Word/Document Processing)

- **Mục đích**: Cho phép người dùng tải lên các loại tài liệu khác nhau và tự động trích xuất cấu trúc biểu mẫu từ chúng.
- **Chi tiết**:
  - **Tải lên và phân tích (`/api/word/upload`)**:
    - **Đầu vào**: File tài liệu (hỗ trợ .docx, .pdf, .xlsx, .xls, .csv, .txt) và `user_id`.
    - **Xử lý**:
      - Hệ thống sử dụng một `FileParserFactory` để chọn trình phân tích (parser) phù hợp dựa trên phần mở rộng của file.
      - Trình phân tích sẽ đọc nội dung file và cố gắng xác định các trường có thể điền được (ví dụ: các dòng có dấu chấm "...", gạch dưới "___").
      - Nếu không tìm thấy trường nào, một trường mặc định sẽ được tạo dựa trên tên file.
      - Cấu trúc được trích xuất (dưới dạng JSON) và siêu dữ liệu của file được lưu vào cơ sở dữ liệu dưới dạng một `WordTemplate`.
    - **Đầu ra**: Thông tin về mẫu đã tạo, bao gồm ID, tên và danh sách các trường.

## 4. Dịch vụ thay thế biểu mẫu (Form Replacement Service)

- **Mục đích**: Cung cấp khả năng phát hiện biểu mẫu thông minh hơn cho các file `.docx`, giữ lại cấu trúc và bố cục phức tạp.
- **Chi tiết**:
  - **Phát hiện thông minh (`/api/form-replacement/upload-with-intelligent-detection`)**:
    - **Đầu vào**: File `.docx` và `user_id`.
    - **Xử lý**:
      - Sử dụng `IntelligentDetector`, hệ thống phân tích sâu hơn vào cấu trúc tài liệu Word.
      - Nó có thể xác định các tiêu đề, các phần (sections), và các nhãn (labels) liên quan đến các trường có thể điền.
      - Cấu trúc này được bảo toàn, cho phép tạo ra một biểu mẫu HTML phản ánh chính xác bố cục của tài liệu gốc.
      - Kết quả phân tích được lưu dưới dạng một mẫu (template) trong cơ sở dữ liệu.
    - **Đầu ra**: Một biểu mẫu HTML được tạo ra, sẵn sàng để người dùng điền thông tin, cùng với siêu dữ liệu về cấu trúc đã phát hiện.

## 5. Xử lý file Excel (Excel Processing)

- **Mục đích**: Cho phép người dùng tải lên các file Excel và trích xuất dữ liệu có cấu trúc từ chúng.
- **Chi tiết**:
  - **Tải lên và phân tích (`/api/excel/upload`)**:
    - **Đầu vào**: File Excel (.xlsx hoặc .xls).
    - **Xử lý**:
      - Đọc file Excel bằng các thư viện như `openpyxl` hoặc `xlrd`.
      - Tự động phát hiện hàng tiêu đề (header row) bằng cách tìm kiếm các từ khóa phổ biến (ví dụ: "STT", "Mã", "Tên").
      - Cố gắng xác định kiểu dữ liệu cho mỗi cột (ví dụ: 'date', 'number', 'text') dựa trên tên tiêu đề.
      - Chuẩn hóa tên cột để loại bỏ khoảng trắng thừa và các ký tự không cần thiết.
      - Dữ liệu được trích xuất và lưu trữ tạm thời trong bộ nhớ (`excel_data_store`) để có thể được sử dụng để điền vào các biểu mẫu khác.
    - **Đầu ra**: Một cấu trúc JSON chứa các trường đã phát hiện và dữ liệu của chúng.

## 6. Soạn thảo tài liệu với AI (AI Composer)

- **Mục đích**: Hỗ trợ người dùng soạn thảo tài liệu bằng cách cung cấp các gợi ý do AI tạo ra.
- **Chi tiết**:
  - **Quản lý tài liệu**:
    - Cung cấp các điểm cuối (endpoints) RESTful tiêu chuẩn để tạo (`POST /documents`), cập nhật (`PUT /documents/{id}`), và lấy (`GET /documents`) tài liệu.
    - Mỗi tài liệu được liên kết với một người dùng và có tiêu đề, nội dung và mô tả.
  - **Gợi ý nội dung AI (`/api/composer/suggestions`)**:
    - **Đầu vào**: Một đoạn ngữ cảnh (văn bản hiện tại) mà người dùng đang viết.
    - **Xử lý**:
      - Gửi ngữ cảnh đến một dịch vụ AI (được mô phỏng trong `AIComposerService`).
      - Dịch vụ AI tạo ra một số gợi ý để hoàn thành hoặc mở rộng văn bản.
    - **Đầu ra**: Một danh sách các chuỗi gợi ý.
  - **Theo dõi lịch sử soạn thảo (`/api/composer/actions`)**:
    - **Đầu vào**: Thông tin về hành động của người dùng, chẳng hạn như `document_id`, loại hành động ('edit', 'suggestion'), văn bản gốc, văn bản đã sửa đổi, và liệu gợi ý có được chấp nhận hay không.
    - **Xử lý**:
      - Ghi lại hành động này vào cơ sở dữ liệu. Dữ liệu này có thể được sử dụng trong tương lai để cải thiện các gợi ý của AI.
    - **Đầu ra**: Xác nhận rằng hành động đã được ghi lại.
