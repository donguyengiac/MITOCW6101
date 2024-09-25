(bắt-đầu
    (gán (fibonacci n) (fib-bước n 0 1))

    (gán (fib-bước n a b)
      (nếu (so-sánh-bằng n 1)
        b 
        (nếu (so-sánh-bằng n 0)
          a
          (fib-bước (- n 1) b (+ a b))
        )
      )
    )

    (gán (bình_phương x) (* x x))
)
