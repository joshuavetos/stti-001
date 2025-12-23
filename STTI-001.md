# STTI-001: No Side Effect Without Provenance

## Summary

STTI-001 defines an optional safety invariant for agent systems that invoke
side-effecting tools.

The invariant is simple:

No tool with side effects may execute unless every argument can be traced
to a value produced by a prior trusted tool output within the same session.

This specification is framework-agnostic and implementation-neutral.
It is intended to describe a failure mode and a deterministic architectural
control, not to mandate a specific API or implementation.

---

## Failure Mode

Modern agent frameworks typically validate tool arguments using JSON schema
(type and shape) only.

Large language models can generate schema-valid but hallucinated values,
for example identifiers, paths, or targets that were never observed or
confirmed by the system.

When such values are passed to side-effecting tools (delete, write, send,
mutate), unintended or unsafe actions may occur despite schema validation
passing.

This class of failure cannot be reliably mitigated through prompting,
system messages, or model alignment alone.

---

## Invariant

No tool with side effects may execute unless **every argument** originates
from a value produced by a prior trusted tool output within the same session.

The invariant applies at execution time and is independent of:
- Prompt wording
- Model choice
- Safety tuning
- Agent reasoning strategy

If argument provenance cannot be established, execution must fail closed.

---

## Scope

STTI-001 specifies:
- The failure mode
- The invariant
- The expected pass/fail behavior

It does not specify:
- Storage mechanisms
- Value derivation rules
- Agent architecture
- Framework APIs
- Vendor-specific behavior

---

## Intended Use

This specification is intended for:
- Framework design discussions
- Agent safety analysis
- Production hardening reviews
- Cross-framework comparison

It is not a vulnerability disclosure and does not propose an exploit.

---

## Status

Stable.

This document exists to enable discussion of whether such an invariant
should be supported at the framework level, and if so, how.
