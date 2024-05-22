# CMakeLists.txt
cmake_minimum_required(VERSION 3.12)
project(cmake_example)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(POLICY CMP0148)
    cmake_policy(SET CMP0148 NEW)
endif()

add_subdirectory(pybind11)

# Add include directories
include_directories(${CMAKE_SOURCE_DIR}/src/AIWine/src)

# Add source files
set(SOURCE_FILES
    src/main.cpp
    src/AIWine/src/AIWine.cpp
    src/AIWine/src/Chess.cpp
    src/AIWine/src/Board.cpp
    src/AIWine/src/ChessShape.cpp
)

pybind11_add_module(cmake_example ${SOURCE_FILES})
