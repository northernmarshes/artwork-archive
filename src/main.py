from PySide6.QtWidgets import QApplication
import sys
from archive import MainWindow
from pathlib import Path

app = QApplication(sys.argv)

style_file = Path("styles/gray-theme.qss")
with open(style_file, "r", encoding="utf-8") as f:
    app.setStyleSheet(f.read())


main = MainWindow()
main.show()

app.exec()
