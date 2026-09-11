import os
import sys
import json
import base64
import hashlib
import secrets
from pathlib import Path

from PySide6.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve,
    QSize, Signal
)
from PySide6.QtGui import (
    QFont, QColor, QPainter, QPainterPath, QPen
)
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QListWidget, QListWidgetItem,
    QFileDialog, QMessageBox, QLineEdit, QFrame,
    QInputDialog, QMenu, QGraphicsOpacityEffect,
    QSlider
)

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# ============================================================
# GLOXVAULT CONFIGURATION
# ============================================================

APP_NAME = "GloxVault"
VAULT_FOLDER = "GloxVaultData"
INDEX_FILE = "index.json"
MAGIC = b"GLOXVAULT1"
PBKDF2_ITERATIONS = 600_000

BASE_DIR = (
    Path(sys.executable).resolve().parent
    if getattr(sys, "frozen", False)
    else Path(__file__).resolve().parent
)

VAULT_DIR = BASE_DIR / VAULT_FOLDER
INDEX_PATH = VAULT_DIR / INDEX_FILE


# ============================================================
# THEMES
# ============================================================

THEMES = {

    "Obsidian": {
        "bg": "#0c0d10",
        "card": "#17191e",
        "card2": "#1d2026",
        "border": "#343740",
        "button": "#24272e",
        "button_hover": "#30343c",
        "text": "#f5f5f7",
        "muted": "#9699a4",
        "accent": "#ffffff",
        "danger": "#3a2024",
        "danger_hover": "#51282e",
        "selection": "#343841"
    },

    "Graphite": {
        "bg": "#111214",
        "card": "#202124",
        "card2": "#27282b",
        "border": "#3a3b40",
        "button": "#2d2f33",
        "button_hover": "#393b40",
        "text": "#eeeeef",
        "muted": "#999ba1",
        "accent": "#eeeeee",
        "danger": "#3b2427",
        "danger_hover": "#512e32",
        "selection": "#3c3e43"
    },

    "Charcoal": {
        "bg": "#151515",
        "card": "#222222",
        "card2": "#292929",
        "border": "#3b3b3b",
        "button": "#303030",
        "button_hover": "#3c3c3c",
        "text": "#fafafa",
        "muted": "#999999",
        "accent": "#ffffff",
        "danger": "#402426",
        "danger_hover": "#593033",
        "selection": "#414141"
    },

    "Espresso": {
        "bg": "#17120f",
        "card": "#241b17",
        "card2": "#2c211c",
        "border": "#46362d",
        "button": "#352820",
        "button_hover": "#443229",
        "text": "#f7eee8",
        "muted": "#ad9890",
        "accent": "#fff2e9",
        "danger": "#432326",
        "danger_hover": "#5b2c30",
        "selection": "#4a352c"
    },

    "Slate": {
        "bg": "#10151a",
        "card": "#1a2229",
        "card2": "#222c34",
        "border": "#35434e",
        "button": "#26313a",
        "button_hover": "#33414c",
        "text": "#eff6fa",
        "muted": "#94a2ad",
        "accent": "#e9f7ff",
        "danger": "#382529",
        "danger_hover": "#4e3036",
        "selection": "#34434e"
    },

    "Midnight": {
        "bg": "#080b15",
        "card": "#111728",
        "card2": "#172038",
        "border": "#2b3856",
        "button": "#1b2640",
        "button_hover": "#253354",
        "text": "#eef3ff",
        "muted": "#8997b5",
        "accent": "#f1f5ff",
        "danger": "#3c202b",
        "danger_hover": "#542b39",
        "selection": "#293653"
    },

    "Crystal Cream": {
        "bg": "#eeeae3",
        "card": "#f8f5ef",
        "card2": "#ffffff",
        "border": "#d8d1c5",
        "button": "#e7e0d5",
        "button_hover": "#dcd4c7",
        "text": "#292622",
        "muted": "#817a71",
        "accent": "#1f1d1a",
        "danger": "#ead5d2",
        "danger_hover": "#dfc2bd",
        "selection": "#ddd5c8"
    },

    "Aurora Night": {
        "bg": "#0b1015",
        "card": "#131c22",
        "card2": "#19272c",
        "border": "#2c4447",
        "button": "#1e3033",
        "button_hover": "#294346",
        "text": "#eafcf7",
        "muted": "#8aa8a5",
        "accent": "#e6fff8",
        "danger": "#392329",
        "danger_hover": "#512e37",
        "selection": "#2b4646"
    },

    "Lavender": {
        "bg": "#11101a",
        "card": "#1d192b",
        "card2": "#26213a",
        "border": "#3c3358",
        "button": "#302943",
        "button_hover": "#403654",
        "text": "#f5f0ff",
        "muted": "#a99dbd",
        "accent": "#f6eeff",
        "danger": "#42252f",
        "danger_hover": "#5a303e",
        "selection": "#413657"
    },

    "Glowy Sunshine": {
        "bg": "#15130b",
        "card": "#25200d",
        "card2": "#302913",
        "border": "#4c401c",
        "button": "#3b3116",
        "button_hover": "#4b3e1c",
        "text": "#fff9df",
        "muted": "#b3a779",
        "accent": "#fff5c2",
        "danger": "#432528",
        "danger_hover": "#5a3035",
        "selection": "#4c401c"
    },

    "Mono": {
        "bg": "#080808",
        "card": "#141414",
        "card2": "#1d1d1d",
        "border": "#333333",
        "button": "#252525",
        "button_hover": "#303030",
        "text": "#eeeeee",
        "muted": "#8c8c8c",
        "accent": "#ffffff",
        "danger": "#303030",
        "danger_hover": "#414141",
        "selection": "#373737"
    },

    "Blood Red": {
        "bg": "#11090b",
        "card": "#1e1013",
        "card2": "#281419",
        "border": "#4a242b",
        "button": "#32191f",
        "button_hover": "#442027",
        "text": "#fff0f2",
        "muted": "#b18b91",
        "accent": "#ffe9ec",
        "danger": "#4b2027",
        "danger_hover": "#632b34",
        "selection": "#4a242c"
    }
}


# ============================================================
# CRYPTOGRAPHY
# ============================================================

def derive_key(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
        dklen=32
    )


def encrypt_bytes(data, key):
    nonce = secrets.token_bytes(12)
    encrypted = AESGCM(key).encrypt(
        nonce,
        data,
        MAGIC
    )
    return nonce + encrypted


def decrypt_bytes(data, key):
    if len(data) < 13:
        raise ValueError("Invalid encrypted data.")

    nonce = data[:12]
    encrypted = data[12:]

    return AESGCM(key).decrypt(
        nonce,
        encrypted,
        MAGIC
    )


def create_vault(password):

    VAULT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    salt = secrets.token_bytes(32)

    key = derive_key(password, salt)

    verification = encrypt_bytes(
        b"GLOX_VAULT_PASSWORD_OK",
        key
    )

    config = {
        "version": 1,
        "salt": base64.b64encode(salt).decode(),
        "verification": base64.b64encode(
            verification
        ).decode(),
        "files": []
    }

    save_config(config)

    return config


def load_vault():

    if not INDEX_PATH.exists():
        return None

    try:
        with open(
            INDEX_PATH,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)

    except Exception:
        return None


def save_config(config):

    VAULT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    temporary = INDEX_PATH.with_suffix(".tmp")

    with open(
        temporary,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            config,
            f,
            indent=2
        )

    os.replace(
        temporary,
        INDEX_PATH
    )


def unlock_vault(password):

    config = load_vault()

    if not config:
        return None, None

    try:

        salt = base64.b64decode(
            config["salt"]
        )

        verification = base64.b64decode(
            config["verification"]
        )

        key = derive_key(
            password,
            salt
        )

        result = decrypt_bytes(
            verification,
            key
        )

        if result != b"GLOX_VAULT_PASSWORD_OK":
            return None, None

        return config, key

    except Exception:
        return None, None


def encrypted_filename():

    return secrets.token_hex(32) + ".glox"


def encrypt_file(
    source,
    destination,
    key
):

    with open(
        source,
        "rb"
    ) as f:
        data = f.read()

    encrypted = encrypt_bytes(
        data,
        key
    )

    with open(
        destination,
        "wb"
    ) as f:
        f.write(encrypted)


def decrypt_file(
    source,
    destination,
    key
):

    with open(
        source,
        "rb"
    ) as f:
        encrypted = f.read()

    data = decrypt_bytes(
        encrypted,
        key
    )

    with open(
        destination,
        "wb"
    ) as f:
        f.write(data)


# ============================================================
# ANIMATED BUTTON
# ============================================================

class AnimatedButton(QPushButton):

    def __init__(
        self,
        text="",
        parent=None
    ):

        super().__init__(
            text,
            parent
        )

        self.setCursor(
            Qt.PointingHandCursor
        )

        self.original_size = None

        self.press_animation = QPropertyAnimation(
            self,
            b"geometry"
        )

        self.press_animation.setDuration(90)

        self.press_animation.setEasingCurve(
            QEasingCurve.OutCubic
        )

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            geo = self.geometry()

            smaller = geo.adjusted(
                2,
                2,
                -2,
                -2
            )

            self.press_animation.stop()

            self.press_animation.setStartValue(
                geo
            )

            self.press_animation.setEndValue(
                smaller
            )

            self.press_animation.start()

        super().mousePressEvent(event)


# ============================================================
# DROP ZONE
# ============================================================

class DropList(QListWidget):

    filesDropped = Signal(list)

    def __init__(self):

        super().__init__()

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):

        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):

        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):

        paths = []

        for url in event.mimeData().urls():

            if url.isLocalFile():

                path = url.toLocalFile()

                if os.path.isfile(path):
                    paths.append(path)

        if paths:
            self.filesDropped.emit(paths)

        event.acceptProposedAction()


# ============================================================
# BASE STYLE
# ============================================================

def build_stylesheet(theme):

    t = THEMES[theme]

    return f"""
    QWidget {{
        background: {t["bg"]};
        color: {t["text"]};
        font-family: "Segoe UI";
    }}

    QFrame#Card {{
        background: {t["card"]};
        border: 1px solid {t["border"]};
        border-radius: 28px;
    }}

    QFrame#TopCard {{
        background: {t["card2"]};
        border: 1px solid {t["border"]};
        border-radius: 24px;
    }}

    QLabel#Title {{
        font-size: 30px;
        font-weight: 700;
        color: {t["text"]};
    }}

    QLabel#Subtitle {{
        color: {t["muted"]};
        font-size: 13px;
    }}

    QLabel#Status {{
        color: {t["muted"]};
        font-size: 12px;
    }}

    QLabel#Logo {{
        font-size: 38px;
        font-weight: 700;
        color: {t["text"]};
    }}

    QLineEdit {{
        background: {t["card2"]};
        border: 1px solid {t["border"]};
        border-radius: 16px;
        padding: 14px 16px;
        color: {t["text"]};
        font-size: 15px;
    }}

    QLineEdit:focus {{
        border: 1px solid {t["accent"]};
    }}

    QPushButton {{
        background: {t["button"]};
        color: {t["text"]};
        border: 1px solid {t["border"]};
        border-radius: 15px;
        padding: 12px 18px;
        font-size: 13px;
        font-weight: 600;
    }}

    QPushButton:hover {{
        background: {t["button_hover"]};
    }}

    QPushButton#Primary {{
        background: {t["accent"]};
        color: {t["bg"]};
        border: none;
    }}

    QPushButton#Primary:hover {{
        background: {t["text"]};
    }}

    QPushButton#Danger {{
        background: {t["danger"]};
        border: 1px solid {t["border"]};
    }}

    QPushButton#Danger:hover {{
        background: {t["danger_hover"]};
    }}

    QListWidget {{
        background: {t["card"]};
        border: 1px solid {t["border"]};
        border-radius: 22px;
        padding: 10px;
        outline: none;
    }}

    QListWidget::item {{
        padding: 16px;
        border-radius: 14px;
        margin: 3px;
    }}

    QListWidget::item:hover {{
        background: {t["button_hover"]};
    }}

    QListWidget::item:selected {{
        background: {t["selection"]};
    }}

    QMenu {{
        background: {t["card2"]};
        color: {t["text"]};
        border: 1px solid {t["border"]};
        border-radius: 14px;
        padding: 7px;
    }}

    QMenu::item {{
        padding: 9px 18px;
        border-radius: 9px;
    }}

    QMenu::item:selected {{
        background: {t["button_hover"]};
    }}

    QSlider::groove:horizontal {{
        height: 5px;
        background: {t["border"]};
        border-radius: 3px;
    }}

    QSlider::handle:horizontal {{
        width: 16px;
        margin: -6px 0;
        background: {t["accent"]};
        border-radius: 8px;
    }}
    """


# ============================================================
# LOGIN
# ============================================================

class LoginWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.theme = "Obsidian"

        self.setWindowTitle(
            "GloxVault"
        )

        self.setMinimumSize(
            560,
            520
        )

        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):

        outer = QVBoxLayout(self)

        outer.setContentsMargins(
            55,
            50,
            55,
            50
        )

        card = QFrame()

        card.setObjectName(
            "Card"
        )

        layout = QVBoxLayout(card)

        layout.setContentsMargins(
            40,
            40,
            40,
            40
        )

        layout.setSpacing(17)

        logo = QLabel("◈")

        logo.setObjectName(
            "Logo"
        )

        logo.setAlignment(
            Qt.AlignCenter
        )

        title = QLabel(
            "GloxVault"
        )

        title.setObjectName(
            "Title"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        subtitle = QLabel(
            "Private encrypted storage"
        )

        subtitle.setObjectName(
            "Subtitle"
        )

        subtitle.setAlignment(
            Qt.AlignCenter
        )

        self.password = QLineEdit()

        self.password.setPlaceholderText(
            "Enter vault password"
        )

        self.password.setEchoMode(
            QLineEdit.Password
        )

        self.button = AnimatedButton(
            "Unlock Vault"
        )

        self.button.setObjectName(
            "Primary"
        )

        self.button.clicked.connect(
            self.unlock
        )

        self.status = QLabel()

        self.status.setObjectName(
            "Status"
        )

        self.status.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            logo
        )

        layout.addWidget(
            title
        )

        layout.addWidget(
            subtitle
        )

        layout.addSpacing(
            15
        )

        layout.addWidget(
            self.password
        )

        layout.addWidget(
            self.button
        )

        layout.addWidget(
            self.status
        )

        outer.addWidget(
            card
        )

        self.password.returnPressed.connect(
            self.unlock
        )

    def apply_theme(self):

        QApplication.instance().setStyleSheet(
            build_stylesheet(
                self.theme
            )
        )

    def unlock(self):

        password = self.password.text()

        if not password:

            self.status.setText(
                "Enter your password."
            )

            return

        config = load_vault()

        if config is None:

            confirm, ok = QInputDialog.getText(
                self,
                "Create GloxVault",
                "Create your vault password:",
                QLineEdit.Password
            )

            if not ok:
                return

            if confirm != password:

                self.status.setText(
                    "Passwords do not match."
                )

                return

            if len(password) < 6:

                self.status.setText(
                    "Use at least 6 characters."
                )

                return

            create_vault(
                password
            )

            config, key = unlock_vault(
                password
            )

            self.open_vault(
                config,
                key
            )

            return

        config, key = unlock_vault(
            password
        )

        if key is None:

            self.status.setText(
                "Incorrect password."
            )

            self.password.clear()

            return

        self.open_vault(
            config,
            key
        )

    def open_vault(
        self,
        config,
        key
    ):

        self.hide()

        self.vault_window = VaultWindow(
            config,
            key,
            self
        )

        self.vault_window.show()


# ============================================================
# VAULT
# ============================================================

class VaultWindow(QWidget):

    def __init__(
        self,
        config,
        key,
        login_window
    ):

        super().__init__()

        self.config = config
        self.key = key
        self.login_window = login_window

        self.theme = "Obsidian"

        self.setWindowTitle(
            "GloxVault — Secure Vault"
        )

        self.resize(
            920,
            700
        )

        self.setMinimumSize(
            760,
            600
        )

        self.setup_ui()
        self.apply_theme()
        self.refresh_files()

    # --------------------------------------------------------

    def setup_ui(self):

        outer = QVBoxLayout(self)

        outer.setContentsMargins(
            32,
            28,
            32,
            28
        )

        outer.setSpacing(
            18
        )

        # HEADER
        header = QFrame()

        header.setObjectName(
            "TopCard"
        )

        header_layout = QHBoxLayout(
            header
        )

        header_layout.setContentsMargins(
            25,
            20,
            25,
            20
        )

        left = QVBoxLayout()

        title = QLabel(
            "GloxVault"
        )

        title.setObjectName(
            "Title"
        )

        subtitle = QLabel(
            "🔒  Vault unlocked • encrypted storage"
        )

        subtitle.setObjectName(
            "Subtitle"
        )

        left.addWidget(
            title
        )

        left.addWidget(
            subtitle
        )

        header_layout.addLayout(
            left
        )

        header_layout.addStretch()

        theme_button = AnimatedButton(
            "◐  Theme"
        )

        theme_button.clicked.connect(
            self.show_theme_menu
        )

        header_layout.addWidget(
            theme_button
        )

        lock_button = AnimatedButton(
            "🔒  Lock"
        )

        lock_button.clicked.connect(
            self.lock_vault
        )

        header_layout.addWidget(
            lock_button
        )

        outer.addWidget(
            header
        )

        # FILE LIST
        self.file_list = DropList()

        self.file_list.filesDropped.connect(
            self.encrypt_dropped_files
        )

        self.file_list.itemDoubleClicked.connect(
            lambda _: self.extract_file()
        )

        outer.addWidget(
            self.file_list,
            1
        )

        # BUTTONS
        controls = QHBoxLayout()

        controls.setSpacing(
            10
        )

        add_button = AnimatedButton(
            "＋  Add Files"
        )

        add_button.setObjectName(
            "Primary"
        )

        add_button.clicked.connect(
            self.add_files
        )

        extract_button = AnimatedButton(
            "↓  Extract"
        )

        extract_button.clicked.connect(
            self.extract_file
        )

        delete_button = AnimatedButton(
            "⌫  Delete"
        )

        delete_button.setObjectName(
            "Danger"
        )

        delete_button.clicked.connect(
            self.delete_file
        )

        controls.addWidget(
            add_button
        )

        controls.addWidget(
            extract_button
        )

        controls.addWidget(
            delete_button
        )

        controls.addStretch()

        opacity_label = QLabel(
            "Opacity"
        )

        opacity_label.setObjectName(
            "Status"
        )

        self.opacity_slider = QSlider(
            Qt.Horizontal
        )

        self.opacity_slider.setRange(
            70,
            100
        )

        self.opacity_slider.setValue(
            100
        )

        self.opacity_slider.setFixedWidth(
            100
        )

        self.opacity_slider.valueChanged.connect(
            self.change_opacity
        )

        controls.addWidget(
            opacity_label
        )

        controls.addWidget(
            self.opacity_slider
        )

        outer.addLayout(
            controls
        )

        self.status = QLabel()

        self.status.setObjectName(
            "Status"
        )

        outer.addWidget(
            self.status
        )

    # --------------------------------------------------------

    def apply_theme(self):

        QApplication.instance().setStyleSheet(
            build_stylesheet(
                self.theme
            )
        )

    # --------------------------------------------------------

    def show_theme_menu(self):

        menu = QMenu(
            self
        )

        for theme_name in THEMES:

            action = menu.addAction(
                theme_name
            )

            action.triggered.connect(
                lambda checked=False,
                name=theme_name:
                self.change_theme(name)
            )

        menu.exec(
            self.sender().mapToGlobal(
                self.sender().rect().bottomLeft()
            )
        )

    # --------------------------------------------------------

    def change_theme(
        self,
        theme
    ):

        self.theme = theme

        self.apply_theme()

        self.status.setText(
            f"Theme: {theme}"
        )

    # --------------------------------------------------------

    def change_opacity(
        self,
        value
    ):

        self.setWindowOpacity(
            value / 100
        )

    # --------------------------------------------------------

    def refresh_files(self):

        self.file_list.clear()

        files = self.config.get(
            "files",
            []
        )

        if not files:

            item = QListWidgetItem(
                "      ◈   Your vault is empty\n"
                "          Drop files here or use Add Files"
            )

            item.setFlags(
                Qt.NoItemFlags
            )

            self.file_list.addItem(
                item
            )

            self.status.setText(
                "0 encrypted files"
            )

            return

        for info in files:

            name = info["name"]

            size = self.format_size(
                info.get(
                    "size",
                    0
                )
            )

            item = QListWidgetItem(
                f"  ◈  {name}     ·     {size}"
            )

            item.setData(
                Qt.UserRole,
                info
            )

            self.file_list.addItem(
                item
            )

            self.animate_item(
                item
            )

        self.status.setText(
            f"{len(files)} encrypted file"
            + (
                "s"
                if len(files) != 1
                else ""
            )
        )

    # --------------------------------------------------------

    def animate_item(
        self,
        item
    ):

        row = self.file_list.row(
            item
        )

        QTimer.singleShot(
            row * 35,
            lambda:
            self.file_list.scrollToItem(
                item,
                QListWidget.PositionAtCenter
            )
        )

    # --------------------------------------------------------

    def add_files(self):

        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Add files to GloxVault"
        )

        if files:
            self.encrypt_dropped_files(
                files
            )

    # --------------------------------------------------------

    def encrypt_dropped_files(
        self,
        files
    ):

        added = 0

        for source in files:

            source_path = Path(
                source
            )

            encrypted_name = encrypted_filename()

            encrypted_path = (
                VAULT_DIR /
                encrypted_name
            )

            try:

                encrypt_file(
                    source_path,
                    encrypted_path,
                    self.key
                )

                self.config.setdefault(
                    "files",
                    []
                ).append(
                    {
                        "name":
                            source_path.name,

                        "encrypted_name":
                            encrypted_name,

                        "size":
                            source_path.stat().st_size
                    }
                )

                added += 1

            except Exception as e:

                QMessageBox.warning(
                    self,
                    "Encryption Error",
                    f"Could not encrypt:\n"
                    f"{source_path.name}\n\n{e}"
                )

        save_config(
            self.config
        )

        self.refresh_files()

        if added:

            self.status.setText(
                f"✓ Encrypted {added} file"
                + (
                    "s"
                    if added != 1
                    else ""
                )
            )

    # --------------------------------------------------------

    def extract_file(self):

        item = self.file_list.currentItem()

        if not item:
            return

        info = item.data(
            Qt.UserRole
        )

        if not info:
            return

        destination, _ = QFileDialog.getSaveFileName(
            self,
            "Extract encrypted file",
            info["name"]
        )

        if not destination:
            return

        encrypted_path = (
            VAULT_DIR /
            info["encrypted_name"]
        )

        try:

            decrypt_file(
                encrypted_path,
                destination,
                self.key
            )

            self.status.setText(
                f"✓ Extracted {info['name']}"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Extraction Failed",
                f"Could not decrypt the file.\n\n{e}"
            )

    # --------------------------------------------------------

    def delete_file(self):

        item = self.file_list.currentItem()

        if not item:
            return

        info = item.data(
            Qt.UserRole
        )

        if not info:
            return

        confirm = QMessageBox.question(
            self,
            "Delete File",
            f"Delete '{info['name']}' permanently?",
            QMessageBox.Yes |
            QMessageBox.No,
            QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        encrypted_path = (
            VAULT_DIR /
            info["encrypted_name"]
        )

        try:

            if encrypted_path.exists():
                encrypted_path.unlink()

            self.config["files"].remove(
                info
            )

            save_config(
                self.config
            )

            self.refresh_files()

            self.status.setText(
                "✓ File deleted"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Delete Failed",
                str(e)
            )

    # --------------------------------------------------------

    def lock_vault(self):

        self.key = None

        self.close()

        self.login_window.password.clear()

        self.login_window.status.setText(
            "Vault locked."
        )

        self.login_window.show()

    # --------------------------------------------------------

    @staticmethod
    def format_size(
        size
    ):

        units = [
            "B",
            "KB",
            "MB",
            "GB",
            "TB"
        ]

        value = float(size)

        for unit in units:

            if value < 1024:

                return (
                    f"{value:.1f} {unit}"
                )

            value /= 1024

        return f"{value:.1f} PB"

    # --------------------------------------------------------

    def closeEvent(
        self,
        event
    ):

        self.key = None

        if self.login_window:

            self.login_window.close()

        event.accept()


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

    window = LoginWindow()

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()