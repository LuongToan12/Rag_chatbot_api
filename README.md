# TÀI LIỆU HƯỚNG DẪN TRIỂN KHAI & VẬN HÀNH DOCKER
## DỰ ÁN: RAG CHATBOT BACKEND API

---

## 1. TỔNG QUAN DỰ ÁN
Tài liệu này hướng dẫn cách build, chia sẻ và khởi chạy ứng dụng **RAG Chatbot API** sử dụng Docker. 

Hệ thống sử dụng:
* **Framework:** FastAPI (Python 3.12)
* **Vector Database:** ChromaDB (lưu trữ vector embedding cục bộ)
* **Embedding Model:** Hugging Face (`sentence-transformers/all-MiniLM-L6-v2`)
* **LLM Engine:** Google Gemini API (`gemma-4-31b-it`)
* **Docker Package Manager:** Sử dụng `uv` để tối ưu hóa hiệu suất tải thư viện và cache build.

---

## 2. YÊU CẦU TRƯỚC KHI CÀI ĐẶT (PREREQUISITES)
Trước khi chạy ứng dụng, môi trường của bạn cần đảm bảo các điều kiện sau:
* **Docker Desktop:** Đã cài đặt và đang chạy (Windows/macOS/Linux).
* **Git:** Để nhân bản mã nguồn (nếu cần build từ source).
* **API Key:** Khóa kết nối Google Gemini API (`GOOGLE_API_KEY`).
* **Database Folder:** Thư mục `chroma_db` chứa dữ liệu tri thức đã được thiết lập sẵn trên máy local.

---

## 3. CÁC PHƯƠNG THỨC TRIỂN KHAI

### PHƯƠNG ÁN A: Sử dụng git

Nếu cần tham gia chỉnh sửa mã nguồn hoặc test tính năng mới:

1. **Clone repository của dự án:**
   ```bash
   git clone <URL_REPOSITORY>
   cd Rag_chatbot
   ```

2. **Build Docker Image (Sử dụng cấu hình tối ưu):**
   ```bash
   docker build -t rag-chatbot-api .
   ```
   * *Lưu ý:* Quá trình build sử dụng cache mount của `uv`. Lần build đầu tiên sẽ mất khoảng vài phút để tải các thư viện máy học (PyTorch, Transformers). Các lần build sau chỉ mất **dưới 1 giây**.

3. **Chạy ứng dụng:** Xem hướng dẫn cấu hình chi tiết tại **Mục 4**.

---

### PHƯƠNG ÁN B: Sử dụng Docker Registry

Nếu bạn chỉ cần chạy ứng dụng để sử dụng hoặc tích hợp hệ thống mà không muốn quản lý mã nguồn:

Chạy trực tiếp câu lệnh bên dưới để tự động tải image (không cần tải mã nguồn):

```bash
docker run -d `
  --name rag-chatbot-api `
  -p 8000:8000 `
  -e GOOGLE_API_KEY="ĐIỀN_API_KEY_CỦA_BẠN" `
  -v "ĐƯỜNG_DẪN_THƯ_MỤC_CHROMA_DB_LOCAL:/app/chroma_db" `
  company-registry/rag-chatbot-api:latest
```

## 4. CHI TIẾT CẤU HÌNH THAM SỐ KHỞI CHẠY (CONTAINER RUN SETTINGS)

Khi khởi chạy Container, người vận hành bắt buộc phải cấu hình đúng 3 thông số sau:

### 1. Cổng kết nối (Ports)
* **Host Port:** `8000`
* **Container Port:** `8000`

### 2. Thư mục dữ liệu (Volumes)
* Phải ánh xạ (mount) thư mục `chroma_db` ở local vào container để ứng dụng có thể đọc dữ liệu vector:
  * **Local Path (Host):** Đường dẫn tuyệt đối tới thư mục `chroma_db` trên máy bạn. (Ví dụ: `D:\Code\Rag_chatbot\chroma_db`).
  * **Container Path:** `/app/chroma_db`

### 3. Biến môi trường (Environment Variables)
* **Variable:** `GOOGLE_API_KEY`
* **Value:** Giá trị chuỗi API Key của bạn (Ví dụ: `AQ.Ab...`)

---

### Hướng dẫn chạy qua giao diện đồ họa Docker Desktop

1. Tìm image `rag-chatbot-api` trong mục **Images** và nhấn nút **Run**.
2. Mở rộng phần **Optional settings** và điền:
   * **Container name:** `rag-chatbot-api`
   * **Host port:** `8000`
   * **Volumes:** Chọn thư mục `chroma_db` ở máy của bạn tại **Host path** và điền `/app/chroma_db` vào **Container path**.
   * **Environment variables:** Điền `GOOGLE_API_KEY` tại **Variable** và dán mã key vào **Value**.
3. Bấm **Run**.

---

5. HƯỚNG DẪN KIỂM TRA & SỬ DỤNG API (API TESTING GUIDE)
Sau khi khởi chạy thành công, ứng dụng sẽ cần khoảng 15-30 giây đầu tiên để tải các mô hình học máy vào bộ nhớ.

5.1. Thử nghiệm trực quan qua giao diện Swagger UI 
FastAPI cung cấp sẵn một trang tài liệu tương tác giúp bạn dễ dàng gọi thử API mà không cần cài đặt phần mềm nào khác:

Mở trình duyệt Web và truy cập thẳng đường dẫn gốc: http://localhost:8000/ (hệ thống sẽ tự động chuyển hướng bạn đến trang tài liệu tương tác /docs).
Tại đây, bạn sẽ thấy danh sách các API của hệ thống.
Bấm chọn API POST /chat (màu xanh lá).
Nhấn nút Try it out ở góc phải.
Nhập câu hỏi kiểm tra tại phần request body, ví dụ:
json

{
  "question": "Dự án này là gì?"
}
Nhấn nút Execute (màu xanh dương) để gửi câu hỏi và nhận câu trả lời trực tiếp bên dưới.
IMPORTANT

Lưu ý về lỗi 405 Method Not Allowed:
Không truy cập trực tiếp đường dẫn http://localhost:8000/chat bằng trình duyệt Web. Trình duyệt sẽ gửi yêu cầu dạng GET, trong khi API chỉ chấp nhận dạng POST (gửi kèm câu hỏi). Truy cập trực tiếp sẽ dẫn đến lỗi 405. Hãy sử dụng trang /docs để test thử.

---



