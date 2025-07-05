cmake_minimum_required (VERSION 3.12)

if (POLICY CMP0141)
    cmake_policy(SET CMP0141 NEW)
    set(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT "$<IF:$<AND:$<C_COMPILER_ID:MSVC>,$<CXX_COMPILER_ID:MSVC>>,$<$<CONFIG:Debug,RelWithDebInfo>:EditAndContinue>,$<$<CONFIG:Debug,RelWithDebInfo>:ProgramDatabase>>")
endif()

project("Root")

if(MSVC)
    add_compile_options(/utf-8)
    add_compile_options(/EHsc)
    if(OFF)
        if(CMAKE_BUILD_TYPE STREQUAL "Debug")
            add_compile_options(/MTd)
        else()
            add_compile_options(/MT)
        endif()
    endif()
endif()

add_subdirectory("PyMCBridge")