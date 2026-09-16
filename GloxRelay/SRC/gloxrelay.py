import sys
import os
import json
import webbrowser

from PySide6.QtCore import (
    Qt,
    QTimer,
    QEasingCurve,
    QPropertyAnimation,
    QRect,
    Signal,
)
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPainterPath,
    QPen,
    QBrush,
    QFont,
    QAction,
)
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QLineEdit,
    QDialog,
    QCheckBox,
    QSlider,
    QComboBox,
    QMessageBox,
    QFrame,
    QGraphicsDropShadowEffect,
    QMenu,
)


# ============================================================
# CONFIG
# ============================================================

APP_NAME = "Glox Relay"

CONFIG_DIR = os.path.join(
    os.path.expanduser("~"),
    ".gloxrelay"
)

CONFIG_FILE = os.path.join(
    CONFIG_DIR,
    "config.json"
)

os.makedirs(CONFIG_DIR, exist_ok=True)


DEFAULT_DESTINATIONS = [
    {
        "title": "ChatGPT",
        "url": "https://chatgpt.com/",
        "enabled": True,
        "submit": True,
    },
    {
        "title": "Gemini",
        "url": "https://gemini.google.com/",
        "enabled": True,
        "submit": True,
    },
    {
        "title": "Claude",
        "url": "https://claude.ai/",
        "enabled": True,
        "submit": True,
    },
    {
        "title": "Google",
        "url": "https://www.google.com/",
        "enabled": True,
        "submit": True,
    },
    {
        "title": "Yahoo",
        "url": "https://search.yahoo.com/",
        "enabled": True,
        "submit": True,
    },
    {
        "title": "Bing",
        "url": "https://www.bing.com/",
        "enabled": True,
        "submit": True,
    },
    {
        "title": "DuckDuckGo",
        "url": "https://duckduckgo.com/",
        "enabled": True,
        "submit": True,
    },
    {
        "title": "Perplexity",
        "url": "https://www.perplexity.ai/",
        "enabled": True,
        "submit": True,
    },
]


# ============================================================
# 12 GLOX THEMES
# ============================================================

THEMES = {

    "Glox Cream": {
        "bg": "#E7DED0",
        "panel": "#F2E9DD",
        "card": "#DED0BD",
        "text": "#463A2E",
        "muted": "#7E6E5D",
        "accent": "#92785A",
        "accent2": "#B19672",
        "border": "#C6B6A0",
        "bubble": "#E9DDCE",
    },

    "Coffee": {
        "bg": "#30251F",
        "panel": "#41332B",
        "card": "#513F35",
        "text": "#F2E6D8",
        "muted": "#BBA592",
        "accent": "#B88C69",
        "accent2": "#D0A27D",
        "border": "#665044",
        "bubble": "#49382F",
    },

    "Midnight": {
        "bg": "#14151A",
        "panel": "#202229",
        "card": "#292C34",
        "text": "#ECEBF0",
        "muted": "#9B9CA7",
        "accent": "#9289C4",
        "accent2": "#AEA5DD",
        "border": "#3A3D48",
        "bubble": "#282A31",
    },

    "Lavender Dream": {
        "bg": "#D9D0E8",
        "panel": "#E9E3F1",
        "card": "#C9BEDC",
        "text": "#44384F",
        "muted": "#786B86",
        "accent": "#856DA4",
        "accent2": "#A88BC7",
        "border": "#B9AACA",
        "bubble": "#D9CEE7",
    },

    "Deep Lavender": {
        "bg": "#302A3D",
        "panel": "#403750",
        "card": "#504465",
        "text": "#F0EAF7",
        "muted": "#B7A9C7",
        "accent": "#9A7BC1",
        "accent2": "#B796DF",
        "border": "#625576",
        "bubble": "#473B59",
    },

    "Golden Hour": {
        "bg": "#E7D6A5",
        "panel": "#F2E4B9",
        "card": "#D9C27D",
        "text": "#4B3C1F",
        "muted": "#806B3A",
        "accent": "#B38A24",
        "accent2": "#D0A83D",
        "border": "#C4AA60",
        "bubble": "#E7D397",
    },

    "Sage": {
        "bg": "#D9E1D6",
        "panel": "#E7EEE4",
        "card": "#C9D5C6",
        "text": "#394638",
        "muted": "#6F7F6C",
        "accent": "#718A69",
        "accent2": "#8EA486",
        "border": "#B4C2B0",
        "bubble": "#D3DED0",
    },

    "Rose": {
        "bg": "#E8D7D9",
        "panel": "#F1E4E5",
        "card": "#DDC3C6",
        "text": "#503A3E",
        "muted": "#886C71",
        "accent": "#A66F79",
        "accent2": "#C38A94",
        "border": "#C9AFB3",
        "bubble": "#E5D0D3",
    },

    "Ocean": {
        "bg": "#D4E1E3",
        "panel": "#E5EFF0",
        "card": "#C0D4D7",
        "text": "#314449",
        "muted": "#688087",
        "accent": "#628B93",
        "accent2": "#82AAB0",
        "border": "#AAC2C6",
        "bubble": "#CEE0E2",
    },

    "Blood Red": {
        "bg": "#211416",
        "panel": "#30191C",
        "card": "#422124",
        "text": "#F4E8E8",
        "muted": "#B9989A",
        "accent": "#7F2028",
        "accent2": "#A8323D",
        "border": "#5E2B30",
        "bubble": "#382023",
    },

    "Mono": {
        "bg": "#D8D8D8",
        "panel": "#E8E8E8",
        "card": "#C8C8C8",
        "text": "#303030",
        "muted": "#707070",
        "accent": "#666666",
        "accent2": "#858585",
        "border": "#B7B7B7",
        "bubble": "#D0D0D0",
    },
}


# ============================================================
# CONFIG
# ============================================================

def load_config():

    if not os.path.exists(CONFIG_FILE):

        return {
            "theme": "Glox Cream",
            "opacity": 94,
            "destinations": [dict(x) for x in DEFAULT_DESTINATIONS],
        }

    try:

        with open(
            CONFIG_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        destinations = data.get("destinations")

        if not destinations:
            destinations = [dict(x) for x in DEFAULT_DESTINATIONS]

        return {
            "theme": data.get(
                "theme",
                "Glox Cream"
            ),
            "opacity": data.get(
                "opacity",
                94
            ),
            "destinations": destinations,
        }

    except Exception:

        return {
            "theme": "Glox Cream",
            "opacity": 94,
            "destinations": [dict(x) for x in DEFAULT_DESTINATIONS],
        }


def save_config(data):

    try:

        with open(
            CONFIG_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )

    except Exception:
        pass


# ============================================================
# ROUNDED FRAME
# ============================================================

class RoundedFrame(QFrame):

    def __init__(
        self,
        radius=32,
        parent=None
    ):

        super().__init__(parent)

        self.radius = radius

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        rect = self.rect().adjusted(
            1,
            1,
            -1,
            -1
        )

        path = QPainterPath()

        path.addRoundedRect(
            rect,
            self.radius,
            self.radius
        )

        painter.fillPath(
            path,
            QBrush(
                self.palette().window().color()
            )
        )

        painter.setPen(
            QPen(
                QColor(255, 255, 255, 42),
                1
            )
        )

        painter.drawPath(path)


# ============================================================
# DESTINATION BUBBLE
# ============================================================

class DestinationBubble(QPushButton):

    toggled_destination = Signal()

    def __init__(
        self,
        destination,
        theme,
        parent=None
    ):

        super().__init__(parent)

        self.destination = destination
        self.theme = theme

        self.setCheckable(True)

        self.setChecked(
            destination.get(
                "enabled",
                True
            )
        )

        self.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.setFixedHeight(39)

        self.refresh()

    def refresh(self):

        t = self.theme

        self.setText(
            "●  " +
            self.destination.get(
                "title",
                "Website"
            )
        )

        self.setStyleSheet(f"""
            QPushButton {{
                background: {t["bubble"]};
                color: {t["text"]};
                border: 1px solid {t["border"]};
                border-radius: 19px;
                padding: 0px 15px;
                font-size: 11px;
                font-weight: 600;
            }}

            QPushButton:hover {{
                background: {t["card"]};
                border-color: {t["accent"]};
            }}

            QPushButton:checked {{
                background: {t["accent"]};
                color: white;
                border-color: {t["accent"]};
            }}

            QPushButton:pressed {{
                padding-top: 2px;
            }}
        """)

    def mouseReleaseEvent(self, event):

        super().mouseReleaseEvent(event)

        self.destination["enabled"] = (
            self.isChecked()
        )

        self.toggled_destination.emit()


# ============================================================
# COLLAPSED DRAG BUTTON
# ============================================================

class CollapsedButton(QPushButton):

    moved = Signal()
    clicked_to_expand = Signal()

    def __init__(
        self,
        theme,
        parent=None
    ):

        super().__init__(parent)

        self.theme = theme

        self.drag_start = None
        self.was_dragged = False

        self.setText("GLOX")

        self.setFixedSize(
            100,
            50
        )

        self.setCursor(
            Qt.CursorShape.OpenHandCursor
        )

        self.apply_theme()

    def apply_theme(self):

        t = self.theme

        self.setStyleSheet(
            f"""
            QPushButton {{
                background: {t["accent"]};
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 12px;
                font-weight: 700;
                letter-spacing: 1px;
            }}

            QPushButton:hover {{
                background: {t["accent2"]};
            }}

            QPushButton:pressed {{
                padding-top: 2px;
            }}
            """
        )

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:

            self.drag_start = (
                event.globalPosition().toPoint()
            )

            self.was_dragged = False

            self.setCursor(
                Qt.CursorShape.ClosedHandCursor
            )

            event.accept()

            return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):

        if (
            self.drag_start is not None
            and
            event.buttons()
            &
            Qt.MouseButton.LeftButton
        ):

            current = (
                event.globalPosition().toPoint()
            )

            delta = (
                current -
                self.drag_start
            )

            if (
                abs(delta.x()) > 3
                or
                abs(delta.y()) > 3
            ):

                self.was_dragged = True

                window = self.window()

                window.move(
                    window.pos() + delta
                )

                self.drag_start = current

                self.moved.emit()

            event.accept()

            return

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):

        self.setCursor(
            Qt.CursorShape.OpenHandCursor
        )

        if (
            event.button()
            ==
            Qt.MouseButton.LeftButton
        ):

            if not self.was_dragged:

                self.clicked_to_expand.emit()

            self.drag_start = None

            event.accept()

            return

        super().mouseReleaseEvent(event)


# ============================================================
# ADD WEBSITE
# ============================================================

class AddWebsiteDialog(QDialog):

    def __init__(
        self,
        theme,
        parent=None
    ):

        super().__init__(parent)

        self.theme = theme
        self.result_data = None

        self.setWindowTitle(
            "Add Destination"
        )

        self.setFixedSize(
            430,
            285
        )

        self.build()

    def build(self):

        t = self.theme

        self.setStyleSheet(
            f"""
            QDialog {{
                background: {t["panel"]};
            }}

            QLabel {{
                color: {t["text"]};
            }}

            QLineEdit {{
                background: {t["card"]};
                color: {t["text"]};
                border: 1px solid {t["border"]};
                border-radius: 12px;
                padding: 10px 12px;
            }}

            QCheckBox {{
                color: {t["text"]};
            }}
            """
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            25,
            22,
            25,
            22
        )

        layout.setSpacing(12)

        heading = QLabel(
            "Add website"
        )

        heading.setFont(
            QFont(
                "Segoe UI",
                15,
                QFont.Weight.Bold
            )
        )

        description = QLabel(
            "Create a custom Glox destination."
        )

        description.setStyleSheet(
            f"color: {t['muted']};"
        )

        self.title_input = QLineEdit()

        self.title_input.setPlaceholderText(
            "Title   e.g. Perplexity"
        )

        self.url_input = QLineEdit()

        self.url_input.setPlaceholderText(
            "https://example.com"
        )

        self.submit_check = QCheckBox(
            "Press Enter after pasting"
        )

        self.submit_check.setChecked(True)

        buttons = QHBoxLayout()

        cancel = QPushButton(
            "Cancel"
        )

        add = QPushButton(
            "Add"
        )

        for button in (
            cancel,
            add
        ):

            button.setFixedHeight(
                38
            )

            button.setCursor(
                Qt.CursorShape.PointingHandCursor
            )

        cancel.setStyleSheet(
            f"""
            QPushButton {{
                background: {t["card"]};
                color: {t["text"]};
                border: none;
                border-radius: 19px;
                padding: 0 20px;
            }}
            """
        )

        add.setStyleSheet(
            f"""
            QPushButton {{
                background: {t["accent"]};
                color: white;
                border: none;
                border-radius: 19px;
                padding: 0 25px;
                font-weight: 600;
            }}

            QPushButton:hover {{
                background: {t["accent2"]};
            }}
            """
        )

        cancel.clicked.connect(
            self.reject
        )

        add.clicked.connect(
            self.accept_destination
        )

        buttons.addStretch()

        buttons.addWidget(
            cancel
        )

        buttons.addWidget(
            add
        )

        layout.addWidget(
            heading
        )

        layout.addWidget(
            description
        )

        layout.addSpacing(5)

        layout.addWidget(
            self.title_input
        )

        layout.addWidget(
            self.url_input
        )

        layout.addWidget(
            self.submit_check
        )

        layout.addStretch()

        layout.addLayout(
            buttons
        )

    def accept_destination(self):

        title = (
            self.title_input
            .text()
            .strip()
        )

        url = (
            self.url_input
            .text()
            .strip()
        )

        if not title:

            QMessageBox.warning(
                self,
                "Missing title",
                "Enter a title."
            )

            return

        if not url.startswith(
            (
                "http://",
                "https://"
            )
        ):

            QMessageBox.warning(
                self,
                "Invalid URL",
                "URL must begin with http:// or https://"
            )

            return

        self.result_data = {
            "title": title,
            "url": url,
            "enabled": True,
            "submit": self.submit_check.isChecked(),
        }

        self.accept()


# ============================================================
# MAIN WIDGET
# ============================================================

class GloxRelay(QWidget):

    def __init__(self):

        super().__init__()

        self.config = load_config()

        self.theme_name = self.config.get(
            "theme",
            "Glox Cream"
        )

        if self.theme_name not in THEMES:
            self.theme_name = "Glox Cream"

        self.opacity_value = self.config.get(
            "opacity",
            94
        )

        self.destinations = self.config.get(
            "destinations",
            [dict(x) for x in DEFAULT_DESTINATIONS]
        )

        self.collapsed = False
        self.old_geometry = None

        self.drag_pos = None

        self.relay_running = False
        self.relay_queue = []
        self.relay_prompt_text = ""
        self.current_destination_index = 0

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            |
            Qt.WindowType.WindowStaysOnTopHint
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.resize(
            650,
            600
        )

        self.build_ui()

        self.apply_theme()

        self.create_bubbles()

    # ========================================================
    # BUILD
    # ========================================================

    def build_ui(self):

        self.root = RoundedFrame(
            34,
            self
        )

        self.root_layout = QVBoxLayout(
            self.root
        )

        self.root_layout.setContentsMargins(
            25,
            20,
            25,
            22
        )

        self.root_layout.setSpacing(
            11
        )

        header = QHBoxLayout()

        logo = QLabel("G")

        logo.setObjectName(
            "logo"
        )

        logo.setFixedSize(
            36,
            36
        )

        logo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        logo.setFont(
            QFont(
                "Segoe UI",
                15,
                QFont.Weight.Bold
            )
        )

        title_box = QVBoxLayout()

        title_box.setSpacing(
            0
        )

        self.title_label = QLabel(
            "GLOX RELAY"
        )

        self.title_label.setFont(
            QFont(
                "Segoe UI",
                13,
                QFont.Weight.Bold
            )
        )

        self.subtitle_label = QLabel(
            "one prompt  •  everywhere"
        )

        title_box.addWidget(
            self.title_label
        )

        title_box.addWidget(
            self.subtitle_label
        )

        self.settings_button = QPushButton(
            "⚙"
        )

        self.settings_button.setFixedSize(
            35,
            35
        )

        self.settings_button.clicked.connect(
            self.open_settings
        )

        self.hide_button = QPushButton(
            "—"
        )

        self.hide_button.setFixedSize(
            35,
            35
        )

        self.hide_button.clicked.connect(
            self.collapse_widget
        )

        self.quit_button = QPushButton(
            "×"
        )

        self.quit_button.setFixedSize(
            35,
            35
        )

        self.quit_button.clicked.connect(
            QApplication.quit
        )

        header.addWidget(
            logo
        )

        header.addLayout(
            title_box
        )

        header.addStretch()

        header.addWidget(
            self.settings_button
        )

        header.addWidget(
            self.hide_button
        )

        header.addWidget(
            self.quit_button
        )

        self.root_layout.addLayout(
            header
        )

        # ----------------------------------------------------
        # PROMPT
        # ----------------------------------------------------

        self.prompt = QTextEdit()

        self.prompt.setAcceptRichText(
            False
        )

        self.prompt.setPlaceholderText(
            "Write one prompt and send it everywhere..."
        )

        self.prompt.setMinimumHeight(
            275
        )

        self.root_layout.addWidget(
            self.prompt
        )

        # ----------------------------------------------------
        # DESTINATIONS
        # ----------------------------------------------------

        destination_header = QHBoxLayout()

        destination_title = QLabel(
            "DESTINATIONS"
        )

        destination_title.setFont(
            QFont(
                "Segoe UI",
                9,
                QFont.Weight.Bold
            )
        )

        self.selected_label = QLabel(
            "0 selected"
        )

        destination_header.addWidget(
            destination_title
        )

        destination_header.addStretch()

        destination_header.addWidget(
            self.selected_label
        )

        self.root_layout.addLayout(
            destination_header
        )

        self.bubble_frame = QFrame()

        self.bubble_layout = QHBoxLayout(
            self.bubble_frame
        )

        self.bubble_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.bubble_layout.setSpacing(
            7
        )

        self.root_layout.addWidget(
            self.bubble_frame
        )

        # ----------------------------------------------------
        # ADD
        # ----------------------------------------------------

        self.add_button = QPushButton(
            "+ Add website"
        )

        self.add_button.setFixedHeight(
            36
        )

        self.add_button.clicked.connect(
            self.add_destination
        )

        self.root_layout.addWidget(
            self.add_button
        )

        # ----------------------------------------------------
        # SEND
        # ----------------------------------------------------

        self.send_button = QPushButton(
            "RELAY PROMPT   →"
        )

        self.send_button.setFixedHeight(
            52
        )

        self.send_button.clicked.connect(
            self.start_relay
        )

        self.root_layout.addWidget(
            self.send_button
        )

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        self.status = QLabel(
            "Ready"
        )

        self.status.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.root_layout.addWidget(
            self.status
        )

    # ========================================================
    # THEME
    # ========================================================

    def apply_theme(self):

        t = THEMES[
            self.theme_name
        ]

        self.setWindowOpacity(
            self.opacity_value / 100
        )

        self.root.setStyleSheet(
            f"""
            QFrame {{
                background: {t["panel"]};
            }}
            """
        )

        self.title_label.setStyleSheet(
            f"color: {t['text']};"
        )

        self.subtitle_label.setStyleSheet(
            f"""
            color: {t["muted"]};
            font-size: 10px;
            """
        )

        self.selected_label.setStyleSheet(
            f"""
            color: {t["muted"]};
            font-size: 10px;
            """
        )

        self.status.setStyleSheet(
            f"""
            color: {t["muted"]};
            font-size: 10px;
            """
        )

        self.prompt.setStyleSheet(
            f"""
            QTextEdit {{
                background: {t["bg"]};
                color: {t["text"]};
                border: 1px solid {t["border"]};
                border-radius: 25px;
                padding: 18px;
                font-size: 14px;
            }}

            QTextEdit:focus {{
                border: 1px solid {t["accent"]};
            }}
            """
        )

        logo = self.root.findChild(
            QLabel,
            "logo"
        )

        logo.setStyleSheet(
            f"""
            QLabel {{
                background: {t["accent"]};
                color: white;
                border-radius: 18px;
            }}
            """
        )

        small_button_style = f"""
            QPushButton {{
                background: {t["card"]};
                color: {t["text"]};
                border: 1px solid {t["border"]};
                border-radius: 17px;
                font-size: 15px;
            }}

            QPushButton:hover {{
                background: {t["accent"]};
                color: white;
            }}
        """

        self.settings_button.setStyleSheet(
            small_button_style
        )

        self.hide_button.setStyleSheet(
            small_button_style
        )

        self.quit_button.setStyleSheet(
            small_button_style
        )

        self.add_button.setStyleSheet(
            f"""
            QPushButton {{
                background: transparent;
                color: {t["muted"]};
                border: 1px dashed {t["border"]};
                border-radius: 18px;
                font-size: 11px;
            }}

            QPushButton:hover {{
                background: {t["card"]};
                color: {t["text"]};
            }}
            """
        )

        self.send_button.setStyleSheet(
            f"""
            QPushButton {{
                background: {t["accent"]};
                color: white;
                border: none;
                border-radius: 26px;
                font-size: 12px;
                font-weight: 700;
                letter-spacing: 1px;
            }}

            QPushButton:hover {{
                background: {t["accent2"]};
            }}

            QPushButton:pressed {{
                padding-top: 3px;
            }}

            QPushButton:disabled {{
                background: {t["border"]};
                color: {t["muted"]};
            }}
            """
        )

        self.update_bubbles_theme()

        self.update()

        QApplication.processEvents()

    # ========================================================
    # RIGHT CLICK MENU
    # ========================================================

    def contextMenuEvent(
        self,
        event
    ):

        menu = QMenu(
            self
        )

        t = THEMES[
            self.theme_name
        ]

        menu.setStyleSheet(
            f"""
            QMenu {{
                background: {t["panel"]};
                color: {t["text"]};
                border: 1px solid {t["border"]};
                padding: 6px;
            }}

            QMenu::item {{
                padding: 8px 18px;
                border-radius: 8px;
            }}

            QMenu::item:selected {{
                background: {t["accent"]};
                color: white;
            }}

            QMenu::separator {{
                height: 1px;
                background: {t["border"]};
                margin: 5px 10px;
            }}
            """
        )

        theme_menu = menu.addMenu(
            "Background / Theme"
        )

        for name in THEMES:

            action = QAction(
                name,
                self
            )

            action.setCheckable(
                True
            )

            action.setChecked(
                name == self.theme_name
            )

            action.triggered.connect(
                lambda checked=False,
                selected=name:
                self.change_theme(
                    selected
                )
            )

            theme_menu.addAction(
                action
            )

        menu.addSeparator()

        opacity_menu = menu.addMenu(
            "Opacity"
        )

        for opacity in (
            70,
            75,
            80,
            85,
            90,
            95,
            100
        ):

            action = QAction(
                f"{opacity}%",
                self
            )

            action.setCheckable(
                True
            )

            action.setChecked(
                opacity ==
                self.opacity_value
            )

            action.triggered.connect(
                lambda checked=False,
                value=opacity:
                self.change_opacity(
                    value
                )
            )

            opacity_menu.addAction(
                action
            )

        menu.addSeparator()

        add_action = QAction(
            "+ Add Website",
            self
        )

        add_action.triggered.connect(
            self.add_destination
        )

        menu.addAction(
            add_action
        )

        # ----------------------------------------------------
        # REMOVE WEBSITE
        # ----------------------------------------------------

        if self.destinations:

            remove_menu = menu.addMenu(
                "Remove Website"
            )

            for index, destination in enumerate(
                self.destinations
            ):

                title = destination.get(
                    "title",
                    "Website"
                )

                remove_action = QAction(
                    f"Remove {title}",
                    self
                )

                remove_action.triggered.connect(
                    lambda checked=False,
                    idx=index:
                    self.remove_destination(idx)
                )

                remove_menu.addAction(
                    remove_action
                )

        menu.addSeparator()

        hide_action = QAction(
            "Hide Glox Relay",
            self
        )

        hide_action.triggered.connect(
            self.collapse_widget
        )

        menu.addAction(
            hide_action
        )

        menu.exec(
            event.globalPos()
        )

    def remove_destination(self, index):

        if index < 0 or index >= len(self.destinations):
            return

        destination = self.destinations[index]

        title = destination.get(
            "title",
            "Website"
        )

        self.destinations.pop(index)

        self.create_bubbles()

        self.save()

        self.status.setText(
            f"Removed {title}"
        )

        QTimer.singleShot(
            1800,
            lambda: self.status.setText("Ready")
        )

    def change_theme(
        self,
        name
    ):

        if name not in THEMES:
            return

        self.theme_name = name

        self.apply_theme()

        self.create_bubbles()

        self.save()

    def change_opacity(
        self,
        value
    ):

        self.opacity_value = value

        self.setWindowOpacity(
            value / 100
        )

        self.save()

    # ========================================================
    # DESTINATION BUBBLES
    # ========================================================

    def create_bubbles(self):

        while self.bubble_layout.count():

            item = self.bubble_layout.takeAt(
                0
            )

            if item.widget():

                item.widget().deleteLater()

        t = THEMES[
            self.theme_name
        ]

        for destination in self.destinations:

            bubble = DestinationBubble(
                destination,
                t,
                self.bubble_frame
            )

            bubble.toggled_destination.connect(
                self.destination_toggled
            )

            self.bubble_layout.addWidget(
                bubble
            )

        self.bubble_layout.addStretch()

        self.update_selected()

    def update_bubbles_theme(self):

        t = THEMES[
            self.theme_name
        ]

        for bubble in self.bubble_frame.findChildren(
            DestinationBubble
        ):

            bubble.theme = t

            bubble.refresh()

    def update_selected(self):

        count = sum(
            1
            for d in self.destinations
            if d.get(
                "enabled",
                True
            )
        )

        self.selected_label.setText(
            f"{count} selected"
        )

    def destination_toggled(self):

        self.update_selected()

        self.save()

    # ========================================================
    # ADD WEBSITE
    # ========================================================

    def add_destination(self):

        dialog = AddWebsiteDialog(
            THEMES[
                self.theme_name
            ],
            self
        )

        if (
            dialog.exec()
            ==
            QDialog.DialogCode.Accepted
        ):

            self.destinations.append(
                dialog.result_data
            )

            self.create_bubbles()

            self.save()

    # ========================================================
    # RELAY
    # ========================================================

    def start_relay(self):

        prompt_text = (
            self.prompt
            .toPlainText()
            .strip()
        )

        if not prompt_text:

            self.status.setText(
                "Write a prompt first."
            )

            return

        selected = [
            destination
            for destination in self.destinations
            if destination.get(
                "enabled",
                True
            )
        ]

        if not selected:

            self.status.setText(
                "Select at least one destination."
            )

            return

        self.relay_prompt_text = (
            prompt_text
        )

        self.relay_queue = (
            selected
        )

        self.current_destination_index = 0

        self.relay_running = True

        self.send_button.setEnabled(
            False
        )

        QApplication.clipboard().setText(
            self.relay_prompt_text
        )

        self.status.setText(
            "Starting relay..."
        )

        QTimer.singleShot(
            250,
            self.relay_next
        )

    def relay_next(self):

        if not self.relay_running:
            return

        if (
            self.current_destination_index
            >= len(self.relay_queue)
        ):

            self.finish_relay()

            return

        destination = self.relay_queue[
            self.current_destination_index
        ]

        title = destination.get(
            "title",
            "Website"
        )

        url = destination.get(
            "url",
            ""
        )

        self.status.setText(
            f"Opening {title}..."
        )

        try:

            webbrowser.open_new_tab(
                url
            )

        except Exception:

            self.status.setText(
                f"Could not open {title}"
            )

            self.next_destination()

            return

        QTimer.singleShot(
            4500,
            self.paste_current
        )

    def paste_current(self):

        if not self.relay_running:
            return

        destination = self.relay_queue[
            self.current_destination_index
        ]

        title = destination.get(
            "title",
            "Website"
        )

        self.status.setText(
            f"Sending to {title}..."
        )

        QApplication.clipboard().setText(
            self.relay_prompt_text
        )

        QTimer.singleShot(
            250,
            self.execute_paste
        )

    def execute_paste(self):

        try:

            import pyautogui

            pyautogui.hotkey(
                "ctrl",
                "v"
            )

            destination = self.relay_queue[
                self.current_destination_index
            ]

            if destination.get(
                "submit",
                True
            ):

                QTimer.singleShot(
                    600,
                    self.execute_enter
                )

            else:

                QTimer.singleShot(
                    600,
                    self.next_destination
                )

        except Exception as error:

            self.status.setText(
                f"Paste failed: {error}"
            )

            QTimer.singleShot(
                500,
                self.next_destination
            )

    def execute_enter(self):

        try:

            import pyautogui

            pyautogui.press(
                "enter"
            )

        except Exception:
            pass

        QTimer.singleShot(
            1000,
            self.next_destination
        )

    def next_destination(self):

        self.current_destination_index += 1

        QTimer.singleShot(
            500,
            self.relay_next
        )

    def finish_relay(self):

        self.relay_running = False

        self.send_button.setEnabled(
            True
        )

        self.status.setText(
            "✓ Prompt relayed everywhere"
        )

        QTimer.singleShot(
            3500,
            lambda:
            self.status.setText(
                "Ready"
            )
        )

    # ========================================================
    # COLLAPSE
    # ========================================================

    def collapse_widget(self):

        if self.collapsed:
            return

        self.collapsed = True

        self.old_geometry = (
            self.geometry()
        )

        animation = QPropertyAnimation(
            self,
            b"geometry"
        )

        animation.setDuration(
            350
        )

        animation.setEasingCurve(
            QEasingCurve.Type.OutCubic
        )

        start = self.geometry()

        end = QRect(
            start.x(),
            start.y(),
            100,
            50
        )

        animation.setStartValue(
            start
        )

        animation.setEndValue(
            end
        )

        animation.finished.connect(
            self.finish_collapse
        )

        self.collapse_animation = animation

        animation.start()

    def finish_collapse(self):

        self.root.hide()

        self.collapsed_button = (
            CollapsedButton(
                THEMES[
                    self.theme_name
                ],
                self
            )
        )

        self.collapsed_button.setGeometry(
            0,
            0,
            100,
            50
        )

        self.collapsed_button.clicked_to_expand.connect(
            self.expand_widget
        )

        self.collapsed_button.show()

    # ========================================================
    # EXPAND
    # ========================================================

    def expand_widget(self):

        if not self.collapsed:
            return

        self.collapsed_button.hide()

        self.root.show()

        current = self.geometry()

        target = self.old_geometry

        animation = QPropertyAnimation(
            self,
            b"geometry"
        )

        animation.setDuration(
            400
        )

        animation.setEasingCurve(
            QEasingCurve.Type.OutBack
        )

        animation.setStartValue(
            current
        )

        animation.setEndValue(
            target
        )

        animation.finished.connect(
            self.expansion_finished
        )

        self.expand_animation = animation

        animation.start()

    def expansion_finished(self):

        if hasattr(
            self,
            "collapsed_button"
        ):

            self.collapsed_button.deleteLater()

        self.collapsed = False

    # ========================================================
    # MAIN WIDGET DRAGGING
    # ========================================================

    def mousePressEvent(
        self,
        event
    ):

        if (
            event.button()
            ==
            Qt.MouseButton.LeftButton
        ):

            self.drag_pos = (
                event.globalPosition().toPoint()
                -
                self.frameGeometry().topLeft()
            )

            event.accept()

            return

        super().mousePressEvent(
            event
        )

    def mouseMoveEvent(
        self,
        event
    ):

        if (
            self.drag_pos is not None
            and
            event.buttons()
            &
            Qt.MouseButton.LeftButton
        ):

            self.move(
                event.globalPosition().toPoint()
                -
                self.drag_pos
            )

            event.accept()

            return

        super().mouseMoveEvent(
            event
        )

    def mouseReleaseEvent(
        self,
        event
    ):

        self.drag_pos = None

        super().mouseReleaseEvent(
            event
        )

    # ========================================================
    # SETTINGS
    # ========================================================

    def open_settings(self):

        dialog = QDialog(
            self
        )

        dialog.setWindowTitle(
            "Glox Relay Settings"
        )

        dialog.setFixedSize(
            410,
            315
        )

        t = THEMES[
            self.theme_name
        ]

        dialog.setStyleSheet(
            f"""
            QDialog {{
                background: {t["panel"]};
            }}

            QLabel {{
                color: {t["text"]};
            }}

            QComboBox {{
                background: {t["card"]};
                color: {t["text"]};
                border: 1px solid {t["border"]};
                border-radius: 10px;
                padding: 8px;
            }}

            QSlider::groove:horizontal {{
                height: 5px;
                background: {t["border"]};
                border-radius: 2px;
            }}

            QSlider::handle:horizontal {{
                width: 15px;
                margin: -5px 0;
                background: {t["accent"]};
                border-radius: 8px;
            }}
            """
        )

        layout = QVBoxLayout(
            dialog
        )

        layout.setContentsMargins(
            25,
            22,
            25,
            22
        )

        heading = QLabel(
            "Appearance"
        )

        heading.setFont(
            QFont(
                "Segoe UI",
                15,
                QFont.Weight.Bold
            )
        )

        layout.addWidget(
            heading
        )

        layout.addWidget(
            QLabel("Theme")
        )

        theme_combo = QComboBox()

        theme_combo.addItems(
            list(THEMES.keys())
        )

        theme_combo.setCurrentText(
            self.theme_name
        )

        layout.addWidget(
            theme_combo
        )

        layout.addWidget(
            QLabel("Opacity")
        )

        opacity_slider = QSlider(
            Qt.Orientation.Horizontal
        )

        opacity_slider.setRange(
            70,
            100
        )

        opacity_slider.setValue(
            self.opacity_value
        )

        layout.addWidget(
            opacity_slider
        )

        opacity_label = QLabel(
            f"{self.opacity_value}%"
        )

        layout.addWidget(
            opacity_label
        )

        def theme_changed(
            name
        ):

            self.change_theme(
                name
            )

            dialog.setStyleSheet(
                f"""
                QDialog {{
                    background: {THEMES[name]["panel"]};
                }}

                QLabel {{
                    color: {THEMES[name]["text"]};
                }}

                QComboBox {{
                    background: {THEMES[name]["card"]};
                    color: {THEMES[name]["text"]};
                    border: 1px solid {THEMES[name]["border"]};
                    border-radius: 10px;
                    padding: 8px;
                }}
                """
            )

        def opacity_changed(
            value
        ):

            opacity_label.setText(
                f"{value}%"
            )

            self.change_opacity(
                value
            )

        theme_combo.currentTextChanged.connect(
            theme_changed
        )

        opacity_slider.valueChanged.connect(
            opacity_changed
        )

        layout.addStretch()

        done = QPushButton(
            "Done"
        )

        done.setFixedHeight(
            40
        )

        done.setStyleSheet(
            f"""
            QPushButton {{
                background: {t["accent"]};
                color: white;
                border: none;
                border-radius: 20px;
                font-weight: 600;
            }}

            QPushButton:hover {{
                background: {t["accent2"]};
            }}
            """
        )

        done.clicked.connect(
            dialog.accept
        )

        layout.addWidget(
            done
        )

        dialog.exec()

    # ========================================================
    # SAVE
    # ========================================================

    def save(self):

        save_config(
            {
                "theme": self.theme_name,
                "opacity": self.opacity_value,
                "destinations": self.destinations,
            }
        )

    # ========================================================
    # SHADOW
    # ========================================================

    def showEvent(
        self,
        event
    ):

        super().showEvent(
            event
        )

        shadow = QGraphicsDropShadowEffect(
            self
        )

        shadow.setBlurRadius(
            45
        )

        shadow.setOffset(
            0,
            12
        )

        shadow.setColor(
            QColor(
                0,
                0,
                0,
                75
            )
        )

        self.root.setGraphicsEffect(
            shadow
        )


# ============================================================
# MAIN
# ============================================================

def main():

    app = QApplication(
        sys.argv
    )

    app.setApplicationName(
        APP_NAME
    )

    app.setStyle(
        "Fusion"
    )

    widget = GloxRelay()

    screen = app.primaryScreen()

    if screen:

        available = (
            screen.availableGeometry()
        )

        widget.move(
            available.center()
            -
            widget.rect().center()
        )

    widget.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()