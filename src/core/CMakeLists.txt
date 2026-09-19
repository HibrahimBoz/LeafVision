cmake_minimum_required(VERSION 3.15)
project(LeafVision CXX)

set(CMAKE_CXX_STANDARD 17)

# Yerel pybind11 kullanımı (Offline derleme için)
add_subdirectory(../../extern/pybind11 extern/pybind11)

# OpenCV kurulum dizini: once ortam degiskeni, yoksa bu makinedeki
# varsayilan yola dus (baska bir makinede -DOpenCV_DIR=... ile gecersiz kilinabilir)
if(NOT OpenCV_DIR AND DEFINED ENV{OpenCV_DIR})
  set(OpenCV_DIR "$ENV{OpenCV_DIR}")
endif()
if(NOT OpenCV_DIR)
  set(OpenCV_DIR "C:/Users/Halil/Downloads/Programs/opencv/build" CACHE PATH "OpenCVConfig.cmake dizini")
endif()

find_package(OpenCV REQUIRED)

# Python modülünü oluştur (İsmi: leaf_vision)
pybind11_add_module(leaf_vision leaf_boundary.cpp)

# OpenCV bağımlılıklarını modüle bağla
target_include_directories(leaf_vision PRIVATE ${OpenCV_INCLUDE_DIRS})
target_link_libraries(leaf_vision PRIVATE ${OpenCV_LIBS})

# Derleme sonrası dosyayı kök dizine kopyala (Python'un görebilmesi için)
add_custom_command(TARGET leaf_vision POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
    $<TARGET_FILE:leaf_vision>
    ${CMAKE_CURRENT_SOURCE_DIR}/../../leaf_vision.pyd
)