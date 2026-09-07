import sys
import os
import json
import uuid
import subprocess

from PySide6.QtCore import Qt, QRectF, QPropertyAnimation, Property
from PySide6.QtGui import QColor, QPainter, QPen, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QLineEdit,
    QTextEdit,
    QDialog,
    QDialogButtonBox,
    QComboBox,
    QMessageBox,
    QScrollArea,
    QFrame,
    QGraphicsDropShadowEffect,
)


# ============================================================
# STORAGE
# ============================================================

APP_NAME = "Glox Library"

APP_DIR = os.path.join(
    os.path.expanduser("~"),
    ".gloxlibrary"
)

DATA_FILE = os.path.join(
    APP_DIR,
    "games.json"
)


def ensure_storage():
    os.makedirs(APP_DIR, exist_ok=True)

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)


def load_games():
    ensure_storage()

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_games(games):
    ensure_storage()

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(games, f, indent=4)


# ============================================================
# 20 THEMES
# ============================================================

THEMES = {

    "Obsidian": {
        "bg": "#080808",
        "panel": "#101010",
        "library": "#0D0D0D",
        "card": "#191919",
        "text": "#F5F5F5",
        "subtext": "#969696",
        "accent": "#FFFFFF",
        "accent2": "#777777",
        "green": "#22C55E",
    },

    "Arctic": {
        "bg": "#DCECF3",
        "panel": "#C8DDE6",
        "library": "#D3E5EC",
        "card": "#B6D0DB",
        "text": "#10242D",
        "subtext": "#55717D",
        "accent": "#0E7490",
        "accent2": "#38BDF8",
        "green": "#15803D",
    },

    "Midnight Blue": {
        "bg": "#060A18",
        "panel": "#0D1430",
        "library": "#0A1026",
        "card": "#151F43",
        "text": "#F2F5FF",
        "subtext": "#98A4C8",
        "accent": "#3B82F6",
        "accent2": "#6366F1",
        "green": "#22C55E",
    },

    "Ocean": {
        "bg": "#04151C",
        "panel": "#082731",
        "library": "#061F29",
        "card": "#0D3844",
        "text": "#ECFEFF",
        "subtext": "#89B6C0",
        "accent": "#06B6D4",
        "accent2": "#0891B2",
        "green": "#22C55E",
    },

    "Emerald": {
        "bg": "#071A13",
        "panel": "#0D2A1D",
        "library": "#0A2419",
        "card": "#123825",
        "text": "#F0FFF7",
        "subtext": "#8BB69E",
        "accent": "#10B981",
        "accent2": "#34D399",
        "green": "#22C55E",
    },

    "Forest": {
        "bg": "#0B120B",
        "panel": "#162316",
        "library": "#111E12",
        "card": "#213322",
        "text": "#F4FFF2",
        "subtext": "#9AAA95",
        "accent": "#65A30D",
        "accent2": "#84CC16",
        "green": "#22C55E",
    },

    "Neon Lime": {
        "bg": "#090D05",
        "panel": "#141B09",
        "library": "#101707",
        "card": "#1E290D",
        "text": "#F7FFE9",
        "subtext": "#B4C59B",
        "accent": "#A3FF12",
        "accent2": "#65D300",
        "green": "#65D300",
    },

    "Cyber Cyan": {
        "bg": "#030D10",
        "panel": "#07191E",
        "library": "#051419",
        "card": "#0B252C",
        "text": "#E9FDFF",
        "subtext": "#82B8C0",
        "accent": "#00E5FF",
        "accent2": "#00A8CC",
        "green": "#00E676",
    },

    "Violet": {
        "bg": "#10081A",
        "panel": "#1A0E2A",
        "library": "#160C23",
        "card": "#27133B",
        "text": "#F8F0FF",
        "subtext": "#B89AC9",
        "accent": "#A855F7",
        "accent2": "#7C3AED",
        "green": "#22C55E",
    },

    "Royal Purple": {
        "bg": "#12091F",
        "panel": "#211035",
        "library": "#1B0D2B",
        "card": "#30174D",
        "text": "#FAF5FF",
        "subtext": "#C2A7D6",
        "accent": "#8B5CF6",
        "accent2": "#C084FC",
        "green": "#22C55E",
    },

    "Rose": {
        "bg": "#1A0810",
        "panel": "#2B0F1B",
        "library": "#230B17",
        "card": "#3B1526",
        "text": "#FFF5F8",
        "subtext": "#D2A0B0",
        "accent": "#F43F5E",
        "accent2": "#FB7185",
        "green": "#22C55E",
    },

    "Crimson": {
        "bg": "#170607",
        "panel": "#280B0E",
        "library": "#21090C",
        "card": "#3A1115",
        "text": "#FFF4F4",
        "subtext": "#C99699",
        "accent": "#E11D48",
        "accent2": "#EF4444",
        "green": "#22C55E",
    },

    "Inferno": {
        "bg": "#180A05",
        "panel": "#2A1007",
        "library": "#220D06",
        "card": "#3B180B",
        "text": "#FFF5EC",
        "subtext": "#D0A28C",
        "accent": "#F97316",
        "accent2": "#EF4444",
        "green": "#22C55E",
    },

    "Sunset": {
        "bg": "#1A0B12",
        "panel": "#2C111E",
        "library": "#240E19",
        "card": "#3D1930",
        "text": "#FFF6FA",
        "subtext": "#D2A1B8",
        "accent": "#FB7185",
        "accent2": "#F97316",
        "green": "#22C55E",
    },

    "Amber": {
        "bg": "#181004",
        "panel": "#291B07",
        "library": "#211606",
        "card": "#3A280B",
        "text": "#FFF9E7",
        "subtext": "#CFB67C",
        "accent": "#F59E0B",
        "accent2": "#FBBF24",
        "green": "#22C55E",
    },

    "Gold": {
        "bg": "#171408",
        "panel": "#27220D",
        "library": "#211D0B",
        "card": "#383215",
        "text": "#FFFCEB",
        "subtext": "#C8BB85",
        "accent": "#EAB308",
        "accent2": "#FACC15",
        "green": "#22C55E",
    },

    "Espresso": {
        "bg": "#17100C",
        "panel": "#241912",
        "library": "#1F1510",
        "card": "#302218",
        "text": "#FFF8EF",
        "subtext": "#BBA999",
        "accent": "#C08457",
        "accent2": "#8B5E3C",
        "green": "#4FA46D",
    },

    "Glox Cream": {
        "bg": "#E8DED0",
        "panel": "#D7CABB",
        "library": "#E0D5C7",
        "card": "#C6B5A3",
        "text": "#2B2018",
        "subtext": "#746356",
        "accent": "#805C3E",
        "accent2": "#A67C5B",
        "green": "#3F7F54",
    },

    "Slate": {
        "bg": "#101214",
        "panel": "#191C1F",
        "library": "#15181B",
        "card": "#23272B",
        "text": "#F1F3F5",
        "subtext": "#9AA1A8",
        "accent": "#94A3B8",
        "accent2": "#64748B",
        "green": "#22C55E",
    },

    "Monochrome": {
        "bg": "#EDEDED",
        "panel": "#DCDCDC",
        "library": "#E5E5E5",
        "card": "#C8C8C8",
        "text": "#111111",
        "subtext": "#555555",
        "accent": "#222222",
        "accent2": "#666666",
        "green": "#228B22",
    },
}


# ============================================================
# GLOW BORDER
# ============================================================

class GlowBorder(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._strength = 0.0
        self.color = QColor("#FFFFFF")

        self.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )

    def get_strength(self):
        return self._strength

    def set_strength(self, value):
        self._strength = value
        self.update()

    strength = Property(
        float,
        get_strength,
        set_strength
    )

    def set_color(self, color):
        self.color = QColor(color)
        self.update()

    def paintEvent(self, event):

        if self._strength <= 0:
            return

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        for i in range(16, 0, -1):

            alpha = int(
                (i / 16)
                * 30
                * self._strength
            )

            color = QColor(self.color)
            color.setAlpha(alpha)

            painter.setPen(
                QPen(
                    color,
                    i * 1.3
                )
            )

            painter.drawRoundedRect(
                QRectF(
                    i,
                    i,
                    self.width() - i * 2,
                    self.height() - i * 2
                ),
                18,
                18
            )

        border = QColor(self.color)
        border.setAlpha(
            int(245 * self._strength)
        )

        painter.setPen(
            QPen(
                border,
                1.6
            )
        )

        painter.drawRoundedRect(
            QRectF(
                1,
                1,
                self.width() - 2,
                self.height() - 2
            ),
            18,
            18
        )


# ============================================================
# GAME CARD
# ============================================================

class GameCard(QFrame):

    def __init__(
        self,
        game,
        theme,
        callback,
        parent=None
    ):
        super().__init__(parent)

        self.game = game
        self.theme = theme
        self.callback = callback

        self.setFixedSize(
            190,
            285
        )

        self.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.setObjectName(
            "gameCard"
        )

        # ----------------------------------------------------
        # COVER
        # ----------------------------------------------------

        self.cover = QLabel(self)

        self.cover.setGeometry(
            0,
            0,
            190,
            285
        )

        self.cover.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.cover.setObjectName(
            "cover"
        )

        self.load_cover()

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        self.title = QLabel(
            game.get(
                "title",
                "Unknown Game"
            ),
            self
        )

        self.title.setGeometry(
            0,
            238,
            190,
            47
        )

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.title.setWordWrap(True)

        # ----------------------------------------------------
        # GLOW
        # ----------------------------------------------------

        self.glow = GlowBorder(self)

        self.glow.setGeometry(
            0,
            0,
            190,
            285
        )

        self.glow_animation = QPropertyAnimation(
            self.glow,
            b"strength"
        )

        self.glow_animation.setDuration(
            200
        )

        self.apply_theme()

    def load_cover(self):

        path = self.game.get(
            "cover",
            ""
        )

        if os.path.exists(path):

            pixmap = QPixmap(path)

            if not pixmap.isNull():

                pixmap = pixmap.scaled(
                    190,
                    285,
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation
                )

                self.cover.setPixmap(
                    pixmap
                )

    def apply_theme(self):

        t = self.theme

        # IMPORTANT:
        # Card itself now receives the theme color.

        self.setStyleSheet(f"""
            QFrame#gameCard {{
                background: {t["card"]};
                border: 1px solid rgba(255,255,255,25);
                border-radius: 18px;
            }}
        """)

        self.cover.setStyleSheet(f"""
            background: {t["card"]};
            border-radius: 18px;
        """)

        self.title.setStyleSheet(f"""
            color: {t["text"]};
            background: rgba(0,0,0,145);
            border-bottom-left-radius: 18px;
            border-bottom-right-radius: 18px;
            padding: 7px;
            font-size: 13px;
            font-weight: 800;
        """)

        self.glow.set_color(
            t["accent"]
        )

    def enterEvent(self, event):

        self.raise_()

        self.glow_animation.stop()

        self.glow_animation.setStartValue(
            self.glow.strength
        )

        self.glow_animation.setEndValue(
            1.0
        )

        self.glow_animation.start()

        super().enterEvent(event)

    def leaveEvent(self, event):

        self.glow_animation.stop()

        self.glow_animation.setStartValue(
            self.glow.strength
        )

        self.glow_animation.setEndValue(
            0.0
        )

        self.glow_animation.start()

        super().leaveEvent(event)

    def mousePressEvent(self, event):

        if (
            event.button()
            == Qt.MouseButton.LeftButton
        ):
            self.callback(
                self.game
            )

        super().mousePressEvent(event)


# ============================================================
# ADD GAME DIALOG
# ============================================================

class AddGameDialog(QDialog):

    def __init__(
        self,
        theme,
        parent=None
    ):
        super().__init__(parent)

        self.theme = theme

        self.setWindowTitle(
            "Add Game"
        )

        self.setMinimumWidth(
            540
        )

        layout = QVBoxLayout(self)

        layout.setSpacing(
            13
        )

        title = QLabel(
            "ADD GAME"
        )

        title.setStyleSheet("""
            font-size: 24px;
            font-weight: 900;
        """)

        layout.addWidget(
            title
        )

        self.title_input = QLineEdit()

        self.title_input.setPlaceholderText(
            "Game title"
        )

        layout.addWidget(
            QLabel("GAME TITLE")
        )

        layout.addWidget(
            self.title_input
        )

        self.cover_input = QLineEdit()

        self.cover_input.setPlaceholderText(
            "Vertical cover image"
        )

        cover_button = QPushButton(
            "BROWSE"
        )

        cover_button.clicked.connect(
            self.choose_cover
        )

        row = QHBoxLayout()

        row.addWidget(
            self.cover_input
        )

        row.addWidget(
            cover_button
        )

        layout.addWidget(
            QLabel("GAME COVER")
        )

        layout.addLayout(
            row
        )

        self.exe_input = QLineEdit()

        self.exe_input.setPlaceholderText(
            "Game executable"
        )

        exe_button = QPushButton(
            "BROWSE"
        )

        exe_button.clicked.connect(
            self.choose_exe
        )

        row2 = QHBoxLayout()

        row2.addWidget(
            self.exe_input
        )

        row2.addWidget(
            exe_button
        )

        layout.addWidget(
            QLabel("GAME FILE")
        )

        layout.addLayout(
            row2
        )

        self.description_input = QTextEdit()

        self.description_input.setFixedHeight(
            110
        )

        self.description_input.setPlaceholderText(
            "Optional description..."
        )

        layout.addWidget(
            QLabel("DESCRIPTION")
        )

        layout.addWidget(
            self.description_input
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel
            |
            QDialogButtonBox.StandardButton.Save
        )

        buttons.accepted.connect(
            self.accept
        )

        buttons.rejected.connect(
            self.reject
        )

        layout.addWidget(
            buttons
        )

        self.apply_theme()

    def apply_theme(self):

        t = self.theme

        self.setStyleSheet(f"""
            QDialog {{
                background: {t["bg"]};
                color: {t["text"]};
            }}

            QLabel {{
                color: {t["text"]};
                font-weight: 700;
            }}

            QLineEdit,
            QTextEdit {{
                background: {t["panel"]};
                color: {t["text"]};
                border: 1px solid rgba(255,255,255,35);
                border-radius: 11px;
                padding: 10px;
            }}

            QPushButton {{
                background: {t["card"]};
                color: {t["text"]};
                border: none;
                border-radius: 10px;
                padding: 9px 15px;
            }}

            QPushButton:hover {{
                border: 1px solid {t["accent"]};
            }}
        """)

    def choose_cover(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Game Cover",
            "",
            "Images (*.png *.jpg *.jpeg *.webp *.bmp)"
        )

        if path:
            self.cover_input.setText(
                path
            )

    def choose_exe(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Game Executable",
            "",
            "Executables (*.exe);;All Files (*.*)"
        )

        if path:
            self.exe_input.setText(
                path
            )

    def get_game(self):

        return {
            "id": str(
                uuid.uuid4()
            ),
            "title":
                self.title_input
                .text()
                .strip(),
            "cover":
                self.cover_input
                .text()
                .strip(),
            "exe":
                self.exe_input
                .text()
                .strip(),
            "description":
                self.description_input
                .toPlainText()
                .strip(),
        }

    def accept(self):

        if not self.title_input.text().strip():

            QMessageBox.warning(
                self,
                "Missing Title",
                "Please enter a game title."
            )

            return

        if not self.exe_input.text().strip():

            QMessageBox.warning(
                self,
                "Missing Game",
                "Please select the game executable."
            )

            return

        super().accept()


# ============================================================
# GAME DETAILS
# ============================================================

class GameDetailsDialog(QDialog):

    def __init__(
        self,
        game,
        theme,
        delete_callback,
        parent=None
    ):
        super().__init__(parent)

        self.game = game
        self.theme = theme
        self.delete_callback = delete_callback

        self.setWindowTitle(
            game.get(
                "title",
                "Game"
            )
        )

        self.setMinimumSize(
            760,
            470
        )

        layout = QHBoxLayout(
            self
        )

        layout.setContentsMargins(
            28,
            28,
            28,
            28
        )

        layout.setSpacing(
            25
        )

        cover = QLabel()

        cover.setFixedSize(
            245,
            370
        )

        cover.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        cover.setStyleSheet(
            f"""
            background: {theme["card"]};
            border-radius: 20px;
            """
        )

        cover_path = game.get(
            "cover",
            ""
        )

        if os.path.exists(
            cover_path
        ):

            pixmap = QPixmap(
                cover_path
            )

            if not pixmap.isNull():

                cover.setPixmap(
                    pixmap.scaled(
                        245,
                        370,
                        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                        Qt.TransformationMode.SmoothTransformation
                    )
                )

        layout.addWidget(
            cover
        )

        right = QVBoxLayout()

        title = QLabel(
            game.get(
                "title",
                "Unknown Game"
            )
        )

        title.setWordWrap(
            True
        )

        title.setStyleSheet("""
            font-size: 30px;
            font-weight: 900;
        """)

        right.addWidget(
            title
        )

        description = QLabel(
            game.get(
                "description",
                ""
            )
            or
            "No description added."
        )

        description.setWordWrap(
            True
        )

        description.setStyleSheet(
            f"""
            color: {theme["subtext"]};
            font-size: 14px;
            """
        )

        right.addWidget(
            description
        )

        right.addStretch()

        play = QPushButton(
            "▶  PLAY"
        )

        play.setMinimumHeight(
            56
        )

        play.clicked.connect(
            self.play_game
        )

        play.setStyleSheet(f"""
            QPushButton {{
                background: {theme["green"]};
                color: white;
                border: none;
                border-radius: 14px;
                font-size: 17px;
                font-weight: 900;
            }}

            QPushButton:hover {{
                background: {theme["accent"]};
            }}
        """)

        right.addWidget(
            play
        )

        remove = QPushButton(
            "REMOVE FROM LIBRARY"
        )

        remove.clicked.connect(
            self.delete_game
        )

        right.addWidget(
            remove
        )

        layout.addLayout(
            right,
            1
        )

        self.setStyleSheet(f"""
            QDialog {{
                background: {theme["bg"]};
                color: {theme["text"]};
            }}

            QLabel {{
                color: {theme["text"]};
            }}

            QPushButton {{
                background: {theme["card"]};
                color: {theme["text"]};
                border: none;
                border-radius: 12px;
                padding: 11px;
                font-weight: 800;
            }}

            QPushButton:hover {{
                border: 1px solid {theme["accent"]};
            }}
        """)

    def play_game(self):

        exe = self.game.get(
            "exe",
            ""
        )

        if not os.path.exists(exe):

            QMessageBox.warning(
                self,
                "Game Not Found",
                "The game executable could not be found."
            )

            return

        try:

            subprocess.Popen(
                [exe],
                cwd=os.path.dirname(exe)
            )

            self.accept()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Launch Error",
                str(e)
            )

    def delete_game(self):

        answer = QMessageBox.question(
            self,
            "Remove Game",
            f"Remove "
            f"{self.game.get('title')} "
            f"from Glox Library?",
            QMessageBox.StandardButton.Yes
            |
            QMessageBox.StandardButton.No
        )

        if (
            answer
            == QMessageBox.StandardButton.Yes
        ):

            self.delete_callback(
                self.game
            )

            self.accept()


# ============================================================
# MAIN GLOX LIBRARY
# ============================================================

class GloxLibrary(QMainWindow):

    def __init__(self):

        super().__init__()

        self.games = load_games()

        self.theme_name = "Obsidian"

        self.theme = THEMES[
            self.theme_name
        ]

        self.drag_position = None

        # Completely frameless window
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
        )

        # Makes the corners outside the widget transparent
        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.resize(
            1280,
            800
        )

        self.build_ui()

        self.apply_theme()

        self.refresh_library()

    # ========================================================
    # UI
    # ========================================================

    def build_ui(self):

        # Transparent outer layer
        self.root = QWidget()

        self.root.setObjectName(
            "root"
        )

        root_layout = QVBoxLayout(
            self.root
        )

        root_layout.setContentsMargins(
            14,
            14,
            14,
            14
        )

        self.setCentralWidget(
            self.root
        )

        # Actual visible widget
        self.container = QFrame()

        self.container.setObjectName(
            "container"
        )

        root_layout.addWidget(
            self.container
        )

        # Floating shadow
        shadow = QGraphicsDropShadowEffect()

        shadow.setBlurRadius(
            50
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
                190
            )
        )

        self.container.setGraphicsEffect(
            shadow
        )

        main_layout = QVBoxLayout(
            self.container
        )

        main_layout.setContentsMargins(
            28,
            20,
            28,
            25
        )

        main_layout.setSpacing(
            18
        )

        # ====================================================
        # HEADER
        # ====================================================

        header = QHBoxLayout()

        brand = QVBoxLayout()

        brand.setSpacing(
            0
        )

        self.title = QLabel(
            "GLOX LIBRARY"
        )

        self.title.setStyleSheet("""
            font-size: 29px;
            font-weight: 900;
            letter-spacing: 2px;
        """)

        self.subtitle = QLabel(
            "YOUR PERSONAL GAME COLLECTION"
        )

        brand.addWidget(
            self.title
        )

        brand.addWidget(
            self.subtitle
        )

        header.addLayout(
            brand
        )

        header.addStretch()

        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "Search games..."
        )

        self.search.setFixedWidth(
            210
        )

        self.search.textChanged.connect(
            self.refresh_library
        )

        header.addWidget(
            self.search
        )

        self.theme_selector = QComboBox()

        self.theme_selector.addItems(
            list(THEMES.keys())
        )

        self.theme_selector.currentTextChanged.connect(
            self.change_theme
        )

        header.addWidget(
            self.theme_selector
        )

        self.add_button = QPushButton(
            "+ ADD GAME"
        )

        self.add_button.clicked.connect(
            self.add_game
        )

        header.addWidget(
            self.add_button
        )

        minimize = QPushButton(
            "—"
        )

        close = QPushButton(
            "×"
        )

        minimize.setFixedSize(
            34,
            34
        )

        close.setFixedSize(
            34,
            34
        )

        minimize.clicked.connect(
            self.showMinimized
        )

        close.clicked.connect(
            self.close
        )

        header.addWidget(
            minimize
        )

        header.addWidget(
            close
        )

        main_layout.addLayout(
            header
        )

        # ====================================================
        # LIBRARY HEADER
        # ====================================================

        self.library_title = QLabel(
            "ALL GAMES"
        )

        self.library_title.setStyleSheet("""
            font-size: 18px;
            font-weight: 900;
            letter-spacing: 1px;
        """)

        main_layout.addWidget(
            self.library_title
        )

        # ====================================================
        # LIBRARY PANEL
        # ====================================================

        self.library_panel = QFrame()

        self.library_panel.setObjectName(
            "libraryPanel"
        )

        library_panel_layout = QVBoxLayout(
            self.library_panel
        )

        library_panel_layout.setContentsMargins(
            10,
            10,
            10,
            10
        )

        # Scroll area
        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(
            True
        )

        self.scroll.setFrameShape(
            QFrame.Shape.NoFrame
        )

        # IMPORTANT:
        # The viewport itself gets themed too.
        self.scroll.viewport().setObjectName(
            "libraryViewport"
        )

        self.library_widget = QWidget()

        self.library_widget.setObjectName(
            "libraryWidget"
        )

        self.grid = QGridLayout(
            self.library_widget
        )

        self.grid.setAlignment(
            Qt.AlignmentFlag.AlignTop
            |
            Qt.AlignmentFlag.AlignLeft
        )

        self.grid.setHorizontalSpacing(
            28
        )

        self.grid.setVerticalSpacing(
            28
        )

        self.grid.setContentsMargins(
            8,
            8,
            8,
            30
        )

        self.scroll.setWidget(
            self.library_widget
        )

        library_panel_layout.addWidget(
            self.scroll
        )

        main_layout.addWidget(
            self.library_panel,
            1
        )

    # ========================================================
    # THEME
    # ========================================================

    def change_theme(
        self,
        theme_name
    ):

        if theme_name not in THEMES:
            return

        self.theme_name = theme_name

        self.theme = THEMES[
            theme_name
        ]

        self.apply_theme()

        self.refresh_library()

    def apply_theme(self):

        t = self.theme

        # ----------------------------------------------------
        # WHOLE WINDOW
        # ----------------------------------------------------

        self.root.setStyleSheet("""
            QWidget#root {
                background: transparent;
            }
        """)

        # ----------------------------------------------------
        # OUTER ROUNDED WIDGET
        # ----------------------------------------------------

        self.container.setStyleSheet(f"""
            QFrame#container {{
                background: {t["bg"]};
                border: 1px solid rgba(255,255,255,35);
                border-radius: 32px;
            }}
        """)

        # ----------------------------------------------------
        # LIBRARY PANEL
        # ----------------------------------------------------

        self.library_panel.setStyleSheet(f"""
            QFrame#libraryPanel {{
                background: {t["panel"]};
                border: 1px solid rgba(255,255,255,20);
                border-radius: 22px;
            }}
        """)

        # ----------------------------------------------------
        # SCROLL AREA + VIEWPORT + ACTUAL LIBRARY
        #
        # THIS IS THE IMPORTANT FIX
        # ----------------------------------------------------

        self.scroll.setStyleSheet(f"""
            QScrollArea {{
                background: {t["library"]};
                border: none;
                border-radius: 17px;
            }}

            QScrollArea > QWidget {{
                background: {t["library"]};
                border-radius: 17px;
            }}

            QScrollBar:vertical {{
                background: transparent;
                width: 8px;
                margin: 5px;
            }}

            QScrollBar::handle:vertical {{
                background: {t["accent"]};
                border-radius: 4px;
                min-height: 35px;
            }}

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                height: 0px;
            }}

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {{
                background: transparent;
            }}
        """)

        self.scroll.viewport().setStyleSheet(
            f"""
            QWidget#libraryViewport {{
                background: {t["library"]};
                border-radius: 17px;
            }}
            """
        )

        # Actual widget containing cards
        self.library_widget.setStyleSheet(
            f"""
            QWidget#libraryWidget {{
                background: {t["library"]};
                border-radius: 17px;
            }}
            """
        )

        # ----------------------------------------------------
        # LABELS
        # ----------------------------------------------------

        self.title.setStyleSheet(f"""
            color: {t["text"]};
            font-size: 29px;
            font-weight: 900;
            letter-spacing: 2px;
        """)

        self.subtitle.setStyleSheet(f"""
            color: {t["subtext"]};
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 2px;
        """)

        self.library_title.setStyleSheet(f"""
            color: {t["text"]};
            font-size: 18px;
            font-weight: 900;
            letter-spacing: 1px;
        """)

        # ----------------------------------------------------
        # SEARCH
        # ----------------------------------------------------

        self.search.setStyleSheet(f"""
            QLineEdit {{
                background: {t["card"]};
                color: {t["text"]};
                border: 1px solid rgba(255,255,255,25);
                border-radius: 12px;
                padding: 10px 14px;
                selection-background-color: {t["accent"]};
            }}

            QLineEdit:focus {{
                border: 1px solid {t["accent"]};
            }}
        """)

        # ----------------------------------------------------
        # THEME SELECTOR
        # ----------------------------------------------------

        self.theme_selector.setStyleSheet(f"""
            QComboBox {{
                background: {t["card"]};
                color: {t["text"]};
                border: 1px solid rgba(255,255,255,25);
                border-radius: 12px;
                padding: 9px 14px;
                min-width: 145px;
            }}

            QComboBox:hover {{
                border: 1px solid {t["accent"]};
            }}

            QComboBox QAbstractItemView {{
                background: {t["panel"]};
                color: {t["text"]};
                border: 1px solid {t["accent"]};
                selection-background-color: {t["accent"]};
                selection-color: white;
            }}
        """)

        # ----------------------------------------------------
        # ADD BUTTON
        # ----------------------------------------------------

        self.add_button.setStyleSheet(f"""
            QPushButton {{
                background: {t["accent"]};
                color: white;
                border: none;
                border-radius: 12px;
                padding: 10px 17px;
                font-weight: 900;
            }}

            QPushButton:hover {{
                background: {t["accent2"]};
            }}

            QPushButton:pressed {{
                background: {t["accent"]};
            }}
        """)

    # ========================================================
    # LIBRARY REFRESH
    # ========================================================

    def refresh_library(self):

        while self.grid.count():

            item = self.grid.takeAt(
                0
            )

            widget = item.widget()

            if widget:
                widget.deleteLater()

        query = (
            self.search.text()
            .strip()
            .lower()
        )

        filtered_games = [
            game
            for game in self.games
            if query in game.get(
                "title",
                ""
            ).lower()
        ]

        # 5 cards on normal 1280px window
        columns = max(
            1,
            int(
                max(
                    1,
                    self.scroll.viewport().width()
                )
                / 225
            )
        )

        if not filtered_games:

            empty = QLabel(
                "YOUR LIBRARY IS EMPTY\n\n"
                "ADD YOUR FIRST GAME"
            )

            empty.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            empty.setMinimumHeight(
                400
            )

            empty.setStyleSheet(f"""
                color: {self.theme["subtext"]};
                background: transparent;
                font-size: 16px;
                font-weight: 800;
                letter-spacing: 1px;
            """)

            self.grid.addWidget(
                empty,
                0,
                0,
                1,
                columns
            )

            return

        for index, game in enumerate(
            filtered_games
        ):

            row = index // columns
            column = index % columns

            card = GameCard(
                game,
                self.theme,
                self.open_game_details
            )

            self.grid.addWidget(
                card,
                row,
                column
            )

        # Push cards toward the top
        self.grid.setRowStretch(
            self.grid.rowCount(),
            1
        )

    # ========================================================
    # ADD GAME
    # ========================================================

    def add_game(self):

        dialog = AddGameDialog(
            self.theme,
            self
        )

        if dialog.exec():

            self.games.append(
                dialog.get_game()
            )

            save_games(
                self.games
            )

            self.refresh_library()

    # ========================================================
    # DETAILS
    # ========================================================

    def open_game_details(
        self,
        game
    ):

        dialog = GameDetailsDialog(
            game,
            self.theme,
            self.remove_game,
            self
        )

        dialog.exec()

    # ========================================================
    # REMOVE
    # ========================================================

    def remove_game(
        self,
        game
    ):

        self.games = [
            item
            for item in self.games
            if item.get("id")
            != game.get("id")
        ]

        save_games(
            self.games
        )

        self.refresh_library()

    # ========================================================
    # DRAG WINDOW
    # ========================================================

    def mousePressEvent(
        self,
        event
    ):

        if (
            event.button()
            == Qt.MouseButton.LeftButton
        ):

            self.drag_position = (
                event.globalPosition().toPoint()
                -
                self.frameGeometry().topLeft()
            )

        super().mousePressEvent(
            event
        )

    def mouseMoveEvent(
        self,
        event
    ):

        if (
            self.drag_position is not None
            and
            event.buttons()
            == Qt.MouseButton.LeftButton
        ):

            self.move(
                event.globalPosition().toPoint()
                -
                self.drag_position
            )

        super().mouseMoveEvent(
            event
        )

    def mouseReleaseEvent(
        self,
        event
    ):

        self.drag_position = None

        super().mouseReleaseEvent(
            event
        )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )

    app.setApplicationName(
        APP_NAME
    )

    window = GloxLibrary()

    window.show()

    sys.exit(
        app.exec()
    )