import sqlite3
from pathlib import Path
from PySide6.QtCore import QSortFilterProxyModel, Qt, Signal
from PySide6.QtGui import (
    # QAction,
    # QImage,
    QIntValidator,
    QPixmap,
    QStandardItem,
    QStandardItemModel,
)

from PySide6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    # QMenu,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QTableView,
    QVBoxLayout,
    QWidget,
    QStatusBar,
)
from src.database.sample_data import three_valid_artworks


class Archive(QWidget):
    statusMessage = Signal(str)

    def __init__(self, datapath=None):
        super().__init__()

        self.setWindowTitle("artwork-archive")
        self.setGeometry(100, 100, 500, 100)

        # ---------------------------------
        # - Initializing Database Section -
        # ---------------------------------
        if datapath is None:
            self.datapath = Path("database/artworks.db")
        else:
            self.datapath = Path(datapath)

        if self.datapath.exists():
            self.con = sqlite3.connect(self.datapath)
            self.cur = self.con.cursor()
            self.statusMessage.emit("Connected to database!")
            print("Database exists - connected to database")
        else:
            self.con = sqlite3.connect(self.datapath)
            self.cur = self.con.cursor()
            self.cur.execute(
                "CREATE TABLE ARTWORKS(author, title, size, medium, year, thumbnail)"
            )
            self.statusMessage.emit("Created a new database!")
            print("Created a new database")

            data = three_valid_artworks

            self.cur.executemany("INSERT INTO ARTWORKS VALUES(?, ?, ?, ?, ?, ?)", data)
            self.con.commit()
            print("Created a sample row")
            self.con.close()

        # - Uploading database -
        self.con = sqlite3.connect(self.datapath)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM ARTWORKS")
        self.rows = cur.fetchall()
        self.headers = [d[0] for d in cur.description]
        self.con.close()

        # - Creating a model -
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(self.headers)
        self.thumbnail_column = self.headers.index("thumbnail")

        # # - Loading Model
        for row in self.rows:
            items = []
            for col_index, col_value in enumerate(row):
                if col_index == self.thumbnail_column:
                    item = QStandardItem()
                    # img_path = Path(col_value)
                    # pixmap = QPixmap(str(img_path))
                    # scaledpixmap = pixmap.scaledToHeight(
                    #     100, mode=Qt.TransformationMode.FastTransformation
                    # )
                    # item.setData(scaledpixmap, Qt.ItemDataRole.DecorationRole)
                    items.append(item)
                else:
                    items.append(QStandardItem(str(col_value)))
            self.model.appendRow(items)
        #
        # - Creating a QTableView -
        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.setSortingEnabled(True)
        self.table_view.setCornerButtonEnabled(False)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)

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
        #
        #     self.table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        #     self.table_view.customContextMenuRequested.connect(self.show_context_menu)
        #
        # def show_context_menu(self, position):
        #     index = self.table_view.indexAt(position)
        #
        #     if not index.isValid():
        #         return
        #
        #     self.clicked_row = index.row()
        #
        #     menu = QMenu(self.table_view)
        #
        #     edit_action = QAction("Edit", self)
        #     edit_action.triggered.connect(self.deleteArtwork)
        #     menu.addAction(edit_action)
        #     menu.exec(self.table_view.viewport().mapToGlobal(position))

        # ---------------------------------
        # ---------Filter Section----------
        # ---------------------------------
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setFilterKeyColumn(-1)  # searching all columns
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.sort(0, Qt.SortOrder.AscendingOrder)
        self.proxy_model.setSortCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
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
        thumbnail_label = QLabel("Image")

        # Validators
        self.yearValidator = QIntValidator(0, 2100)

        # Edits
        self.author_line_edit = QLineEdit()
        self.title_line_edit = QLineEdit()
        self.size_line_edit = QLineEdit()
        self.medium_line_edit = QLineEdit()
        self.year_line_edit = QLineEdit()
        self.year_line_edit.setValidator(self.yearValidator)

        # File Selection
        self.file_browse = QPushButton("Browse")
        self.file_browse.clicked.connect(self.openFileDialog)
        self.filename_edit = QLineEdit()

        # Bottom Buttons
        button_clearInput = QPushButton("Clear Input")
        button_clearInput.clicked.connect(self.clearInput)
        button_update_data = QPushButton("Remove artwork")
        button_update_data.clicked.connect(self.deleteArtwork)
        button_addArtwork = QPushButton("Add an artwork")
        button_addArtwork.clicked.connect(self.addArtwork)

        # ---------------------------------
        # ---------Layout Section----------
        # ---------------------------------

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
        h_layout06.addWidget(self.filename_edit)
        h_layout06.addWidget(self.file_browse)

        # Layout - Buttons
        h_layout07 = QHBoxLayout()
        h_layout07.addWidget(button_clearInput)
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
        layout.setStretch(1, 4)
        layout.setStretch(2, 1)
        layout.setStretch(3, 1)
        self.setLayout(layout)

        # ---------------------------------
        # ----------Keybindings------------
        # ---------------------------------
        # self.shortcut_delete = QShortcut(QKeySequence("Delete"), self.table_view)
        # self.shortcut_delete.activated.connect(self.deleteArtwork)
        # self.shortcut_save = QShortcut(QKeySequence("Ctrl+S"), self)
        # self.shortcut_save.activated.connect(self.saveArchive)
        # Stronger binding in the menu parametres

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
            self.filename_edit.text(),
        ]
        self.cur.execute(
            "INSERT INTO ARTWORKS VALUES(?, ?, ?, ?, ?, ?)", self.new_artwork
        )

        # Checking if title field is filled
        if not self.title_line_edit.text():
            self.statusMessage.emit("Title is required")
            self.con.close()
            raise ValueError("Title is required")

        # Checking if year is an integer
        if not self.year_line_edit.hasAcceptableInput():
            self.statusMessage.emit("Year must be a number")
            self.con.close()
            raise ValueError("Invalid year value")

        self.con.commit()

        row_items = []
        self.thumbnail_column = self.headers.index("thumbnail")
        for col_index, item_value in enumerate(self.new_artwork):
            if col_index == self.thumbnail_column:
                item = QStandardItem()
                img_path = Path("database") / item_value
                if img_path.exists():
                    pixmap = QPixmap(str(img_path))
                    if not pixmap.isNull():
                        scaledpixmap = pixmap.scaledToHeight(
                            100, mode=Qt.TransformationMode.FastTransformation
                        )
                        item.setData(scaledpixmap, Qt.ItemDataRole.DecorationRole)
                    row_items.append(item)
            else:
                row_items.append(QStandardItem(str(item_value)))
        self.model.appendRow(row_items)
        self.con.close()

        self.author_line_edit.clear()
        self.title_line_edit.clear()
        self.size_line_edit.clear()
        self.medium_line_edit.clear()
        self.year_line_edit.clear()
        self.filename_edit.clear()

        print("Artwork added!")
        self.statusMessage.emit("Artwork added!")

    def clearInput(self):
        self.author_line_edit.clear()
        self.title_line_edit.clear()
        self.size_line_edit.clear()
        self.medium_line_edit.clear()
        self.year_line_edit.clear()
        self.filename_edit.clear()
        self.statusMessage.emit("Input Cleared")

    def deleteArtwork(self):
        """A method that deletes an artwork"""
        self.con = sqlite3.connect(self.datapath)
        self.cur = self.con.cursor()
        indexes = self.table_view.selectionModel().selectedRows()
        index = indexes[0]
        source_index = self.proxy_model.mapToSource(index)
        row = source_index.row()
        self.model.removeRow(row)
        self.con.close()

        print("Artwork deleted successfully")
        self.statusMessage.emit("Artwork deleted")

    def saveArchive(self):
        """A method to save changes to database"""
        con = sqlite3.connect(self.datapath)
        cur = con.cursor()

        cur.execute("DELETE FROM ARTWORKS")
        for row in range(self.model.rowCount()):
            record = []
            for col in range(self.model.columnCount()):
                item = self.model.item(row, col)
                record.append(item.text() if item else None)

            cur.execute(
                "INSERT INTO ARTWORKS (author, title, size, medium, year, thumbnail) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                record,
            )
        con.commit()
        con.close()
        self.statusMessage.emit("Database saved!")
        print("Updated")

    def openFileDialog(self):
        filename, ok = QFileDialog.getOpenFileName(
            self, "Select a File", "/", "Images (*.jpg *png)"
        )
        if filename:
            path = Path(filename)
            self.filename_edit.setText(str(path))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.statusbar = QStatusBar()
        self.Widget = Archive()
        self.setCentralWidget(self.Widget)
        self.Widget.statusMessage.connect(self.statusbar.showMessage)
        self.menu()
        self.setStatusBar(self.statusbar)

    def menu(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("File")
        saveArchive = fileMenu.addAction("Save Archive", "CTRL+S")
        saveArchive.triggered.connect(self.Widget.saveArchive)
        pdfAction = fileMenu.addAction("Export PDF list")
        backupAction = fileMenu.addAction("Export a Backup File")
        exitAction = fileMenu.addAction("Exit and Save")
        exitAction.triggered.connect(self.Widget.saveArchive)
        exitAction.triggered.connect(self.close)
        editMenu = menubar.addMenu("Edit")
        addRow = editMenu.addAction("Add an Artwork", "CTRL+Return")
        addRow.triggered.connect(self.Widget.addArtwork)
        deleteRow = editMenu.addAction("Delete Row", "DEL")
        deleteRow.triggered.connect(self.Widget.deleteArtwork)
        aboutMenu = menubar.addMenu("About")
