#pragma once
#include <iostream>

template <typename... Args>
void debug_log_impl(Args&&... args)
{
    ((std::cout << std::forward<Args>(args) << " "), ...);
    std::cout << std::endl;
}

#ifdef _DEBUG
    #define DEBUG_LOG(...)                                     \
        do                                                     \
        {                                                      \
            std::cout << "[DEBUG] " << __FILE__ << ":" << __LINE__ << ": "; \
            debug_log_impl(__VA_ARGS__);                       \
        } while (0)
#else
    #define DEBUG_LOG(...) do {} while (0)
#endif

