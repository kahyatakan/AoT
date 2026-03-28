"""AOT komut satırı arayüzü — `aot launch` ile web arayüzünü başlatır."""

from __future__ import annotations

import argparse
import os
import platform
import signal
import subprocess
import sys
import time
import webbrowser


def _find_project_root() -> str:
    """pyproject.toml'ın bulunduğu proje kök dizinini döndürür."""
    # Bu dosya aot/ altında; üst dizin proje kökü
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)
    if os.path.exists(os.path.join(root, "pyproject.toml")):
        return root
    # Fallback: mevcut çalışma dizini
    return os.getcwd()


def _npm_cmd() -> list[str]:
    """Platform'a göre npm komutunu döndürür (Windows'ta npm.cmd)."""
    if platform.system() == "Windows":
        return ["npm.cmd"]
    return ["npm"]


def launch(open_browser: bool = True, port: int = 5173) -> None:
    """Backend + frontend'i başlatır, tarayıcıyı açar.

    Args:
        open_browser: True ise tarayıcıyı otomatik açar.
        port: Frontend port numarası (varsayılan: 5173).
    """
    project_root = _find_project_root()
    web_dir = os.path.join(project_root, "web")

    if not os.path.exists(web_dir):
        print("Hata: web/ dizini bulunamadı. Proje kök dizininden çalıştırın.", file=sys.stderr)
        sys.exit(1)

    print("🔨 Anvil of Taylor başlatılıyor...")
    print(f"   Backend  → http://localhost:8000")
    print(f"   Frontend → http://localhost:{port}")
    print("   Durdurmak için Ctrl+C\n")

    # Backend process
    backend = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "server.main:app",
         "--reload", "--port", "8000"],
        cwd=project_root,
    )

    # Frontend process — dist varsa http.server, yoksa npm run dev
    dist_index = os.path.join(web_dir, "dist", "index.html")
    if os.path.exists(dist_index):
        frontend = subprocess.Popen(
            [sys.executable, "-m", "http.server", str(port), "--directory", "dist"],
            cwd=web_dir,
        )
    else:
        npm = _npm_cmd()
        # node_modules yoksa önce npm install
        if not os.path.exists(os.path.join(web_dir, "node_modules")):
            print("   npm install çalıştırılıyor (ilk kurulum)...")
            subprocess.run(npm + ["install"], cwd=web_dir, check=True)
        frontend = subprocess.Popen(
            npm + ["run", "dev", "--", "--port", str(port)],
            cwd=web_dir,
        )

    # Tarayıcıyı aç (sunucuların ayağa kalkması için bekle)
    if open_browser:
        time.sleep(2.5)
        webbrowser.open(f"http://localhost:{port}")

    # Ctrl+C ile ikisini birden temizce kapat
    def _shutdown(sig, frame):
        print("\n   Kapatılıyor...")
        backend.terminate()
        frontend.terminate()
        try:
            backend.wait(timeout=5)
            frontend.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend.kill()
            frontend.kill()
        sys.exit(0)

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    try:
        backend.wait()
    except KeyboardInterrupt:
        _shutdown(None, None)


def main() -> None:
    """CLI giriş noktası — `aot` komutu buraya gelir."""
    parser = argparse.ArgumentParser(
        prog="aot",
        description="Anvil of Taylor -- Taylor series expansion tool",
    )
    subparsers = parser.add_subparsers(dest="command")

    # aot launch
    launch_parser = subparsers.add_parser(
        "launch",
        help="Start the web UI (backend + frontend + browser)",
    )
    launch_parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not open the browser automatically",
    )
    launch_parser.add_argument(
        "--port",
        type=int,
        default=5173,
        help="Frontend port (default: 5173)",
    )

    args = parser.parse_args()

    if args.command == "launch":
        launch(open_browser=not args.no_browser, port=args.port)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
