import sys
from datetime import datetime

from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMenu,
    QLineEdit,
    QScrollArea,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
)


class ClipboardItem:

    def __init__(self, text):
        self.text = text
        self.pinned = False
        self.created = datetime.now()

    @property
    def preview(self):
        text = self.text.replace("\n", " ").strip()

        if len(text) > 90:
            return text[:90] + "..."

        return text


class GloxClipboard(QWidget):

    WIDTH = 330
    HEIGHT = 460
    MAX_ITEMS = 50

    THEMES = {
        "Warm Brown": QColor(55, 52, 48, 248),
        "Obsidian": QColor(25, 26, 28, 248),
        "Graphite": QColor(38, 40, 42, 248),
        "Charcoal": QColor(45, 45, 44, 248),
        "Espresso": QColor(48, 39, 34, 248),
        "Slate": QColor(39, 43, 47, 248),
        "Midnight": QColor(27, 30, 38, 248),
    }

    def __init__(self):
        super().__init__()

        self.setWindowTitle("GLOX Clipboard")

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

        self.items = []

        self.current_theme = "Warm Brown"

        self.dragging = False
        self.drag_offset = QPointF()

        self.last_clipboard = ""

        self.build_ui()

        self.monitor_timer = QTimer(self)

        self.monitor_timer.timeout.connect(
            self.check_clipboard
        )

        self.monitor_timer.start(250)

    # =========================================================
    # UI
    # =========================================================

    def build_ui(self):

        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(
            18,
            16,
            18,
            16
        )

        self.main_layout.setSpacing(10)

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        header = QHBoxLayout()

        title = QLabel("GLOX")

        title.setFont(
            QFont(
                "Segoe UI",
                15,
                QFont.Weight.Bold
            )
        )

        title.setStyleSheet(
            "color: #F3EEE5; background: transparent;"
        )

        subtitle = QLabel("CLIPBOARD")

        subtitle.setFont(
            QFont(
                "Segoe UI",
                8,
                QFont.Weight.Medium
            )
        )

        subtitle.setStyleSheet(
            "color: #A9A39A; background: transparent;"
        )

        header.addWidget(title)
        header.addWidget(subtitle)
        header.addStretch()

        self.count_label = QLabel("0")

        self.count_label.setStyleSheet(
            """
            QLabel {
                color: #C8C0B5;
                background: transparent;
            }
            """
        )

        header.addWidget(
            self.count_label
        )

        self.main_layout.addLayout(
            header
        )

        # -----------------------------------------------------
        # SEARCH
        # -----------------------------------------------------

        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "Search clipboard..."
        )

        self.search.setStyleSheet(
            """
            QLineEdit {
                background: rgba(255,255,255,18);
                color: #F3EEE5;
                border: 1px solid rgba(255,255,255,25);
                border-radius: 8px;
                padding: 8px 10px;
                selection-background-color: #70685E;
            }

            QLineEdit:focus {
                border: 1px solid rgba(220,190,140,90);
            }
            """
        )

        self.search.textChanged.connect(
            self.refresh_items
        )

        self.main_layout.addWidget(
            self.search
        )

        # -----------------------------------------------------
        # SCROLL AREA
        # -----------------------------------------------------

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(
            True
        )

        self.scroll.setFrameShape(
            QFrame.NoFrame
        )

        self.scroll.setStyleSheet(
            """
            QScrollArea {
                background: transparent;
                border: none;
            }

            QScrollArea > QWidget {
                background: transparent;
            }

            QScrollArea > QWidget > QWidget {
                background: transparent;
            }

            QScrollBar:vertical {
                background: transparent;
                width: 6px;
                margin: 0px;
            }

            QScrollBar::handle:vertical {
                background: rgba(255,255,255,45);
                border-radius: 3px;
                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover {
                background: rgba(255,255,255,70);
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: transparent;
            }
            """
        )

        # IMPORTANT:
        # Make the actual viewport transparent.
        self.scroll.viewport().setStyleSheet(
            "background: transparent; border: none;"
        )

        self.list_widget = QWidget()

        self.list_widget.setStyleSheet(
            "background: transparent;"
        )

        self.list_layout = QVBoxLayout(
            self.list_widget
        )

        self.list_layout.setContentsMargins(
            0,
            0,
            4,
            0
        )

        self.list_layout.setSpacing(7)

        self.list_layout.addStretch()

        self.scroll.setWidget(
            self.list_widget
        )

        self.main_layout.addWidget(
            self.scroll
        )

        # -----------------------------------------------------
        # BOTTOM
        # -----------------------------------------------------

        bottom = QHBoxLayout()

        clear_button = QPushButton(
            "Clear"
        )

        clear_button.clicked.connect(
            self.clear_history
        )

        clear_button.setStyleSheet(
            self.button_style()
        )

        bottom.addWidget(
            clear_button
        )

        bottom.addStretch()

        info = QLabel(
            "Click item to copy"
        )

        info.setStyleSheet(
            """
            QLabel {
                color: #858078;
                background: transparent;
                font-size: 8pt;
            }
            """
        )

        bottom.addWidget(
            info
        )

        self.main_layout.addLayout(
            bottom
        )

        self.refresh_items()

    # =========================================================
    # BUTTON STYLE
    # =========================================================

    def button_style(self):

        return """
        QPushButton {
            background: rgba(255,255,255,15);
            color: #D8D1C7;
            border: 1px solid rgba(255,255,255,25);
            border-radius: 6px;
            padding: 5px 12px;
        }

        QPushButton:hover {
            background: rgba(255,255,255,28);
        }

        QPushButton:pressed {
            background: rgba(255,255,255,40);
        }
        """

    # =========================================================
    # CLIPBOARD MONITOR
    # =========================================================

    def check_clipboard(self):

        clipboard = QApplication.clipboard()

        text = clipboard.text()

        if not text:
            return

        if text == self.last_clipboard:
            return

        self.last_clipboard = text

        self.add_item(text)

    # =========================================================
    # ADD ITEM
    # =========================================================

    def add_item(self, text):

        if self.items:

            if self.items[0].text == text:
                return

        # Remove duplicate
        self.items = [
            item
            for item in self.items
            if item.text != text
        ]

        item = ClipboardItem(text)

        self.items.insert(
            0,
            item
        )

        # Keep max history
        if len(self.items) > self.MAX_ITEMS:

            unpinned = [
                item
                for item in self.items
                if not item.pinned
            ]

            while len(self.items) > self.MAX_ITEMS:

                if unpinned:

                    old = unpinned.pop()

                    if old in self.items:
                        self.items.remove(old)

                else:
                    break

        self.refresh_items()

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh_items(self):

        while self.list_layout.count() > 1:

            child = self.list_layout.takeAt(0)

            widget = child.widget()

            if widget:
                widget.deleteLater()

        query = (
            self.search.text()
            .lower()
            .strip()
        )

        visible_items = []

        for item in self.items:

            if (
                not query
                or query in item.text.lower()
            ):
                visible_items.append(item)

        for item in visible_items:

            card = self.create_card(item)

            self.list_layout.insertWidget(
                self.list_layout.count() - 1,
                card
            )

        self.count_label.setText(
            str(len(self.items))
        )

    # =========================================================
    # CARD
    # =========================================================

    def create_card(self, item):

        card = QFrame()

        card.setObjectName(
            "clipboardCard"
        )

        card.setStyleSheet(
            """
            QFrame#clipboardCard {
                background: rgba(255,255,255,10);
                border: 1px solid rgba(255,255,255,20);
                border-radius: 9px;
            }

            QFrame#clipboardCard:hover {
                background: rgba(255,255,255,18);
                border: 1px solid rgba(220,190,140,55);
            }
            """
        )

        layout = QVBoxLayout(card)

        layout.setContentsMargins(
            11,
            9,
            9,
            9
        )

        layout.setSpacing(5)

        # -----------------------------------------------------
        # CLIPBOARD TEXT
        # -----------------------------------------------------

        text_label = QLabel(
            item.preview
        )

        text_label.setWordWrap(
            True
        )

        text_label.setFont(
            QFont(
                "Segoe UI",
                9
            )
        )

        text_label.setStyleSheet(
            """
            QLabel {
                color: #F0EBE3;
                background: transparent;
                border: none;
            }
            """
        )

        text_label.setCursor(
            Qt.PointingHandCursor
        )

        text_label.mousePressEvent = (
            lambda event,
            i=item:
            self.copy_item(i)
        )

        layout.addWidget(
            text_label
        )

        # -----------------------------------------------------
        # BOTTOM ROW
        # -----------------------------------------------------

        row = QHBoxLayout()

        if item.pinned:

            pin = QLabel(
                "PINNED"
            )

            pin.setStyleSheet(
                """
                QLabel {
                    color: #D7B56D;
                    background: transparent;
                    font-size: 7pt;
                }
                """
            )

            row.addWidget(pin)

        row.addStretch()

        pin_button = QPushButton("📌")

        pin_button.setFixedSize(
            28,
            24
        )

        pin_button.setStyleSheet(
            self.button_style()
        )

        pin_button.clicked.connect(
            lambda checked=False,
            i=item:
            self.toggle_pin(i)
        )

        row.addWidget(
            pin_button
        )

        delete_button = QPushButton("×")

        delete_button.setFixedSize(
            28,
            24
        )

        delete_button.setStyleSheet(
            self.button_style()
        )

        delete_button.clicked.connect(
            lambda checked=False,
            i=item:
            self.delete_item(i)
        )

        row.addWidget(
            delete_button
        )

        layout.addLayout(
            row
        )

        return card

    # =========================================================
    # COPY
    # =========================================================

    def copy_item(self, item):

        QApplication.clipboard().setText(
            item.text
        )

        self.last_clipboard = item.text

    # =========================================================
    # PIN
    # =========================================================

    def toggle_pin(self, item):

        item.pinned = not item.pinned

        self.refresh_items()

    # =========================================================
    # DELETE
    # =========================================================

    def delete_item(self, item):

        if item in self.items:
            self.items.remove(item)

        self.refresh_items()

    # =========================================================
    # CLEAR
    # =========================================================

    def clear_history(self):

        self.items.clear()

        self.refresh_items()

    # =========================================================
    # THEME
    # =========================================================

    def change_theme(self, theme):

        self.current_theme = theme

        self.update()

    # =========================================================
    # PAINT
    # =========================================================

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        # Shadow
        painter.setPen(
            Qt.NoPen
        )

        painter.setBrush(
            QColor(
                0,
                0,
                0,
                110
            )
        )

        painter.drawRoundedRect(
            4,
            4,
            self.width() - 8,
            self.height() - 8,
            15,
            15
        )

        # Background
        painter.setBrush(
            self.THEMES[
                self.current_theme
            ]
        )

        painter.drawRoundedRect(
            8,
            8,
            self.width() - 16,
            self.height() - 16,
            14,
            14
        )

        # Border
        painter.setBrush(
            Qt.NoBrush
        )

        painter.setPen(
            QPen(
                QColor(
                    235,
                    225,
                    210,
                    45
                ),
                1
            )
        )

        painter.drawRoundedRect(
            8,
            8,
            self.width() - 16,
            self.height() - 16,
            14,
            14
        )

    # =========================================================
    # DRAGGING
    # =========================================================

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.dragging = True

            self.drag_offset = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

            event.accept()

    def mouseMoveEvent(self, event):

        if self.dragging:

            position = (
                event.globalPosition().toPoint()
                - self.drag_offset
            )

            self.move(position)

            event.accept()

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.dragging = False

            event.accept()

    # =========================================================
    # RIGHT CLICK MENU
    # =========================================================

    def contextMenuEvent(self, event):

        menu = QMenu(self)

        menu.setStyleSheet(
            """
            QMenu {
                background: #292825;
                color: #F3EEE5;
                border: 1px solid #4B4842;
                padding: 5px;
            }

            QMenu::item {
                padding: 7px 22px;
                border-radius: 5px;
            }

            QMenu::item:selected {
                background: #3D3A35;
            }

            QMenu::separator {
                height: 1px;
                background: #4A4741;
                margin: 5px 8px;
            }
            """
        )

        # -----------------------------------------------------
        # Background
        # -----------------------------------------------------

        backgrounds = QMenu(
            "Background",
            menu
        )

        backgrounds.setStyleSheet(
            menu.styleSheet()
        )

        for theme in self.THEMES:

            action = backgrounds.addAction(
                theme
            )

            action.triggered.connect(
                lambda checked=False,
                t=theme:
                self.change_theme(t)
            )

        menu.addMenu(
            backgrounds
        )

        # -----------------------------------------------------
        # Opacity
        # -----------------------------------------------------

        opacity_menu = QMenu(
            "Opacity",
            menu
        )

        opacity_menu.setStyleSheet(
            menu.styleSheet()
        )

        for value in [
            100,
            80,
            60,
            50
        ]:

            action = opacity_menu.addAction(
                f"{value}%"
            )

            action.triggered.connect(
                lambda checked=False,
                v=value:
                self.setWindowOpacity(
                    v / 100
                )
            )

        menu.addMenu(
            opacity_menu
        )

        menu.addSeparator()

        # -----------------------------------------------------
        # Clear
        # -----------------------------------------------------

        clear_action = menu.addAction(
            "Clear Clipboard"
        )

        clear_action.triggered.connect(
            self.clear_history
        )

        menu.addSeparator()

        # -----------------------------------------------------
        # Quit
        # -----------------------------------------------------

        quit_action = menu.addAction(
            "Quit GLOX Clipboard"
        )

        quit_action.triggered.connect(
            QApplication.quit
        )

        menu.exec(
            event.globalPos()
        )


# =============================================================
# MAIN
# =============================================================

def main():

    app = QApplication(sys.argv)

    app.setApplicationName(
        "GLOX Clipboard"
    )

    app.setQuitOnLastWindowClosed(
        True
    )

    clipboard = GloxClipboard()

    screen = (
        app.primaryScreen()
        .availableGeometry()
    )

    clipboard.move(
        screen.right()
        - clipboard.width()
        - 35,
        screen.top()
        + 35
    )

    clipboard.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()