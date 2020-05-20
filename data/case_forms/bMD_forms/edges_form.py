from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QLabel, QSpinBox, \
    QFormLayout, QGroupBox, QPushButton, QScrollArea, QVBoxLayout, QComboBox, QGridLayout


class EdgesForm(QWidget):

   def __init__( self):
      super().__init__()

      self.blocks_edges = QVBoxLayout()
      self.blocks_edges.setAlignment(Qt.AlignVCenter | Qt.AlignTop)
      scroll_widget = QWidget()
      scroll_widget.setLayout(self.blocks_edges)
      scroll = QScrollArea()
      scroll.setWidget(scroll_widget)
      scroll.setWidgetResizable(True)

      layout = QVBoxLayout(self)
      layout.addWidget(scroll)

   def create_block_edges(self, edges):
       block_edges = BlockEdges(edges)
       self.blocks_edges.addWidget(block_edges)

class BlockEdges(QWidget):
    def __init__( self, edges):
      super().__init__()

      self.general_edges = edges

      layout = QVBoxLayout(self)
      block_edges = QGroupBox()
      layout.addWidget(block_edges)

      hbox = QHBoxLayout()
      hbox.setSpacing(50)
      hbox.addWidget(QLabel("Edge"))
      hbox.addWidget(QLabel("Inflection point"))

      self.edges_points_vbox = QVBoxLayout()
      self.edges_points_vbox.setSpacing(4)

      hbox_btn = QHBoxLayout()
      delete_btn = QPushButton("Delete last curved edge")
      add_btn = QPushButton("Add curved edge")
      delete_btn.clicked.connect(self.delete_edge)
      add_btn.clicked.connect(self.add_edge)
      hbox_btn.addWidget(delete_btn)
      hbox_btn.addWidget(add_btn)

      vbox = QVBoxLayout()
      block_edges.setLayout(vbox)
      vbox.addLayout(hbox)
      vbox.addLayout(self.edges_points_vbox)
      vbox.addLayout(hbox_btn)


    def set_edges(self, edges):
        keys = list(edges.keys())
        values = list(edges.values())

        count = len(edges)
        for i in range(0, count):
            self.add_edge()

        for i in range(0, self.edges_points_vbox.count()):
            item = self.edges_points_vbox.itemAt(i).widget().layout()
            edge = item.itemAt(0).widget()
            edge.setCurrentText(keys[i])
            point = item.itemAt(1).layout()
            point.itemAt(0).widget().setText(values[i][0])
            point.itemAt(1).widget().setText(values[i][1])
            point.itemAt(2).widget().setText(values[i][2])



    def add_edge(self):
        edge = QComboBox()
        edge_list = [str(item) for item in self.general_edges]
        edge.addItems(edge_list)

        point_hbox = QHBoxLayout()
        point_hbox.setSpacing(5)
        x = QLineEdit()
        y = QLineEdit()
        z = QLineEdit()
        x.setValidator(QDoubleValidator(-999999.0, 999999.0, 50))
        y.setValidator(QDoubleValidator(-999999.0, 999999.0, 50))
        z.setValidator(QDoubleValidator(-999999.0, 999999.0, 50))
        x.setCursorPosition(0)
        point_hbox.addWidget(x)
        point_hbox.addWidget(y)
        point_hbox.addWidget(z)

        edge_point_hbox = QHBoxLayout()
        edge_point_hbox.setSpacing(200)
        edge_point_hbox.addWidget(edge)
        edge_point_hbox.addLayout(point_hbox)

        widget = QWidget()
        widget.setLayout(edge_point_hbox)
        self.edges_points_vbox.addWidget(widget)

    def delete_edge(self):
         last_edges_points_num = self.edges_points_vbox.count()
         if last_edges_points_num == 0:
             return
         edges_points = self.edges_points_vbox.takeAt(last_edges_points_num - 1)
         edges_points.widget().deleteLater()

    def read_block_edgesGUIdata(self):
        edges_points_dict = {}
        for i in range(0, self.edges_points_vbox.count()):
            item = self.edges_points_vbox.itemAt(i).widget()
            edge_point_hbox = item.layout()
            edge = edge_point_hbox.itemAt(0).widget()
            edge = edge.currentText()

            point_hbox = edge_point_hbox.itemAt(1).layout()
            point_coords = []
            for c in range(0, point_hbox.count()):
                coord = point_hbox.itemAt(c).widget()
                coord = coord.text().replace(',', '.')
                point_coords.append(coord)
            point_coords = " ".join(point_coords)
            point_coords = "(" + point_coords + ")"
            edges_points_dict.update({edge : point_coords})
        return edges_points_dict

