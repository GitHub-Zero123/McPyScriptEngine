#pragma once
#include <iostream>
#include <vector>
#include <unordered_map>
// By Zero123

namespace QPyMCBridge
{
	// 事件管理器
	template <typename T>
	class EventManager
	{
	private:
		std::vector<T> handlers;
	public:
		void addHandler(const T& obj)
		{
			handlers.push_back(obj);
		}

		void addHandler(T&& obj)
		{
			handlers.push_back(std::move(obj));
		}

		void clear()
		{
			handlers.clear();
		}

		template <typename... Args>
		void call(Args&&... args)
		{
			static_assert(std::is_invocable<T, Args...>::value, "Handler type T must be callable with provided arguments");
			auto size = handlers.size();
			for (size_t i = 0; i < size; ++i)
			{
				try
				{
					handlers[i](std::forward<Args>(args)...);
				}
				catch (const std::exception& e)
				{
					std::cerr << e.what() << "\n";
				}
			}
		}
	};

	// 映射表事件管理器
	template <typename T1, typename T2>
	class MapEventManager
	{
	private:
		std::unordered_map<T1, EventManager<T2>> eventMaps;
	public:
		void regHandler(const T1& eventId, const T2& handler)
		{
			eventMaps[eventId].addHandler(handler);
		}

		void regHandler(T1&& eventId, T2&& handler)
		{
			eventMaps[std::move(eventId)].addHandler(std::move(handler));
		}

		void regHandler(const T1& eventId, T2&& handler)
		{
			eventMaps[eventId].addHandler(std::move(handler));
		}

		void clear()
		{
			eventMaps.clear();
		}

		template <typename... Args>
		void call(const T1& eventId, Args&&... args)
		{
			auto it = eventMaps.find(eventId);
			if (it != eventMaps.end())
			{
				it->second.call(std::forward<Args>(args)...);
			}
		}

		bool hasEvent(const T1& eventId) const
		{
			return eventMaps.find(eventId) != eventMaps.end();
		}
	};
}