import unittest

from subhunterx.core.analyzer import SubdomainAnalyzer
from subhunterx.database.manager import DBManager
from subhunterx.utils.helpers import is_valid_domain


class CoreLogicTests(unittest.TestCase):
    def test_domain_validation(self):
        self.assertTrue(is_valid_domain("example.com"))
        self.assertTrue(is_valid_domain("sub.example.co"))
        self.assertFalse(is_valid_domain("invalid"))
        self.assertFalse(is_valid_domain("-bad.example.com"))

    def test_risk_scoring_keywords_and_sensitive_paths(self):
        analyzer = SubdomainAnalyzer({"subhunterx": {"timeout": 1, "retry": 1}})
        result = analyzer.calculate_risk(
            "admin-dev.example.com",
            {"status_code": 200, "body_preview": "Admin Login"},
            {"cname": None},
            {"expired": False},
            ["/.env"],
        )
        self.assertEqual(result["level"], "high")
        self.assertGreaterEqual(result["score"], 70)
        self.assertTrue(any("sensitive paths" in reason for reason in result["reasons"]))

    def test_takeover_candidate_scoring(self):
        analyzer = SubdomainAnalyzer({"subhunterx": {"timeout": 1, "retry": 1}})
        result = analyzer.calculate_risk(
            "old.example.com",
            {},
            {"cname": "old.github.io"},
            {"expired": False},
            [],
        )
        self.assertTrue(result["takeover_candidate"])

    def test_snapshot_diff(self):
        before = {"a.example.com": {"subdomain": "a.example.com", "status_code": 200, "risk_level": "low"}}
        after = {
            "a.example.com": {"subdomain": "a.example.com", "status_code": 403, "risk_level": "medium"},
            "b.example.com": {"subdomain": "b.example.com", "status_code": 200, "risk_level": "low"},
        }
        diff = DBManager.diff_snapshots(before, after)
        self.assertEqual(len(diff["new"]), 1)
        self.assertEqual(len(diff["removed"]), 0)
        self.assertEqual(len(diff["changed"]), 1)


if __name__ == "__main__":
    unittest.main()
