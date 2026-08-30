# ============================================================
# GLOX LENS
# Desktop magnifier + live pixel color inspector
# ============================================================

import sys

from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
    QFont,
    QCursor,
    QPainterPath,
)
from PySide6.QtWidgets import QApplication, QWidget, QMenu


class GloxLens(QWidget):

    WIDTH = 270
    HEIGHT = 330

    ZOOM_LEVELS = [2, 3, 4, 5, 6, 8, 10]

    def __init__(self):
        super().__init__()

        self.zoom = 4
        self.lens_size = 210
        self.locked = False

        self.current_color = QColor(255, 255, 255)
        self.current_hex = "#FFFFFF"
        self.current_rgb = (255, 255, 255)

        self.dragging = False
        self.drag_offset = QPoint()

        self.setWindowTitle("GLOX Lens")
        self.setFixedSize(self.WIDTH, self.HEIGHT)

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground
        )

        self.setup_position()

        # Update the magnifier ~25 times/sec.
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_lens)
        self.timer.start(40)

    # =========================================================
    # POSITION
    # =========================================================

    def setup_position(self):

        screen = QApplication.primaryScreen()

        if not screen:
            return

        geometry = screen.availableGeometry()

        self.move(
            geometry.right() - self.WIDTH - 30,
            geometry.top() + 80
        )

    # =========================================================
    # SCREEN CAPTURE
    # =========================================================

    def capture_screen(self):

        screen = QApplication.primaryScreen()

        if not screen:
            return None

        return screen.grabWindow(0)

    # =========================================================
    # UPDATE LENS
    # =========================================================

    def update_lens(self):

        screenshot = self.capture_screen()

        if screenshot is None or screenshot.isNull():
            return

        cursor = QCursor.pos()

        x = cursor.x()
        y = cursor.y()

        if (
            0 <= x < screenshot.width()
            and
            0 <= y < screenshot.height()
        ):

            image = screenshot.toImage()

            self.current_color = image.pixelColor(
                x,
                y
            )

            self.current_rgb = (
                self.current_color.red(),
                self.current_color.green(),
                self.current_color.blue()
            )

            self.current_hex = (
                self.current_color.name().upper()
            )

        self.update()

    # =========================================================
    # PAINT
    # =========================================================

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        painter.setRenderHint(
            QPainter.SmoothPixmapTransform
        )

        # -----------------------------------------------------
        # SHADOW
        # -----------------------------------------------------

        painter.setPen(Qt.NoPen)

        painter.setBrush(
            QColor(0, 0, 0, 125)
        )

        painter.drawRoundedRect(
            5,
            7,
            self.WIDTH - 10,
            self.HEIGHT - 10,
            22,
            22
        )

        # -----------------------------------------------------
        # MAIN BODY
        # -----------------------------------------------------

        painter.setBrush(
            QColor(42, 40, 37, 245)
        )

        painter.setPen(
            QPen(
                QColor(235, 225, 210, 48),
                1
            )
        )

        painter.drawRoundedRect(
            2,
            2,
            self.WIDTH - 6,
            self.HEIGHT - 6,
            21,
            21
        )

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        painter.setPen(
            QColor("#F3EEE5")
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                14,
                QFont.Weight.Bold
            )
        )

        painter.drawText(
            18,
            28,
            "GLOX"
        )

        painter.setPen(
            QColor("#A9A39A")
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                8,
                QFont.Weight.Medium
            )
        )

        painter.drawText(
            62,
            27,
            "LENS"
        )

        painter.setPen(
            QColor("#817A72")
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                7
            )
        )

        painter.drawText(
            self.WIDTH - 60,
            27,
            "LOCKED" if self.locked else "LIVE"
        )

        # -----------------------------------------------------
        # LENS
        # -----------------------------------------------------

        lens_x = (
            self.WIDTH - self.lens_size
        ) // 2

        lens_y = 43

        # Shadow underneath lens
        painter.setPen(Qt.NoPen)

        painter.setBrush(
            QColor(0, 0, 0, 90)
        )

        painter.drawEllipse(
            lens_x + 2,
            lens_y + 4,
            self.lens_size,
            self.lens_size
        )

        # Capture desktop again for drawing
        screenshot = self.capture_screen()

        painter.save()

        path = QPainterPath()

        path.addEllipse(
            lens_x,
            lens_y,
            self.lens_size,
            self.lens_size
        )

        painter.setClipPath(path)

        if screenshot and not screenshot.isNull():

            cursor = QCursor.pos()

            source_size = max(
                10,
                int(
                    self.lens_size /
                    self.zoom
                )
            )

            source_x = (
                cursor.x()
                - source_size // 2
            )

            source_y = (
                cursor.y()
                - source_size // 2
            )

            painter.drawPixmap(
                lens_x,
                lens_y,
                self.lens_size,
                self.lens_size,
                screenshot,
                source_x,
                source_y,
                source_size,
                source_size
            )

        else:

            painter.fillRect(
                lens_x,
                lens_y,
                self.lens_size,
                self.lens_size,
                QColor("#202020")
            )

        painter.restore()

        # -----------------------------------------------------
        # LENS BORDER
        # -----------------------------------------------------

        painter.setBrush(Qt.NoBrush)

        painter.setPen(
            QPen(
                QColor(245, 238, 226, 110),
                2
            )
        )

        painter.drawEllipse(
            lens_x,
            lens_y,
            self.lens_size,
            self.lens_size
        )

        # -----------------------------------------------------
        # CROSSHAIR
        # -----------------------------------------------------

        cx = (
            lens_x
            + self.lens_size // 2
        )

        cy = (
            lens_y
            + self.lens_size // 2
        )

        painter.setPen(
            QPen(
                QColor(255, 255, 255, 150),
                1
            )
        )

        painter.drawLine(
            cx - 13,
            cy,
            cx + 13,
            cy
        )

        painter.drawLine(
            cx,
            cy - 13,
            cx,
            cy + 13
        )

        painter.setPen(
            QPen(
                QColor(20, 20, 20, 180),
                1
            )
        )

        painter.drawEllipse(
            cx - 3,
            cy - 3,
            6,
            6
        )

        # -----------------------------------------------------
        # COLOR INFO
        # -----------------------------------------------------

        info_y = 269

        # Color square

        painter.setBrush(
            self.current_color
        )

        painter.setPen(
            QPen(
                QColor(255, 255, 255, 55),
                1
            )
        )

        painter.drawRoundedRect(
            18,
            info_y,
            30,
            30,
            8,
            8
        )

        # HEX

        painter.setPen(
            QColor("#F0EBE3")
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                12,
                QFont.Weight.Bold
            )
        )

        painter.drawText(
            58,
            info_y + 13,
            self.current_hex
        )

        # RGB

        r, g, b = self.current_rgb

        painter.setPen(
            QColor("#9E978E")
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                8
            )
        )

        painter.drawText(
            58,
            info_y + 27,
            f"RGB  {r}, {g}, {b}"
        )

        # Zoom indicator

        painter.setPen(
            QColor("#77716A")
        )

        painter.drawText(
            self.WIDTH - 50,
            info_y + 27,
            f"{self.zoom}×"
        )

        # -----------------------------------------------------
        # FOOTER
        # -----------------------------------------------------

        painter.setPen(
            QColor("#716B64")
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                7
            )
        )

        painter.drawText(
            18,
            self.HEIGHT - 15,
            "Click: copy HEX   •   Right click: options"
        )

    # =========================================================
    # MOUSE
    # =========================================================

    def mousePressEvent(self, event):

        # Right click = settings
        if event.button() == Qt.RightButton:

            self.show_menu(
                event.globalPosition().toPoint()
            )

            return

        # Left click = copy color
        if event.button() == Qt.LeftButton:

            QApplication.clipboard().setText(
                self.current_hex
            )

            event.accept()

    # =========================================================
    # CONTEXT MENU
    # =========================================================

    def show_menu(self, position):

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
                padding: 7px 24px;
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
        # ZOOM
        # -----------------------------------------------------

        zoom_menu = QMenu(
            "Zoom",
            menu
        )

        zoom_menu.setStyleSheet(
            menu.styleSheet()
        )

        for value in self.ZOOM_LEVELS:

            action = zoom_menu.addAction(
                f"{value}×"
            )

            action.setCheckable(True)

            action.setChecked(
                value == self.zoom
            )

            action.triggered.connect(
                lambda checked=False,
                v=value:
                self.change_zoom(v)
            )

        menu.addMenu(
            zoom_menu
        )

        # -----------------------------------------------------
        # LENS SIZE
        # -----------------------------------------------------

        size_menu = QMenu(
            "Lens Size",
            menu
        )

        size_menu.setStyleSheet(
            menu.styleSheet()
        )

        for value in (
            170,
            210,
            240
        ):

            action = size_menu.addAction(
                f"{value}px"
            )

            action.setCheckable(True)

            action.setChecked(
                value == self.lens_size
            )

            action.triggered.connect(
                lambda checked=False,
                v=value:
                self.change_lens_size(v)
            )

        menu.addMenu(
            size_menu
        )

        # -----------------------------------------------------
        # LOCK
        # -----------------------------------------------------

        lock_action = menu.addAction(
            "Unlock Position"
            if self.locked
            else "Lock Position"
        )

        lock_action.triggered.connect(
            self.toggle_lock
        )

        # -----------------------------------------------------
        # COPY
        # -----------------------------------------------------

        copy_action = menu.addAction(
            "Copy HEX"
        )

        copy_action.triggered.connect(
            self.copy_hex
        )

        menu.addSeparator()

        # -----------------------------------------------------
        # EXIT
        # -----------------------------------------------------

        exit_action = menu.addAction(
            "Exit GLOX Lens"
        )

        exit_action.triggered.connect(
            QApplication.quit
        )

        menu.exec(position)

    # =========================================================
    # SETTINGS
    # =========================================================

    def change_zoom(self, value):

        self.zoom = value

        self.update()

    def change_lens_size(self, value):

        self.lens_size = value

        self.update()

    def toggle_lock(self):

        self.locked = not self.locked

    def copy_hex(self):

        QApplication.clipboard().setText(
            self.current_hex
        )

    # =========================================================
    # DRAGGING
    # =========================================================

    def mouseMoveEvent(self, event):

        if (
            self.dragging
            and
            not self.locked
        ):

            new_pos = (
                event.globalPosition().toPoint()
                - self.drag_offset
            )

            self.move(new_pos)

            event.accept()

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.dragging = False

            event.accept()

    # =========================================================
    # KEYBOARD
    # =========================================================

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:

            self.close()

        elif event.key() in (
            Qt.Key_Plus,
            Qt.Key_Equal
        ):

            self.zoom = min(
                10,
                self.zoom + 1
            )

            self.update()

        elif event.key() == Qt.Key_Minus:

            self.zoom = max(
                2,
                self.zoom - 1
            )

            self.update()


# ============================================================
# MAIN
# ============================================================

def main():

    app = QApplication(sys.argv)

    app.setApplicationName(
        "GLOX Lens"
    )

    app.setQuitOnLastWindowClosed(
        True
    )

    widget = GloxLens()

    widget.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()