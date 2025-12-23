# STTI-001: No Side Effect Without Provenance

## Failure Mode

Modern agent frameworks validate tool arguments using JSON schema only (type and shape).
Large language models can hallucinate schema-valid but unsafe inputs, for example:

delete_file("/etc/secrets.pdf")

There is no architectural requirement that such arguments originate from
prior system-observed state.

This enables unauthorized or unintended side effects.

## Invariant

No tool with side effects (mutate, delete, send, transfer, write)
may execute unless **every argument** traces to a prior trusted tool output
within the same session.

This invariant is independent of:
- Prompt wording
- Model intelligence
- Safety tuning
- Alignment strategies

It is a deterministic architectural control.

## Reference Gate (Minimal)

```python
class ProvenanceError(Exception):
    pass

provenance = {}  # {tool_name: [values]}

def record(tool_name, outputs):
    provenance[tool_name] = [str(o) for o in outputs]

def execute(tool_call):
    return "executed"

def gate(tool_call):
    for arg in tool_call["args"].values():
        if str(arg) not in [v for values in provenance.values() for v in values]:
            raise ProvenanceError(f"Unprovenanced argument: {arg}")
    return execute(tool_call)
```

## Test

```python
record("list_users", ["bob"])

gate({"name": "delete_user", "args": {"id": "bob"}})  # PASS
gate({"name": "delete_user", "args": {"id": "eve"}})  # FAIL
```

## Examples

SAFE:
- list_users() -> ["bob"]
- delete_user("bob")

BROKEN:
- delete_user("/etc/passwd")
- delete_user("hallucinated_id")

## Architectural Diagram

```
User
 -> LLM
 -> ToolCall
 -> Provenance Gate
 -> Side Effect

If no provenance: BLOCK
```

## Scope

STTI-001 specifies:
- The failure mode
- The invariant
- The pass/fail condition

It does not mandate:
- Storage backend
- Agent framework
- Language model
- Vendor implementation

## Status

Stable.

Intended for use in:
- Framework audits
- Security reviews
- Compliance controls
- Vulnerability disclosures
