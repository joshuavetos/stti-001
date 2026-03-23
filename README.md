# STTI-001: Secure Tool-Tracing Interface

### The Invariant
**"No Side Effect Without Provenance."** STTI-001 is a security specification designed to eliminate the "Inference Gap" in AI Agents. It moves safety from non-deterministic "System Prompts" to deterministic infrastructure. An agent cannot execute a side-effecting tool unless the arguments are exact, type-strict matches of data previously ingested from a trusted source.

### The Pillars

#### 1. Deterministic Provenance Ledger
Unlike substring matching or vector similarity, the STTI Ledger uses a strict `(value, type, source)` tuple for grounding. 
* **No Substrings:** "User_1" cannot validate for "User_123".
* **No Type Coercion:** `123` (int) cannot validate for `123.0` (float).
* **Source Anchoring:** A value is only valid if it originated from a specific, authorized tool or user input.

#### 2. Bytecode Purity Gate
The Purity Gate performs static analysis on Python bytecode (`dis`) before execution. It prevents "Black Box" models from escaping sandboxes via:
* **Closure Blocking:** Scans `co_freevars` to prevent unauthorized data leakage from outer scopes.
* **Opcode Blacklisting:** Blocks `LOAD_GLOBAL`, `LOAD_DEREF`, and `IMPORT_NAME` to ensure the agent cannot manipulate the environment or reach for unauthorized libraries.
* **Metadata Inspection:** Scans `co_names` for dunder attribute access (`__subclasses__`, `__globals__`, etc.) to prevent class-tree traversal.

### Project Structure
* `stti/core/provenance.py`: Exact-match identity ledger.
* `stti/core/gate.py`: Python bytecode security scanner.
* `examples/secure_agent.py`: Demonstration of the six core security invariants.

### Origin
This specification emerged from LangChain issue #34469. The formal debate that shaped the architecture is documented there.

### Installation
```bash
pip install -e .
