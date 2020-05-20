import sys

from PyQt5.QtWidgets import QApplication

from data.windows.start_window import StartWindow

if __name__ == '__main__':

    app = QApplication(sys.argv)
    start_win = StartWindow()
    start_win.show()
    sys.exit(app.exec_())
