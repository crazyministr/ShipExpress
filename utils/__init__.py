# -*- coding: utf-8 -*-
def matrix(n, m, default=0):
    a = [default] * n
    for i in range(n):
        a[i] = [default] * m

    return a
