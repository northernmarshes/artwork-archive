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
    QVBoxLayout,
    QWidget,
)


class Archive(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("artwork-archive")
        self.setGeometry(100, 100, 500, 100)

        # Initializing database
        datafile = Path("database/artworks.db")
        if datafile.exists():
            print("Database exists - did nothing")
            pass
        else:
            self.con = sqlite3.connect("database/artworks.db")
            self.cur = self.con.cursor()
            self.cur.execute(
                "CREATE TABLE artworks(author, title, size, medium, year, thumbnail)"
            )
            print("created database")

        # Table section
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

        # Input section

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

        button_add_data = QPushButton("Add an artwork")
        # button_add_data.clicked.connect(self.add_data)

        button_update_data = QPushButton("Update")
        # button_update_data.clicked.connect(self.update_data)

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
        h_layout07.addWidget(button_add_data)
        h_layout07.addWidget(button_update_data)

        # Grouping elements
        add_form = QGroupBox()

        # Layout of the form
        form_layout = QVBoxLayout()
        form_layout.addLayout((h_layout01))
        form_layout.addLayout((h_layout02))
        form_layout.addLayout((h_layout03))
        form_layout.addLayout((h_layout04))
        form_layout.addLayout((h_layout05))
        form_layout.addLayout((h_layout06))
        form_layout.addLayout((h_layout07))
        add_form.setLayout(form_layout)

        # Displaying
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(add_form)
        self.setLayout(layout)

    # def create_connection(self):
    #     pass
    #
    # def update_data(self):
    #     pass
    #
    # def add_data(self):
    # self.cursor = self.create_connection().cursor()
    #
    # self.new_artwork = [
    #     self.author_line_edit.text(),
    #     self.title_line_edit.text(),
    #     self.size_line_edit.text(),
    #     self.medium_line_edit.text(),
    #     self.year_line_edit.text(),
    #     self.thumbnail_line_edit.text(),
    # ]
    # # Add artwork
    # self.cursor.execute(
    #     "Insert into artwork_list values (?,?,?,?,?,?)", self.new_artwork
    # )
    # # Clear Edits
    # self.author_line_edit.clear()
    # self.title_line_edit.clear()
    # self.size_line_edit.clear()
    # self.medium_line_edit.clear()
    # self.year_line_edit.clear()
    # self.thumbnail_line_edit.clear()
    # self.connection.commit()
    # self.connection.close

    # def load_data(self):
    #     pass

    # def call_data(self):
    #     pass
    #
    # def delete_data(self):
    #     pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        Widget = Archive()
        self.setCentralWidget(Widget)
        self.menu()

    def menu(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("File")
        exitAction = fileMenu.addAction("Exit")
        exitAction.triggered.connect(self.close)
        editMenu = menubar.addMenu("Edit")
        aboutMenu = menubar.addMenu("About")
