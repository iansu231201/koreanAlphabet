# koreanAlphabet 韓文字母發音表

靜態網頁：子音／母音／尾音／399 組合表的發音，以及「子音＋母音＋尾音」組字頁。
語音以 edge-tts（ko-KR-SunHiNeural）預先產生為 mp3，網頁直接播放靜態檔，不依賴任何執行期 API。
單獨音節的尾音只有 7 種代表音（닭→[닥]、값→[갑]），因此只合成「無尾音＋7 代表音」共 3,192 個音節，其餘字播放其代表音字的音檔，涵蓋全部 11,172 字。

已知限制：edge-tts 對 쇼/쑈、셀/쎌、뮌/뮨 讀成相同聲音。

`python scripts/check_audio.py` 檢查音檔齊全、長度正常，並列出內容相同的音檔組。

```bash
nix develop
python scripts/gen_audio.py        # 產生 / 補齊 site/audio（已存在會跳過）
python -m http.server -d site 8000 # 本機預覽
```

push 到 `main` 後由 GitHub Actions 部署 `site/` 到 GitHub Pages。
