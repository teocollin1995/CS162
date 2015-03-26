(define length
        (lambda (list)
        (cond ((null? list) 0)
                 (else (+ 1 (length (cdr list)))))))

;;Maps length
 (define mapL
        (lambda (list) (map length list)))
;;What it says on the tin
 (define test1? (lambda (list)
        (fold-right (lambda (x y) (and x y)) #t (map (lambda (x) (eq? x (length list))) (mapL list)))))

;;if all elements in a list are 0 or 1.
 (define zone? (lambda (list)
        (cond ((null? list) #t)
        ((not (or (eq? (car list) 0) (eq? (car list) 1))) #f)
                (else (zone? (cdr list))))))

 (define test2? (lambda (list)
        (cond ((null? list) #t)
        ((not (zone? (car list))) #f)
                (else (test2? (cdr list))))))

 (define test3? (lambda (list)
        (cond ((null? list) #t)
        ((not (zero? (car (car list)))) #f)
                (else (test3? (map cdr (cdr list)))))))

(define (transpose m) (apply map list m))
;;I knew there was an easy one for mit scheme so I just googled it… http://rosettacode.org/wiki/Matrix_transposition#Scheme

 (define test4? (lambda (list) (equal? (transpose  list) list)))

 (define amatrix? (lambda (list)
        (and (and (test1? list) (test2? list)) (and (test3? list) (test4? list)))))
