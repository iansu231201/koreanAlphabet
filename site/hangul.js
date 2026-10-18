// 韓文字母資料、組字、羅馬拼音（文化觀光部式）與注音近似音
const H = (() => {
  const L = [
    { j: "ㄱ", rr: "g",  zy: "ㄍ", name: "기역",   type: "平音" },
    { j: "ㄲ", rr: "kk", zy: "ㄍ", name: "쌍기역", type: "緊音" },
    { j: "ㄴ", rr: "n",  zy: "ㄋ", name: "니은",   type: "鼻音" },
    { j: "ㄷ", rr: "d",  zy: "ㄉ", name: "디귿",   type: "平音" },
    { j: "ㄸ", rr: "tt", zy: "ㄉ", name: "쌍디귿", type: "緊音" },
    { j: "ㄹ", rr: "r",  zy: "ㄌ", name: "리을",   type: "流音" },
    { j: "ㅁ", rr: "m",  zy: "ㄇ", name: "미음",   type: "鼻音" },
    { j: "ㅂ", rr: "b",  zy: "ㄅ", name: "비읍",   type: "平音" },
    { j: "ㅃ", rr: "pp", zy: "ㄅ", name: "쌍비읍", type: "緊音" },
    { j: "ㅅ", rr: "s",  zy: "ㄙ", name: "시옷",   type: "平音" },
    { j: "ㅆ", rr: "ss", zy: "ㄙ", name: "쌍시옷", type: "緊音" },
    { j: "ㅇ", rr: "",   zy: "",   name: "이응",   type: "無聲" },
    { j: "ㅈ", rr: "j",  zy: "ㄗ", name: "지읒",   type: "平音" },
    { j: "ㅉ", rr: "jj", zy: "ㄗ", name: "쌍지읒", type: "緊音" },
    { j: "ㅊ", rr: "ch", zy: "ㄘ", name: "치읓",   type: "激音" },
    { j: "ㅋ", rr: "k",  zy: "ㄎ", name: "키읔",   type: "激音" },
    { j: "ㅌ", rr: "t",  zy: "ㄊ", name: "티읕",   type: "激音" },
    { j: "ㅍ", rr: "p",  zy: "ㄆ", name: "피읖",   type: "激音" },
    { j: "ㅎ", rr: "h",  zy: "ㄏ", name: "히읗",   type: "喉音" },
  ];
  // pal: 遇到 ㄧ 開頭的母音時，ㅅㅈㅊ 改用 ㄒㄐㄑ
  const PAL = { "ㄙ": "ㄒ", "ㄗ": "ㄐ", "ㄘ": "ㄑ" };
  const V = [
    { j: "ㅏ", rr: "a",   zy: "ㄚ" },   { j: "ㅐ", rr: "ae",  zy: "ㄝ" },
    { j: "ㅑ", rr: "ya",  zy: "ㄧㄚ" }, { j: "ㅒ", rr: "yae", zy: "ㄧㄝ" },
    { j: "ㅓ", rr: "eo",  zy: "ㄛ" },   { j: "ㅔ", rr: "e",   zy: "ㄝ" },
    { j: "ㅕ", rr: "yeo", zy: "ㄧㄛ" }, { j: "ㅖ", rr: "ye",  zy: "ㄧㄝ" },
    { j: "ㅗ", rr: "o",   zy: "ㄡ" },   { j: "ㅘ", rr: "wa",  zy: "ㄨㄚ" },
    { j: "ㅙ", rr: "wae", zy: "ㄨㄝ" }, { j: "ㅚ", rr: "oe",  zy: "ㄨㄝ" },
    { j: "ㅛ", rr: "yo",  zy: "ㄧㄡ" }, { j: "ㅜ", rr: "u",   zy: "ㄨ" },
    { j: "ㅝ", rr: "wo",  zy: "ㄨㄛ" }, { j: "ㅞ", rr: "we",  zy: "ㄨㄝ" },
    { j: "ㅟ", rr: "wi",  zy: "ㄨㄧ" }, { j: "ㅠ", rr: "yu",  zy: "ㄧㄨ" },
    { j: "ㅡ", rr: "eu",  zy: "ㄜ" },   { j: "ㅢ", rr: "ui",  zy: "ㄜㄧ" },
    { j: "ㅣ", rr: "i",   zy: "ㄧ" },
  ];
  // 7 種代表音
  const REP = {
    k:  { rr: "k",  zy: "ㄍ", label: "ㄱ [k]" },
    n:  { rr: "n",  zy: "ㄣ", label: "ㄴ [n]" },
    t:  { rr: "t",  zy: "ㄉ", label: "ㄷ [t]" },
    l:  { rr: "l",  zy: "ㄌ", label: "ㄹ [l]" },
    m:  { rr: "m",  zy: "ㄇ", label: "ㅁ [m]" },
    p:  { rr: "p",  zy: "ㄅ", label: "ㅂ [p]" },
    ng: { rr: "ng", zy: "ㄥ", label: "ㅇ [ng]" },
  };
  const T = [
    { j: "", rep: null }, { j: "ㄱ", rep: "k" }, { j: "ㄲ", rep: "k" }, { j: "ㄳ", rep: "k" },
    { j: "ㄴ", rep: "n" }, { j: "ㄵ", rep: "n" }, { j: "ㄶ", rep: "n" }, { j: "ㄷ", rep: "t" },
    { j: "ㄹ", rep: "l" }, { j: "ㄺ", rep: "k" }, { j: "ㄻ", rep: "m" }, { j: "ㄼ", rep: "l" },
    { j: "ㄽ", rep: "l" }, { j: "ㄾ", rep: "l" }, { j: "ㄿ", rep: "p" }, { j: "ㅀ", rep: "l" },
    { j: "ㅁ", rep: "m" }, { j: "ㅂ", rep: "p" }, { j: "ㅄ", rep: "p" }, { j: "ㅅ", rep: "t" },
    { j: "ㅆ", rep: "t" }, { j: "ㅇ", rep: "ng" }, { j: "ㅈ", rep: "t" }, { j: "ㅊ", rep: "t" },
    { j: "ㅋ", rep: "k" }, { j: "ㅌ", rep: "t" }, { j: "ㅍ", rep: "p" }, { j: "ㅎ", rep: "t" },
  ];

  // 代表音對應的尾音索引
  const REP_T = { k: 1, n: 4, t: 7, l: 8, m: 16, p: 17, ng: 21 };

  const compose =(l, v, t = 0) => String.fromCharCode(0xac00 + (l * 21 + v) * 28 + t);
  const decompose = (ch) => {
    const n = ch.charCodeAt(0) - 0xac00;
    return { l: Math.floor(n / 588), v: Math.floor((n % 588) / 28), t: n % 28 };
  };
  // 單獨音節的尾音代表音；밟 為例外，讀 [밥]
  const repOf = (l, v, t) => (t === 11 && l === 7 && v === 0 ? "p" : T[t].rep);

  const info = (l, v, t = 0) => {
    const rep = repOf(l, v, t);
    const fin = rep ? REP[rep] : null;
    let lz = L[l].zy;
    if (PAL[lz] && V[v].zy.startsWith("ㄧ")) lz = PAL[lz];
    let vz = V[v].zy, tz = fin ? fin.zy : "";
    if (vz.endsWith("ㄚ") && (rep === "n" || rep === "ng")) {
      vz = vz.slice(0, -1) + (rep === "n" ? "ㄢ" : "ㄤ");
      tz = "";
    }
    const ch = compose(l, v, t);
    // 實際發音：尾音換成代表音後的字（僅複合 / 非代表尾音時與原字不同）。
    // 單獨音節的發音與其代表音字完全相同，因此播放代表音字的音檔。
    const sound = compose(l, v, REP_T[rep] ?? 0);
    return {
      ch,
      rr: L[l].rr + V[v].rr + (fin ? fin.rr : ""),
      zy: lz + vz,
      zyFinal: tz,
      sound,
      audio: `audio/${sound.charCodeAt(0).toString(16).toUpperCase()}.mp3`,
    };
  };

  let player;
  const play = (src) => {
    if (!player) player = new Audio();
    player.pause();
    player.src = src;
    player.currentTime = 0;
    player.play().catch(() => {});
  };

  const syllableAudio = (ch) => {
    const { l, v, t } = decompose(ch);
    return info(l, v, t).audio;
  };

  return { L, V, T, REP, compose, decompose, info, play, syllableAudio, nameAudio: (i) => `audio/name${i}.mp3` };
})();
