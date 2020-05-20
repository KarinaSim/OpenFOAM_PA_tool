import sys

from PyQt5.QtWidgets import QApplication, QHBoxLayout, QStackedWidget, QWidget, QListWidget

from data.case_forms.sHMD_forms.addLayersC_form import AddLayersControlsForm
from data.case_forms.sHMD_forms.castellatedMC_form import CastellatedMCForm
from data.case_forms.sHMD_forms.geometry_form import GeometryForm
from data.case_forms.sHMD_forms.meshQC_form import MeshQControlsForm
from data.case_forms.sHMD_forms.otherParams_form import OtherParamsForm
from data.case_forms.sHMD_forms.snapC_form import SnapControlsForm


class SHMDWindow(QWidget):

    def __init__(self, statusBar, bMD_tab):
        super(SHMDWindow, self).__init__()

        self.bMD_tab = bMD_tab

        self.statusBar = statusBar

        self.leftlist = QListWidget()
        self.leftlist.setFixedWidth(180)
        self.leftlist.insertItem(0, 'geometry')
        self.leftlist.insertItem(1, 'castellatedMeshControls')
        self.leftlist.insertItem(2, 'snapControls')
        self.leftlist.insertItem(3, 'addLayersControls')
        self.leftlist.insertItem(4, 'meshQualityControls')
        self.leftlist.insertItem(5, 'other params')

        self.leftlist.currentRowChanged.connect(self.display)


        self.Stack = QStackedWidget(self)

        self.geometry_form = None
        self.castellatedMC_form = None
        self.snapC_form = None
        self.addLayersC_form = None
        self.meshQC_form = None
        self.otherParams_form = None

        hbox = QHBoxLayout()
        hbox.addWidget(self.leftlist)
        hbox.addWidget(self.Stack)

        self.setLayout(hbox)

    def initialize(self):

        self.geometry_form = GeometryForm(self.statusBar)
        self.castellatedMC_form = CastellatedMCForm()
        self.snapC_form = SnapControlsForm()
        self.addLayersC_form = AddLayersControlsForm()
        self.meshQC_form = MeshQControlsForm()
        self.otherParams_form = OtherParamsForm()

        self.geometry_form.set_geometry_connections(self.castellatedMC_form)

        self.geometry_form.new_region_dialog.new_region_signal.connect(self.add_region)
        self.geometry_form.new_surface_dialog.new_surface_signal.connect(self.add_surface)
        self.geometry_form.del_surface_signal.connect(self.delete_surface)

        self.Stack.addWidget(self.geometry_form)
        self.Stack.addWidget(self.castellatedMC_form)
        self.Stack.addWidget(self.snapC_form)
        self.Stack.addWidget(self.addLayersC_form)
        self.Stack.addWidget(self.meshQC_form)
        self.Stack.addWidget(self.otherParams_form)


    def set_surfaces(self, surfaces, csurfaces):
        surface_count = len(surfaces)
        for i in range(0, surface_count):
            self.geometry_form.new_surface_signal_handler("")
            self.add_surface("")

        for item in range(0, self.geometry_form.surfaces.count()):
            surface = self.geometry_form.surfaces.itemAt(item).widget()
            surface.set_surface(surfaces[item])

        for item in range(0, self.castellatedMC_form.surfaces.count()):
            surface = self.castellatedMC_form.surfaces.itemAt(item).widget()
            surface.set_surface(csurfaces[item])

    def set_regions(self, regions, cregions):
        region_count = len(regions)
        for i in range(0, region_count):
            self.geometry_form.new_region_signal_handler("")
            self.add_region("")

        for item in range(0, self.geometry_form.regions.count()):
            region = self.geometry_form.regions.itemAt(item).widget()
            region.set_region(regions[item])

        for item in range(0, self.castellatedMC_form.regions.count()):
            region = self.castellatedMC_form.regions.itemAt(item).widget()
            region.set_region(cregions[item])


    def add_region(self, name):

        # current_region_num = self.geometry_form.regions.count()
        # current_region = self.geometry_form.regions.itemAt(current_region_num - 1).widget()
        #
        # current_region_name = current_region.name.text()

        self.castellatedMC_form.create_region(name)

    def add_surface(self, name):

        # current_region_num = self.geometry_form.regions.count()
        # current_region = self.geometry_form.regions.itemAt(current_region_num - 1).widget()
        #
        # current_region_name = current_region.name.text()
        #
        self.castellatedMC_form.create_surface(name)
        self.bMD_tab.initialconds_form.add_sHMD_surface(name)


    def delete_surface(self):
        self.bMD_tab.initialconds_form.delete_sHMD_surface()


    def display(self, i):
       self.Stack.setCurrentIndex(i)
