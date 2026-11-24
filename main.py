"""Warning label entry: examine the label line against the gate, then stamp it out."""
import json
import os
import pathlib

LABEL = "entry.txt"
STAMP_CAP = 160


class LabelGate:
    @staticmethod
    def examine(text: str) -> dict:
        flat = " ".join(text.split())
        return {
            "flat": flat,
            "ink_bytes": len(text.encode("utf-8")),
            "imprint_cap_ok": len(flat) <= STAMP_CAP,
            "imprint_present": flat != "" and len(text.encode("utf-8")) > 0,
            "one_imprint": text.strip().count("\n") == 0,
        }


def stamp() -> int:
    sheet = pathlib.Path(__file__).resolve().parent / LABEL
    raw = sheet.read_text(encoding="utf-8")
    finding = LabelGate.examine(raw)
    finding["printed"] = finding["imprint_cap_ok"] and finding["imprint_present"] and finding["one_imprint"]
    crate = os.environ.get("MAKEFUN_OUTPUT_DIR") or str(sheet.parent / "crate")
    pathlib.Path(crate).mkdir(parents=True, exist_ok=True)
    (pathlib.Path(crate) / LABEL).write_bytes(raw.encode("utf-8"))
    print(json.dumps({"label": "human-caution", "finding": finding, "crate": crate}))
    return 0 if finding["printed"] else 1


if __name__ == "__main__":
    raise SystemExit(stamp())
