(bắt-đầu
    (gán (xử-lý-danh-sách hàm_biến_đổi danh_sách_gốc)
        (nếu (so-sánh-bằng (lấy-độ-dài danh_sách_gốc) 1) 
            (danh-sách (hàm_biến_đổi (lấy-vị-trí danh_sách_gốc 0)))
            (nếu (so-sánh-bằng (lấy-độ-dài danh_sách_gốc) 0)
                #trống
                (nối 
                    (danh-sách (hàm_biến_đổi (lấy-vị-trí danh_sách_gốc 0)))
                    (xử-lý-danh-sách hàm_biến_đổi (lấy-con-trỏ danh_sách_gốc))
                )
            )
        )
    )
    

    (gán (lọc-danh-sách hàm_điều_kiện danh_sách_gốc)
        (nếu (so-sánh-bằng (lấy-độ-dài danh_sách_gốc) 1) 
            (nếu (hàm_điều_kiện (lấy-vị-trí danh_sách_gốc 0))
                danh_sách_gốc
                #trống
            )
            (nếu (so-sánh-bằng (lấy-độ-dài danh_sách_gốc) 0)
                #trống
                (nối 
                    (lọc-danh-sách hàm_điều_kiện (danh-sách (lấy-vị-trí danh_sách_gốc 0)))
                    (lọc-danh-sách hàm_điều_kiện (lấy-con-trỏ danh_sách_gốc))
                )
            )
        )
    )

    (gán (gấp-danh-sách hàm_biến_đổi danh_sách_gốc giá_trị_đầu)
        (nếu (so-sánh-bằng (lấy-độ-dài danh_sách_gốc) 0)
            giá_trị_đầu
            (gấp-danh-sách hàm_biến_đổi (lấy-con-trỏ danh_sách_gốc) (hàm_biến_đổi giá_trị_đầu (lấy-giá-trị danh_sách_gốc)))
        )
    )

    #trống
)
