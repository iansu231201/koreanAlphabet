"""產生全部韓文音節（11,172）與子音名稱的 mp3。

已存在的檔案會跳過，可中斷後重跑。
用法: python scripts/gen_audio.py [--force]
"""
import asyncio
import subprocess
import sys
import tempfile
from pathlib import Path

import edge_tts

VOICE = "ko-KR-SunHiNeural"
CONCURRENCY = 8
OUT = Path(__file__).resolve().parent.parent / "site" / "audio"

# 19 個子音名稱（順序同初聲）
CONSONANT_NAMES = [
    "기역", "쌍기역", "니은", "디귿", "쌍디귿", "리을", "미음", "비읍", "쌍비읍", "시옷",
    "쌍시옷", "이응", "지읒", "쌍지읒", "치읓", "키읔", "티읕", "피읖", "히읗",
]


def jobs():
    for cp in range(0xAC00, 0xD7A4):
        yield chr(cp), OUT / f"{cp:04X}.mp3"
    for i, name in enumerate(CONSONANT_NAMES):
        yield name, OUT / f"name{i}.mp3"


def trim(src: Path, dst: Path):
    """去除前後靜音，轉單聲道 48kbps。"""
    silence = "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.05"
    subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-y", "-i", str(src),
         "-af", f"{silence},areverse,{silence},areverse,apad=pad_dur=0.1",
         "-ac", "1", "-b:a", "48k", str(dst)],
        check=True,
    )


async def make(text: str, dst: Path, sem: asyncio.Semaphore, tmp: Path):
    async with sem:
        raw = tmp / dst.name
        for attempt in range(5):
            try:
                await edge_tts.Communicate(text, VOICE).save(str(raw))
                if raw.stat().st_size < 1000:
                    raise RuntimeError("音檔過小")
                break
            except Exception as e:  # noqa: BLE001
                if attempt == 4:
                    print(f"失敗 {text}: {e}", file=sys.stderr)
                    return False
                await asyncio.sleep(2 ** attempt)
        await asyncio.to_thread(trim, raw, dst)
        raw.unlink()
        return True


async def main():
    force = "--force" in sys.argv
    OUT.mkdir(parents=True, exist_ok=True)
    todo = [(t, p) for t, p in jobs() if force or not p.exists()]
    print(f"待產生 {len(todo)} 個")
    sem = asyncio.Semaphore(CONCURRENCY)
    with tempfile.TemporaryDirectory() as d:
        tasks = [make(t, p, sem, Path(d)) for t, p in todo]
        ok = 0
        for i, fut in enumerate(asyncio.as_completed(tasks), 1):
            ok += await fut
            if i % 500 == 0:
                print(f"{i}/{len(todo)}")
    print(f"完成 {ok}/{len(todo)}")
    if ok != len(todo):
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
