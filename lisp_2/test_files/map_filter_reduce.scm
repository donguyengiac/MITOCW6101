(begin
    (define (map function oldlist)
        (if (equal? (length oldlist) 1) 
            (list (function (list-ref oldlist 0)))
            (if (equal? (length oldlist) 0)
                #none
                (append 
                    (list (function (list-ref oldlist 0)))
                    (map function (cdr oldlist))
                )
            )
        )
    )
    

    (define (filter function oldlist) ;passing in function and list, return list
        (if (equal? (length oldlist) 1) 
            (if (function (list-ref oldlist 0))
                oldlist
                #none
            )
            (if (equal? (length oldlist) 0)
                #none
                (append 
                    (filter function (list (list-ref oldlist 0)))
                    (filter function (cdr oldlist))
                )
            )
        )
    )

    (define (reduce function oldlist initval) ;passing in function, list & value, return value
        (if (equal? (length oldlist) 0)
            initval
            (reduce function (cdr oldlist) (function initval (car oldlist)))
        )
    )

    #none
)
