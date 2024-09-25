(bắt-đầu
    (gán (giai-thừa x)
        (nếu (so-sánh-bằng  x  1)
            1
            (* x (giai-thừa (- x 1)))
        )
    )

    (gán (giai-thừa-danh-sách danh_sách_nhập_)
        (xử-lý-danh-sách giai-thừa danh_sách_nhập_)
    )

    (gán (lọc-số-dương  danh_sách_nhập_) 
        (bắt-đầu
            (gán (lớn-hơn-0  x)
                (nếu (so-sánh-lớn  x  0)
                    #đúng
                    #sai
                )
            )
            (lọc-danh-sách  lớn-hơn-0  danh_sách_nhập_)
        )
    )
    #trống
)