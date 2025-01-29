// SPDX-FileCopyrightText: 2024 The meson-python developers
//
// SPDX-License-Identifier: MIT

#pragma once
#include "cmaketest_export.h"

class CMAKETEST_EXPORT Test {
private:
  int x;
public:
  Test(int x);
  int add(int y) const;
};
