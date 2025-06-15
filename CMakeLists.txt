cmake_minimum_required(VERSION 3.16)
project(CatTrackerApp)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Use vcpkg toolchain (set in settings.json or command line)
# No need to specify here if VSCode already passes it

# Find OpenCV (vcpkg handles the path)
find_package(OpenCV REQUIRED)

# Source files
add_executable(cat_tracker_app
    src/main.cpp
    src/tracker.cpp
)

# Include headers
target_include_directories(cat_tracker_app PRIVATE ${OpenCV_INCLUDE_DIRS} src/)

# Link OpenCV libs
target_link_libraries(cat_tracker_app PRIVATE ${OpenCV_LIBS})
