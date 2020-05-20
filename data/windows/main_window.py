import os
import signal
import subprocess

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QTabWidget, QAction, QDockWidget, \
    QPlainTextEdit, QMessageBox

from data.windows.bMD_window import BMDWindow
from libs.caseDB_loader import CaseDBLoader
from libs.caseDB_saver import CaseDBSaver
from libs.case_saver import CaseSaver
from data.windows.sHMD_window import SHMDWindow
from data.windows.system_window import SystemWindow


class MainWindow(QMainWindow):

    def __init__(self, flag, case_dirname):
        super(MainWindow, self).__init__()

        self.case_dirname = case_dirname

        self.statusBar().setFixedHeight(60)

        self.run_bM_flag = False
        self.run_sHM_flag = False
        self.proc = None

        save_case_action = QAction('Save in dir', self)
        save_case_action.setShortcut('Ctrl+S')
        save_case_action.triggered.connect(self.save_case)

        savedb_case_action = QAction('Save in DB', self)
        savedb_case_action.triggered.connect(self.savedb_case)

        del_sHMDict_action = QAction("Del sHMDict", self)
        del_sHMDict_action.triggered.connect(self.del_sHMDict)

        add_sHMDict_action = QAction("Add sHMDict", self)
        add_sHMDict_action.triggered.connect(self.add_sHMDict)

        run_blockMesh_action = QAction("Run blockMesh", self)
        run_blockMesh_action.triggered.connect(self.run_blockMesh)

        run_snappyHexMesh_action = QAction("Run snappyHexMesh", self)
        run_snappyHexMesh_action.triggered.connect(self.run_snappyHexMesh)

        run_simpleFoam_action = QAction("Run simpleFoam", self)
        run_simpleFoam_action.triggered.connect(self.run_simpleFoam)

        clean_case_action = QAction("Clean case", self)
        clean_case_action.triggered.connect(self.clean_case)

        stop_command_action = QAction('Stop command', self)
        stop_command_action.triggered.connect(self.stop_command)

        run_paraView_action = QAction('Run paraView', self)
        run_paraView_action.triggered.connect(self.run_paraView)

        self.toolbar = self.addToolBar('Case commands')
        self.toolbar.addAction(save_case_action)
        self.toolbar.addAction(savedb_case_action)

        self.toolbar.addAction(del_sHMDict_action)
        self.toolbar.addAction(add_sHMDict_action)

        self.toolbar.addAction(run_blockMesh_action)
        self.toolbar.addAction(run_snappyHexMesh_action)
        self.toolbar.addAction(run_simpleFoam_action)

        self.toolbar.addAction(clean_case_action)
        self.toolbar.addAction(stop_command_action)
        self.toolbar.addAction(run_paraView_action)


        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)


        if flag == "new":
            self.new_case()
        else:
            self.open_case(case_dirname)

        self.dock_widget = QDockWidget("Command output", self)
        self.dock_widget.setBaseSize(800, 900)

        self.plain_text_edit = QPlainTextEdit()
        self.plain_text_edit.setReadOnly(True)
        self.dock_widget.setWidget(self.plain_text_edit)

        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)
        self.resize(1700, 900)
        self.setWindowTitle("OpenFOAM_PA_tool: " + case_dirname)
        self.center()
        self.show()

    def new_case(self):

        measure = [1, 1, 1]
        shift = [0, 0, 0]
        cells = ["20", "20", "20"]
        ratios = ["1", "1", "1"]
        vertices = []
        block = [measure, shift, vertices, cells, ratios]
        self.bMD_tab = BMDWindow()
        scale = "1"
        self.bMD_tab.initialize("new", scale, block)

        self.system_tab = SystemWindow()
        self.system_tab.initialize()

        self.tabs.insertTab(0, self.bMD_tab, "bMD setup")
        self.tabs.insertTab(1, self.system_tab, "system setup")

    def open_case(self, case_dirname):

        loader = CaseDBLoader(case_dirname, self.statusBar())

        self.bMD_tab, self.system_tab, self.sHMD_tab = loader.set_tabs()

        self.tabs.insertTab(0, self.bMD_tab, "bMD setup")
        self.tabs.insertTab(1, self.system_tab, "System setup")

        if self.sHMD_tab is not None:
            self.tabs.insertTab(2, self.sHMD_tab, "sHMD setup")

    def clean_case(self):
        exist_flag = self.check_dir_existing(self.case_dirname)
        if exist_flag == "False":
            self.statusBar().showMessage("Clearning case error! Case " + self.case_dirname + " does not exist!", 8000)
        else:
            output = subprocess.run(["bash", "/home/karina/PycharmProjects/OpenFOAM_PA_tool/bin/clean_case"],
                                    cwd = self.case_dirname, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out = output.stdout.decode('utf-8')
            err = output.stderr.decode('utf-8')
            if err != '':
                self.statusBar().showMessage("Cleaning case error: " + err, 8000)
            else:
                self.statusBar().showMessage("Case " + self.case_dirname + " was successfully cleared", 5000)


    def save_case(self):
        sHMD_tab = None
        if self.tabs.count() == 3:
            sHMD_tab = self.tabs.widget(2)
        CaseSaver(self.statusBar(), self.case_dirname, self.bMD_tab, self.system_tab, sHMD_tab)

    def savedb_case(self):
        sHMD_tab = None
        if self.tabs.count() == 3:
            sHMD_tab = self.tabs.widget(2)
        CaseDBSaver(self.statusBar(), self.case_dirname, self.bMD_tab, self.system_tab, sHMD_tab)

    def del_sHMDict(self):
        if self.tabs.count() == 2:
            return
        self.tabs.removeTab(2)
        self.bMD_tab.initialconds_form.delete_surfaces_form()
        self.statusBar().showMessage("snappyHexMeshDict form was deleted", 4000)

    def add_sHMDict(self):
        if self.tabs.count() == 3:
            return
        else:
            self.sHMD_tab = SHMDWindow(self.statusBar(), self.bMD_tab)
            self.sHMD_tab.initialize()
            self.tabs.insertTab(2, self.sHMD_tab, "sHMD setup")
            self.statusBar().showMessage("snappyHexMeshDict form was added", 4000)


    def check_dir_existing(self, case_dirname):
        output = subprocess.run(["bash", "/home/karina/PycharmProjects/OpenFOAM_PA_tool/bin/check_direxist", case_dirname],
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = output.stdout.decode("utf-8").rstrip()
        return out


    def check_snappy_existing(self):
        path = self.case_dirname + "system/snappyHexMeshDict"
        output = subprocess.run(["bash", "/home/karina/PycharmProjects/OpenFOAM_PA_tool/bin/check_snappy_exist", path],
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = output.stdout.decode("utf-8").rstrip()
        return out



    def run_command(self, param):

        self.statusBar().showMessage("Run " + param)
        self.proc = subprocess.Popen(["bash", "/home/karina/PycharmProjects/OpenFOAM_PA_tool/bin/run_command", param], cwd = self.case_dirname,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, preexec_fn=os.setsid)

        out = self.proc.stdout.read()
        err = self.proc.stderr.read()
        output = out + err
        if self.dock_widget.isHidden():
            self.dock_widget.show()
        self.dock_widget.setWindowTitle(param + " output")
        self.plain_text_edit.setPlainText(output)


        if err == '':
            self.statusBar().showMessage(param + " was successfully completed", 8000)
        else:
            self.statusBar().showMessage(param + " execution error: " + err, 8000)

    def run_blockMesh(self):
        exist_flag = self.check_dir_existing(self.case_dirname)
        if exist_flag == "False":
            self.statusBar().showMessage("blockMesh was not executed! Save case to directory!", 8000)
        else:
            self.statusBar().showMessage("Run blockMesh", 2000)
            self.run_command("blockMesh")
            self.run_bM_flag = True


    def run_snappyHexMesh(self):
        exist_flag = self.check_snappy_existing()
        if self.run_bM_flag == 'False':
            self.statusBar().showMessage("snappyHexMesh was not executed! First run blockMesh!", 8000)
        else:
            if exist_flag == "False":
                self.statusBar().showMessage("snappyHexMesh was not executed! Save snappyHexMeshDict file to directory!", 8000)
            else:
                self.statusBar().showMessage("Run snappyHexMesh", 2000)
                self.run_command("snappyHexMesh")
                self.run_sHM_flag = True

    def stop_command(self):

        # if self.proc is None:
        #     self.statusBar().showMessage("No command is running", 2000)
        # else:
        #     try:
        #         print("kill")
        os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
        self.statusBar().showMessage("Command execution stopped", 5000)
            # except:
            #     self.statusBar().showMessage("Stop command error", 5000)
            #     print("stop")


    def run_simpleFoam(self):
        dir_exist_flag = self.check_dir_existing(self.case_dirname)
        snap_exist_flag = self.check_snappy_existing()
        if (dir_exist_flag == "True" and self.run_bM_flag is True) or (snap_exist_flag == "True" and self.run_sHM_flag is True):
            self.statusBar().showMessage("Run simpleFoam", 2000)
            self.run_command("simpleFoam")
        else:
            self.statusBar().showMessage("simpleFoam was not executed! First run blockMesh or snappyHexMesh!", 8000)


    def run_paraView(self):

        if self.run_bM_flag is True or self.run_sHM_flag is True:
            self.statusBar().showMessage("Run paraView", 2000)
            output = subprocess.run(["bash", "/home/karina/PycharmProjects/OpenFOAM_PA_tool/bin/run_command", "paraFoam"], cwd = self.case_dirname,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            self.statusBar().showMessage("paraView is not running! First run blockMesh or snappyHexMesh!", 8000)


    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Window Close',
            "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
