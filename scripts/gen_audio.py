"""產生韓文音節（代表音尾音，涵蓋全部 11,172 字的發音）與子音名稱的 mp3。

已存在的檔案會跳過，可中斷後重跑。
用法: python scripts/gen_audio.py [--force]
"""
import asyncio
import sys
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


# 只產生「無尾音」與 7 個代表音尾音（ㄱㄴㄷㄹㅁㅂㅇ）的音節：19 × 21 × 8 = 3,192 個。
# 單獨音節中其他尾音一律讀成代表音（닭→[닥]、값→[갑]），網頁直接播放代表音字的音檔。
# （edge-tts 對 ㄺ、ㄻ、ㄿ 等複合尾音常讀錯，例如 갉 讀成 갈，所以不直接合成。）
REP_FINALS = (0, 1, 4, 7, 8, 16, 17, 21)


def jobs():
    for cp in range(0xAC00, 0xD7A4):
        if (cp - 0xAC00) % 28 in REP_FINALS:
            yield chr(cp), OUT / f"{cp:04X}.mp3"
    for i, name in enumerate(CONSONANT_NAMES):
        yield name, OUT / f"name{i}.mp3"


# 直接保存 edge-tts 原始輸出，不做裁剪：裁掉靜音會切到 ㅅ 等弱起音（사과 聽起來像 차과）。
async def make(text: str, dst: Path, sem: asyncio.Semaphore):
    async with sem:
        part = dst.with_suffix(".part")
        for attempt in range(5):
            try:
                await edge_tts.Communicate(text, VOICE).save(str(part))
                if part.stat().st_size < 1000:
                    raise RuntimeError("音檔過小")
                part.rename(dst)
                return True
            except Exception as e:  # noqa: BLE001
                if attempt == 4:
                    print(f"失敗 {text}: {e}", file=sys.stderr)
                    return False
                await asyncio.sleep(2 ** attempt)


async def main():
    force = "--force" in sys.argv
    OUT.mkdir(parents=True, exist_ok=True)
    todo = [(t, p) for t, p in jobs() if force or not p.exists()]
    print(f"待產生 {len(todo)} 個")
    sem = asyncio.Semaphore(CONCURRENCY)
    tasks = [make(t, p, sem) for t, p in todo]
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
