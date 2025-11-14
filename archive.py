import sqlite3
from pathlib import Path
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class Archive(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("artwork-archive")
        self.setGeometry(100, 100, 500, 100)

        # - Initializing Database Section -
        datapath = Path("database/artworks.db")
        if datapath.exists():
            self.con = sqlite3.connect(datapath)
            self.cur = self.con.cursor()
            print("Database exists - connected to database")
        else:
            self.con = sqlite3.connect(datapath)
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
            print("Created sample raw")

        # -------- Table Section --------
        self.table = QTableWidget(self)
        # self.table.setMaximumWidth(1200)
        self.table.setColumnCount(6)
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 150)
        self.table.setColumnWidth(5, 150)
        self.table.setColumnWidth(6, 150)
        self.table.setHorizontalHeaderLabels(
            ["Author", "Title", "Size", "Medium", "Year", "Photo"]
        )

        self.tableUpdate()

        # -------- Input Section --------

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
        button_update_data.clicked.connect(self.tableUpdate)
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
        layout.addWidget(self.table)
        layout.addWidget(self.add_form)
        self.setLayout(layout)

    # --- Update QTable ---
    def tableUpdate(self):
        self.cur.execute("SELECT * FROM ARTWORKS")
        data = self.cur.fetchall()
        self.table.setRowCount(0)  # resetowanie tabeli
        for row, item in enumerate(data):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(item[0]))
            self.table.setItem(row, 1, QTableWidgetItem(item[1]))
            self.table.setItem(row, 2, QTableWidgetItem(item[2]))
            self.table.setItem(row, 3, QTableWidgetItem(item[3]))
            self.table.setItem(row, 4, QTableWidgetItem(item[4]))
            self.table.setItem(row, 5, QTableWidgetItem(item[5]))

    def addArtwork(self):
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

        self.author_line_edit.clear()
        self.title_line_edit.clear()
        self.size_line_edit.clear()
        self.medium_line_edit.clear()
        self.year_line_edit.clear()
        self.thumbnail_line_edit.clear()
        self.tableUpdate()
        print("New artwork added")


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
