# SPDX-FileCopyrightText: 2024 The meson-python developers
#
# SPDX-License-Identifier: MIT

cdef extern from "cmaketest.hpp":
    cdef cppclass Test:
        Test(int) except +
        int add(int)


def sum(int a, int b):
    t = new Test(a)
    return t.add(b)
