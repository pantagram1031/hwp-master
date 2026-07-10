# HWP/HWPX troubleshooting knowledge base

These signatures were generalized from real assembly failures. Match the symptom,
apply the smallest fix, rebuild from a pristine form copy, and verify the saved
HWPX plus exported PDF.

| ID | Symptom | Cause | Corrective action | Verification |
|---|---|---|---|---|
| T1 | Stray 2–3 line gaps between subsections | Literal newline replacement cannot target empty HWP paragraphs reliably | Use explicit paragraph targeting or offline `tidy_hwpx.py`; never drain paragraph marks near headings through COM | Run the gap check and inspect the affected page |
| T2 | Multi-row matrix renders as one broken row | LaTeX row separators were not translated to HwpEqn `#` | Convert separators inside matrix bodies and fail sanity checks on leftovers | Inspect equation script and exported PDF |
| T3 | Hyperlink text is truncated and tail text appears elsewhere | Cursor positions captured before field creation became stale | Reacquire the end position after inserting the hyperlink field | Inspect the saved field and visible URL tail |
| T4 | Designed cover or summary whitespace fails uniformity | Global gap thresholds ignore intentional page roles | Declare cover pages and page-bottom exemptions before running QA | Confirm only declared regions are exempt |
| T5 | Anchor search fails although text is visible | The visible label spans multiple character-property runs | Choose a unique substring contained in one run | Verify uniqueness in both form and content |
| T6 | Heading size changes or merges with the previous paragraph | Deleting a paragraph boundary inherits pending character properties | Perform blank cleanup in an offline HWPX post-pass | Compare heading character sizes with the baseline |
| T7 | Body text is inserted into a table label cell | Moving to the next paragraph did not leave a single-paragraph cell | Check whether the cursor still contains the anchor; explicitly split before insertion | Inspect table text and paragraph boundaries |
| T8 | Inserted body text is centered unexpectedly | A new paragraph inherited the label paragraph's centered shape | Explicitly set body paragraph alignment after splitting the anchor paragraph | Run paragraph-format comparison |
| T9 | Form headings lose their designed line spacing | A document-wide body spacing operation also changed form-owned paragraphs | Capture `para_formats` during intake and restore them after assembly | Run `style_diff.py --check-para-formats` |
| T10 | A section moves onto the previous page after cleanup | The form used blank paragraphs as implicit page pushers | Add an explicit `page_break_before` rule for the frozen heading anchor | Inspect page starts after tidy |
| T11 | A table caption is orphaned at a page bottom | Caption lacks keep-with-next behavior | Apply `keepWithNext=1` to declared caption prefixes | Inspect the caption/table page pair |
| T12 | A batch stops after partially editing the document | Invalid operation was discovered during execution | Validate the complete ops payload before opening Hancom | Confirm invalid batches fail with no output mutation |

## COM session hangs

- Close stale HWP processes before retrying.
- Check for modal dialogs or security-module prompts.
- Work in small batches of roughly 5–8 operations.
- Always save to a distinct output path.
- Treat a timed-out or partial output as disposable; rebuild from the form copy.

## A test passes but the document looks wrong

Operation success proves only that Hancom accepted the command. Validation needs
three independent views:

1. structural inspection of the saved HWPX;
2. deterministic format/layout checks;
3. visual proof of the exported PDF, starting with a contact sheet.

## A global formatting fix seems convenient

Global operations frequently damage form-owned labels, headings, and tables.
Prefer a targeted operation. If a global body operation is unavoidable, capture
the form baseline first and restore tracked form paragraphs afterward.
