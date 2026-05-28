"""
Minimal plugin interfaces for SubCandalena extensions.
"""

from typing import Dict, Iterable, List, Protocol


class PassiveSourcePlugin(Protocol):
    name: str

    def discover(self, domain: str, config: dict) -> Iterable[str]:
        """Return discovered subdomains for a domain."""


class AnalyzerPlugin(Protocol):
    name: str

    def analyze(self, subdomain: str, context: dict) -> Dict:
        """Return additional fields or risk reasons for a subdomain."""


class ExporterPlugin(Protocol):
    name: str

    def export(self, results: List[dict], output_dir: str) -> str:
        """Export results and return the output path."""


def merge_plugin_analysis(base: Dict, plugin_results: Iterable[Dict]) -> Dict:
    """Merge analyzer plugin output into a result dictionary."""
    merged = dict(base)
    reasons = list(merged.get("risk_reasons") or [])
    for result in plugin_results:
        for key, value in result.items():
            if key == "risk_reasons":
                reasons.extend(value if isinstance(value, list) else [value])
            else:
                merged[key] = value
    merged["risk_reasons"] = reasons
    return merged
