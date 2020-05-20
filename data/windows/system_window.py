from PyQt5.QtWidgets import QHBoxLayout, QStackedWidget, QListWidget, QWidget

from data.case_forms.system_forms.numschemes_form import NumschemesForm
from data.case_forms.system_forms.transportprops_form import TransportPropsForm
from data.case_forms.system_forms.runtime_form import RuntimeForm
from data.case_forms.system_forms.solcontrol_form import SolcontrolForm
from data.case_forms.system_forms.turbulenceprops_form import TurbulencePropsForm


class SystemWindow(QWidget):

    def __init__(self):
        super(SystemWindow, self).__init__()

        self.vertex_num = 0


        self.leftlist = QListWidget()
        self.leftlist.setFixedWidth(150)

        self.leftlist.insertItem(0, 'Transport properties')
        self.leftlist.insertItem(1, 'Turbulence properties')
        self.leftlist.insertItem(2, 'Runtime control')
        self.leftlist.insertItem(3, 'Numerical schemes')
        self.leftlist.insertItem(4, 'Solution control')

        self.leftlist.currentRowChanged.connect(self.display)

        self.Stack = QStackedWidget(self)

        hbox = QHBoxLayout()
        hbox.addWidget(self.leftlist)
        hbox.addWidget(self.Stack)
        self.setLayout(hbox)


    def initialize(self):
        self.transportprops_form = TransportPropsForm()
        self.turbulenceprops_form = TurbulencePropsForm()
        self.runtime_form = RuntimeForm()
        self.numschemes_form = NumschemesForm()
        self.solcontrol_form = SolcontrolForm()

        self.Stack.addWidget(self.transportprops_form)
        self.Stack.addWidget(self.turbulenceprops_form)
        self.Stack.addWidget(self.runtime_form)
        self.Stack.addWidget(self.numschemes_form)
        self.Stack.addWidget(self.solcontrol_form)

    def display(self, i):
       self.Stack.setCurrentIndex(i)
