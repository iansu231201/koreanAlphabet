{
  description = "韓文字母發音表 — 開發環境";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAll = f: nixpkgs.lib.genAttrs systems (s: f nixpkgs.legacyPackages.${s});
    in {
      devShells = forAll (pkgs: {
        default = pkgs.mkShell {
          packages = [
            pkgs.python3
            pkgs.ffmpeg
            pkgs.gh
            pkgs.git
          ];
          shellHook = ''
            echo "產生語音: python scripts/gen_audio.py"
            echo "本機預覽: python -m http.server -d site 8000"
          '';
        };

        # 本機語音模型（MeloTTS 等）：pip 套件與模型放在 .tts/（已 gitignore）
        tts = pkgs.mkShell {
          packages = [ pkgs.python311 pkgs.uv pkgs.ffmpeg pkgs.git ];
          LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [ pkgs.stdenv.cc.cc.lib pkgs.zlib ];
          shellHook = ''
            export UV_PROJECT_ENVIRONMENT=$PWD/.tts/venv
            export UV_CACHE_DIR=$PWD/.tts/uv-cache
            export HF_HOME=$PWD/.tts/hf
            export NLTK_DATA=$PWD/.tts/nltk
            [ -d .tts/venv ] || uv venv -q --python ${pkgs.python311}/bin/python .tts/venv
            source .tts/venv/bin/activate
          '';
        };
      });
    };
}
