import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QFormLayout, \
    QWidget, QVBoxLayout, QPushButton, QGroupBox, QScrollArea, QLineEdit

from data.case_forms.bMD_forms.new_block_dwin import BlockDialog


class BlocksForm(QWidget):
    def __init__(self, ):
        super(BlocksForm, self).__init__()

        self.vertex_generalnum = 0
        self.edges_generalnum = 0
        self.patches_generalnum = 0

        self.block_id = 0
        self.general_patches_list = []

        self.patches_form = None
        self.edges_form = None
        self.mergedpatches_form = None
        self.initialconds_form = None

        self.blocks = QVBoxLayout()
        self.blocks.setAlignment(Qt.AlignVCenter | Qt.AlignTop)

        scale_hbox = QHBoxLayout()
        scale_hbox.setSpacing(25)
        scale_hbox.addWidget(QLabel("Scaling factor"))
        self.scale = QLineEdit()
        self.scale.setValidator(QDoubleValidator(0.0, 999999, 50))
        scale_hbox.addWidget(self.scale)


        scroll_widget = QWidget()
        scroll_widget.setLayout(self.blocks)
        scroll = QScrollArea()
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)

        btn_hbox = QHBoxLayout()
        del_btn = QPushButton("Delete last block")
        del_btn.clicked.connect(self.delete_block)
        btn_hbox.addWidget(del_btn)
        add_btn = QPushButton("Add block")
        add_btn.clicked.connect(self.new_block)
        btn_hbox.addWidget(add_btn)

        layout = QVBoxLayout(self)
        layout.addLayout(scale_hbox)
        layout.addWidget(scroll)
        layout.addLayout(btn_hbox)

        self.new_block_dialog = BlockDialog()
        self.new_block_dialog.new_block_signal.connect(self.new_block_signal_handler)


    def set_vertex_list(self, vertices):
        vertices = [tuple(item) for item in vertices]
        old_hex_num = self.vertex_generalnum
        self.vertex_generalnum += 8
        labels = [l for l in range(old_hex_num, self.vertex_generalnum)]
        coords = vertices
        vertices =  dict(zip(labels, coords))
        return vertices


    def initialize(self, block):

        measure, shift, vertices, cells, ratios = block
        self.block_id += 1

        edges = self.get_edges(vertices)
        patches = self.get_patches(vertices)
        block = Block(self.block_id, measure, shift, vertices, edges, patches, cells, ratios)
        self.blocks.addWidget(block)
        self.general_patches_list = block.pnames


    def new_block(self):
       self.new_block_dialog.show()

    def new_block_signal_handler(self, measure, shift, cells, ratios):
        measure = [float(item.replace(',','.')) for item in measure]
        shift = [float(item.replace(',','.')) for item in shift]
        # cells = [int(item) for item in cells]
        # ratios = [float(item.replace(',','.')) for item in ratios]

        self.block_id += 1

        vertices = self.get_vertex_list(measure, shift)
        edges = self.get_edges(vertices)
        patches = self.get_patches(vertices)
        block = Block(self.block_id, measure, shift, vertices, edges, patches, cells, ratios)
        self.blocks.addWidget(block)

    def set_block(self, block):
        vertices, cells, ratios = block
        measure = [0, 0, 0]
        shift = [0, 0, 0]
        self.block_id += 1

        vertices = self.set_vertex_list(vertices)
        edges = self.get_edges(vertices)
        patches = self.get_patches(vertices)
        block = Block(self.block_id, measure, shift, vertices, edges, patches, cells, ratios)
        self.blocks.addWidget(block)

    def set_block_connections(self, patches_form, edges_form, mergedpatches_form, initialconds_form):
        self.patches_form = patches_form
        self.edges_form = edges_form
        self.mergedpatches_form = mergedpatches_form
        self.initialconds_form = initialconds_form

    def delete_block(self):

       last_block_num = self.blocks.count()
       if last_block_num == 1:
           return

       self.vertex_generalnum -= 8
       self.block_id -= 1

       for i in range(0, 6):
           self.general_patches_list.pop()

       self.blocks.takeAt(last_block_num - 1).widget().deleteLater()
       self.patches_form.blocks_patches.takeAt(last_block_num - 1).widget().deleteLater()
       self.edges_form.blocks_edges.takeAt(last_block_num - 1).widget().deleteLater()
       self.mergedpatches_form.merged_patches.takeAt(last_block_num - 2).widget().deleteLater()
       self.initialconds_form.blocks_pU.takeAt(last_block_num - 1).widget().deleteLater()


    def get_vertex_list(self, mesure, shift_vector):
        x, y, z = mesure
        v0 = v1 = v2 = v3 = v4 = v5 = v6 = v7 = []
        old_hex_num = self.vertex_generalnum
        self.vertex_generalnum += 8

        xx, yy, zz = shift_vector
        v0 = (0.0 + xx, 0.0 + yy, 0.0 + zz)
        v1 = (0.0 + xx,  y  + yy, 0.0 + zz)
        v2 = (0.0 + xx,  y  + yy,  z  + zz)
        v3 = (0.0 + xx, 0.0 + yy,  z  + zz)
        v4 = ( x  + xx, 0.0 + yy, 0.0 + zz)
        v5 = ( x  + xx,  y  + yy, 0.0 + zz)
        v6 = ( x + 0.0,  y  + yy,  z  + zz)
        v7 = ( x  + xx, 0.0 + yy,  z  + zz)
        labels = [l for l in range(old_hex_num, self.vertex_generalnum)]
        coords = [v0, v1, v2, v3, v4, v5, v6, v7]
        vertices =  dict(zip(labels, coords))
        return vertices

    def get_edges(self, vertices):
        self.edges_generalnum += 12
        v0, v1, v2, v3, v4, v5, v6, v7 = vertices
        e1 = (v0, v1)
        e2 = (v1, v2)
        e3 = (v2, v3)
        e4 = (v3, v0)

        e5 = (v4, v5)
        e6 = (v5, v6)
        e7 = (v6, v7)
        e8 = (v7, v4)

        e9 = (v0, v4)
        e10 = (v3, v7)
        e11 = (v5, v1)
        e12 = (v2, v6)

        edges = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12]
        edges = [str(e) for e in edges]
        edges = [re.sub(r"[(,)]","", e) for e in edges]
        return edges

    def get_patches(self, vertices):
        self.patches_generalnum += 6
        v0, v1, v2, v3, v4, v5, v6, v7 = vertices
        f1 = (v0, v1, v2, v3)
        f2 = (v4, v5, v6, v7)
        f3 = (v4, v0, v3, v7)
        f4 = (v5, v1, v2, v6)
        f5 = (v4, v5, v1, v0)
        f6 = (v7, v6, v2, v3)
        faces = [f1, f2, f3, f4, f5, f6]
        faces = [str(e) for e in faces]
        faces = [re.sub(r",","", e) for e in faces]
        return faces



class Block(QWidget):
    def __init__(self, id, measure, shift, vertices, edges, patches, cells, ratios):
        super(Block, self).__init__()

        self.block_id = id

        self.edges = edges
        self.patches = patches

        p1name = "Backpatch" + str(self.block_id)
        p2name = "Frontpatch" + str(self.block_id)
        p3name = "Leftpatch" + str(self.block_id)
        p4name = "Rightpatch" + str(self.block_id)
        p5name = "Bottompatch" + str(self.block_id)
        p6name = "Toppatch" + str(self.block_id)

        self.pnames = [p1name, p2name, p3name, p4name, p5name, p6name]

        self.vertices = vertices
        self.cells = cells
        self.ratios = ratios

        self.new_vertices_coords = []

        layout = QVBoxLayout(self)
        block = QGroupBox()
        layout.addWidget(block)
        inner_vbox = QVBoxLayout()
        inner_vbox.setAlignment(Qt.AlignVCenter | Qt.AlignTop)
        block.setLayout(inner_vbox)

        measure = [str(item) for item in measure]
        shift = [str(item) for item in shift]

        measure_hbox = QHBoxLayout()
        measure_hbox.setSpacing(60)
        inner_vbox.addLayout(measure_hbox)
        measure_hbox.addWidget(QLabel("Measurements"))
        self.mx = QLineEdit()
        self.mx.setValidator(QDoubleValidator(0.0, 999999.0, 50))
        self.mx.setText(measure[0])
        self.my = QLineEdit()
        self.my.setValidator(QDoubleValidator(0.0, 999999.0, 50))
        self.my.setText(measure[1])
        self.mz = QLineEdit()
        self.mz.setValidator(QDoubleValidator(0.0, 999999.0, 50))
        self.mz.setText(measure[2])
        measure_hbox.addWidget(self.mx)
        measure_hbox.addWidget(self.my)
        measure_hbox.addWidget(self.mz)

        shift_hbox = QHBoxLayout()
        shift_hbox.setSpacing(85)
        inner_vbox.addLayout(shift_hbox)
        shift_hbox.addWidget(QLabel("Shift vector"))
        self.sx = QLineEdit()
        self.sx.setValidator(QDoubleValidator(-999999.0, 999999.0, 50))
        self.sx.setText(shift[0])
        self.sy = QLineEdit()
        self.sy.setValidator(QDoubleValidator(-999999.0, 999999.0, 50))
        self.sy.setText(shift[1])
        self.sz = QLineEdit()
        self.sz.setValidator(QDoubleValidator(-999999.0, 999999.0, 50))
        self.sz.setText(shift[2])
        shift_hbox.addWidget(self.sx)
        shift_hbox.addWidget(self.sy)
        shift_hbox.addWidget(self.sz)


        vertices_gbox = QGroupBox()
        self.form = QFormLayout()
        vertices_gbox.setLayout(self.form)
        self.form.setContentsMargins(20, 0, 0, 0)
        self.form.setHorizontalSpacing(100)
        self.form.setAlignment(Qt.AlignCenter)
        self.form.setVerticalSpacing(2)
        inner_vbox.addWidget(vertices_gbox)

        hbox = QHBoxLayout()
        hbox.setSpacing(50)
        hbox.addWidget(QLabel("X"))
        hbox.addWidget(QLabel("Y"))
        hbox.addWidget(QLabel("Z"))
        self.form.addRow("Label", hbox)
        keys = self.vertices.keys()
        for k in keys:
            coords = self.vertices[k]
            coords = [str(item) for item in coords]
            x = QLineEdit()
            x.setValidator(QDoubleValidator(-999999.0, 999999.0, 50))
            x.setText(coords[0])
            y = QLineEdit()
            y.setValidator(QDoubleValidator(-999999.0, 999999.0, 50))
            y.setText(coords[1])
            z = QLineEdit()
            z.setValidator(QDoubleValidator(-999999.0, 999999.0, 50))
            z.setText(coords[2])
            hbox = QHBoxLayout()
            hbox.setSpacing(25)
            hbox.addWidget(x)
            hbox.addWidget(y)
            hbox.addWidget(z)
            self.form.addRow(str(k), hbox)

        chbox = QHBoxLayout()
        chbox.setSpacing(50)
        inner_vbox.addLayout(chbox)
        chbox.addWidget(QLabel("Number of cells"))
        # cells = [str(item) for item in cells]
        self.cx = QLineEdit()
        self.cx.setValidator(QIntValidator(0, 999999))
        self.cx.setText(cells[0])
        self.cy = QLineEdit()
        self.cy.setValidator(QIntValidator(0, 999999))
        self.cy.setText(cells[1])
        self.cz = QLineEdit()
        self.cz.setValidator(QIntValidator(0, 999999))
        self.cz.setText(cells[2])
        chbox.addWidget(self.cx)
        chbox.addWidget(self.cy)
        chbox.addWidget(self.cz)


        rhbox = QHBoxLayout()
        rhbox.setSpacing(20)
        inner_vbox.addLayout(rhbox)
        rhbox.addWidget(QLabel("Cell expansion ratios"))
        # ratios = [str(item) for item in ratios]
        self.rx = QLineEdit()
        self.rx.setValidator(QDoubleValidator(0.0, 999999.0, 50))
        self.rx.setText(ratios[0])
        self.ry = QLineEdit()
        self.ry.setValidator(QDoubleValidator(0.0, 999999.0, 50))
        self.ry.setText(ratios[1])
        self.rz = QLineEdit()
        self.rz.setValidator(QDoubleValidator(0.0, 999999.0, 50))
        self.rz.setText(ratios[2])
        rhbox.addWidget(self.rx)
        rhbox.addWidget(self.ry)
        rhbox.addWidget(self.rz)


        update_btn = QPushButton("update coords")
        update_btn.clicked.connect(self.update)
        inner_vbox.addWidget(update_btn)

        self.show()

    def get_vertex_coords_list(self, mesure, shift_vector):
       mesure = [float(item.replace(',','.')) for item in mesure]
       shift_vector = [float(item.replace(',','.')) for item in shift_vector]
       x, y, z = mesure
       v0 = v1 = v2 = v3 = v4 = v5 = v6 = v7 = []
       xx, yy, zz = shift_vector
       v0 = (0.0 + xx, 0.0 + yy, 0.0 + zz)
       v1 = (0.0 + xx,  y  + yy, 0.0 + zz)
       v2 = (0.0 + xx,  y  + yy,  z  + zz)
       v3 = (0.0 + xx, 0.0 + yy,  z  + zz)
       v4 = ( x  + xx, 0.0 + yy, 0.0 + zz)
       v5 = ( x  + xx,  y  + yy, 0.0 + zz)
       v6 = ( x  + xx,  y  + yy,  z  + zz)
       v7 = ( x  + xx, 0.0 + yy,  z  + zz)
       coords = [v0, v1, v2, v3, v4, v5, v6, v7]
       return coords


    def update(self):
        mx = self.mx.text()
        my = self.my.text()
        mz = self.mz.text()
        new_measure = [mx, my, mz]

        sx = self.sx.text()
        sy = self.sy.text()
        sz = self.sz.text()
        new_shift = [sx, sy, sz]
        new_vertices_coords = self.get_vertex_coords_list(new_measure, new_shift)

        for row in range(1, self.form.rowCount()):
            item = [str(i) for i in new_vertices_coords[row - 1]]
            hbox = self.form.itemAt(row, 1).layout()
            for vertex in range(0, hbox.count()):
                new_coord = hbox.itemAt(vertex).widget()
                new_coord.setText(item[vertex])

        labels = self.vertices.keys()
        self.vertices =  dict(zip(labels, new_vertices_coords))
        self.cells = [self.cx.text(), self.cy.text(), self.cz.text()]
        # self.cells = [float(item) for item in self.cells]
        self.ratios = [self.rx.text(), self.ry.text(), self.rz.text()]
        # self.ratios = [float(item) for item in self.ratios]


    def read_blockGUIdata(self):
        vertices= self.vertices
        keys = vertices.keys()
        keys = [str(k) for k in keys]
        keys = " ".join(keys)
        keys = "(" + keys + ")"

        values = vertices.values()
        values = [str(v) for v in values]
        values = [re.sub(r",", "", v) for v in values]

        cells = [self.cx.text(), self.cy.text(), self.cz.text()]
        # cells = [str(c) for c in cells]
        cells = " ".join(cells)
        cells = "(" + cells + ")"

        ratios = [self.rx.text().replace(',', '.'), self.ry.text().replace(',', '.'), self.rz.text().replace(',', '.')]
        # ratios = [str(r) for r in ratios]
        ratios = " ".join(ratios)
        ratios = "(" + ratios + ")"

        return [keys, values, cells, ratios]


