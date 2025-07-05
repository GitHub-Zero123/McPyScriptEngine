cmake_minimum_required (VERSION 3.12)

project("PyMCBridge")

set(CMAKE_CXX_STANDARD 20)
# set(CMAKE_CXX_STANDARD_REQUIRED ON)

# find_package(Python COMPONENTS Interpreter Development REQUIRED)
set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 REQUIRED)
find_package(JNI REQUIRED)

message(STATUS "PyBind11引用路径: ${pybind11_DIR}")

if (JNI_FOUND)
    message(STATUS "JNI found!")
    message(STATUS "JNI include dirs: ${JNI_INCLUDE_DIRS}")
    message(STATUS "JNI libraries: ${JNI_LIBRARIES}")
else()
    message(FATAL_ERROR "JNI not found!")
endif()

include_directories(${JNI_INCLUDE_DIRS})
include_directories(${pybind11_INCLUDE_DIRS})

# PyBridge模块
add_library(PyBridgeObj OBJECT
    "PyBridge/VMManager.cpp"
    "PyBridge/GameThread.cpp"
    "PyBridge/GameEvent.cpp"
    "PyBridge/PyBridge.cpp"
    "PyBridge/ModLoader.cpp"
    "PyBridge/Utils/Math.cpp"
)

# JNI模块
add_library(JNIModulesObj OBJECT
    "JNI/ModLoader.cpp"
    "JNI/EventManager.cpp"
    "JNI/JNIManager.cpp"
)

# PyMCBridge
if(OFF)
    add_executable(PyMCBridge "main.cpp" "Utils/EnvEncode.cpp")
else()
    add_library(PyMCBridge SHARED)
endif()

target_link_libraries(PyMCBridge PRIVATE pybind11::embed)

# 把 OBJECT 库里的所有对象文件加入可执行文件
target_sources(PyMCBridge PRIVATE
    $<TARGET_OBJECTS:PyBridgeObj>
    $<TARGET_OBJECTS:JNIModulesObj>
)

## PyMCBridge
# add_executable (PyMCBridge "main.cpp" "utils/EnvEncode.cpp" "PyBridge/VMManager.cpp" "PyBridge/GameThread.cpp" "PyBridge/GameEvent.cpp" "PyBridge/PyBridge.cpp" "PyBridge/ModLoader.cpp" "JNI/com_zero123_PyMcBridge_ModLoader.cpp" "JNI/Manager.cpp")
# target_link_libraries(PyMCBridge PRIVATE pybind11::embed)
