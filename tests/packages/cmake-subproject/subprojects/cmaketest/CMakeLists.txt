# SPDX-FileCopyrightText: 2024 The meson-python developers
#
# SPDX-License-Identifier: MIT

cmake_minimum_required(VERSION 3.5)

project(cmaketest)
set(CMAKE_CXX_STANDARD 14)

include_directories(${CMAKE_CURRENT_BINARY_DIR})

add_library(cmaketest SHARED cmaketest.cpp)

include(GenerateExportHeader)
generate_export_header(cmaketest)

install(TARGETS cmaketest)
