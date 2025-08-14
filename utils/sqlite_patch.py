import importlib.util
import platform
import sqlite3
import sys

MIN_SQLITE_VERSION = (3, 35, 0)

if sqlite3.sqlite_version_info < MIN_SQLITE_VERSION:
    if platform.system() == "Linux" and platform.machine() == "x86_64":
        spec = importlib.util.find_spec("pysqlite3")
        if spec is None:
            raise RuntimeError("pysqlite3-binary is required but not installed.")

        pysqlite3 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pysqlite3)
        sys.modules["sqlite3"] = pysqlite3
    else:
        raise RuntimeError(
            f"Your system sqlite3 is too old ({sqlite3.sqlite_version}) and can't be patched automatically."
        )
