# ============================================================
# GLOX CELEBRATE
# Desktop celebration effects widget
# ============================================================

import sys
import random
import math
import time

from PySide6.QtCore import Qt, QTimer, QPoint, QRectF
from PySide6.QtGui import QColor, QPainter, QPen, QFont
from PySide6.QtWidgets import QApplication, QWidget, QMenu


# ============================================================
# FULL SCREEN EFFECT
# ============================================================

class CelebrationOverlay(QWidget):

    def __init__(self, effect, intensity, duration):
        super().__init__()

        self.effect = effect
        self.intensity = intensity
        self.duration = duration

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground
        )

        self.setAttribute(
            Qt.WA_TransparentForMouseEvents
        )

        screen = QApplication.primaryScreen()

        self.setGeometry(
            screen.geometry()
        )

        self.start_time = time.perf_counter()

        self.particles = []

        self.fireworks = []

        self.next_firework = 0

        self.phase = 0

        self.setup_effect()

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.animate
        )

        self.timer.start(16)

    # ========================================================
    # HELPERS
    # ========================================================

    def amount(self, base):

        return int(
            base * (
                0.55
                + self.intensity * 0.22
            )
        )

    @staticmethod
    def random_color():

        return QColor.fromHsv(
            random.randint(0, 359),
            random.randint(150, 245),
            255,
            random.randint(190, 255)
        )

    # ========================================================
    # SETUP
    # ========================================================

    def setup_effect(self):

        width = self.width()
        height = self.height()

        # ----------------------------------------------------
        # CONFETTI
        # ----------------------------------------------------

        if self.effect in (
            "Confetti",
            "Confetti Storm"
        ):

            count = self.amount(
                180
            )

            for _ in range(count):

                self.particles.append({
                    "x": random.uniform(
                        0,
                        width
                    ),
                    "y": random.uniform(
                        -height,
                        0
                    ),
                    "vx": random.uniform(
                        -1.8,
                        1.8
                    ),
                    "vy": random.uniform(
                        2,
                        7
                    ),
                    "size": random.uniform(
                        5,
                        12
                    ),
                    "rot": random.uniform(
                        0,
                        360
                    ),
                    "spin": random.uniform(
                        -8,
                        8
                    ),
                    "color":
                        self.random_color()
                })

        # ----------------------------------------------------
        # FIREWORKS
        # ----------------------------------------------------

        elif self.effect == "Fireworks":

            self.fireworks = []

        # ----------------------------------------------------
        # SPARKLE BURST
        # ----------------------------------------------------

        elif self.effect == "Sparkle Burst":

            cx = width / 2
            cy = height / 2

            for _ in range(
                self.amount(130)
            ):

                angle = random.uniform(
                    0,
                    math.tau
                )

                speed = random.uniform(
                    2,
                    9
                )

                self.particles.append({
                    "x": cx,
                    "y": cy,
                    "vx":
                        math.cos(angle)
                        * speed,
                    "vy":
                        math.sin(angle)
                        * speed,
                    "life":
                        random.uniform(
                            .5,
                            1.4
                        ),
                    "max": 1.4,
                    "size":
                        random.uniform(
                            2,
                            5
                        ),
                    "color":
                        self.random_color()
                })

        # ----------------------------------------------------
        # BALLOONS
        # ----------------------------------------------------

        elif self.effect == "Balloons":

            for _ in range(
                self.amount(35)
            ):

                self.particles.append({
                    "x":
                        random.uniform(
                            0,
                            width
                        ),
                    "y":
                        random.uniform(
                            height,
                            height + 300
                        ),
                    "vy":
                        random.uniform(
                            -1.2,
                            -3.2
                        ),
                    "size":
                        random.uniform(
                            18,
                            34
                        ),
                    "color":
                        self.random_color(),
                    "phase":
                        random.uniform(
                            0,
                            math.tau
                        )
                })

        # ----------------------------------------------------
        # EMOJI RAIN
        # ----------------------------------------------------

        elif self.effect == "Emoji Rain":

            emojis = [
                "🎉",
                "⭐",
                "✨",
                "🎊",
                "💫",
                "🌟",
                "🥳"
            ]

            for _ in range(
                self.amount(65)
            ):

                self.particles.append({
                    "x":
                        random.uniform(
                            0,
                            width
                        ),
                    "y":
                        random.uniform(
                            -height,
                            0
                        ),
                    "vy":
                        random.uniform(
                            2,
                            6
                        ),
                    "size":
                        random.randint(
                            18,
                            34
                        ),
                    "emoji":
                        random.choice(
                            emojis
                        ),
                    "phase":
                        random.uniform(
                            0,
                            math.tau
                        )
                })

        # ----------------------------------------------------
        # STARS
        # ----------------------------------------------------

        elif self.effect == "Stars":

            for _ in range(
                self.amount(160)
            ):

                self.particles.append({
                    "x":
                        random.uniform(
                            0,
                            width
                        ),
                    "y":
                        random.uniform(
                            0,
                            height
                        ),
                    "size":
                        random.uniform(
                            1,
                            4
                        ),
                    "phase":
                        random.uniform(
                            0,
                            math.tau
                        ),
                    "speed":
                        random.uniform(
                            .8,
                            2
                        )
                })

        # ----------------------------------------------------
        # PARTY WAVE
        # ----------------------------------------------------

        elif self.effect == "Party Wave":

            for _ in range(
                self.amount(90)
            ):

                self.particles.append({
                    "x":
                        random.uniform(
                            -100,
                            width
                        ),
                    "y":
                        random.uniform(
                            0,
                            height
                        ),
                    "size":
                        random.uniform(
                            3,
                            8
                        ),
                    "speed":
                        random.uniform(
                            2,
                            6
                        ),
                    "phase":
                        random.uniform(
                            0,
                            math.tau
                        ),
                    "color":
                        self.random_color()
                })

        # ----------------------------------------------------
        # CELEBRATION BURST
        # ----------------------------------------------------

        elif self.effect == "Celebration Burst":

            cx = width / 2
            cy = height / 2

            for _ in range(
                self.amount(220)
            ):

                angle = random.uniform(
                    0,
                    math.tau
                )

                speed = random.uniform(
                    3,
                    14
                )

                self.particles.append({
                    "x": cx,
                    "y": cy,
                    "vx":
                        math.cos(angle)
                        * speed,
                    "vy":
                        math.sin(angle)
                        * speed,
                    "life":
                        random.uniform(
                            .7,
                            1.8
                        ),
                    "size":
                        random.uniform(
                            2,
                            7
                        ),
                    "color":
                        self.random_color()
                })

    # ========================================================
    # ANIMATION
    # ========================================================

    def animate(self):

        elapsed = (
            time.perf_counter()
            - self.start_time
        )

        if elapsed >= self.duration:

            self.close()

            return

        dt = 0.016

        width = self.width()
        height = self.height()

        # ----------------------------------------------------
        # CONFETTI
        # ----------------------------------------------------

        if self.effect in (
            "Confetti",
            "Confetti Storm"
        ):

            for particle in self.particles:

                particle["x"] += (
                    particle["vx"]
                )

                particle["y"] += (
                    particle["vy"]
                )

                particle["vy"] += .055

                particle["rot"] += (
                    particle["spin"]
                )

                if particle["y"] > height + 20:

                    particle["y"] = (
                        random.uniform(
                            -80,
                            -10
                        )
                    )

                    particle["x"] = (
                        random.uniform(
                            0,
                            width
                        )
                    )

                    particle["vy"] = (
                        random.uniform(
                            2,
                            7
                        )
                    )

        # ----------------------------------------------------
        # SPARKLES
        # ----------------------------------------------------

        elif self.effect in (
            "Sparkle Burst",
            "Celebration Burst"
        ):

            for particle in self.particles:

                particle["x"] += (
                    particle["vx"]
                )

                particle["y"] += (
                    particle["vy"]
                )

                particle["vx"] *= .985

                particle["vy"] *= .985

                particle["life"] -= dt

        # ----------------------------------------------------
        # BALLOONS
        # ----------------------------------------------------

        elif self.effect == "Balloons":

            for particle in self.particles:

                particle["y"] += (
                    particle["vy"]
                )

                particle["x"] += (
                    math.sin(
                        elapsed * 2
                        + particle["phase"]
                    )
                    * .7
                )

                if particle["y"] < -80:

                    particle["y"] = (
                        height
                        + random.uniform(
                            30,
                            150
                        )
                    )

                    particle["x"] = (
                        random.uniform(
                            0,
                            width
                        )
                    )

        # ----------------------------------------------------
        # EMOJI
        # ----------------------------------------------------

        elif self.effect == "Emoji Rain":

            for particle in self.particles:

                particle["y"] += (
                    particle["vy"]
                )

                particle["x"] += (
                    math.sin(
                        elapsed * 2
                        + particle["phase"]
                    )
                    * .8
                )

                if particle["y"] > height + 50:

                    particle["y"] = -50

                    particle["x"] = (
                        random.uniform(
                            0,
                            width
                        )
                    )

        # ----------------------------------------------------
        # STARS
        # ----------------------------------------------------

        elif self.effect == "Stars":

            for particle in self.particles:

                particle["phase"] += (
                    particle["speed"]
                    * dt
                )

        # ----------------------------------------------------
        # PARTY WAVE
        # ----------------------------------------------------

        elif self.effect == "Party Wave":

            for particle in self.particles:

                particle["x"] += (
                    particle["speed"]
                )

                particle["y"] += (
                    math.sin(
                        particle["x"]
                        * .008
                        + particle["phase"]
                    )
                    * .8
                )

                if particle["x"] > width + 50:

                    particle["x"] = -50

        # ----------------------------------------------------
        # FIREWORKS
        # ----------------------------------------------------

        elif self.effect == "Fireworks":

            if elapsed > self.next_firework:

                self.spawn_firework()

                self.next_firework = (
                    elapsed
                    + random.uniform(
                        .25,
                        .65
                    )
                )

            for firework in self.fireworks:

                for particle in (
                    firework["particles"]
                ):

                    particle["x"] += (
                        particle["vx"]
                    )

                    particle["y"] += (
                        particle["vy"]
                    )

                    particle["vy"] += .045

                    particle["life"] -= dt

            self.fireworks = [
                firework
                for firework in self.fireworks
                if any(
                    particle["life"] > 0
                    for particle
                    in firework["particles"]
                )
            ]

        self.update()

    # ========================================================
    # FIREWORK CREATION
    # ========================================================

    def spawn_firework(self):

        x = random.uniform(
            self.width() * .15,
            self.width() * .85
        )

        y = random.uniform(
            self.height() * .15,
            self.height() * .55
        )

        color = self.random_color()

        particles = []

        for _ in range(
            self.amount(65)
        ):

            angle = random.uniform(
                0,
                math.tau
            )

            speed = random.uniform(
                2,
                6.5
            )

            particles.append({
                "x": x,
                "y": y,
                "vx":
                    math.cos(angle)
                    * speed,
                "vy":
                    math.sin(angle)
                    * speed,
                "life":
                    random.uniform(
                        .7,
                        1.5
                    ),
                "color": color,
                "size":
                    random.uniform(
                        2,
                        4
                    )
            })

        self.fireworks.append({
            "particles":
                particles
        })

    # ========================================================
    # PAINT
    # ========================================================

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        elapsed = (
            time.perf_counter()
            - self.start_time
        )

        fade = min(
            1,
            elapsed / .35,
            (self.duration - elapsed) / .45
        )

        # ----------------------------------------------------
        # CONFETTI
        # ----------------------------------------------------

        if self.effect in (
            "Confetti",
            "Confetti Storm"
        ):

            for particle in self.particles:

                color = QColor(
                    particle["color"]
                )

                color.setAlpha(
                    int(
                        color.alpha()
                        * max(0, fade)
                    )
                )

                painter.save()

                painter.translate(
                    particle["x"],
                    particle["y"]
                )

                painter.rotate(
                    particle["rot"]
                )

                painter.setBrush(
                    color
                )

                painter.setPen(
                    Qt.NoPen
                )

                painter.drawRoundedRect(
                    QRectF(
                        -particle["size"] / 2,
                        -particle["size"] / 2,
                        particle["size"],
                        particle["size"] * .55
                    ),
                    2,
                    2
                )

                painter.restore()

        # ----------------------------------------------------
        # SPARKLE / BURST
        # ----------------------------------------------------

        elif self.effect in (
            "Sparkle Burst",
            "Celebration Burst"
        ):

            for particle in self.particles:

                if particle.get(
                    "life",
                    0
                ) <= 0:

                    continue

                alpha = int(
                    255
                    * max(
                        0,
                        particle["life"]
                        / particle.get(
                            "max",
                            1
                        )
                    )
                    * fade
                )

                color = QColor(
                    particle["color"]
                )

                color.setAlpha(
                    alpha
                )

                painter.setPen(
                    QPen(
                        color,
                        max(
                            1,
                            particle["size"] / 2
                        )
                    )
                )

                painter.drawLine(
                    QPoint(
                        int(particle["x"]),
                        int(particle["y"])
                    ),
                    QPoint(
                        int(
                            particle["x"]
                            - particle["vx"] * 2
                        ),
                        int(
                            particle["y"]
                            - particle["vy"] * 2
                        )
                    )
                )

        # ----------------------------------------------------
        # BALLOONS
        # ----------------------------------------------------

        elif self.effect == "Balloons":

            for particle in self.particles:

                color = QColor(
                    particle["color"]
                )

                color.setAlpha(
                    int(
                        color.alpha()
                        * fade
                    )
                )

                painter.setBrush(
                    color
                )

                painter.setPen(
                    QPen(
                        color.darker(140),
                        1
                    )
                )

                size = particle["size"]

                painter.drawEllipse(
                    QRectF(
                        particle["x"]
                        - size / 2,
                        particle["y"]
                        - size * .65,
                        size,
                        size * 1.25
                    )
                )

                painter.drawLine(
                    int(particle["x"]),
                    int(
                        particle["y"]
                        + size * .55
                    ),
                    int(particle["x"]),
                    int(
                        particle["y"]
                        + size * 1.7
                    )
                )

        # ----------------------------------------------------
        # EMOJI RAIN
        # ----------------------------------------------------

        elif self.effect == "Emoji Rain":

            painter.setFont(
                QFont(
                    "Segoe UI Emoji",
                    24
                )
            )

            for particle in self.particles:

                painter.setOpacity(
                    fade
                )

                painter.drawText(
                    int(particle["x"]),
                    int(particle["y"]),
                    particle["emoji"]
                )

            painter.setOpacity(1)

        # ----------------------------------------------------
        # STARS
        # ----------------------------------------------------

        elif self.effect == "Stars":

            for particle in self.particles:

                glow = (
                    math.sin(
                        particle["phase"]
                    )
                    + 1
                ) / 2

                painter.setPen(
                    Qt.NoPen
                )

                painter.setBrush(
                    QColor(
                        255,
                        245,
                        220,
                        int(
                            80
                            + glow * 175
                        )
                    )
                )

                size = (
                    particle["size"]
                    * (
                        .6
                        + glow
                    )
                )

                painter.drawEllipse(
                    QRectF(
                        particle["x"],
                        particle["y"],
                        size,
                        size
                    )
                )

        # ----------------------------------------------------
        # PARTY WAVE
        # ----------------------------------------------------

        elif self.effect == "Party Wave":

            for particle in self.particles:

                painter.setPen(
                    QPen(
                        particle["color"],
                        max(
                            1,
                            particle["size"] / 2
                        )
                    )
                )

                painter.drawPoint(
                    int(particle["x"]),
                    int(particle["y"])
                )

        # ----------------------------------------------------
        # FIREWORKS
        # ----------------------------------------------------

        elif self.effect == "Fireworks":

            for firework in self.fireworks:

                for particle in (
                    firework["particles"]
                ):

                    if particle["life"] <= 0:
                        continue

                    color = QColor(
                        particle["color"]
                    )

                    color.setAlpha(
                        int(
                            255
                            * min(
                                1,
                                particle["life"]
                            )
                            * fade
                        )
                    )

                    painter.setPen(
                        QPen(
                            color,
                            max(
                                1,
                                particle["size"]
                            )
                        )
                    )

                    painter.drawPoint(
                        int(particle["x"]),
                        int(particle["y"])
                    )


# ============================================================
# GLOX CELEBRATE WIDGET
# ============================================================

class GloxCelebrate(QWidget):

    WIDTH = 300
    HEIGHT = 255

    EFFECTS = [
        "Confetti",
        "Confetti Storm",
        "Fireworks",
        "Sparkle Burst",
        "Balloons",
        "Emoji Rain",
        "Stars",
        "Party Wave",
        
    ]

    def __init__(self):

        super().__init__()

        self.setFixedSize(
            self.WIDTH,
            self.HEIGHT
        )

        self.setWindowTitle(
            "GLOX Celebrate"
        )

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground
        )

        self.effect = "Confetti"

        self.intensity = 3

        self.duration = 5

        self.random_mode = False

        self.dragging = False

        self.drag_offset = QPoint()

        self.overlay = None

        self.setup_position()

    # ========================================================
    # POSITION
    # ========================================================

    def setup_position(self):

        screen = (
            QApplication
            .primaryScreen()
            .availableGeometry()
        )

        self.move(
            screen.right()
            - self.width()
            - 35,
            screen.bottom()
            - self.height()
            - 35
        )

    # ========================================================
    # CELEBRATE
    # ========================================================

    def celebrate(self):

        if self.random_mode:

            effect = random.choice(
                self.EFFECTS
            )

            intensity = random.randint(
                1,
                5
            )

            duration = random.choice(
                [3, 5, 7, 10]
            )

        else:

            effect = self.effect

            intensity = self.intensity

            duration = self.duration

        self.overlay = CelebrationOverlay(
            effect,
            intensity,
            duration
        )

        self.overlay.show()

        self.overlay.raise_()

    # ========================================================
    # PAINT
    # ========================================================

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
            5,
            6,
            self.width() - 10,
            self.height() - 10,
            19,
            19
        )

        # Body

        painter.setBrush(
            QColor(
                48,
                43,
                39,
                248
            )
        )

        painter.setPen(
            QPen(
                QColor(
                    220,
                    205,
                    185,
                    55
                ),
                1
            )
        )

        painter.drawRoundedRect(
            2,
            2,
            self.width() - 6,
            self.height() - 6,
            18,
            18
        )

        # Header

        painter.setPen(
            QColor("#F3EEE5")
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                13,
                QFont.Weight.Bold
            )
        )

        painter.drawText(
            18,
            27,
            "GLOX  CELEBRATE"
        )

        painter.setPen(
            QColor("#A9A39A")
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                7
            )
        )

        painter.drawText(
            18,
            42,
            "DESKTOP CELEBRATION CONTROL"
        )

        # Effect

        painter.setPen(
            QColor("#F3EEE5")
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                10,
                QFont.Weight.DemiBold
            )
        )

        painter.drawText(
            18,
            68,
            self.effect
        )

        painter.setPen(
            QColor("#A9A39A")
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                7
            )
        )

        painter.drawText(
            18,
            83,
            "EFFECT"
        )

        # Intensity

        painter.setPen(
            QColor("#D8D1C7")
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                8
            )
        )

        painter.drawText(
            18,
            111,
            "INTENSITY"
        )

        for i in range(5):

            x = 80 + i * 24

            painter.setBrush(
                QColor("#D7B56D")
                if i < self.intensity
                else QColor(
                    255,
                    255,
                    255,
                    30
                )
            )

            painter.setPen(
                Qt.NoPen
            )

            painter.drawRoundedRect(
                x,
                104,
                17,
                7,
                3,
                3
            )

        painter.setPen(
            QColor("#D8D1C7")
        )

        painter.drawText(
            215,
            111,
            str(self.intensity)
        )

        # Duration

        painter.setPen(
            QColor("#D8D1C7")
        )

        painter.drawText(
            18,
            137,
            "DURATION"
        )

        painter.setPen(
            QColor("#D7B56D")
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                9,
                QFont.Weight.Bold
            )
        )

        painter.drawText(
            82,
            137,
            f"{self.duration}s"
        )

        # Random

        painter.setPen(
            QColor("#D7B56D")
            if self.random_mode
            else QColor("#A9A39A")
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                8
            )
        )

        painter.drawText(
            135,
            137,
            "● RANDOMIZE"
            if self.random_mode
            else "○ RANDOMIZE"
        )

        # Celebrate button

        painter.setBrush(
            QColor(
                215,
                181,
                109,
                42
            )
        )

        painter.setPen(
            QPen(
                QColor(
                    215,
                    181,
                    109,
                    120
                ),
                1
            )
        )

        painter.drawRoundedRect(
            18,
            153,
            264,
            48,
            12,
            12
        )

        painter.setPen(
            QColor("#F3EEE5")
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                10,
                QFont.Weight.Bold
            )
        )

        painter.drawText(
            18,
            153,
            264,
            48,
            Qt.AlignCenter,
            "✦  CELEBRATE"
        )

        # Footer

        painter.setPen(
            QColor("#77716A")
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                6
            )
        )

        painter.drawText(
            18,
            225,
            "Left click: celebrate   •   Right click: options"
        )

    # ========================================================
    # MOUSE
    # ========================================================

    def mousePressEvent(self, event):

        if event.button() == Qt.RightButton:

            self.show_menu(
                event.globalPosition().toPoint()
            )

            return

        if event.button() == Qt.LeftButton:

            x = event.position().x()
            y = event.position().y()

            # Celebrate button

            if 153 <= y <= 201:

                self.celebrate()

                return

            # Intensity

            if 98 <= y <= 120:

                if 75 <= x <= 215:

                    value = round(
                        (x - 80) / 24
                    ) + 1

                    self.intensity = max(
                        1,
                        min(
                            5,
                            value
                        )
                    )

                    self.random_mode = False

                    self.update()

                    return

            # Randomize

            if (
                120 <= y <= 145
                and 125 <= x <= 280
            ):

                self.random_mode = (
                    not self.random_mode
                )

                self.update()

                return

            # Drag

            self.dragging = True

            self.drag_offset = (
                event.globalPosition()
                .toPoint()
                - self.frameGeometry()
                .topLeft()
            )

    def mouseMoveEvent(self, event):

        if (
            self.dragging
            and event.buttons()
            & Qt.LeftButton
        ):

            self.move(
                event.globalPosition()
                .toPoint()
                - self.drag_offset
            )

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.dragging = False

    # ========================================================
    # MENU
    # ========================================================

    def show_menu(self, position):

        menu = QMenu(self)

        menu.setStyleSheet("""
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
        """)

        # Effects

        effects = menu.addMenu(
            "Celebration"
        )

        for effect in self.EFFECTS:

            action = effects.addAction(
                effect
            )

            action.setCheckable(True)

            action.setChecked(
                effect == self.effect
                and not self.random_mode
            )

            action.triggered.connect(
                lambda checked=False,
                e=effect:
                self.set_effect(e)
            )

        # Intensity

        intensity_menu = menu.addMenu(
            "Intensity"
        )

        labels = [
            "Subtle",
            "Light",
            "Normal",
            "High",
            "INSANE"
        ]

        for value in range(1, 6):

            action = intensity_menu.addAction(
                f"{value} — {labels[value - 1]}"
            )

            action.triggered.connect(
                lambda checked=False,
                v=value:
                self.set_intensity(v)
            )

        # Duration

        duration_menu = menu.addMenu(
            "Duration"
        )

        for value in [3, 5, 7, 10]:

            action = duration_menu.addAction(
                f"{value} seconds"
            )

            action.triggered.connect(
                lambda checked=False,
                v=value:
                self.set_duration(v)
            )

        # Randomize

        random_action = menu.addAction(
            "🎲 Randomize Everything"
        )

        random_action.setCheckable(True)

        random_action.setChecked(
            self.random_mode
        )

        random_action.triggered.connect(
            self.toggle_random
        )

        menu.addSeparator()

        # Celebrate

        celebrate_action = menu.addAction(
            "✦ Celebrate Now"
        )

        celebrate_action.triggered.connect(
            self.celebrate
        )

        menu.addSeparator()

        # Exit

        exit_action = menu.addAction(
            "Exit GLOX Celebrate"
        )

        exit_action.triggered.connect(
            QApplication.quit
        )

        menu.exec(
            position
        )

    # ========================================================
    # SETTINGS
    # ========================================================

    def set_effect(self, effect):

        self.effect = effect

        self.random_mode = False

        self.update()

    def set_intensity(self, value):

        self.intensity = value

        self.random_mode = False

        self.update()

    def set_duration(self, value):

        self.duration = value

        self.random_mode = False

        self.update()

    def toggle_random(self):

        self.random_mode = (
            not self.random_mode
        )

        self.update()


# ============================================================
# MAIN
# ============================================================

def main():

    app = QApplication(sys.argv)

    app.setApplicationName(
        "GLOX Celebrate"
    )

    app.setStyle(
        "Fusion"
    )

    widget = GloxCelebrate()

    widget.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":

    main()