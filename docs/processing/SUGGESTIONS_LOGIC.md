# Logic Gợi Ý Mới - First Entry vs Later Entries

## Mô tả
Hệ thống gợi ý được cập nhật để phân biệt giữa:
- **Lần nhập đầu tiên (< 2 entries)**: Không có gợi ý, chỉ lưu dữ liệu
- **Từ lần nhập thứ 2 trở đi (>= 2 entries)**: Gợi ý từ lịch sử database

## Flow

### Lần Nhập Thứ 1
```
User nhập dữ liệu → API GET /api/suggestions → entry_count = 0
  ↓
is_first_entry = true, suggestions = []
  ↓
Không hiển thị gợi ý
  ↓
API POST /api/suggestions/save → Lưu vào database
```

### Lần Nhập Thứ 2 Trở Đi
```
User nhập dữ liệu → API GET /api/suggestions → entry_count >= 2
  ↓
is_first_entry = false, suggestions = [list từ database]
  ↓
Hiển thị gợi ý dựa trên tần suất
  ↓
API POST /api/suggestions/save → Lưu vào database
```

## API Endpoints

### 1. GET /api/suggestions
Lấy gợi ý cho một field

**Parameters:**
- `user_id` (int): ID người dùng
- `field_id` (int): ID trường form
- `top_k` (int, optional): Số lượng gợi ý top (mặc định 5, max 5)

**Response:**
```json
{
  "user_id": 1,
  "field_id": 1,
  "suggestions": [
    {
      "value": "Hà Nội",
      "frequency": 3,
      "ranking": 3
    },
    {
      "value": "TP Hồ Chí Minh",
      "frequency": 1,
      "ranking": 1
    }
  ],
  "total_count": 2,
  "entry_count": 4,
  "is_first_entry": false,
  "message": "Suggestions retrieved from history"
}
```

**Logic:**
- Nếu `entry_count < 2`: `is_first_entry = true`, `suggestions = []`
- Nếu `entry_count >= 2`: `is_first_entry = false`, `suggestions = [từ database]`

### 2. GET /api/suggestions/by-name
Lấy gợi ý theo tên field (thay vì field_id)

**Parameters:**
- `user_id` (int): ID người dùng
- `field_name` (str): Tên field (e.g., "họ_và_tên", "địa_chỉ")
- `form_id` (int, optional): ID form (mặc định 1)
- `top_k` (int, optional): Số lượng gợi ý top

**Response:** Tương tự GET /api/suggestions

**Ưu điểm:** Không cần biết field_id, tự động tìm từ field_name

### 3. POST /api/suggestions/save
Lưu dữ liệu nhập vào database

**Parameters:**
- `user_id` (int): ID người dùng
- `field_id` (int): ID trường form
- `form_id` (int): ID form
- `value` (str): Giá trị được nhập

**Response:**
```json
{
  "status": "success",
  "entry_id": 42,
  "message": "Entry saved successfully"
}
```

## Quy Trình Hoàn Chỉnh

### Client Flow:
```
1. User bắt đầu điền form
2. Client gọi GET /api/suggestions (lần 1)
   → entry_count = 0, is_first_entry = true, suggestions = []
   → Plugin không hiển thị gợi ý
3. User nhập giá trị vào field
4. Client gọi POST /api/suggestions/save
   → Lưu vào database
5. User tiếp tục sang field khác (hoặc quay lại field này)
6. Client gọi GET /api/suggestions (lần 2)
   → entry_count = 1, is_first_entry = true, suggestions = []
   → Vẫn không hiển thị gợi ý (chưa đủ 2 entries)
7. User nhập giá trị khác
8. Client gọi POST /api/suggestions/save
   → Lưu vào database
9. Client gọi GET /api/suggestions (lần 3+)
   → entry_count >= 2, is_first_entry = false, suggestions = [...]
   → Plugin hiển thị gợi ý
```

## Response Fields Mới

### `entry_count`
- Số lượng entries đã lưu cho field này của user
- Dùng để client biết khi nào bật gợi ý (>= 2)
- Giúp UI hiển thị "Nhập X lần nữa để bật gợi ý"

### `is_first_entry`
- `true`: Chưa đủ dữ liệu (< 2 entries)
- `false`: Đã đủ dữ liệu (>= 2 entries), có thể gợi ý

### `message`
- Mô tả chi tiết tình trạng hiện tại
- Giúp UI hiển thị thông báo cho user

## Ví Dụ Thực Tế

**Lần 1:** User nhập "Hà Nội"
```
GET /api/suggestions?user_id=1&field_id=1
→ entry_count=0, is_first_entry=true, suggestions=[]
   "message": "Chưa đủ dữ liệu (nhập 2 lần nữa để bật gợi ý)"

POST /api/suggestions/save?user_id=1&field_id=1&form_id=1&value=Hà Nội
→ entry_id=1, status=success
```

**Lần 2:** User nhập "Hà Nội"
```
GET /api/suggestions?user_id=1&field_id=1
→ entry_count=1, is_first_entry=true, suggestions=[]
   "message": "Chưa đủ dữ liệu (nhập 1 lần nữa để bật gợi ý)"

POST /api/suggestions/save?user_id=1&field_id=1&form_id=1&value=Hà Nội
→ entry_id=2, status=success
```

**Lần 3:** User bắt đầu nhập
```
GET /api/suggestions?user_id=1&field_id=1
→ entry_count=2, is_first_entry=false, suggestions=[
    {"value": "Hà Nội", "frequency": 2, "ranking": 2}
  ]
   "message": "Suggestions retrieved from history"

POST /api/suggestions/save?user_id=1&field_id=1&form_id=1&value=TP Hồ Chí Minh
→ entry_id=3, status=success
```

## Implementation Notes

### Backend Changes:
1. **routes/suggestions.py**
   - GET / endpoint: Thêm logic kiểm tra `entry_count < 2`
   - GET /by-name endpoint: Thêm logic kiểm tra `entry_count < 2`
   - Response schema mở rộng: `entry_count`, `is_first_entry`

2. **schemas/suggestion.py**
   - SuggestionsListResponse: Thêm fields `entry_count`, `is_first_entry`

### Frontend Changes (khi sử dụng):
1. Kiểm tra `is_first_entry` trước khi hiển thị gợi ý
2. Hiển thị message từ `message` field
3. Tùy chọn: Hiển thị "Nhập X lần nữa" dựa trên `entry_count`

## Testing

Chạy script test:
```bash
python test_new_suggestions.py
```

Script sẽ:
1. Nhập 3 lần giá trị khác nhau
2. Kiểm tra response sau mỗi lần
3. Verify logic:
   - Lần 1: is_first_entry=true, suggestions=[]
   - Lần 2: is_first_entry=true, suggestions=[]
   - Lần 3: is_first_entry=false, suggestions=[...]
