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
            (pkgs.python3.withPackages (ps: [ ps.edge-tts ]))
            pkgs.ffmpeg
            pkgs.gh
            pkgs.git
          ];
          shellHook = ''
            echo "產生語音: python scripts/gen_audio.py"
            echo "本機預覽: python -m http.server -d site 8000"
          '';
        };
      });
    };
}
