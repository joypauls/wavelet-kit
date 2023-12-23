import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QFileDialog,
    QGridLayout,
    QPushButton,
    QLabel,
    QListWidget,
    QLineEdit,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QDockWidget,
)
from PyQt6.QtGui import QIcon, QPixmap, QTransform, QPainter, QAction, QGuiApplication
from PyQt6.QtCore import Qt, QSize, QRect
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog


class EmptyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowTitle("Astro Viewer")
        self.show()


class SaveWindow(QWidget):
    """
    Window for saving the image.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # setup window
        self.setWindowTitle("PyQt File Dialog")
        self.setGeometry(100, 100, 400, 100)
        # self.setFixedSize(1000, 600)
        layout = QGridLayout()
        self.setLayout(layout)

        # button to open file selection widget
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.handle_open_file_dialog)
        self.filename_edit = QLineEdit()

        # button to open image viewing window
        open_button = QPushButton("Open")

        # add components to the layout
        layout.addWidget(QLabel("File:"), 0, 0)
        layout.addWidget(self.filename_edit, 0, 1)
        layout.addWidget(browse_button, 0, 2)
        layout.addWidget(open_button, 1, 2)

        # add handlers
        open_button.clicked.connect(self.handle_open_image)

        self.show()

    def handle_open_file_dialog(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select a File", ".", "Images (*.png *.jpg *.jpeg *.fits)"
        )
        if filename:
            path = Path(filename)
            self.filename_edit.setText(str(path))

    def handle_open_image(self):
        print(self.filename_edit.text())


class ImagePlaceholder(QWidget):
    """
    Placeholder before selecting an image.
    """

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addStretch()

        # text label
        label = QLabel("Click to select a file")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # file dialog button
        browse_button = QPushButton("Open")
        browse_button.clicked.connect(self.handle_open_file)
        browse_button.setFixedSize(100, 60)
        layout.addWidget(browse_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # selected file stuff, need to keep track of the file path
        self.current_file = None
        self.debug_label = QLabel("Selected:")
        self.debug_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.debug_label)

        layout.addStretch()
        self.setLayout(layout)

    def handle_open_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select a File",
            ".",
            "Images (*.png *.jpg *.jpeg *.fits *.tiff *.tif)",
        )
        if filename:
            path = Path(filename)
            self.current_file = str(path)
            self.debug_label.setText(f"Selected: {self.current_file}")
            print(self.current_file)

            self.image = QPixmap(self.current_file)
            self.debug_label.setPixmap(
                self.image.scaled(
                    self.debug_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )


class ImageContainer(QWidget):
    """
    Displays the currently loaded image.
    """

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addStretch()

        # text label
        label = QLabel("Click to select a file")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # file dialog button
        browse_button = QPushButton("Open")
        browse_button.clicked.connect(self.handle_open_file)
        browse_button.setFixedSize(100, 60)
        layout.addWidget(browse_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # selected file stuff, need to keep track of the file path
        self.current_file = None
        self.debug_label = QLabel("Selected:")
        self.debug_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.debug_label)

        layout.addStretch()
        self.setLayout(layout)


if __name__ == "__main__":
    print("Test")
    app = QApplication(sys.argv)
    window = ImageContainer()
    sys.exit(app.exec())
