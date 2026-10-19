"""用 Google Cloud Text-to-Speech 產生韓文音節（代表音尾音，涵蓋全部 11,172 字的發音）與子音名稱的 mp3。

金鑰從環境變數 GOOGLE_TTS_KEY 或 .tts/google_key 讀取（.tts/ 已 gitignore）。
已存在的檔案會跳過，可中斷後重跑。
用法: python scripts/gen_audio.py [--force]
"""
import asyncio
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

VOICE = "ko-KR-Standard-A"
CONCURRENCY = 4
PROJECT = Path(__file__).resolve().parent.parent
OUT = PROJECT / "site" / "audio"
KEY_FILE = PROJECT / ".tts" / "google_key"
API = "https://texttospeech.googleapis.com/v1/text:synthesize"

# 19 個子音名稱（順序同初聲）
CONSONANT_NAMES = [
    "기역", "쌍기역", "니은", "디귿", "쌍디귿", "리을", "미음", "비읍", "쌍비읍", "시옷",
    "쌍시옷", "이응", "지읒", "쌍지읒", "치읓", "키읔", "티읕", "피읖", "히읗",
]


# 只產生「無尾音」與 7 個代表音尾音（ㄱㄴㄷㄹㅁㅂㅇ）的音節：19 × 21 × 8 = 3,192 個。
# 單獨音節中其他尾音一律讀成代表音（닭→[닥]、값→[갑]），網頁直接播放代表音字的音檔。
REP_FINALS = (0, 1, 4, 7, 8, 16, 17, 21)


def jobs():
    for cp in range(0xAC00, 0xD7A4):
        if (cp - 0xAC00) % 28 in REP_FINALS:
            yield chr(cp), OUT / f"{cp:04X}.mp3"
    for i, name in enumerate(CONSONANT_NAMES):
        yield name, OUT / f"name{i}.mp3"


def synthesize(text: str, key: str) -> bytes:
    body = {
        "input": {"text": text},
        "voice": {"languageCode": "ko-KR", "name": VOICE},
        "audioConfig": {"audioEncoding": "MP3"},
    }
    req = urllib.request.Request(
        API, data=json.dumps(body).encode(),
        headers={"X-Goog-Api-Key": key, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return base64.b64decode(json.load(r)["audioContent"])


async def make(text: str, dst: Path, sem: asyncio.Semaphore, key: str):
    async with sem:
        for attempt in range(6):
            try:
                data = await asyncio.to_thread(synthesize, text, key)
                if len(data) < 1000:
                    raise RuntimeError("音檔過小")
                dst.write_bytes(data)
                return True
            except urllib.error.HTTPError as e:
                if e.code not in (429, 500, 503) or attempt == 5:
                    print(f"失敗 {text}: HTTP {e.code} {e.read().decode()[:200]}", file=sys.stderr)
                    return False
            except Exception as e:  # noqa: BLE001
                if attempt == 5:
                    print(f"失敗 {text}: {e}", file=sys.stderr)
                    return False
            await asyncio.sleep(2 ** attempt)


async def main():
    key = os.environ.get("GOOGLE_TTS_KEY") or (KEY_FILE.read_text().strip() if KEY_FILE.exists() else "")
    if not key:
        sys.exit("找不到 Google API 金鑰：請設定 GOOGLE_TTS_KEY 或建立 .tts/google_key")
    force = "--force" in sys.argv
    OUT.mkdir(parents=True, exist_ok=True)
    todo = [(t, p) for t, p in jobs() if force or not p.exists()]
    print(f"待產生 {len(todo)} 個")
    sem = asyncio.Semaphore(CONCURRENCY)
    tasks = [make(t, p, sem, key) for t, p in todo]
    ok = 0
    for i, fut in enumerate(asyncio.as_completed(tasks), 1):
        ok += await fut
        if i % 500 == 0:
            print(f"{i}/{len(todo)}", flush=True)
    print(f"完成 {ok}/{len(todo)}")
    if ok != len(todo):
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
