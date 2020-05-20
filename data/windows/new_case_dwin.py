from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDesktopWidget, QPushButton, QHBoxLayout, QLabel, QLineEdit, \
    QVBoxLayout, QFileDialog, QDialog, QFormLayout, QDialogButtonBox

class NewCaseDialog(QDialog):
    new_case_dialog_signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setModal(True)
        vbox = QVBoxLayout()

        form = QFormLayout()

        self.case_name = QLineEdit("newCase")
        form.addRow("Case name", self.case_name)
        form.setSpacing(20)

        setdir_hbox = QHBoxLayout()
        self.case_dir = QLineEdit()
        dir_btn = QPushButton('...', self)
        dir_btn.clicked.connect(self.set_directory)
        setdir_hbox.addWidget(self.case_dir)
        setdir_hbox.addWidget(dir_btn)
        form.addRow("Case parent directory", setdir_hbox)

        buttonbox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)

        vbox.addLayout(form)
        vbox.addWidget(buttonbox)
        self.setLayout(vbox)

        self.setFixedSize(550, 350)
        self.center()
        self.setWindowTitle('Create case')

    def set_directory(self):
        dir = QFileDialog.getExistingDirectory(self,"Choose case parent directory","/home")
        self.case_dir.setText(dir)

    def accept(self):
        case_dirname = self.case_dir.text() + "/" + self.case_name.text() + "/"
        self.new_case_dialog_signal.emit(case_dirname)
        super().accept()


    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
