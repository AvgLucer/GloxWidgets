# ============================================================
# GLOX PET
# Lightweight robotic desktop pet
# ============================================================

import sys
import random
import math
import time

from PySide6.QtCore import (
    Qt,
    QTimer,
    QPointF,
)

from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
    QBrush,
    QFont,
)

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMenu,
)


# ============================================================
# GLOX MESSAGE
# ============================================================

class GloxMessage(QWidget):

    def __init__(self, text, parent_pet):

        super().__init__()

        self.parent_pet = parent_pet

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground
        )

        self.setFixedSize(
            190,
            70
        )

        self.text = text

        self.opacity = 1.0

        self.show()

        # Position above the pet

        pet_pos = parent_pet.pos()

        self.move(
            pet_pos.x()
            + parent_pet.width() // 2
            - self.width() // 2,

            pet_pos.y()
            - self.height()
            - 8
        )

        # Auto close

        QTimer.singleShot(
            2200,
            self.close
        )

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        # Shadow

        painter.setPen(Qt.NoPen)

        painter.setBrush(
            QColor(
                0,
                0,
                0,
                100
            )
        )

        painter.drawRoundedRect(
            5,
            5,
            self.width() - 10,
            self.height() - 10,
            14,
            14
        )

        # Main bubble

        painter.setBrush(
            QColor(
                35,
                35,
                40,
                245
            )
        )

        painter.setPen(
            QPen(
                self.parent_pet.THEMES[
                    self.parent_pet.theme
                ]["eye"],
                1
            )
        )

        painter.drawRoundedRect(
            2,
            2,
            self.width() - 8,
            self.height() - 8,
            14,
            14
        )

        # Text

        painter.setPen(
            QColor(
                240,
                240,
                245
            )
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                10,
                QFont.Weight.Bold
            )
        )

        painter.drawText(
            self.rect(),
            Qt.AlignCenter,
            self.text
        )


# ============================================================
# FIREWORKS + DIWALI EFFECT
# ============================================================

class FireworksOverlay(QWidget):

    def __init__(self):

        super().__init__()

        self.particles = []
        self.rockets = []
        self.fountains = []

        self.start_time = time.time()

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

        if screen:

            self.setGeometry(
                screen.geometry()
            )

        # Create limited Diwali fountain positions

        width = self.width()
        height = self.height()

        self.fountains = [

            {
                "x": width * 0.18,
                "y": height * 0.92,
                "timer": random.randint(0, 30),
            },

            {
                "x": width * 0.82,
                "y": height * 0.92,
                "timer": random.randint(0, 30),
            },

            {
                "x": width * 0.50,
                "y": height * 0.95,
                "timer": random.randint(0, 30),
            },
        ]

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.animate
        )

        self.timer.start(30)

        self.spawn_timer = QTimer(self)

        self.spawn_timer.timeout.connect(
            self.spawn_firework
        )

        self.spawn_timer.start(180)

        self.show()

    # ========================================================
    # FIREWORK ROCKET
    # ========================================================

    def spawn_firework(self):

        # Stop creating new ones near the end

        if time.time() - self.start_time > 8.5:
            return

        if len(self.rockets) >= 7:
            return

        width = self.width()
        height = self.height()

        x = random.randint(
            70,
            max(
                71,
                width - 70
            )
        )

        target_y = random.randint(
            int(height * 0.12),
            int(height * 0.58)
        )

        self.rockets.append({

            "x": float(x),

            "y": float(height),

            "target": float(target_y),

            "speed": random.uniform(
                11,
                17
            ),

            "color": random.choice([
                QColor(120, 220, 255),
                QColor(255, 120, 180),
                QColor(255, 210, 90),
                QColor(170, 130, 255),
                QColor(120, 255, 170),
                QColor(255, 150, 90),
            ])
        })

    # ========================================================
    # FIREWORK EXPLOSION
    # ========================================================

    def explode(
        self,
        x,
        y,
        color
    ):

        for _ in range(70):

            angle = random.uniform(
                0,
                math.pi * 2
            )

            speed = random.uniform(
                2,
                7
            )

            self.particles.append({

                "type": "firework",

                "x": float(x),

                "y": float(y),

                "vx": math.cos(angle) * speed,

                "vy": math.sin(angle) * speed,

                "life": random.randint(
                    35,
                    70
                ),

                "max_life": 70,

                "color": color,

                "size": random.uniform(
                    1.5,
                    3.5
                ),
            })

    # ========================================================
    # DIWALI FOUNTAIN PARTICLES
    # ========================================================

    def spawn_fountain_particle(
        self,
        fountain
    ):

        color = random.choice([
            QColor(255, 190, 50),
            QColor(255, 120, 50),
            QColor(255, 230, 100),
            QColor(255, 160, 80),
        ])

        angle = random.uniform(
            math.radians(205),
            math.radians(335)
        )

        speed = random.uniform(
            3,
            7
        )

        self.particles.append({

            "type": "fountain",

            "x": fountain["x"],

            "y": fountain["y"],

            "vx": math.cos(angle) * speed,

            "vy": math.sin(angle) * speed,

            "life": random.randint(
                20,
                42
            ),

            "max_life": 42,

            "color": color,

            "size": random.uniform(
                1.2,
                3
            ),
        })

    # ========================================================
    # ANIMATION
    # ========================================================

    def animate(self):

        elapsed = (
            time.time()
            - self.start_time
        )

        # HARD 10 SECOND LIMIT

        if elapsed >= 10:

            self.close()

            return

        # ----------------------------------------------------
        # Rockets
        # ----------------------------------------------------

        remaining_rockets = []

        for rocket in self.rockets:

            rocket["y"] -= rocket["speed"]

            if (
                rocket["y"]
                <= rocket["target"]
            ):

                self.explode(
                    rocket["x"],
                    rocket["y"],
                    rocket["color"]
                )

            else:

                remaining_rockets.append(
                    rocket
                )

        self.rockets = (
            remaining_rockets
        )

        # ----------------------------------------------------
        # Fountain generation
        # ----------------------------------------------------

        if elapsed < 8.5:

            for fountain in self.fountains:

                fountain["timer"] += 1

                if fountain["timer"] % 2 == 0:

                    self.spawn_fountain_particle(
                        fountain
                    )

        # ----------------------------------------------------
        # Particle physics
        # ----------------------------------------------------

        remaining_particles = []

        for particle in self.particles:

            particle["x"] += (
                particle["vx"]
            )

            particle["y"] += (
                particle["vy"]
            )

            if particle["type"] == "firework":

                particle["vy"] += 0.075

                particle["vx"] *= 0.985
                particle["vy"] *= 0.985

            else:

                # Fountain gravity

                particle["vy"] += 0.12

                particle["vx"] *= 0.99

            particle["life"] -= 1

            if particle["life"] > 0:

                remaining_particles.append(
                    particle
                )

        self.particles = (
            remaining_particles
        )

        self.update()

    # ========================================================
    # DRAW
    # ========================================================

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        # ----------------------------------------------------
        # Rockets
        # ----------------------------------------------------

        painter.setPen(
            QPen(
                QColor(
                    255,
                    255,
                    255,
                    190
                ),
                2
            )
        )

        for rocket in self.rockets:

            painter.drawLine(
                int(rocket["x"]),
                int(rocket["y"]),
                int(rocket["x"]),
                int(rocket["y"] + 16)
            )

        # ----------------------------------------------------
        # Particles
        # ----------------------------------------------------

        painter.setPen(
            Qt.NoPen
        )

        for particle in self.particles:

            alpha = int(
                255
                * (
                    particle["life"]
                    / particle["max_life"]
                )
            )

            color = QColor(
                particle["color"]
            )

            color.setAlpha(
                max(
                    0,
                    alpha
                )
            )

            painter.setBrush(
                color
            )

            size = particle["size"]

            painter.drawEllipse(
                int(
                    particle["x"]
                    - size / 2
                ),

                int(
                    particle["y"]
                    - size / 2
                ),

                int(size),

                int(size)
            )


# ============================================================
# GLOX PET
# ============================================================

class GloxPet(QWidget):

    WIDTH = 170
    HEIGHT = 190

    THEMES = {

        "Obsidian": {
            "body": QColor(
                62,
                64,
                70
            ),

            "accent": QColor(
                180,
                185,
                195
            ),

            "eye": QColor(
                120,
                220,
                255
            ),
        },

        "Graphite": {
            "body": QColor(
                72,
                73,
                78
            ),

            "accent": QColor(
                190,
                190,
                195
            ),

            "eye": QColor(
                170,
                220,
                255
            ),
        },

        "Charcoal": {
            "body": QColor(
                80,
                78,
                76
            ),

            "accent": QColor(
                205,
                195,
                185
            ),

            "eye": QColor(
                255,
                205,
                120
            ),
        },

        "Espresso": {
            "body": QColor(
                82,
                67,
                59
            ),

            "accent": QColor(
                210,
                190,
                170
            ),

            "eye": QColor(
                255,
                190,
                110
            ),
        },

        "Slate": {
            "body": QColor(
                62,
                74,
                82
            ),

            "accent": QColor(
                185,
                205,
                215
            ),

            "eye": QColor(
                110,
                225,
                255
            ),
        },

        "Midnight": {
            "body": QColor(
                48,
                53,
                70
            ),

            "accent": QColor(
                175,
                185,
                220
            ),

            "eye": QColor(
                145,
                170,
                255
            ),
        },
    }

    MESSAGES = [

        "Meow!",

        "Grrr!",

        "Mrrp!",

        "Hello!",

        "GLOX!",

        "Blep!",

        "Purrr...",

        "Beep boop!",

        "Feed me!",

        "0101...",

        "Who's coding?",

        "Hehe!",

        "Zoom!",

        "I'm awake!",

        "System nominal!",

        "Meow.exe",

        "GLOX online.",

        "Nice click!",

        "What are you doing?",

        "Boop!",
    ]

    # ========================================================
    # INIT
    # ========================================================

    def __init__(self):

        super().__init__()

        self.theme = "Obsidian"

        self.opacity_value = 100

        self.idle_opacity = 0.60

        self.dragging = False

        self.drag_offset = QPointF()

        self.drag_distance = 0

        self.blinking = False

        self.sleeping = False

        self.eye_direction = 0

        self.walking = False

        self.walk_target = None

        self.animation = None

        self.animation_frame = 0

        # ----------------------------------------------------
        # Click tracking
        # ----------------------------------------------------

        self.click_count = 0

        self.click_timer = QTimer(
            self
        )

        self.click_timer.setSingleShot(
            True
        )

        self.click_timer.timeout.connect(
            self.process_clicks
        )

        # ----------------------------------------------------
        # Idle opacity
        # ----------------------------------------------------

        self.setWindowOpacity(
            self.idle_opacity
        )

        self.opacity_timer = QTimer(
            self
        )

        self.opacity_timer.setSingleShot(
            True
        )

        self.opacity_timer.timeout.connect(
            self.return_idle
        )

        # ----------------------------------------------------

        self.setFixedSize(
            self.WIDTH,
            self.HEIGHT
        )

        self.setWindowTitle(
            "GLOX Pet"
        )

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground
        )

        # ----------------------------------------------------
        # Main animation timer
        # ----------------------------------------------------

        self.animation_timer = QTimer(
            self
        )

        self.animation_timer.timeout.connect(
            self.animate
        )

        self.animation_timer.start(
            30
        )

        # ----------------------------------------------------
        # Blink
        # ----------------------------------------------------

        self.blink_timer = QTimer(
            self
        )

        self.blink_timer.timeout.connect(
            self.blink
        )

        self.blink_timer.start(
            random.randint(
                2500,
                5000
            )
        )

        # ----------------------------------------------------
        # Random behavior
        # ----------------------------------------------------

        self.behavior_timer = QTimer(
            self
        )

        self.behavior_timer.timeout.connect(
            self.random_behavior
        )

        self.behavior_timer.start(
            5000
        )

        # ----------------------------------------------------
        # Start position
        # ----------------------------------------------------

        screen = QApplication.primaryScreen()

        if screen:

            geometry = (
                screen.availableGeometry()
            )

            self.move(
                geometry.right()
                - self.WIDTH
                - 40,

                geometry.bottom()
                - self.HEIGHT
                - 30
            )

    # ========================================================
    # OPACITY
    # ========================================================

    def wake_visual(self):

        self.setWindowOpacity(
            self.opacity_value / 100
        )

        self.opacity_timer.start(
            1800
        )

    def return_idle(self):

        if not self.dragging:

            self.setWindowOpacity(
                self.idle_opacity
            )

    # ========================================================
    # CLICK
    # ========================================================

    def register_click(self):

        self.wake_visual()

        self.click_count += 1

        self.click_timer.start(
            350
        )

    # ========================================================
    # PROCESS CLICKS
    # ========================================================

    def process_clicks(self):

        count = self.click_count

        self.click_count = 0

        if count >= 3:

            self.start_fireworks()

        elif count == 2:

            self.start_cartwheel()

        else:

            self.start_happy()

            self.show_message()

    # ========================================================
    # MESSAGE
    # ========================================================

    def show_message(self):

        message = random.choice(
            self.MESSAGES
        )

        self.message_window = (
            GloxMessage(
                message,
                self
            )
        )

    # ========================================================
    # HAPPY
    # ========================================================

    def start_happy(self):

        self.animation = "happy"

        self.animation_frame = 0

        self.sleeping = False

        self.walking = False

        self.update()

    # ========================================================
    # CARTWHEEL
    # ========================================================

    def start_cartwheel(self):

        self.animation = "cartwheel"

        self.animation_frame = 0

        self.sleeping = False

        self.walking = False

        self.update()

    # ========================================================
    # FIREWORKS
    # ========================================================

    def start_fireworks(self):

        self.animation = "celebrate"

        self.animation_frame = 0

        self.sleeping = False

        self.walking = False

        self.fireworks = (
            FireworksOverlay()
        )

        self.update()

    # ========================================================
    # ANIMATION
    # ========================================================

    def animate(self):

        if self.animation:

            self.animation_frame += 1

            if self.animation == "happy":

                if self.animation_frame > 30:

                    self.animation = None

            elif self.animation == "cartwheel":

                if self.animation_frame > 50:

                    self.animation = None

            elif self.animation == "celebrate":

                if self.animation_frame > 90:

                    self.animation = None

        # ----------------------------------------------------
        # Walking
        # ----------------------------------------------------

        if (
            self.walking
            and self.walk_target
            and not self.animation
        ):

            x = self.x()
            y = self.y()

            tx, ty = self.walk_target

            dx = tx - x
            dy = ty - y

            distance = (
                dx * dx
                + dy * dy
            ) ** 0.5

            if distance < 4:

                self.walking = False

                self.walk_target = None

            else:

                speed = 2

                self.move(
                    int(
                        x
                        + dx
                        / distance
                        * speed
                    ),

                    int(
                        y
                        + dy
                        / distance
                        * speed
                    )
                )

        self.update()

    # ========================================================
    # BLINK
    # ========================================================

    def blink(self):

        if (
            self.sleeping
            or self.animation
            or self.dragging
        ):

            return

        self.blinking = True

        self.update()

        QTimer.singleShot(
            150,
            self.finish_blink
        )

        self.blink_timer.start(
            random.randint(
                2500,
                6000
            )
        )

    def finish_blink(self):

        self.blinking = False

        self.update()

    # ========================================================
    # RANDOM BEHAVIOR
    # ========================================================

    def random_behavior(self):

        if (
            self.animation
            or self.dragging
        ):

            return

        action = random.choice([
            "nothing",
            "look",
            "walk",
            "sleep",
        ])

        if action == "look":

            self.eye_direction = random.choice(
                [-1, 0, 1]
            )

        elif action == "walk":

            screen = QApplication.primaryScreen()

            if screen:

                geometry = (
                    screen.availableGeometry()
                )

                self.walk_target = (

                    random.randint(
                        geometry.left() + 20,
                        geometry.right()
                        - self.WIDTH
                        - 20
                    ),

                    random.randint(
                        geometry.top() + 20,
                        geometry.bottom()
                        - self.HEIGHT
                        - 20
                    )
                )

                self.walking = True

        elif action == "sleep":

            self.sleeping = True

            QTimer.singleShot(
                random.randint(
                    2500,
                    6000
                ),
                self.wake_up
            )

        self.update()

    def wake_up(self):

        self.sleeping = False

        self.update()

    # ========================================================
    # PAINT
    # ========================================================

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        theme = self.THEMES[
            self.theme
        ]

        body = theme["body"]

        accent = theme["accent"]

        eye = theme["eye"]

        painter.save()

        # ----------------------------------------------------
        # Cartwheel
        # ----------------------------------------------------

        if self.animation == "cartwheel":

            progress = min(
                1,
                self.animation_frame / 50
            )

            angle = (
                progress
                * 360
            )

            painter.translate(
                self.WIDTH / 2,
                95
            )

            painter.rotate(
                angle
            )

            painter.translate(
                -self.WIDTH / 2,
                -95
            )

        # ----------------------------------------------------
        # Happy / celebration bounce
        # ----------------------------------------------------

        elif self.animation in (
            "happy",
            "celebrate"
        ):

            bounce = (
                math.sin(
                    self.animation_frame
                    * 0.4
                )
                * 8
            )

            painter.translate(
                0,
                -abs(bounce)
            )

        # ----------------------------------------------------
        # Shadow
        # ----------------------------------------------------

        painter.setPen(
            Qt.NoPen
        )

        painter.setBrush(
            QColor(
                0,
                0,
                0,
                70
            )
        )

        painter.drawEllipse(
            28,
            151,
            114,
            20
        )

        # ----------------------------------------------------
        # Tail
        # ----------------------------------------------------

        pen = QPen(
            accent,
            8
        )

        pen.setCapStyle(
            Qt.RoundCap
        )

        painter.setPen(pen)

        painter.drawArc(
            105,
            105,
            45,
            45,
            -80 * 16,
            180 * 16
        )

        # ----------------------------------------------------
        # Body
        # ----------------------------------------------------

        painter.setPen(
            QPen(
                QColor(
                    255,
                    255,
                    255,
                    45
                ),
                2
            )
        )

        painter.setBrush(
            body
        )

        painter.drawRoundedRect(
            38,
            82,
            94,
            73,
            25,
            25
        )

        # ----------------------------------------------------
        # Chest panel
        # ----------------------------------------------------

        painter.setPen(
            Qt.NoPen
        )

        painter.setBrush(
            QColor(
                255,
                255,
                255,
                18
            )
        )

        painter.drawRoundedRect(
            60,
            107,
            50,
            32,
            10,
            10
        )

        painter.setBrush(
            eye
        )

        painter.drawEllipse(
            82,
            119,
            7,
            7
        )

        # ----------------------------------------------------
        # Head
        # ----------------------------------------------------

        painter.setPen(
            QPen(
                QColor(
                    255,
                    255,
                    255,
                    55
                ),
                2
            )
        )

        painter.setBrush(
            body
        )

        painter.drawRoundedRect(
            28,
            36,
            114,
            78,
            27,
            27
        )

        # ----------------------------------------------------
        # Ears
        # ----------------------------------------------------

        painter.setPen(
            Qt.NoPen
        )

        painter.setBrush(
            body
        )

        painter.drawPolygon([
            QPointF(38, 52),
            QPointF(43, 20),
            QPointF(65, 43),
        ])

        painter.drawPolygon([
            QPointF(105, 43),
            QPointF(127, 20),
            QPointF(132, 52),
        ])

        # ----------------------------------------------------
        # Ear highlights
        # ----------------------------------------------------

        painter.setBrush(
            QColor(
                255,
                255,
                255,
                30
            )
        )

        painter.drawPolygon([
            QPointF(43, 42),
            QPointF(47, 28),
            QPointF(57, 43),
        ])

        painter.drawPolygon([
            QPointF(110, 43),
            QPointF(124, 28),
            QPointF(127, 42),
        ])

        # ----------------------------------------------------
        # Eyes
        # ----------------------------------------------------

        if (
            self.blinking
            or self.sleeping
        ):

            pen = QPen(
                eye,
                3
            )

            pen.setCapStyle(
                Qt.RoundCap
            )

            painter.setPen(pen)

            painter.drawLine(
                52,
                69,
                67,
                69
            )

            painter.drawLine(
                102,
                69,
                117,
                69
            )

        else:

            painter.setPen(
                Qt.NoPen
            )

            painter.setBrush(
                eye
            )

            offset = (
                self.eye_direction
                * 3
            )

            painter.drawEllipse(
                52 + offset,
                62,
                15,
                15
            )

            painter.drawEllipse(
                102 + offset,
                62,
                15,
                15
            )

            painter.setBrush(
                QColor(
                    255,
                    255,
                    255,
                    180
                )
            )

            painter.drawEllipse(
                56 + offset,
                65,
                4,
                4
            )

            painter.drawEllipse(
                106 + offset,
                65,
                4,
                4
            )

        # ----------------------------------------------------
        # Nose
        # ----------------------------------------------------

        painter.setPen(
            QPen(
                accent,
                2
            )
        )

        painter.drawLine(
            82,
            84,
            85,
            87
        )

        painter.drawLine(
            85,
            87,
            88,
            84
        )

        # ----------------------------------------------------
        # Whiskers
        # ----------------------------------------------------

        painter.setPen(
            QPen(
                QColor(
                    255,
                    255,
                    255,
                    80
                ),
                1
            )
        )

        painter.drawLine(
            43,
            84,
            22,
            80
        )

        painter.drawLine(
            43,
            90,
            21,
            91
        )

        painter.drawLine(
            122,
            84,
            143,
            80
        )

        painter.drawLine(
            122,
            90,
            144,
            91
        )

        # ----------------------------------------------------
        # Feet
        # ----------------------------------------------------

        painter.setPen(
            Qt.NoPen
        )

        painter.setBrush(
            accent
        )

        painter.drawRoundedRect(
            48,
            143,
            24,
            12,
            6,
            6
        )

        painter.drawRoundedRect(
            98,
            143,
            24,
            12,
            6,
            6
        )

        # ----------------------------------------------------
        # GLOX
        # ----------------------------------------------------

        painter.setPen(
            QColor(
                255,
                255,
                255,
                70
            )
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                7,
                QFont.Weight.Bold
            )
        )

        painter.drawText(
            65,
            176,
            "GLOX"
        )

        painter.restore()

    # ========================================================
    # MOUSE PRESS
    # ========================================================

    def mousePressEvent(self, event):

        if event.button() == Qt.RightButton:

            self.show_menu(
                event.globalPosition().toPoint()
            )

            return

        if event.button() == Qt.LeftButton:

            self.dragging = True

            self.drag_distance = 0

            self.drag_offset = (
                event.globalPosition()
                - self.frameGeometry().topLeft()
            )

            self.wake_visual()

            self.sleeping = False

            self.update()

            event.accept()

    # ========================================================
    # MOUSE MOVE
    # ========================================================

    def mouseMoveEvent(self, event):

        if (
            self.dragging
            and event.buttons()
            & Qt.LeftButton
        ):

            new_pos = (
                event.globalPosition()
                - self.drag_offset
            ).toPoint()

            self.drag_distance += (
                abs(
                    new_pos.x()
                    - self.x()
                )
                +
                abs(
                    new_pos.y()
                    - self.y()
                )
            )

            self.walking = False

            self.move(
                new_pos
            )

            event.accept()

    # ========================================================
    # MOUSE RELEASE
    # ========================================================

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:

            was_dragging = (
                self.drag_distance > 8
            )

            self.dragging = False

            # IMPORTANT:
            # If the mouse actually moved,
            # this is ONLY a drag.
            #
            # No single/double/triple action.

            if not was_dragging:

                self.register_click()

            else:

                self.return_idle()

            event.accept()

    # ========================================================
    # MENU
    # ========================================================

    def show_menu(self, position):

        menu = QMenu(
            self
        )

        menu.setStyleSheet("""
            QMenu {
                background: #252525;
                color: white;
                border: 1px solid #444444;
                padding: 5px;
                border-radius: 8px;
            }

            QMenu::item {
                padding: 7px 28px 7px 12px;
                border-radius: 5px;
            }

            QMenu::item:selected {
                background: #3a3a3a;
            }

            QMenu::separator {
                height: 1px;
                background: #444444;
                margin: 5px;
            }
        """)

        # ----------------------------------------------------
        # Theme
        # ----------------------------------------------------

        theme_menu = menu.addMenu(
            "Theme"
        )

        for name in self.THEMES:

            action = theme_menu.addAction(
                name
            )

            action.setCheckable(
                True
            )

            action.setChecked(
                name == self.theme
            )

            action.triggered.connect(
                lambda checked=False,
                n=name:
                self.change_theme(n)
            )

        # ----------------------------------------------------
        # Opacity
        # ----------------------------------------------------

        opacity_menu = menu.addMenu(
            "Opacity"
        )

        for value in (
            100,
            80,
            60,
            50
        ):

            action = opacity_menu.addAction(
                f"{value}%"
            )

            action.setCheckable(
                True
            )

            action.setChecked(
                value == self.opacity_value
            )

            action.triggered.connect(
                lambda checked=False,
                v=value:
                self.change_opacity(v)
            )

        menu.addSeparator()

        # ----------------------------------------------------
        # Sleep
        # ----------------------------------------------------

        sleep_action = menu.addAction(
            "Wake Up"
            if self.sleeping
            else "Sleep"
        )

        sleep_action.triggered.connect(
            self.toggle_sleep
        )

        menu.addSeparator()

        # ----------------------------------------------------
        # Exit
        # ----------------------------------------------------

        exit_action = menu.addAction(
            "Exit"
        )

        exit_action.triggered.connect(
            QApplication.quit
        )

        menu.exec(
            position
        )

    # ========================================================
    # THEME
    # ========================================================

    def change_theme(self, name):

        self.theme = name

        self.update()

    # ========================================================
    # OPACITY
    # ========================================================

    def change_opacity(self, value):

        self.opacity_value = value

        # Selected opacity becomes the "active" opacity
        # when clicked.

        if not self.dragging:

            self.setWindowOpacity(
                value / 100
            )

            self.opacity_timer.start(
                1800
            )

    # ========================================================
    # SLEEP
    # ========================================================

    def toggle_sleep(self):

        self.sleeping = (
            not self.sleeping
        )

        self.update()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )

    app.setStyle(
        "Fusion"
    )

    pet = GloxPet()

    pet.show()

    sys.exit(
        app.exec()
    )