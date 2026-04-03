# Test Files - Debug & Development

Thư mục này chứa các script test dùng để debug, development và hiểu cách hệ thống hoạt động.

## Danh sách các test files

### 🔍 Test AI Services
| File | Mục đích |
|------|---------|
| **test_ai_services.py** | Kiểm tra AI Services (ThinkingService, SuggestionsService) - test các API gọi từ OpenRouter |

### 🌐 Test API Flow
| File | Mục đích |
|------|---------|
| **test_api_flow.py** | Kiểm tra toàn bộ flow API suggestions (tạo entry, lấy gợi ý) |
| **test_api_cache.py** | Kiểm tra API endpoints đọc từ suggestions cache (phiên bản phức tạp) |
| **test_api_cache_simple.py** | Phiên bản đơn giản hơn của test API cache |

### 📋 Test Complete Scenarios
| File | Mục đích |
|------|---------|
| **test_complete_flow.py** | Kiểm tra toàn bộ quy trình: setup DB → tạo user/form → test lần 1, 2, 3+ |
| **test_fresh_field.py** | Test gợi ý với field mới (chưa có entry nào) |
| **test_new_suggestions.py** | Test logic gợi ý mới - so sánh entries đầu vs các entries sau |

### 🐛 Debug & Development
| File | Mục đích |
|------|---------|
| **test_suggestions_flow.py** | Test simulation suggestions flow (không cần upload file) |
| **test_suggestions_debug.py** | Script debug chi tiết flow suggestions với output rõ ràng |
| **simple_test.py** | Test cơ bản đơn giản |

---

## Cách sử dụng

### Chạy test từ project root:
```bash
cd backend/tests_debug
python test_complete_flow.py
```

### Hoặc từ backend folder:
```bash
python tests_debug/test_api_flow.py
```

---

## Ghi chú

- ✅ **Để chạy các test này**, server backend phải đang chạy: `python run.py`
- 📊 **Database** phải được setup và có dữ liệu test
- 🔑 **Credentials**: Các file này hardcode credentials (dev environment)
- 🧹 **Cleanup**: Một số test sẽ xóa/reset dữ liệu database - dùng sau khi test xong

---

## Khi nào cần dùng?

✅ **Nên dùng khi:**
- Debug issues trong hệ thống
- Muốn hiểu cách API hoạt động
- Kiểm tra regression sau khi update code
- Onboard thành viên mới

❌ **Không cần dùng để:**
- Chạy hệ thống hàng ngày (chỉ dùng `run.py`)
- Kiểm tra production (cần unit tests/integration tests chính thức)

---

**Last updated:** February 2026
