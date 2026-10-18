# koreanAlphabet 韓文字母發音表

靜態網頁：子音／母音／尾音／399 組合表的發音，以及「子音＋母音＋尾音」組字頁。
全部 11,172 個音節的語音預先以 edge-tts（ko-KR-SunHiNeural）產生為 mp3，網頁直接播放靜態檔，不依賴任何執行期 API。

```bash
nix develop
python scripts/gen_audio.py        # 產生 / 補齊 site/audio（已存在會跳過）
python -m http.server -d site 8000 # 本機預覽
```

push 到 `main` 後由 GitHub Actions 部署 `site/` 到 GitHub Pages。
