class _AOSPReturnCode:
	(
		_SUCCESS,
		_MISSING_ARGS,
		_MISSING_DIR,
		_LUNCH_FAILED,
		_CLEAN_FAILED,
		_BUILD_FAILED,
	) = range(6)

	_STRINGS = {
		_SUCCESS: "Build completed successfully",
		_MISSING_ARGS: "Build failed: Missing arguments",
		_MISSING_DIR: "Build failed: Project dir doesn't exists",
		_LUNCH_FAILED: "Build failed: Lunching failed",
		_CLEAN_FAILED: "Build failed: Cleaning failed",
		_BUILD_FAILED: "Build failed: Building failed"
	}

	_NEEDS_LOGS_UPLOAD = {
		_LUNCH_FAILED: "lunch_log.txt",
		_CLEAN_FAILED: "clean_log.txt",
		_BUILD_FAILED: "build_log.txt"
	}

	def __init__(self, return_code: int):
		self.return_code = return_code

	def __int__(self):
		return self.return_code

	def __str__(self):
		return self._STRINGS.get(self.return_code, "Build failed: Unknown error")

	def needs_logs_upload(self):
		return self._NEEDS_LOGS_UPLOAD.get(self.return_code, False)

class AOSPReturnCode(_AOSPReturnCode):
	"""AOSP return code.

	This class indicates the status of a AOSP build.
	Can be casted to int and str.
	"""
	SUCCESS = _AOSPReturnCode(_AOSPReturnCode._SUCCESS)
	MISSING_ARGS = _AOSPReturnCode(_AOSPReturnCode._MISSING_ARGS)
	MISSING_DIR = _AOSPReturnCode(_AOSPReturnCode._MISSING_DIR)
	LUNCH_FAILED = _AOSPReturnCode(_AOSPReturnCode._LUNCH_FAILED)
	CLEAN_FAILED = _AOSPReturnCode(_AOSPReturnCode._CLEAN_FAILED)
	BUILD_FAILED = _AOSPReturnCode(_AOSPReturnCode._BUILD_FAILED)
