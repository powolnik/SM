import sys
from src.ui.app import TUIApp

if __name__ == "__main__":
    char = sys.argv[1] if len(sys.argv) > 1 else "kai"
    app = TUIApp(char)
    app.run()
