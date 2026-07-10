# HWP engine design decisions

## HD-001 — Original forms are immutable

Every assembly iteration begins from a fresh form copy. Input and output paths
must differ. A failed derivative is discarded rather than patched into the next
iteration.

## HD-002 — Inspect before editing

Anchors, fields, page metrics, tables, paragraph formats, and break behavior are
captured before operations are generated. Full body or XML dumps are not used as
agent context.

## HD-003 — Validate the whole operation batch first

Both a bare operation array and the documented wrapper are accepted, but every
operation name and required field is checked before Hancom opens the document.
This prevents an invalid later operation from leaving a half-mutated output.

## HD-004 — Insert, select, then format

Hancom's pending character shape may lag by one insertion. New text is inserted,
selected, and then assigned its size and other character properties. Relying on
the pre-insertion cursor shape can corrupt adjacent headings.

## HD-005 — Preserve printable width when changing binding

Converting an asymmetric book layout to a symmetric submission layout redistributes
left, right, and gutter space while preserving total printable width. Margins are
not replaced by arbitrary defaults.

## HD-006 — Native fields beat simulated formatting

Use HWP fields for form values and native hyperlink fields for URLs. Simulating
links with colored text or relying on auto-format behavior is not deterministic.

## HD-007 — Form-owned paragraph formats are baseline data

Alignment, line spacing, and character sizes of labels and headings are captured
during intake. Added body paragraphs may differ; tracked form paragraphs may not
drift silently.

## HD-008 — Proof combines structure, metrics, and vision

Neither XML inspection nor PDF appearance is sufficient alone. A deliverable is
accepted only after saved-artifact inspection, deterministic QA, and visual proof.

## HD-009 — Layout repair uses content deltas

Page balance is planned before assembly. Post-assembly repairs prefer bounded
one- or two-line rewrites instead of accumulating font, spacing, and margin knobs.

## HD-010 — Optional backends must declare degradation

Offline HWPX processing is useful for structural cleanup, but it is not silently
equivalent to Windows COM editing. Backend limitations are listed in the
capability matrix and the final artifact should be finished on Windows when a
required capability is unavailable.
