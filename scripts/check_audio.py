"""檢查 site/audio 是否齊全：11,172 音節 + 19 子音名稱，且每檔皆為有效、非靜音的 mp3。"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "site" / "audio"
expected = [f"{cp:04X}.mp3" for cp in range(0xAC00, 0xD7A4)] + [f"name{i}.mp3" for i in range(19)]

missing = [f for f in expected if not (OUT / f).exists()]
bad, hashes = [], {}
for f in expected:
    p = OUT / f
    if not p.exists():
        continue
    hashes.setdefault(hashlib.md5(p.read_bytes()).hexdigest(), []).append(f)
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(p)],
        capture_output=True, text=True,
    )
    try:
        d = float(json.loads(r.stdout)["format"]["duration"])
    except Exception:  # noqa: BLE001
        d = 0
    if not 0.2 < d < 3:
        bad.append((f, d))

dups = [v for v in hashes.values() if len(v) > 1]
print(f"缺少 {len(missing)}，長度異常 {len(bad)}，內容重複 {len(dups)} 組")
for x in missing[:20] + bad[:20] + dups[:20]:
    print(" ", x)
sys.exit(1 if missing or bad or dups else 0)
