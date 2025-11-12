from PySide6.QtWidgets import QApplication
import sys
from archive import MainWindow

app = QApplication(sys.argv)

main = MainWindow()
main.show()

app.exec()
