#include "VMManager.h"
#include "PyBridge.h"
#include <vector>
#include <pybind11/embed.h>
#include <optional>
#include <format>
// By Zero123
namespace py = pybind11;

static std::vector<std::string> ENV_PATHS;
static bool _USE_UTF8 = false;
static bool _PY_LINE_FLUSH_MODE = false;
class PyVM
{
public:
	PyVM()
	{
		py::initialize_interpreter();
		// 禁用pyc文件生成
		py::exec("import sys\nsys.dont_write_bytecode = True");

		if (_USE_UTF8)
		{
			// 强制使用utf8输出编码 windows中文环境默认gbk2312
			py::exec("import io\nsys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')\nsys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')");
		}

		if (_PY_LINE_FLUSH_MODE)
		{
			// print行刷新模式
			py::exec("sys.stdout.reconfigure(line_buffering=True)\nsys.stderr.reconfigure(line_buffering=True)");
		}

		if (QPyMCBridge::INIT_PY_THREAD)
		{
			py::exec("import threading");
		}

		for (const auto& p : ENV_PATHS)
		{
			PY_ADD_ENV_PATH(p);
		}
		// 多线程模式支持
		PyEval_SaveThread();
	}

	~PyVM()
	{
		PyGILState_Ensure();
		QPyMCBridge::PyVMDestroyHandler();
		py::finalize_interpreter();
	}

	static void PY_ADD_ENV_PATH(const std::string& p)
	{
		py::exec(std::format("import sys\nsys.path.append('{}')", p));
	}
};
static std::optional<PyVM> _pyVm;

namespace QPyMCBridge
{
	bool INIT_PY_THREAD = false;

	void initVM()
	{
		if (!getVMLiveState())
		{
			_pyVm.emplace();
		}
	}

	void destroyVM()
	{
		_pyVm.reset();
	}

	bool getVMLiveState()
	{
		if (_pyVm)
		{
			return true;
		}
		return false;
	}

	// 添加环境路径 以便loadMod能够准确搜索到目标包体
	void addEnvPath(const std::filesystem::path& path)
	{
		return addEnvPath(path.generic_string());
	}

	void addEnvPath(const std::string& path)
	{
		ENV_PATHS.push_back(path);
		if (getVMLiveState())
		{
			py::gil_scoped_acquire gil;
			PyVM::PY_ADD_ENV_PATH(path);
		}
	}

	void addEnvPath(const char* cstr)
	{
		return addEnvPath(std::string(cstr));
	}

	// 加载MOD(通常搭配setGameThreadInitHandler回调下处理)
	void loadMod(const std::string& name)
	{
		std::string fullName = std::format("{}.modMain", name);
		try
		{
			py::module_::import(fullName.c_str());
		}
		catch (const std::exception& e)
		{
			std::cerr << "Error loading module '" << fullName << "': " << e.what() << std::endl;
		}
	}

	void setUseUTF8(bool state)
	{
		_USE_UTF8 = state;
	}

	void flushPyStdout()
	{
		py::gil_scoped_acquire gil;
		py::module_ sys = py::module_::import("sys");
		sys.attr("stdout").attr("flush")();
	}

	void setPyLineFlushMode(bool enable)
	{
		_PY_LINE_FLUSH_MODE = enable;
	}
}