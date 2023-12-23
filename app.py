import sys
from pathlib import Path
import numpy as np
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
    QSlider,
)
from PyQt6.QtGui import QIcon, QPixmap, QTransform, QPainter, QAction, QGuiApplication
from PyQt6.QtCore import Qt, QSize, QRect
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog


# class EmptyWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initializeUI()

#     def initializeUI(self):
#         self.setGeometry(100, 100, 1000, 600)
#         self.setWindowTitle("Astro Viewer")
#         self.show()


# class SaveWindow(QWidget):
#     """
#     Window for saving the image.
#     """

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # setup window
#         self.setWindowTitle("PyQt File Dialog")
#         self.setGeometry(100, 100, 400, 100)
#         # self.setFixedSize(1000, 600)
#         layout = QGridLayout()
#         self.setLayout(layout)

#         # button to open file selection widget
#         browse_button = QPushButton("Browse")
#         browse_button.clicked.connect(self.handle_open_file_dialog)
#         self.filename_edit = QLineEdit()

#         # button to open image viewing window
#         open_button = QPushButton("Open")

#         # add components to the layout
#         layout.addWidget(QLabel("File:"), 0, 0)
#         layout.addWidget(self.filename_edit, 0, 1)
#         layout.addWidget(browse_button, 0, 2)
#         layout.addWidget(open_button, 1, 2)

#         # add handlers
#         open_button.clicked.connect(self.handle_open_image)

#         self.show()

#     def handle_open_file_dialog(self):
#         filename, _ = QFileDialog.getOpenFileName(
#             self, "Select a File", ".", "Images (*.png *.jpg *.jpeg *.fits)"
#         )
#         if filename:
#             path = Path(filename)
#             self.filename_edit.setText(str(path))

#     def handle_open_image(self):
#         print(self.filename_edit.text())


# class ImagePlaceholder(QWidget):
#     """
#     Placeholder before selecting an image.
#     """

#     def __init__(self):
#         super().__init__()
#         layout = QVBoxLayout()
#         layout.addStretch()

#         # text label
#         label = QLabel("Click to select a file")
#         label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(label)

#         # file dialog button
#         browse_button = QPushButton("Open")
#         browse_button.clicked.connect(self.handle_open_file)
#         browse_button.setFixedSize(100, 60)
#         layout.addWidget(browse_button, alignment=Qt.AlignmentFlag.AlignCenter)

#         # selected file stuff, need to keep track of the file path
#         self.current_file = None
#         self.debug_label = QLabel("Selected:")
#         self.debug_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(self.debug_label)

#         layout.addStretch()
#         self.setLayout(layout)

#     def handle_open_file(self):
#         filename, _ = QFileDialog.getOpenFileName(
#             self,
#             "Select a File",
#             ".",
#             "Images (*.png *.jpg *.jpeg *.fits *.tiff *.tif)",
#         )
#         if filename:
#             path = Path(filename)
#             self.current_file = str(path)
#             self.debug_label.setText(f"Selected: {self.current_file}")
#             print(self.current_file)

#             self.image = QPixmap(self.current_file)
#             self.debug_label.setPixmap(
#                 self.image.scaled(
#                     self.debug_label.size(),
#                     Qt.AspectRatioMode.KeepAspectRatio,
#                     Qt.TransformationMode.SmoothTransformation,
#                 )
#             )


# class ImageContainer(QWidget):
#     """
#     Displays the currently loaded image.
#     """

#     def __init__(self):
#         super().__init__()
#         layout = QVBoxLayout()
#         layout.addStretch()

#         # text label
#         label = QLabel("Click to select a file")
#         label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(label)

#         # file dialog button
#         browse_button = QPushButton("Open")
#         browse_button.clicked.connect(self.handle_open_file)
#         browse_button.setFixedSize(100, 60)
#         layout.addWidget(browse_button, alignment=Qt.AlignmentFlag.AlignCenter)

#         # selected file stuff, need to keep track of the file path
#         self.current_file = None
#         self.debug_label = QLabel("Selected:")
#         self.debug_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(self.debug_label)

#         layout.addStretch()
#         self.setLayout(layout)


def make_slider(lower: int, upper: int, interval: int, value: int) -> QSlider:
    slider = QSlider(Qt.Orientation.Horizontal)
    slider.setRange(min, max)
    slider.setValue(value)
    slider.setTickPosition(QSlider.TickPosition.TicksBelow)
    slider.setTickInterval(interval)
    return slider


class AppWindow(QMainWindow):
    """
    Primary window and entrypoint.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # setup window
        self.setWindowTitle("Wavelet Kit")
        self.setFixedSize(1200, 600)
        self._center_window()

        # setup central widgets and set to placeholder
        self._build_file_dialog()
        self.setCentralWidget(self.image_placeholder)
        self.image = QPixmap()
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # setup toolbar
        self._build_toolbar()

        # setup state tracking variables
        # should we maybe use a dict/object for represting state?
        self.current_file = None
        self.scale_factor = 1

        self.show()

    # INTERNAL HELPERS

    def _center_window(self):
        frame = self.frameGeometry()
        center = QGuiApplication.primaryScreen().availableGeometry().center()
        frame.moveCenter(center)
        self.move(frame.topLeft())

    def _build_file_dialog(self):
        # initialize container widget
        self.image_placeholder = QWidget()
        layout = QVBoxLayout()
        layout.addStretch()

        # create and attach text label
        label = QLabel("Click to select a file")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # create and attach file dialog button
        browse_button = QPushButton("Open")
        browse_button.clicked.connect(self.handle_open_file)
        browse_button.setFixedSize(100, 60)
        layout.addWidget(browse_button, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()
        self.image_placeholder.setLayout(layout)

    def _render_image_label(self):
        dim = self.image_placeholder.frameGeometry()
        print(dim)
        self.image_label.setPixmap(
            # self.image
            self.image.scaled(
                QSize(
                    int(dim.width() * self.scale_factor),
                    int(dim.height() * self.scale_factor),
                ),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        self.setCentralWidget(self.image_label)
        print(self.image_label.frameGeometry())

    # TOOLBAR

    def _build_toolbar(self):
        # toolbar container widget
        self.toolbar = QDockWidget()
        self.toolbar.setWindowTitle("Tools")
        self.toolbar.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea
        )
        # parent widget for all widgets inside the toolbar
        toolbar_contents = QWidget()
        # layout
        toolbar_layout = QVBoxLayout()

        # 2x zoom button
        zoom_button = QPushButton("Zoom In")
        zoom_button.setMinimumWidth(300)
        zoom_button.clicked.connect(self.handle_zoom_in)
        toolbar_layout.addWidget(zoom_button)

        # zoom out button
        zoom_button = QPushButton("Zoom Out")
        zoom_button.setMinimumWidth(300)
        toolbar_layout.addWidget(zoom_button)

        toolbar_layout.addStretch()
        toolbar_contents.setLayout(toolbar_layout)
        self.toolbar.setWidget(toolbar_contents)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.toolbar)

    # BUTTON HANDLERS

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
            print(self.current_file)
            self.image = QPixmap(self.current_file)
            self._render_image_label()

    def handle_zoom_in(self):
        # modify scale factor
        self.scale_factor = np.min([int(self.scale_factor * 2), 2])
        self._render_image_label()
        # self.setCentralWidget(self.image_label)

    def handle_zoom_out(self):
        pass


if __name__ == "__main__":
    print("Test")
    app = QApplication(sys.argv)
    window = AppWindow()
    sys.exit(app.exec())
