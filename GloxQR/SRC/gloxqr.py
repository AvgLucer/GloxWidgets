# GloxQR.py
# =============================================================
# GLOX QR — QR Code Studio
#
# Install:
# pip install PySide6 qrcode pillow
#
# Run:
# python GloxQR.py
# =============================================================

import sys
import io
import qrcode

from qrcode.constants import (
    ERROR_CORRECT_L,
    ERROR_CORRECT_M,
    ERROR_CORRECT_Q,
    ERROR_CORRECT_H,
)

from PySide6.QtCore import Qt, QPointF, QTimer
from PySide6.QtGui import QColor, QPainter, QPen, QFont, QPixmap

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QLineEdit,
    QComboBox,
    QColorDialog,
    QFileDialog,
    QMessageBox,
    QMenu,
)


# =============================================================
# GLOX QR
# =============================================================

class GloxQR(QWidget):

    WIDTH = 560
    HEIGHT = 760

    # =========================================================
    # THEMES
    # =========================================================

    THEMES = {

        "Obsidian": {
            "window": "#161719",
            "foreground": "#FFFFFF",
            "panel": "rgba(255,255,255,12)",
            "border": "rgba(255,255,255,22)",
            "input": "rgba(255,255,255,14)",
            "button": "rgba(255,255,255,18)",
            "hover": "rgba(255,255,255,32)",
            "pressed": "rgba(255,255,255,45)",
            "text": "#FFFFFF",
            "qr_background": "#161719",
            "qr_foreground": "#FFFFFF",
        },

        "Graphite": {
            "window": "#222326",
            "foreground": "#FFFFFF",
            "panel": "rgba(255,255,255,11)",
            "border": "rgba(255,255,255,20)",
            "input": "rgba(255,255,255,14)",
            "button": "rgba(255,255,255,18)",
            "hover": "rgba(255,255,255,30)",
            "pressed": "rgba(255,255,255,42)",
            "text": "#FFFFFF",
            "qr_background": "#222326",
            "qr_foreground": "#FFFFFF",
        },

        "Charcoal": {
            "window": "#2B2B2B",
            "foreground": "#FFFFFF",
            "panel": "rgba(255,255,255,12)",
            "border": "rgba(255,255,255,22)",
            "input": "rgba(255,255,255,14)",
            "button": "rgba(255,255,255,18)",
            "hover": "rgba(255,255,255,30)",
            "pressed": "rgba(255,255,255,42)",
            "text": "#FFFFFF",
            "qr_background": "#2B2B2B",
            "qr_foreground": "#FFFFFF",
        },

        "Crystal Cream": {
            "window": "#EBE7DB",
            "foreground": "#2A2723",
            "panel": "rgba(0,0,0,8)",
            "border": "rgba(0,0,0,20)",
            "input": "rgba(0,0,0,9)",
            "button": "rgba(0,0,0,12)",
            "hover": "rgba(0,0,0,22)",
            "pressed": "rgba(0,0,0,30)",
            "text": "#2A2723",
            "qr_background": "#EBE7DB",
            "qr_foreground": "#2A2723",
        },

        "Aurora": {
            "window": "#1B2230",
            "foreground": "#8EF0C8",
            "panel": "rgba(142,240,200,10)",
            "border": "rgba(142,240,200,25)",
            "input": "rgba(142,240,200,12)",
            "button": "rgba(142,240,200,14)",
            "hover": "rgba(142,240,200,25)",
            "pressed": "rgba(142,240,200,35)",
            "text": "#E8FFF6",
            "qr_background": "#1B2230",
            "qr_foreground": "#8EF0C8",
        },

        "Sunset": {
            "window": "#24191A",
            "foreground": "#FF9B72",
            "panel": "rgba(255,155,114,10)",
            "border": "rgba(255,155,114,25)",
            "input": "rgba(255,155,114,12)",
            "button": "rgba(255,155,114,15)",
            "hover": "rgba(255,155,114,26)",
            "pressed": "rgba(255,155,114,36)",
            "text": "#FFF0EA",
            "qr_background": "#24191A",
            "qr_foreground": "#FF9B72",
        },

        "Ocean": {
            "window": "#10252C",
            "foreground": "#7DE3FF",
            "panel": "rgba(125,227,255,10)",
            "border": "rgba(125,227,255,25)",
            "input": "rgba(125,227,255,12)",
            "button": "rgba(125,227,255,14)",
            "hover": "rgba(125,227,255,25)",
            "pressed": "rgba(125,227,255,35)",
            "text": "#E8FAFF",
            "qr_background": "#10252C",
            "qr_foreground": "#7DE3FF",
        },

        "Lavender": {
            "window": "#211C2D",
            "foreground": "#D7B8FF",
            "panel": "rgba(215,184,255,10)",
            "border": "rgba(215,184,255,25)",
            "input": "rgba(215,184,255,12)",
            "button": "rgba(215,184,255,14)",
            "hover": "rgba(215,184,255,25)",
            "pressed": "rgba(215,184,255,35)",
            "text": "#F7F0FF",
            "qr_background": "#211C2D",
            "qr_foreground": "#D7B8FF",
        },

        "Neon": {
            "window": "#0B0B0B",
            "foreground": "#00FF88",
            "panel": "rgba(0,255,136,9)",
            "border": "rgba(0,255,136,30)",
            "input": "rgba(0,255,136,10)",
            "button": "rgba(0,255,136,13)",
            "hover": "rgba(0,255,136,24)",
            "pressed": "rgba(0,255,136,35)",
            "text": "#E8FFF3",
            "qr_background": "#0B0B0B",
            "qr_foreground": "#00FF88",
        },

        "Minimal": {
            "window": "#FFFFFF",
            "foreground": "#111111",
            "panel": "rgba(0,0,0,8)",
            "border": "rgba(0,0,0,20)",
            "input": "rgba(0,0,0,9)",
            "button": "rgba(0,0,0,12)",
            "hover": "rgba(0,0,0,22)",
            "pressed": "rgba(0,0,0,30)",
            "text": "#111111",
            "qr_background": "#FFFFFF",
            "qr_foreground": "#111111",
        },
    }

    # =========================================================
    # INIT
    # =========================================================

    def __init__(self):

        super().__init__()

        self.current_theme = "Obsidian"

        self.foreground = "#FFFFFF"
        self.background = "#161719"

        self.opacity_value = 100

        self.qr_pixmap = None

        self.dragging = False
        self.drag_offset = QPointF()

        self.setWindowTitle("GloxQR")

        self.setFixedSize(
            self.WIDTH,
            self.HEIGHT
        )

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground
        )

        self.build_ui()
        self.apply_theme()

    # =========================================================
    # UI
    # =========================================================

    def build_ui(self):

        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(
            28,
            22,
            28,
            24
        )

        self.main_layout.setSpacing(4)

        # =====================================================
        # HEADER
        # =====================================================

        header = QHBoxLayout()

        title = QLabel("GLOX")

        title.setFont(
            QFont(
                "Segoe UI",
                22,
                QFont.Weight.Bold
            )
        )

        subtitle = QLabel("QR")

        subtitle.setFont(
            QFont(
                "Segoe UI",
                16,
                QFont.Weight.Bold
            )
        )

        header.addWidget(title)
        header.addWidget(subtitle)
        header.addStretch()

        self.main_layout.addLayout(header)

        # =====================================================
        # INPUT
        # =====================================================

        input_card = QFrame()

        input_layout = QVBoxLayout(
            input_card
        )

        input_layout.setContentsMargins(
            14,
            12,
            14,
            14
        )

        input_layout.setSpacing(7)

        input_label = QLabel("CONTENT")

        input_label.setFont(
            QFont(
                "Segoe UI",
                10,
                QFont.Weight.Bold
            )
        )

        self.input_box = QLineEdit()

        self.input_box.setPlaceholderText(
            "Enter text, URL, email, etc..."
        )

        self.input_box.setFixedHeight(43)

        self.input_box.returnPressed.connect(
            self.generate_qr
        )

        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_box)

        self.main_layout.addWidget(input_card)

        # =====================================================
        # SQUARE QR PREVIEW
        # =====================================================

        self.preview_card = QFrame()

        self.preview_card.setFixedHeight(
            350
        )

        preview_layout = QVBoxLayout(
            self.preview_card
        )

        preview_layout.setContentsMargins(
            10,
            10,
            10,
            10
        )

        self.qr_preview = QLabel(
            "QR PREVIEW"
        )

        self.qr_preview.setAlignment(
            Qt.AlignCenter
        )

        preview_layout.addWidget(
            self.qr_preview
        )

        self.main_layout.addWidget(
            self.preview_card
        )

        # =====================================================
        # OPTIONS
        # =====================================================

        options_card = QFrame()

        options_layout = QHBoxLayout(
            options_card
        )

        options_layout.setContentsMargins(
            12,
            10,
            12,
            10
        )

        options_layout.setSpacing(10)

        self.theme_combo = QComboBox()

        self.theme_combo.addItems(
            list(self.THEMES.keys())
        )

        self.theme_combo.setFixedHeight(
            38
        )

        self.theme_combo.currentTextChanged.connect(
            self.change_theme
        )

        self.correction_combo = QComboBox()

        self.correction_combo.addItems([
            "Low (L)",
            "Medium (M)",
            "Quartile (Q)",
            "High (H)"
        ])

        self.correction_combo.setCurrentIndex(
            1
        )

        self.correction_combo.setFixedHeight(
            38
        )

        options_layout.addWidget(
            self.theme_combo
        )

        options_layout.addWidget(
            self.correction_combo
        )

        self.main_layout.addWidget(
            options_card
        )

        # =====================================================
        # COLORS
        # =====================================================

        color_row = QHBoxLayout()

        color_row.setSpacing(10)

        self.foreground_button = QPushButton(
            "QR COLOR"
        )

        self.background_button = QPushButton(
            "BG COLOR"
        )

        self.foreground_button.setFixedHeight(
            42
        )

        self.background_button.setFixedHeight(
            42
        )

        self.foreground_button.clicked.connect(
            self.pick_foreground
        )

        self.background_button.clicked.connect(
            self.pick_background
        )

        color_row.addWidget(
            self.foreground_button
        )

        color_row.addWidget(
            self.background_button
        )

        self.main_layout.addLayout(
            color_row
        )

        # =====================================================
        # GENERATE
        # =====================================================

        self.generate_button = QPushButton(
            "GENERATE QR"
        )

        self.generate_button.setFixedHeight(
            46
        )

        self.generate_button.clicked.connect(
            self.generate_qr
        )

        self.main_layout.addWidget(
            self.generate_button
        )

        # =====================================================
        # ACTIONS
        # =====================================================

        action_row = QHBoxLayout()

        action_row.setSpacing(10)

        self.copy_button = QPushButton(
            "COPY QR"
        )

        self.save_button = QPushButton(
            "SAVE PNG"
        )

        self.copy_button.setFixedHeight(
            43
        )

        self.save_button.setFixedHeight(
            43
        )

        self.copy_button.clicked.connect(
            self.copy_qr
        )

        self.save_button.clicked.connect(
            self.save_png
        )

        action_row.addWidget(
            self.copy_button
        )

        action_row.addWidget(
            self.save_button
        )

        self.main_layout.addLayout(
            action_row
        )

    # =========================================================
    # THEME
    # =========================================================

    def apply_theme(self):

        theme = self.THEMES[
            self.current_theme
        ]

        self.setStyleSheet(
            f"""
            QLabel {{
                color: {theme["text"]};
                background: transparent;
                font-family: "Segoe UI";
            }}

            QFrame {{
                background: {theme["panel"]};
                border: 1px solid {theme["border"]};
                border-radius: 15px;
            }}

            QLineEdit {{
                background: {theme["input"]};
                color: {theme["text"]};
                border: 1px solid {theme["border"]};
                border-radius: 9px;
                padding-left: 12px;
                padding-right: 12px;
                font-family: "Segoe UI";
                font-size: 11px;
            }}

            QLineEdit:focus {{
                border: 1px solid {theme["foreground"]};
            }}

            QComboBox {{
                background: {theme["input"]};
                color: {theme["text"]};
                border: 1px solid {theme["border"]};
                border-radius: 9px;
                padding-left: 10px;
                font-family: "Segoe UI";
                font-size: 10px;
            }}

            QComboBox QAbstractItemView {{
                background: #252525;
                color: white;
                selection-background-color: #3A3A3A;
            }}

            QPushButton {{
                background: {theme["button"]};
                color: {theme["text"]};
                border: 1px solid {theme["border"]};
                border-radius: 10px;
                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: bold;
            }}

            QPushButton:hover {{
                background: {theme["hover"]};
            }}

            QPushButton:pressed {{
                background: {theme["pressed"]};
            }}
            """
        )

        self.update()

    # =========================================================
    # CHANGE THEME
    # =========================================================

    def change_theme(self, theme_name):

        if theme_name not in self.THEMES:
            return

        self.current_theme = theme_name

        theme = self.THEMES[
            theme_name
        ]

        self.foreground = theme[
            "qr_foreground"
        ]

        self.background = theme[
            "qr_background"
        ]

        self.apply_theme()

        if self.input_box.text().strip():
            self.generate_qr()

    # =========================================================
    # COLORS
    # =========================================================

    def pick_foreground(self):

        color = QColorDialog.getColor(
            QColor(self.foreground),
            self,
            "Choose QR Color"
        )

        if color.isValid():

            self.foreground = color.name()

            if self.input_box.text().strip():
                self.generate_qr()

    def pick_background(self):

        color = QColorDialog.getColor(
            QColor(self.background),
            self,
            "Choose Background Color"
        )

        if color.isValid():

            self.background = color.name()

            if self.input_box.text().strip():
                self.generate_qr()

    # =========================================================
    # ERROR CORRECTION
    # =========================================================

    def get_error_correction(self):

        corrections = [
            ERROR_CORRECT_L,
            ERROR_CORRECT_M,
            ERROR_CORRECT_Q,
            ERROR_CORRECT_H,
        ]

        return corrections[
            self.correction_combo.currentIndex()
        ]

    # =========================================================
    # GENERATE QR
    # =========================================================

    def generate_qr(self):

        data = self.input_box.text().strip()

        if not data:

            self.qr_preview.setText(
                "QR PREVIEW"
            )

            self.qr_pixmap = None

            return

        try:

            qr = qrcode.QRCode(
                version=None,
                error_correction=self.get_error_correction(),
                box_size=12,
                border=4
            )

            qr.add_data(data)
            qr.make(fit=True)

            image = qr.make_image(
                fill_color=self.foreground,
                back_color=self.background
            ).convert("RGB")

            # Exported QR resolution
            image = image.resize(
                (500, 500)
            )

            buffer = io.BytesIO()

            image.save(
                buffer,
                format="PNG"
            )

            pixmap = QPixmap()

            pixmap.loadFromData(
                buffer.getvalue(),
                "PNG"
            )

            self.qr_pixmap = pixmap

            # -------------------------------------------------
            # NORMAL-SIZED UI PREVIEW
            # -------------------------------------------------

            self.qr_preview.setPixmap(
                pixmap.scaled(
                    260,
                    260,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )

        except Exception as e:

            QMessageBox.warning(
                self,
                "GloxQR",
                f"Could not generate QR:\n\n{e}"
            )

    # =========================================================
    # COPY
    # =========================================================

    def copy_qr(self):

        if self.qr_pixmap is None:
            return

        QApplication.clipboard().setPixmap(
            self.qr_pixmap
        )

        self.copy_button.setText(
            "COPIED!"
        )

        QTimer.singleShot(
            1200,
            lambda: self.copy_button.setText(
                "COPY QR"
            )
        )

    # =========================================================
    # SAVE
    # =========================================================

    def save_png(self):

        if self.qr_pixmap is None:

            QMessageBox.information(
                self,
                "GloxQR",
                "Generate a QR code first."
            )

            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save GloxQR",
            "gloxqr.png",
            "PNG Image (*.png)"
        )

        if not path:
            return

        if not path.lower().endswith(".png"):
            path += ".png"

        if self.qr_pixmap.save(
            path,
            "PNG"
        ):

            self.save_button.setText(
                "SAVED!"
            )

            QTimer.singleShot(
                1200,
                lambda: self.save_button.setText(
                    "SAVE PNG"
                )
            )

    # =========================================================
    # RIGHT CLICK MENU
    # =========================================================

    def contextMenuEvent(self, event):

        menu = QMenu(self)

        menu.setStyleSheet("""
            QMenu {
                background: #252525;
                color: white;
                border: 1px solid #444444;
                padding: 5px;
                border-radius: 8px;
            }

            QMenu::item {
                padding: 8px 28px 8px 12px;
                border-radius: 5px;
            }

            QMenu::item:selected {
                background: #3A3A3A;
            }

            QMenu::separator {
                height: 1px;
                background: #444444;
                margin: 5px;
            }
        """)

        # -----------------------------------------------------
        # THEME
        # -----------------------------------------------------

        theme_menu = menu.addMenu(
            "Theme"
        )

        for theme_name in self.THEMES:

            action = theme_menu.addAction(
                theme_name
            )

            action.setCheckable(True)

            action.setChecked(
                theme_name == self.current_theme
            )

            action.triggered.connect(
                lambda checked=False,
                name=theme_name:
                self.select_context_theme(name)
            )

        # -----------------------------------------------------
        # OPACITY
        # -----------------------------------------------------

        opacity_menu = menu.addMenu(
            "Opacity"
        )

        for value in [100, 80, 60, 50]:

            action = opacity_menu.addAction(
                f"{value}%"
            )

            action.setCheckable(True)

            action.setChecked(
                value == self.opacity_value
            )

            action.triggered.connect(
                lambda checked=False,
                v=value:
                self.change_opacity(v)
            )

        menu.addSeparator()

        # -----------------------------------------------------
        # EXIT
        # -----------------------------------------------------

        exit_action = menu.addAction(
            "Exit"
        )

        exit_action.triggered.connect(
            QApplication.quit
        )

        menu.exec(
            event.globalPos()
        )

    # =========================================================
    # CONTEXT THEME
    # =========================================================

    def select_context_theme(self, theme_name):

        self.theme_combo.blockSignals(True)

        self.theme_combo.setCurrentText(
            theme_name
        )

        self.theme_combo.blockSignals(False)

        self.change_theme(
            theme_name
        )

    # =========================================================
    # OPACITY
    # =========================================================

    def change_opacity(self, value):

        self.opacity_value = value

        self.setWindowOpacity(
            value / 100
        )

    # =========================================================
    # PAINT
    # =========================================================

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        theme = self.THEMES[
            self.current_theme
        ]

        painter.setBrush(
            QColor(theme["window"])
        )

        painter.setPen(
            QPen(
                QColor(
                    255,
                    255,
                    255,
                    35
                ),
                1
            )
        )

        painter.drawRoundedRect(
            0,
            0,
            self.width(),
            self.height(),
            22,
            22
        )

    # =========================================================
    # DRAG
    # =========================================================

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.dragging = True

            self.drag_offset = (
                event.globalPosition()
                - self.frameGeometry().topLeft()
            )

            event.accept()

    def mouseMoveEvent(self, event):

        if (
            self.dragging
            and event.buttons() & Qt.LeftButton
        ):

            self.move(
                (
                    event.globalPosition()
                    - self.drag_offset
                ).toPoint()
            )

            event.accept()

    def mouseReleaseEvent(self, event):

        self.dragging = False

        event.accept()


# =============================================================
# MAIN
# =============================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    app.setStyle("Fusion")

    widget = GloxQR()

    widget.show()

    sys.exit(
        app.exec()
    )