# Backend capability matrix

| Capability | Windows COM | Offline HWPX/XML | Notes |
|---|---:|---:|---|
| Read `.hwp` binary files | Yes | No | Requires locally installed Hancom Office HWP |
| Read/write `.hwpx` | Yes | Yes | XML path should preserve untouched package bytes |
| Preserve arbitrary existing form behavior | Strong | Partial | COM uses Hancom's own document engine |
| Fill named fields | Yes | Limited | Prefer native HWP fields through COM |
| Insert native equations | Yes | Partial | Offline path can prepare scripts; final rendering needs Hancom verification |
| Insert/edit tables and pictures | Yes | Partial | Complex layout should be verified through COM |
| Native hyperlinks | Yes | Limited | Do not emulate with blue text |
| PDF export | Yes | No | Hancom performs authoritative export |
| Contact-sheet and PDF QA | Yes, with `.[proof]` | Yes, with `.[proof]` | Requires PyMuPDF/Pillow extras |
| Restore paragraph formats offline | Yes | Yes | `tidy_hwpx.py` uses captured baseline data |
| macOS/Linux execution | No | Yes | `.hwp` binary editing remains unavailable |

“Partial” means the repository can perform a bounded operation but does not
promise pixel or behavior parity with Hancom's native engine. When a required
capability is partial or unavailable, mark the artifact as needing Windows
finalization instead of presenting the backend as equivalent.
