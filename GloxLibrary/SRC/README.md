# Glox Library — Source Code

<p align="center">
  <b>Source Code • Glox Library</b><br>
  <sub>A lightweight local Windows game library and executable launcher.</sub>
</p>

---

## 📁 SRC

This directory contains the core source files required to run **Glox Library** locally.

```text
SRC/
├── README.md
├── requirements.txt
└── gloxlibrary.py
```

---

## 🧩 Files

| File               | Purpose                                          |
| ------------------ | ------------------------------------------------ |
| `gloxlibrary.py`   | Main Glox Library application                    |
| `requirements.txt` | Python dependencies required by the application  |
| `README.md`        | Source-code documentation and setup instructions |

---

## ⚙️ Requirements

Before running Glox Library, make sure you have:

* **Windows**
* **Python 3.10+**
* `pip`
* A local game `.exe` file

Install the required Python packages with:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Glox Library

From inside the `SRC` directory:

```bash
python gloxlibrary.py
```

The application will launch as a desktop window.

---

## 🎮 How It Works

Glox Library is designed around **local executable paths**.

When adding a game, you provide:

* Game name
* Cover image
* Game `.exe`
* Optional description

Glox Library stores the game configuration locally and launches the configured executable directly.

```text
Game
 ↓
Stored locally
 ↓
Saved executable path
 ↓
PLAY
 ↓
Launch game .exe
```

This means Glox Library does **not** depend on desktop shortcuts or third-party game launchers to start your games.

---

## 💾 Local Configuration

Glox Library stores its library data in:

```text
~/.gloxlibrary/
```

The main configuration file is:

```text
games.json
```

Example structure:

```json
[
    {
        "id": "example-id",
        "title": "Example Game",
        "cover": "C:/Games/Example/cover.png",
        "exe": "C:/Games/Example/Game.exe",
        "description": "Example local game."
    }
]
```

Your library configuration is stored locally on your computer.

---

## 🖥️ Supported Games

Glox Library can be used with practically any Windows game that can be launched through a local `.exe`, including:

* DRM-free games
* GOG games
* Indie games
* Older PC games
* Manually installed games
* Games unavailable through major launchers
* Personal game projects
* Standalone Windows executables

> **Note:** Glox Library is a local library/launcher. It does not provide official Steam, Epic Games, GOG, or other platform integrations.

---

## 🎨 Themes

Glox Library includes multiple visual themes that can be selected directly from the application.

Available themes include:

|               |              |
| ------------- | ------------ |
| Obsidian      | Arctic       |
| Midnight Blue | Ocean        |
| Emerald       | Forest       |
| Neon Lime     | Cyber Cyan   |
| Violet        | Royal Purple |
| Rose          | Crimson      |
| Inferno       | Sunset       |
| Amber         | Gold         |
| Espresso      | Glox Cream   |
| Slate         | Monochrome   |

---

## 🔧 Development

The application is built primarily with:

* **Python**
* **PySide6**
* **JSON**
* **Qt Widgets**

The project is intentionally structured as a lightweight desktop application with the main implementation contained in:

```text
gloxlibrary.py
```

---

## ⚠️ Educational & Usage Notice

This source code is provided for **learning, understanding, experimentation, development, and personal user purposes**.

Please do not present the Glox Library project or its source code as your own work.

If you use, modify, study, or build upon this project, please provide appropriate credit to the original creator.

---

## 👤 Credits

**AvgLucer | Gaurav W**
**CEO & Founder — Glox Industries**

Part of the **Glox Widgets** ecosystem.

---

<p align="center">
  <b>GLOX INDUSTRIES</b><br>
  <sub>Build • Experiment • Create</sub>
</p>
