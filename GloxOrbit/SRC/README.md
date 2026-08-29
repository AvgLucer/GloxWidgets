# 🌀 GLOX ORBIT — SOURCE

<div align="center">

# `SRC`

### GLOX Orbit Source Code

<p>
  <img src="https://img.shields.io/badge/GLOX-ORBIT-8B4513?style=for-the-badge">
  <img src="https://img.shields.io/badge/Source-Code-6D4C41?style=for-the-badge">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/PySide6-Qt-41CD52?style=for-the-badge&logo=qt&logoColor=white">
</p>

<p>
  <img src="https://img.shields.io/badge/Desktop-Widget-795548?style=flat-square">
  <img src="https://img.shields.io/badge/GUI-PySide6-41CD52?style=flat-square&logo=qt">
  <img src="https://img.shields.io/badge/Animation-QTimer-9E9E9E?style=flat-square">
  <img src="https://img.shields.io/badge/Rendering-QPainter-6D4C41?style=flat-square">
  <img src="https://img.shields.io/badge/Configuration-JSON-000000?style=flat-square&logo=json">
</p>

</div>

---

## 📁 Source Structure

```text
GloxOrbit/
│
├── SRC/
│   │
│   ├── gloxorbit.py
│   ├── requirements.txt
│   └── README.md
│
├── README.md
├── DOWNLOAD.md
└── banner.png
```

---

# 🐍 `gloxorbit.py`

`gloxorbit.py` is the primary source file for GLOX Orbit.

It contains the complete desktop widget implementation, including:

* GLOX Orbit UI
* Circular node positioning
* Orbit animation
* Center pulse animation
* Themes
* Node management
* URL launching
* Application launching
* Folder launching
* Command launching
* Mouse interaction
* Dragging
* Hover detection
* Context menu
* Persistent configuration
* Application startup

The project is intentionally implemented as a **single Python source file**.

---

# 🧩 Core Architecture

The application is centered around the:

```python
class GloxOrbit(QWidget):
```

The class inherits from `PySide6.QtWidgets.QWidget`.

This allows the application to function as a custom-rendered desktop widget rather than relying on a conventional UI layout.

---

# 🎨 Rendering System

GLOX Orbit uses:

```python
QPainter
QPen
QBrush
QColor
QFont
```

for custom rendering.

The entire interface is drawn inside:

```python
def paintEvent(self, event):
```

This includes:

```text
Glass panel
    ↓
Outer shadow
    ↓
Orbit glow
    ↓
Orbit track
    ↓
Connection lines
    ↓
Center glow
    ↓
GLOX core
    ↓
Orbit nodes
    ↓
Labels
    ↓
Header / footer
```

This provides direct control over the widget's visual appearance.

---

# 🌀 Orbit Mathematics

Orbit nodes are positioned using trigonometry.

The primary calculation occurs inside:

```python
def node_position(self, index):
```

The widget calculates:

```text
Center
   +
Radius
   +
Angular spacing
   +
Current rotation
```

The angular spacing is determined from the number of nodes:

```python
angle_step = 360 / count
```

The current rotation is then added to the node's angle.

The resulting angle is converted into radians:

```python
radians = math.radians(angle)
```

The node coordinates are calculated using:

```text
x = center.x + cos(angle) × radius

y = center.y + sin(angle) × radius
```

This creates the circular orbit.

---

# ⏱️ Animation System

GLOX Orbit uses a Qt timer:

```python
self.timer = QTimer(self)
```

The timer runs approximately every:

```text
16 milliseconds
```

which targets approximately:

```text
60 FPS
```

The timer calls:

```python
self.animate
```

The animation updates:

### Rotation

```python
self.rotation += self.rotation_speed
```

### Center Pulse

```python
self.pulse += (
    0.025 * self.pulse_direction
)
```

The widget is then repainted:

```python
self.update()
```

---

# ⚡ Orbit Speed

Orbit speed is controlled through:

```python
self.rotation_speed
```

Available presets:

| Mode      |  Speed |
| --------- | -----: |
| Slow      | `0.08` |
| Normal    | `0.25` |
| Fast      | `0.55` |
| Very Fast |  `0.9` |

The speed can be changed from the right-click menu.

---

# 🎨 Theme System

Themes are stored inside:

```python
THEMES = {}
```

The source currently defines:

```text
Glox Brown
Obsidian
Espresso
Midnight
Pearl
```

Each theme controls:

```text
Background
Border
Accent
Secondary Accent
Text
Muted Text
```

Example:

```python
"Glox Brown": {
    "background": ...,
    "border": ...,
    "accent": ...,
    "accent2": ...,
    "text": ...,
    "muted": ...,
}
```

This keeps the rendering code independent from the visual theme definitions.

---

# 🎯 Orbit Nodes

Nodes are represented using dictionaries.

Example:

```python
{
    "name": "GitHub",
    "type": "url",
    "target": "https://github.com",
}
```

Each node contains:

| Property | Purpose          |
| -------- | ---------------- |
| `name`   | Display name     |
| `type`   | Destination type |
| `target` | Destination      |

---

# 🔗 Supported Destination Types

The source supports several destination types.

### 🌐 URL

```python
"type": "url"
```

Uses:

```python
webbrowser.open(target)
```

---

### 📁 Folder

```python
"type": "folder"
```

Uses:

```python
os.startfile(target)
```

This is primarily intended for Windows.

---

### ⚙️ Executable

```python
"type": "exe"
```

Uses:

```python
subprocess.Popen(
    target,
    shell=True
)
```

---

### 💻 Command

```python
"type": "command"
```

Also uses:

```python
subprocess.Popen(
    target,
    shell=True
)
```

---

# 🖱️ Mouse Interaction

GLOX Orbit supports interactive mouse controls.

## Left Click

Clicking a node launches its destination.

Clicking elsewhere allows the widget to be dragged.

---

## Right Click

Right-clicking opens the configuration menu.

The menu contains:

```text
Theme
Orbit Speed
Add Orbit
Remove Orbit
Reset Orbits
Exit GLOX Orbit
```

---

# 🖐️ Dragging

The widget can be repositioned by dragging it with the left mouse button.

The drag position is calculated using:

```python
event.globalPosition()
```

and the widget's frame position.

This allows the widget to be freely positioned on the desktop.

---

# 👆 Hover System

The source detects whether the mouse is close to an orbit node through:

```python
def node_at(self, position):
```

The distance between the cursor and node is calculated mathematically.

When a node is hovered:

* The node becomes larger.
* A glow appears.
* The border becomes more visible.
* The cursor changes to a pointing cursor.
* Connection-line opacity increases.

---

# 💾 Persistent Configuration

GLOX Orbit stores its configuration in the user's home directory:

```text
~/.glox_orbit.json
```

The path is generated with:

```python
CONFIG_FILE = os.path.join(
    os.path.expanduser("~"),
    ".glox_orbit.json"
)
```

The configuration stores:

```json
{
  "theme": "Glox Brown",
  "speed": 0.25,
  "nodes": []
}
```

This allows settings to persist between launches.

---

# ➕ Adding Nodes

Nodes can be added through:

```text
Right Click
      ↓
Add Orbit
```

The user provides:

```text
Orbit name
URL / application / folder
```

The application automatically determines the node type.

### URL

If the target begins with:

```text
http://
https://
```

the node becomes a URL node.

### Folder

If:

```python
os.path.isdir(target)
```

returns `True`, it becomes a folder node.

### Everything Else

Other targets are treated as executable destinations.

---

# ➖ Removing Nodes

Nodes can be removed from:

```text
Right Click
      ↓
Remove Orbit
      ↓
Select Node
```

The selected node is removed from the configuration and the interface is immediately updated.

---

# 🔄 Resetting Nodes

The:

```text
Reset Orbits
```

option restores the default node configuration.

The default destinations include:

```text
Browser
VS Code
Files
Terminal
GitHub
YouTube
```

---

# 🧱 Window Configuration

GLOX Orbit uses a fixed:

```text
430 × 430
```

window.

The window uses:

```python
Qt.FramelessWindowHint
Qt.WindowStaysOnTopHint
Qt.Tool
```

This provides the floating-widget behavior.

The application also enables:

```python
Qt.WA_TranslucentBackground
```

for the transparent/glass-style interface.

---

# 📦 Dependencies

The source requires:

```text
PySide6
```

The Python standard library provides the remaining functionality used by the source.

These include:

```text
sys
os
json
math
subprocess
webbrowser
```

No separate installation is required for those modules.

---

# ▶️ Running From Source

Open a terminal inside the `SRC` directory.

Install the dependency:

```bash
pip install -r requirements.txt
```

Then run:

```bash
python gloxorbit.py
```

Alternatively:

```bash
python3 gloxorbit.py
```

depending on your Python installation.

---

# 🧪 Development

For development, the recommended structure is:

```text
GloxOrbit/
└── SRC/
    ├── gloxorbit.py
    ├── requirements.txt
    └── README.md
```

The application is designed so that most behavior can be studied directly from `gloxorbit.py`.

---

# 📖 Educational Topics Covered

This source is useful for studying:

* Python GUI programming
* PySide6
* Qt widgets
* Custom painting
* QPainter
* QTimer
* Event handling
* Mouse events
* JSON configuration
* File handling
* Subprocess execution
* Web browser launching
* Trigonometry
* Circular coordinate systems
* UI animation
* Transparency
* Desktop widgets
* Context menus
* Object-oriented programming

---

# ⚠️ Source Usage Notice

> **GLOX Orbit was created by Avg Lucer | Gaurav W.**

The source code is provided for:

**user purposes, teaching, understanding, experimentation, and educational use only.**

Do **not** claim this source code or GLOX Orbit as your own original project.

Do not remove creator attribution when redistributing, demonstrating, studying, or referencing the project.

If you create your own project after studying this source, make your implementation and project identity genuinely your own and provide appropriate attribution where the original project is referenced.

---

# 👤 Original Creator

**Avg Lucer | Gaurav W**

### Project

**GLOX Orbit**

### Organization / Brand

**GLOX Industries**

---

# 📚 Related Documentation

| File                               | Purpose                       |
| ---------------------------------- | ----------------------------- |
| [`../README.md`](../README.md)     | Main GLOX Orbit documentation |
| [`../DOWNLOAD.md`](../DOWNLOAD.md) | Download information          |
| `gloxorbit.py`                     | Main source code              |
| `requirements.txt`                 | Python dependency list        |

---

<div align="center">

<img src="https://img.shields.io/badge/GLOX-INDUSTRIES-8B4513?style=for-the-badge">

### 🌀 GLOX ORBIT

**Your Desktop. In Motion.**

**Created by Avg Lucer | Gaurav W**

</div>
