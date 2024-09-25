; sudoku solver implemented in Scheme :)

; build up a board as a list of lists, and call
;   (solve-sudoku board)
; to see a result.  it will return the solved board if the board can be solved,
; or -1 otherwise

; multiple boards are already defined for you below (see board1, board2,
; board3 containing the same example boards from lecture 6, and board4
; containing an insoluble puzzle)


(bắt-đầu
    (gán chiều_cao lấy-độ-dài)
    (gán (chiều_rộng bàn) (lấy-độ-dài (lấy-vị-trí bàn 0)))

    (gán (có_chứa? danh_sách_nhập cần_tìm)
        (nếu (so-sánh-bằng (danh-sách) danh_sách_nhập)
            #sai
            (nếu (so-sánh-bằng (lấy-giá-trị danh_sách_nhập) cần_tìm)
                #đúng
                (có_chứa? (lấy-con-trỏ danh_sách_nhập) cần_tìm)
            )
        )
    )

    (gán (cắt_danh_sách danh_sách_nhập đầu cuối)
        (xử-lý-danh-sách
            (hàm (i) (lấy-vị-trí danh_sách_nhập i))
            (trong_khoảng đầu cuối 1)
        )
    )

    (gán (thay_trong_danh_sách danh_sách_nhập vị_trí_thay giá_trị_thay)
        (xử-lý-danh-sách
            (hàm (i) (nếu (so-sánh-bằng i vị_trí_thay) giá_trị_thay (lấy-vị-trí danh_sách_nhập i)))
            (trong_khoảng 0 (lấy-độ-dài danh_sách_nhập) 1)
        )
    )

    (gán (danh_sách_trống? danh_sách_nhập) (so-sánh-bằng danh_sách_nhập ()))

    (gán (bó l1 l2)
        (nếu (danh_sách_trống? l1)
            (danh-sách)
            (nối
                (danh-sách (tạo-cặp (lấy-giá-trị l1) (lấy-giá-trị l2)))
                (bó (lấy-con-trỏ l1) (lấy-con-trỏ l2))
            )
        )
    )

    (gán (vị_trí_ô_nhỏ x)
        ; dễ hơn nếu dùng floor()
        (nếu (có_chứa? (danh-sách 0 1 2) x)
            0
            (nếu (có_chứa? (danh-sách 3 4 5) x)
                1
                (nếu (có_chứa? (danh-sách 6 7 8) x)
                    2
                    -1
                )
            )
        )
    )


    (gán (tìm_khác l1 l2)
        (lọc-danh-sách (hàm (x) (không (có_chứa? l2 x))) l1)
    )

    (gán (trong_khoảng đầu cuối bước)
        (nếu (so-sánh-lớn-bằng đầu cuối)
            (danh-sách)
            (nối (danh-sách đầu) (trong_khoảng (+ đầu bước) cuối bước))
        )
    )
    (gán mọi_bước (trong_khoảng 1 10 1))
    (gán (bước_hợp_lệ bàn r c)
        (tìm_khác
            mọi_bước
            (nối
                (giá_trị_trong_hàng bàn r)
                (giá_trị_trong_cột bàn c)
                (giá_trị_trong_ô_nhỏ bàn (vị_trí_ô_nhỏ r) (vị_trí_ô_nhỏ c))
            )
        )
    )

    (gán (lấy_giá_trị_ô bàn r c) (lấy-vị-trí (lấy-vị-trí bàn r) c))

    (gán (!= x y) (không (so-sánh-bằng x y)))
    (gán (khác_0? x) (!= x 0))
    (gán (giá_trị_khác_0 danh_sách_nhập) (lọc-danh-sách khác_0? danh_sách_nhập))

    (gán (giá_trị_trong_hàng bàn r)
        (giá_trị_khác_0 (lấy-vị-trí bàn r))
    )
    (gán (giá_trị_trong_cột bàn c)
        (giá_trị_khác_0 (xử-lý-danh-sách (hàm (hàng) (lấy-vị-trí hàng c)) bàn))
    )

    (gán (giá_trị_trong_ô_nhỏ bàn sr sc)
        (gán-cục-bộ ((start-r (* sr 3)) (start-c (* sc 3)))
            (giá_trị_khác_0
                (nối
                    (cắt_danh_sách (lấy-vị-trí bàn start-r) start-c (+ start-c 3))
                    (cắt_danh_sách (lấy-vị-trí bàn (+ start-r 1)) start-c (+ start-c 3))
                    (cắt_danh_sách (lấy-vị-trí bàn (+ start-r 2)) start-c (+ start-c 3))
                )
            )
        )
    )

    (gán (thay_trong_bàn bàn r c giá_trị_thay)
        (xử-lý-danh-sách
            (hàm (r-ix)
                (gán-cục-bộ ((hàng_thử (lấy-vị-trí bàn r-ix)))
                    (nếu (so-sánh-bằng r-ix r)
                        (thay_trong_danh_sách hàng_thử c giá_trị_thay)
                        hàng_thử
                    )
                )
            )
            (trong_khoảng 0 (chiều_cao bàn) 1)
        )
    )

    (gán (mọi_cặp l1 l2)
        (gán-cục-bộ ((single-term (hàm (e1) (xử-lý-danh-sách (hàm (e2) (tạo-cặp e1 e2)) l2))))
            (gấp-danh-sách nối (xử-lý-danh-sách single-term l1) (danh-sách))
        )
    )

    (gán (lấy_giá_trị_từ_cặp bàn c) (lấy_giá_trị_ô bàn (lấy-giá-trị c) (lấy-con-trỏ c)))

    (gán (tìm_0_đầu bàn)
        (bắt-đầu
            (gán (hàm_phụ giá_trị_thử)
                (nếu (danh_sách_trống? giá_trị_thử)
                    (tạo-cặp -1 -1)
                    (nếu (so-sánh-bằng 0 (lấy_giá_trị_từ_cặp bàn (lấy-giá-trị giá_trị_thử)))
                        (lấy-giá-trị giá_trị_thử)
                        (hàm_phụ (lấy-con-trỏ giá_trị_thử))
                    )
                )
            )
            (hàm_phụ (mọi_cặp (trong_khoảng 0 9 1) (trong_khoảng 0 9 1)))
        )
    )

    (gán (hàm_phụ_giải bàn r c các_bước_thử)
        (nếu (danh_sách_trống? các_bước_thử)
            -1 ; thử thất bại, trả -1
            (gán-cục-bộ ((kết_quả_thử (giải-sudoku (thay_trong_bàn bàn r c (lấy-giá-trị các_bước_thử)))))
                (nếu (so-sánh-bằng kết_quả_thử -1) ; thử thất bại
                    (hàm_phụ_giải bàn r c (lấy-con-trỏ các_bước_thử)) ; thử bước tiếp theo
                    kết_quả_thử
                )
            )
        )
    )

    (gán (giải-sudoku bàn)
        (gán-cục-bộ ((vị_trí_0 (tìm_0_đầu bàn)))
            (nếu (so-sánh-bằng (lấy-giá-trị vị_trí_0) -1)
                bàn ; nếu không còn số 0, đã giải thành công
                (hàm_phụ_giải bàn (lấy-giá-trị vị_trí_0) (lấy-con-trỏ vị_trí_0) (bước_hợp_lệ bàn (lấy-giá-trị vị_trí_0) (lấy-con-trỏ vị_trí_0)))
            )
        )
    )

    (gán bàn1
         (danh-sách
            (danh-sách 5 1 7 6 0 0 0 3 4)
            (danh-sách 2 8 9 0 0 4 0 0 0)
            (danh-sách 3 4 6 2 0 5 0 9 0)
            (danh-sách 6 0 2 0 0 0 0 1 0)
            (danh-sách 0 3 8 0 0 6 0 4 7)
            (danh-sách 0 0 0 0 0 0 0 0 0)
            (danh-sách 0 9 0 0 0 0 0 7 8)
            (danh-sách 7 0 3 4 0 0 5 6 0)
            (danh-sách 0 0 0 0 0 0 0 0 0)
        )
    )

    (gán bàn2
         (danh-sách
            (danh-sách 5 1 7 6 0 0 0 3 4)
            (danh-sách 0 8 9 0 0 4 0 0 0)
            (danh-sách 3 0 6 2 0 5 0 9 0)
            (danh-sách 6 0 0 0 0 0 0 1 0)
            (danh-sách 0 3 0 0 0 6 0 4 7)
            (danh-sách 0 0 0 0 0 0 0 0 0)
            (danh-sách 0 9 0 0 0 0 0 7 8)
            (danh-sách 7 0 3 4 0 0 5 6 0)
            (danh-sách 0 0 0 0 0 0 0 0 0)
         )
    )

    (gán bàn3
        (danh-sách
            (danh-sách 0 0 1 0 0 9 0 0 3)
            (danh-sách 0 8 0 0 2 0 0 9 0)
            (danh-sách 9 0 0 1 0 0 8 0 0)
            (danh-sách 1 0 0 5 0 0 4 0 0)
            (danh-sách 0 7 0 0 3 0 0 5 0)
            (danh-sách 0 0 6 0 0 4 0 0 7)
            (danh-sách 0 0 8 0 0 5 0 0 6)
            (danh-sách 0 3 0 0 7 0 0 4 0)
            (danh-sách 2 0 0 3 0 0 9 0 0)
        )
    )

    (gán bàn4
         (danh-sách
            (danh-sách 5 1 7 6 8 0 0 3 4)
            (danh-sách 2 8 9 0 0 4 0 0 0)
            (danh-sách 3 4 6 2 0 5 0 9 0)
            (danh-sách 6 0 2 0 0 0 0 1 0)
            (danh-sách 0 3 8 0 0 6 0 4 7)
            (danh-sách 0 0 0 0 0 0 0 0 0)
            (danh-sách 0 9 0 0 0 0 0 7 8)
            (danh-sách 7 0 3 4 0 0 5 6 0)
            (danh-sách 0 0 0 0 0 0 0 0 0)
        )
    )
)
