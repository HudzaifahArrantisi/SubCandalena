"""
Example analyzer plugin for SubCandalena.

Plugins are plain Python classes. Keep network calls optional and return a
dictionary with fields that should be merged into the scan result.
"""


class CustomAnalyzer:
    name = "custom_analyzer"

    def analyze(self, subdomain: str, context: dict) -> dict:
        reasons = []
        score_bonus = 0

        if subdomain.startswith("admin."):
            reasons.append("custom plugin: admin root subdomain")
            score_bonus = 10

        current_score = int(context.get("risk_score") or 0)
        return {
            "risk_score": min(100, current_score + score_bonus),
            "risk_reasons": reasons,
        }


def register():
    return CustomAnalyzer()
