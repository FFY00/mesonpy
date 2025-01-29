// SPDX-FileCopyrightText: 2024 The meson-python developers
//
// SPDX-License-Identifier: MIT

#include "cmaketest.hpp"

Test::Test(int x) {
  this->x = x;
}

int Test::add(int y) const {
  return x + y;
}
