cmake_minimum_required(VERSION 3.15)
project(LeafVision CXX)

set(CMAKE_CXX_STANDARD 17)

# Yerel pybind11 kullanımı (Offline derleme için)
add_subdirectory(../../extern/pybind11 extern/pybind11)

# OpenCV kütüphanesini manuel tanımla (Sürüm uyumsuzluğu hatasını aşmak için)
set(OpenCV_INCLUDE_DIRS "C:/Users/Halil/Downloads/Programs/opencv/build/include")
set(OpenCV_LIBS "C:/Users/Halil/Downloads/Programs/opencv/build/x64/vc16/lib/opencv_world4120.lib")

include_directories(${OpenCV_INCLUDE_DIRS})

# Python modülünü oluştur (İsmi: leaf_vision)
pybind11_add_module(leaf_vision leaf_boundary.cpp)

# OpenCV bağımlılıklarını modüle bağla
target_link_libraries(leaf_vision PRIVATE ${OpenCV_LIBS})

# Derleme sonrası dosyayı kök dizine kopyala (Python'un görebilmesi için)
add_custom_command(TARGET leaf_vision POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
    $<TARGET_FILE:leaf_vision>
    ${CMAKE_CURRENT_SOURCE_DIR}/../../leaf_vision.pyd
)