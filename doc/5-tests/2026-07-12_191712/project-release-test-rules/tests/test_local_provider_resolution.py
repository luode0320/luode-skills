"""只读 local provider 参数查询回归。"""

from __future__ import annotations

import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_ROOT = Path(__file__).parents[5] / "project-release-test-rules" / "scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from release_test_engine.model import InterfaceIR, ParameterIR
from release_test_engine.resolver import resolve_parameters


class LocalProviderResolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.database = self.root / "local.sqlite3"
        connection = sqlite3.connect(self.database)
        try:
            connection.execute("CREATE TABLE users (id TEXT PRIMARY KEY, name TEXT)")
            connection.execute("INSERT INTO users VALUES ('u-1', 'Ada')")
            connection.commit()
        finally:
            connection.close()
        self.interface = InterfaceIR("fp", "svc", "op", "http", {"method": "GET", "path": "/users"}, parameters=(ParameterIR("user_id", "query", required=True),))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_local_database_query_and_cache_are_resolved_with_trace(self) -> None:
        result = resolve_parameters(self.interface, sources={"user_id": [{"type": "local_database", "database": str(self.database), "query": "SELECT id FROM users WHERE name = ?", "query_params": ["Ada"]}]}, project_root=self.root)
        self.assertEqual({"user_id": "u-1"}, result["resolved"])
        self.assertFalse(result["unresolved"])
        cache_result = resolve_parameters(self.interface, sources={"user_id": [{"type": "local_cache", "cache": {"user_id": "cached"}, "key": "user_id"}]}, project_root=self.root)
        self.assertEqual({"user_id": "cached"}, cache_result["resolved"])

    def test_provider_failure_is_unresolved_and_does_not_guess(self) -> None:
        for source in (
            {"type": "local_database", "database": str(self.database), "query": "DELETE FROM users"},
            {"type": "local_database", "database": str(self.database), "query": "SELECT id FROM users WHERE id = 'missing'"},
            {"type": "local_database", "database": "C:/outside.sqlite3", "query": "SELECT id FROM users"},
        ):
            result = resolve_parameters(self.interface, sources={"user_id": [source]}, project_root=self.root)
            self.assertEqual({}, result["resolved"])
            self.assertIn("user_id", result["unresolved"])
            self.assertFalse(any(item.get("resolved") for item in result["dependency_trace"]))


if __name__ == "__main__":
    unittest.main()
