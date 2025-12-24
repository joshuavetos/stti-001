STTI-001 — Worked Examples

This document provides minimal, non-normative examples illustrating the
STTI-001 invariant.

These examples are illustrative only. They do not define APIs, data models,
or implementation requirements.

PASS CASE (PROVENANCED ARGUMENT)

A tool emits observable state:

list_users() -> [“alice”, “bob”]

A subsequent side-effecting tool is invoked using a value that appeared in a
prior trusted tool output:

delete_user(“bob”)

This call is permitted because the argument “bob” was previously observed
within the same session.

FAIL CASE (UNPROVENANCED ARGUMENT)

A side-effecting tool is invoked with an argument that has not appeared in any
prior trusted tool output:

delete_user(“admin_root”)

This call must fail closed because the argument “admin_root” has no established
session provenance.

IMPORTANT NOTES
   •   These examples demonstrate the invariant, not an implementation.
   •   How provenance is tracked is framework-specific.
   •   How values may be derived or transformed is intentionally unspecified.
   •   STTI-001 requires only that a deterministic provenance policy exist and be
enforced consistently.

EDGE CASE (DERIVED VALUES)

A tool emits:
get_user_email("bob") -> "bob@example.com"

A subsequent call uses:
send_email("bob@example.com", "Welcome message")

Whether this is permitted depends on the framework's derivation policy.
STTI-001 requires only that such a policy exist and be applied consistently.
