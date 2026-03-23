from typing import Any, Dict, Tuple

class ProvenanceLedger:
    """
    STTI-001 Strict Provenance Ledger.
    Enforces exact identity lookup to prevent substring/inference vulnerabilities.
    """
    def __init__(self):
        # Key: (value, type, source_tool) -> Value: True
        self._vault: Dict[Tuple[Any, type, str], bool] = {}

    def ingest(self, value: Any, source_tool: str):
        """Adds a value to the ledger with strict type and source anchoring."""
        key = (value, type(value), source_tool)
        self._vault[key] = True

    def is_grounded(self, value: Any, source_tool: str) -> bool:
        """
        Performs an exact dictionary lookup. 
        No substring matching, no 'in' string comparison.
        """
        key = (value, type(value), source_tool)
        return self._vault.get(key, False)
