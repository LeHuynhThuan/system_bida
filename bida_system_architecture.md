# Kiến trúc và Hoạt động của Hệ thống Bida AI

## 1. Các Model và Thư viện (Libraries & Models)
- **OpenCV (`opencv-python`)**: Xử lý luồng stream từ Camera (RTSP/Webcam), đọc từng frame (khung hình), ghi video lưu trữ và cắt clip highlight.
- **MediaPipe**: Thư viện AI của Google (được liệt kê trong `requirements.txt`), thường dùng để nhận diện cử chỉ tay hoặc bộ phận cơ thể (như vẫy tay gọi nhân viên). Trong một số trường hợp có thể thay thế bằng QR code để tăng tính chính xác.
- **Redis (`redis`)**: Đóng vai trò làm Message Broker (giao tiếp giữa các tiến trình) và In-memory Cache. Dùng để truyền các khung hình live (live frames) từ Camera Worker lên Web tốc độ cao, cũng như gửi các sự kiện (event) như yêu cầu cắt clip.
- **SQLAlchemy & PyMySQL**: Thư viện ORM dùng để tương tác với cơ sở dữ liệu (SQLite/MySQL), giúp quản lý thông tin bàn bida, phiên chơi, hóa đơn và đơn hàng món ăn/nước uống.
- **Pydantic**: Ràng buộc và xác thực dữ liệu đầu vào/đầu ra cho các API.
- **Numpy**: Xử lý các ma trận điểm ảnh (frames) từ OpenCV.

## 2. Framework (Nền tảng)
- **Backend Framework**: **FastAPI** – Framework cực kỳ nhanh của Python, hỗ trợ tốt xử lý bất đồng bộ (async), WebSockets, và tạo API RESTful một cách tự động. Phục vụ giao diện web dashboard và các API.
- **Máy chủ Web (Server)**: **Uvicorn** – ASGI server dùng để chạy ứng dụng FastAPI.
- **Frontend**: HTML5, CSS3, và JavaScript thuần (Vanilla JS) tích hợp thẳng trong file. Giao diện được thiết kế hiện đại, tĩnh nhưng tương tác thời gian thực với backend.

## 3. Cách Sử Dụng (How to Use)
1. **Cài đặt thư viện**: Chạy lệnh `pip install -r requirements.txt`.
2. **Khởi động Redis**: Yêu cầu phải có Redis Server đang chạy ở cổng 6379 (`localhost:6379`).
3. **Khởi động AI Workers (Camera)**: Chạy lệnh `python run_workers.py`. Các worker sẽ bật camera, bắt đầu ghi hình 24/7 vào thư mục `archive/` và đẩy hình ảnh live lên Redis.
4. **Khởi động Web Server**: Chạy lệnh `uvicorn main:app --host 0.0.0.0 --port 8000` (hoặc click vào `start_bida.bat`).
5. **Truy cập Giao diện**: Mở trình duyệt và truy cập `http://localhost:8000`. Dashboard sẽ tự động kết nối WebSocket để nhận dữ liệu thời gian thực.

## 4. Mô tả cách Hoạt động của Web (System Workflow)
Hệ thống được thiết kế theo kiến trúc Micro-services thu nhỏ, chia làm hai tiến trình chính chạy song song: **AI Workers** và **Web Server (FastAPI)**.

- **Thu thập hình ảnh**: File `run_workers.py` tạo ra các tiến trình (multiprocessing) độc lập cho mỗi bàn bida. OpenCV trong mỗi worker liên tục đọc hình ảnh từ Camera RTSP hoặc Webcam.
- **Xử lý luồng (Stream Processor)**:
  - **Ghi hình liên tục (24/7 Archive)**: Cứ mỗi phút, luồng video được chẻ ra và ghi vào một file `.mp4` trong thư mục `archive/`. Các file cũ (mặc định > 30 phút) sẽ tự động bị xóa để tiết kiệm ổ cứng.
  - **Live Stream View**: Cứ mỗi 3 frames, hình ảnh được nén thành chuẩn JPEG và đưa thẳng vào Redis (Key: `live_frame_{table_id}`). Web client sẽ lấy ảnh từ đây để hiện thị stream trực tiếp mà không bị độ trễ cao.
  - **Cắt Highlight**: Mỗi worker giữ một "bộ đệm" (buffer) chứa 30 giây video gần nhất trên RAM. Khi quản lý nhấn nút "Cắt Highlight" trên Web, một tín hiệu được đẩy xuống Redis (`clip_request_X`). Worker nhận được sẽ ngay lập tức dump (lưu) bộ đệm này thành 1 file MP4 vào thư mục `clips/` và báo cáo lại trạng thái.
- **Tương tác Thời gian thực (Real-time Web)**: 
  - Giao diện Web kết nối qua giao thức **WebSocket** hai chiều với FastAPI.
  - Ở phía backend, có một luồng nền liên tục lắng nghe từ Redis Pub/Sub.
  - Khi Worker hoàn thành cắt clip (hoặc AI phát hiện có khách vẫy tay/cuốn menu), thông tin sự kiện được đẩy qua Redis -> FastAPI nhận được -> Lập tức bắn tin nhắn qua WebSocket lên Web Client -> Giao diện của quản lý hiện thông báo/cập nhật ngay lập tức mà không cần tải lại trang (reload).
- **Quản lý dữ liệu (Database)**: Mở bàn, đóng bàn, gọi món ăn, tính tiền... đều được thao tác qua API của FastAPI, gọi trực tiếp các phương thức CRUD của SQLAlchemy để lưu vào cơ sở dữ liệu `bida_ai.db`.

## 5. Quy trình Đặt món và Giao diện Khách hàng (Customer Interface)
Phía khách hàng có một giao diện quét mã QR riêng biệt tại bàn (hiển thị qua trình duyệt điện thoại), cung cấp các trải nghiệm:
- **Xem thông tin giờ chơi**: Khách hàng có thể theo dõi thời gian bắt đầu và số phút/giờ đã chơi theo thời gian thực (được đếm tự động).
- **Xem thông tin dịch vụ (Banners)**: Các tiện ích miễn phí (trà đá, mượn cơ), bảng giá giờ chơi, các quy định phụ thu (như mang đồ ăn ngoài) được hiển thị trực quan.
- **Menu Gọi món (Order)**:
  - Hiển thị danh sách thức uống, đồ ăn, thuốc lá được phân loại theo từng Tab, đi kèm hình ảnh và giá tiền.
  - **Quản lý Tồn kho (Stock)**: Nút `+` và `-` sẽ bị vô hiệu hóa nếu số lượng món trong kho đã hết, giúp khách không gọi nhầm món không còn phục vụ. Tổng tiền tự động được tính toán ở thanh dưới cùng.
- **Yêu cầu Nghiệp vụ (Dịch vụ)**: Thay vì gọi to, khách chỉ cần 1 chạm để báo nhân viên thực hiện: `Lấy lơ`, `Xếp bi`, `Quét bàn`, `Đổi bàn`, hoặc nhập `Yêu cầu khác` tùy ý.
- **Gửi Yêu cầu Order**: Khách nhập Tên, Số điện thoại và Ghi chú thêm. Ngay khi nhấn nút "Gửi", ứng dụng gọi API (`POST /api/customer-order/...`) lên FastAPI. Backend ghi nhận và lập tức đẩy thông báo (Notification) kèm âm thanh ra Dashboard của Quầy thu ngân thông qua WebSocket.
- **Lịch sử Đặt món**: Lưu lại các món mà khách đã gọi (và đã được xác nhận) ngay trên màn hình để khách tự kiểm tra chi phí tạm tính một cách minh bạch.

## 6. Luồng Nghiệp vụ Quản trị viên (Admin & Checkout Workflow)
Tại Quầy thu ngân, hệ thống cung cấp các nghiệp vụ khép kín cho nhân viên quản lý:
- **Tiếp nhận Yêu cầu (Real-time Alert)**: Khi khách hàng quét QR gọi món hoặc yêu cầu đổi bàn, thẻ thông báo sự kiện sẽ tự động nổi lên ở thanh thông báo bên phải (kèm âm thanh cảnh báo).
- **Duyệt Đơn hàng (Approve Order)**: 
  - Khi thu ngân ấn **Duyệt món**, API sẽ tự động trừ số lượng hàng trong kho (Inventory) theo thời gian thực và cộng trực tiếp số tiền dịch vụ đó vào Bill nháp của bàn tương ứng.
  - Trạng thái bàn (playing, empty) cũng được đồng bộ màu sắc lập tức (Xanh/Đỏ/Vàng).
- **Quy trình Thanh toán (Checkout) & Tự động In Bill**:
  - Khi khách báo tính tiền, thu ngân nhấn nút **Thanh toán**. Hệ thống gọi API chốt giờ hiện tại (tính ra số phút thực tế đã chơi) và nhân với Đơn giá giờ (tùy thuộc vào Bàn Thường hay Bàn VIP).
  - Tự động cộng dồn với tổng tiền dịch vụ ăn uống.
  - Khi hoàn tất, một Popup Bill được vẽ lên màn hình, chứa chi tiết mọi khoản phí và mã QR thanh toán (VietQR) tự động gán đúng số tiền.
  - Ngay sau đó, trình duyệt được kích hoạt lệnh in (`window.print()`) ở một luồng ẩn để đẩy thẳng bản in xuống máy in hóa đơn nhiệt (thermal printer) 80mm của quán, sau đó tự động dọn dẹp (đóng cửa sổ in).
- **Quản lý Kho & Bàn chơi (Inventory & Table Management)**: 
  - Giao diện cung cấp cửa sổ chia Tabs: Tab **Thực đơn** (CRUD sản phẩm, tự động gợi ý danh mục) và Tab **Bàn Bida** (CRUD số lượng bàn, gắn định danh Camera, thiết lập giá tiền giờ từng bàn theo chuẩn VIP/Thường). Tồn kho và giá cả thay đổi sẽ lập tức áp dụng cho các phiên chơi mới.
