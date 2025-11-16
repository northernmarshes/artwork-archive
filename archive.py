import sqlite3
from pathlib import Path
from PySide6.QtCore import QSortFilterProxyModel, Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel

from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMenu,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QTableView,
    QVBoxLayout,
    QWidget,
)


class Archive(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("artwork-archive")
        self.setGeometry(100, 100, 500, 100)

        # ---------------------------------
        # - Initializing Database Section -
        # ---------------------------------

        self.datapath = Path("database/artworks.db")
        if self.datapath.exists():
            self.con = sqlite3.connect(self.datapath)
            self.cur = self.con.cursor()
            print("Database exists - connected to database")
        else:
            self.con = sqlite3.connect(self.datapath)
            self.cur = self.con.cursor()
            self.cur.execute(
                "CREATE TABLE ARTWORKS(author, title, size, medium, year, thumbnail)"
            )
            print("Created database")

            data = [
                ("Edna Baud", "Throne of Dust", "200cm", "Steel", "2025", "thumb.jpg"),
            ]
            self.cur.executemany("INSERT INTO ARTWORKS VALUES(?, ?, ?, ?, ?, ?)", data)
            self.con.commit()
            print("Created sample row")
            self.con.close()

        # - Uploading database -
        self.con = sqlite3.connect(self.datapath)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM ARTWORKS")
        self.rows = cur.fetchall()
        self.headers = [d[0] for d in cur.description]
        self.con.close()
        print(self.rows)
        print(self.headers)

        # - Creating a model -
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(self.headers)

        for row in self.rows:
            items = [QStandardItem(str(col)) for col in row]
            self.model.appendRow(items)

        # - Creating a QTableView -
        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        # - Headers -text
        self.horizontal_header = self.table_view.horizontalHeader()
        self.vertical_header = self.table_view.verticalHeader()
        self.horizontal_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.vertical_header.setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.horizontal_header.setStretchLastSection(True)

        self.main_layout = QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        size.setHorizontalStretch(1)
        self.table_view.setSizePolicy(size)
        self.main_layout.addWidget(self.table_view)

        # ------ Context Menu ------

        # self.table_view.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.table_view.customContextMenuRequested.connect(self.showContextMenu)

        # self.table_view.context_menu = QMenu(self)
        # action1 = self.table_view.context_menu.addAction("action1")

        # def contextMenuEvent(self, event):
        # self.table_view.context_menu.exec(event.globalPos())

        # def contextMenuEvent(self, event):
        #     """Custom context menu logic"""
        #     if self.table_view.underMouse():
        #         self.contextMenu = QMenu(self)
        #
        #
        #
        #         deleteAction = QAction("Delete", self)
        #         self.contextMenu.addAction(deleteAction)
        #         deleteAction.triggered.connect(self.deleteArtwork)
        #         self.contextMenu.popup(QCursor.pos())

        # ---------------------------------
        # ---------Filter Section----------
        # ---------------------------------
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setFilterKeyColumn(-1)  # searching all columns
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.sort(0, Qt.SortOrder.AscendingOrder)
        self.table_view.setModel(self.proxy_model)
        self.searchbar = QLineEdit()
        self.searchbar.textChanged.connect(self.proxy_model.setFilterFixedString)

        # ---------------------------------
        # --------- Input Section ---------
        # ---------------------------------

        # Labels
        author_label = QLabel("Author")
        title_label = QLabel("Title")
        size_label = QLabel("Size")
        medium_label = QLabel("Medium")
        year_label = QLabel("Year")
        thumbnail_label = QLabel("Thumbnail")

        # Edits
        self.author_line_edit = QLineEdit()
        self.title_line_edit = QLineEdit()
        self.size_line_edit = QLineEdit()
        self.medium_line_edit = QLineEdit()
        self.year_line_edit = QLineEdit()
        self.thumbnail_line_edit = QLineEdit()

        # Bottom Buttons
        button_update_data = QPushButton("Update")
        # button_update_data.clicked.connect(self.tableUpdate)
        button_addArtwork = QPushButton("Add an artwork")
        button_addArtwork.clicked.connect(self.addArtwork)

        # Layout - Author
        h_layout01 = QHBoxLayout()
        h_layout01.addWidget(author_label)
        h_layout01.addWidget(self.author_line_edit)

        # Layout - Title
        h_layout02 = QHBoxLayout()
        h_layout02.addWidget(title_label)
        h_layout02.addWidget(self.title_line_edit)

        # Layout - Size
        h_layout03 = QHBoxLayout()
        h_layout03.addWidget(size_label)
        h_layout03.addWidget(self.size_line_edit)

        # Layout - Medium
        h_layout04 = QHBoxLayout()
        h_layout04.addWidget(medium_label)
        h_layout04.addWidget(self.medium_line_edit)

        # Layout - Year
        h_layout05 = QHBoxLayout()
        h_layout05.addWidget(year_label)
        h_layout05.addWidget(self.year_line_edit)

        # Layout - Thumbnail
        h_layout06 = QHBoxLayout()
        h_layout06.addWidget(thumbnail_label)
        h_layout06.addWidget(self.thumbnail_line_edit)

        # Layout - Thumbnail
        h_layout07 = QHBoxLayout()
        h_layout07.addWidget(button_update_data)
        h_layout07.addWidget(button_addArtwork)

        # Grouping elements
        self.add_form = QGroupBox()

        # Layout of the form
        form_layout = QVBoxLayout()
        form_layout.addLayout((h_layout01))
        form_layout.addLayout((h_layout02))
        form_layout.addLayout((h_layout03))
        form_layout.addLayout((h_layout04))
        form_layout.addLayout((h_layout05))
        form_layout.addLayout((h_layout06))
        form_layout.addLayout((h_layout07))
        self.add_form.setLayout(form_layout)

        # Displaying
        layout = QVBoxLayout()
        layout.addWidget(self.searchbar)
        layout.addWidget(self.table_view)
        layout.addWidget(self.add_form)
        self.setLayout(layout)

    def addArtwork(self):
        """A method to add an artwork to the base"""
        self.con = sqlite3.connect(self.datapath)
        self.cur = self.con.cursor()
        self.new_artwork = [
            self.author_line_edit.text(),
            self.title_line_edit.text(),
            self.size_line_edit.text(),
            self.medium_line_edit.text(),
            self.year_line_edit.text(),
            self.thumbnail_line_edit.text(),
        ]
        print(self.new_artwork)
        self.cur.execute(
            "INSERT INTO ARTWORKS VALUES(?, ?, ?, ?, ?, ?)", self.new_artwork
        )
        self.con.commit()

        # Adding new row without updating
        row_items = [QStandardItem(str(item)) for item in self.new_artwork]
        self.model.appendRow(row_items)

        # Scrolling to bottom of the list
        self.table_view.scrollToBottom()

        self.author_line_edit.clear()
        self.title_line_edit.clear()
        self.size_line_edit.clear()
        self.medium_line_edit.clear()
        self.year_line_edit.clear()
        self.thumbnail_line_edit.clear()

        print("New artwork added")

    # def deleteArtwork(self):
    #     """A method that deletes an artwork"""
    #     self.con = sqlite3.connect(self.datapath)
    #     self.cur = self.con.cursor()
    #     self.model.removeRow(self.clicked_row)
    #     self.table_view.scrollToBottom()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        Widget = Archive()
        self.setCentralWidget(Widget)
        self.menu()

    def menu(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("File")
        pdfAction = fileMenu.addAction("Export pdf list")
        backupAction = fileMenu.addAction("Export backup file")
        exitAction = fileMenu.addAction("Exit")
        exitAction.triggered.connect(self.close)
        editMenu = menubar.addMenu("Edit")
        aboutMenu = menubar.addMenu("About")
