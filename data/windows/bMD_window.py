from PyQt5.QtWidgets import QHBoxLayout, QStackedWidget, QWidget, QListWidget

from data.case_forms.bMD_forms.blocks_form import BlocksForm
from data.case_forms.bMD_forms.edges_form import EdgesForm
from data.case_forms.bMD_forms.initialconds_form import InitialCondsForm
from data.case_forms.bMD_forms.mergedpatches_form import MergedPatchesForm
from data.case_forms.bMD_forms.patches_form import PatchesForm



class BMDWindow(QWidget):

    def __init__(self):
        super(BMDWindow, self).__init__()

        self.vertex_num = 0

        self.leftlist = QListWidget()
        self.leftlist.setFixedWidth(150)
        self.leftlist.insertItem(0, 'blocks')
        self.leftlist.insertItem(1, 'boundary conditions')
        self.leftlist.insertItem(2, 'curved edges')
        self.leftlist.insertItem(3, 'merged patch pairs')
        self.leftlist.insertItem(4, 'Initial conditions')

        self.leftlist.currentRowChanged.connect(self.display)

        self.Stack = QStackedWidget(self)
        self.blocks_form = None
        self.patches_form = None
        self.initialconds_form = None
        self.edges_form = None
        self.mergedpatches_form = None

        hbox = QHBoxLayout()
        hbox.addWidget(self.leftlist)
        hbox.addWidget(self.Stack)
        self.setLayout(hbox)

    def initialize(self, flag, scale, block):
        self.blocks_form = BlocksForm()
        self.blocks_form.scale.setText(scale)
        measure, shift, vertices, cells, ratios = block
        if flag == "new":
            vertices = self.blocks_form.get_vertex_list(measure, shift)
        else:
            vertices = self.blocks_form.set_vertex_list(vertices)

        block = [measure, shift, vertices, cells, ratios]
        self.blocks_form.initialize(block)

        block = self.blocks_form.blocks.itemAt(0).widget()
        patches = block.patches
        pnames = block.pnames

        self.initialconds_form = InitialCondsForm()
        block_pU = self.initialconds_form.create_block_pU(pnames)

        self.patches_form = PatchesForm()
        self.patches_form.create_block_patches(pnames, block_pU, patches)

        self.blocks_form.new_block_dialog.new_block_signal.connect(self.add_block)

        self.edges_form = EdgesForm()
        edges = block.edges
        self.edges_form.create_block_edges(edges)

        self.mergedpatches_form = MergedPatchesForm()

        self.blocks_form.set_block_connections(self.patches_form, self.edges_form,
                                               self.mergedpatches_form, self.initialconds_form)

        self.Stack.addWidget(self.blocks_form)
        self.Stack.addWidget(self.patches_form)
        self.Stack.addWidget(self.edges_form)
        self.Stack.addWidget(self.mergedpatches_form)
        self.Stack.addWidget(self.initialconds_form)


    def set_patchestypes(self, patchestypes):
        current_block_num = self.blocks_form.blocks.count()
        current_block_patches = self.blocks_form.patches_form.blocks_patches.itemAt(current_block_num - 1).widget()
        current_block_patches.set_types(patchestypes)

    def set_edges(self, edges):
        current_block_num = self.blocks_form.blocks.count()
        current_block_edges = self.blocks_form.edges_form.blocks_edges.itemAt(current_block_num - 1).widget()
        current_block_edges.set_edges(edges)

    def set_mergedPatches(self, mergedPatches):
        current_block_num = self.blocks_form.blocks.count()
        current_block_merged_patches = self.blocks_form.mergedpatches_form.merged_patches.itemAt(current_block_num - 2).widget()
        current_block_merged_patches.set_mergedPatches(mergedPatches)

    def set_initialconds(self, p_boundaryField, U_boundaryField):
        current_block_num = self.blocks_form.blocks.count()
        current_block_initconds = self.blocks_form.initialconds_form.blocks_pU.itemAt(current_block_num - 1).widget()
        current_block_initconds.set_initialconds(p_boundaryField, U_boundaryField)

    def add_block(self, measure, shift, cells, ratios):

        current_block_num = self.blocks_form.blocks.count()
        current_block = self.blocks_form.blocks.itemAt(current_block_num - 1).widget()
        current_block_patches = current_block.patches
        current_block_pnames = current_block.pnames

        block_pU = self.initialconds_form.create_block_pU(current_block_pnames)

        self.patches_form.create_block_patches(current_block_pnames, block_pU, current_block_patches)

        current_block_edges = current_block.edges
        self.edges_form.create_block_edges(current_block_edges)

        self.mergedpatches_form.create_merged_patches(current_block_pnames, self.blocks_form.general_patches_list)
        self.blocks_form.general_patches_list.extend(current_block_pnames)

    def display(self, i):
       self.Stack.setCurrentIndex(i)
