(gán  biến_x  5)
(gán  giai_thừa_x (giai-thừa  biến_x))
giai_thừa_x     ; in ra màn hình giá trị của giai_thừa_x
(gán  danh_sách_này_ (danh-sách -5 0 -1 6 4 -3 biến_x 2)) ;tạo danh sách và gán biến
(lấy-vị-trí  danh_sách_này_  0) ;lấy giá trị của danh sách ở vị trí số 0
(lấy-vị-trí  danh_sách_này_  2) ;lấy giá trị của danh sách ở vị trí số 2
(lấy-độ-dài  danh_sách_này_)    ;lấy độ dài danh sách
(gán  các_số_dương (lọc-số-dương  danh_sách_này_)) ;lọc ra những số dương
(gán  giai_thừa_ (giai-thừa-danh-sách  các_số_dương)) ;lấy giai thừa của các số dương
(nếu  (là-danh-sách  giai_thừa_) #đúng  #sai) ;giai_thừa_ là danh sách
(nếu  (là-danh-sách  biến_x) #đúng  #sai)  ;biến_x ko phải danh sách
(gán  danh_sách_nối (nối  giai_thừa_  (danh-sách biến_x)  (danh-sách 1 -2 3 -4 5)))  ;  nối nhiều danh sách với nhau
(gán  hàm-cộng-10  (hàm (x) (+ x 10)))  ;tạo hàm kiểu lambda
(xử-lý-danh-sách  hàm-cộng-10  danh_sách_nối)   ;áp dụng hàm-cộng-10 lên cả danh sách
thoát