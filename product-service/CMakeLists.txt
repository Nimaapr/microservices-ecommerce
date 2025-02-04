# product-service/CMakeLists.txt
cmake_minimum_required(VERSION 3.5)
project(product_service)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Include Crow headers from the cloned repository.
if(DEFINED CROW_INCLUDE_DIR)
    include_directories(${CROW_INCLUDE_DIR})
else()
    message(FATAL_ERROR "CROW_INCLUDE_DIR not set!")
endif()

# Create the executable using main.cpp.
add_executable(product_service main.cpp)

# Link against the PostgreSQL C++ library.
find_package(PkgConfig REQUIRED)
pkg_check_modules(PQXX REQUIRED libpqxx)
include_directories(${PQXX_INCLUDE_DIRS})
target_link_libraries(product_service ${PQXX_LIBRARIES})

# Find threads
find_package(Threads REQUIRED)

# Link with stdc++fs (for filesystem support) and threads.
target_link_libraries(product_service ${PQXX_LIBRARIES} stdc++fs Threads::Threads)