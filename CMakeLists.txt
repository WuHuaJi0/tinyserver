cmake_minimum_required(VERSION 3.5)
project(tinyserver C)

set(CMAKE_C_STANDARD 90)

add_executable(tinyserver
        tinyserver.c src/c/tcp.c src/c/http.c)


add_executable(t test.c)