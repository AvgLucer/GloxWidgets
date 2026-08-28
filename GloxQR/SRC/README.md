

<h1 align="center">Glox QR — Source</h1>

<p align="center">
  <strong>Source code for the Glox QR desktop QR generator.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PySide6-Qt-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="PySide6">
  <img src="https://img.shields.io/badge/Source-Available-2ea44f?style=for-the-badge" alt="Source Available">
</p>

---

## 🧠 About

This directory contains the **complete Python source** for Glox QR.

Glox QR is a lightweight desktop application designed to generate customizable QR codes from:

* 🔗 URLs
* 📝 Text
* 🔢 Numbers
* 🌐 Redirect links
* 📋 Other text-based content

The application uses **PySide6** for its desktop interface and Python-based QR generation libraries for creating the QR output.

---

## 📁 Contents

```text
SRC/
│
├── gloxqr.py
├── requirements.txt
└── README.md
```

### `gloxqr.py`

The main Glox QR application.

Contains:

* 🖥️ PySide6 user interface
* 📱 QR generation
* 🎨 QR customization
* 🌈 Color controls
* 📐 Size configuration
* ⚙️ Error-correction configuration
* 💾 PNG export
* 📋 QR copying
* 🎭 Application themes
* ⚡ Application logic

### `requirements.txt`

Contains the Python packages required to run the source version of Glox QR.

---

## 🛠️ Requirements

Before running the source code, install:

* **Python 3.10 or newer**
* **pip**
* **Windows** recommended
* Required packages listed in `requirements.txt`

Check your Python version:

```bash
python --version
```

---

## 📦 Installation

### 1. Open the SRC directory

Open a terminal inside this folder.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Glox QR

```bash
python gloxqr.py
```

The Glox QR desktop interface should launch.

---

## 🔄 Development Workflow

A simple development workflow:

```text
Edit gloxqr.py
      ↓
Install / update dependencies
      ↓
Run application
      ↓
Test QR generation
      ↓
Test customization
      ↓
Test export / copy
      ↓
Commit changes
```

---

## 🎨 Customization

Most of the application's appearance and behavior can be modified directly inside `gloxqr.py`.

Developers can customize areas such as:

* Application themes
* UI styling
* Fonts
* Button appearance
* QR colors
* Background colors
* Default dimensions
* Error correction
* Window layout
* Export behavior

Because Glox QR is intentionally compact, the source is easy to inspect and modify.

---

## 🧪 Testing Checklist

Before distributing a modified build, test:

* [ ] Application launches correctly
* [ ] URL QR generation works
* [ ] Text QR generation works
* [ ] Number input works
* [ ] Custom colors work
* [ ] QR size changes correctly
* [ ] Error correction changes correctly
* [ ] Copy functionality works
* [ ] PNG export works
* [ ] Application themes work
* [ ] Invalid / empty input is handled correctly

---

## ⚡ Running Without an Installer

The source version does **not** require an installer.

After installing the dependencies, simply run:

```bash
python gloxqr.py
```

This makes the source version useful for:

* 🧑‍💻 Development
* 🧪 Testing
* 🎓 Learning
* 🔧 Customization
* 🐛 Debugging
* 🧩 Extending Glox QR

---

## 🏗️ Building a Release

If you modify the source and want to create a standalone Windows executable, you can package the application using a Python application bundler such as **PyInstaller**.

Example:

```bash
pip install pyinstaller
```

Then:

```bash
pyinstaller --onefile --windowed gloxqr.py
```

The generated executable will normally appear inside:

```text
dist/
└── gloxqr.exe
```

> Build configuration may need to be adjusted depending on the dependencies and assets used by your modified version.

---

## 🔗 Other Documentation

⬅️ **[Back to Glox QR](../README.md)**

⬇️ **[Download Glox QR](../DOWNLOAD.md)**

---

## 👨‍💻 Credits

**Glox QR** is part of the **Glox Widgets** ecosystem.

Created by:

**AvgLUCER | Gaurav W.**

Built with:

* Python
* PySide6
* Open-source Python libraries

---

## ⚠️ Usage & Attribution

This source code is provided for **educational, teaching, learning, understanding, and personal development purposes**.

You may study the source and experiment with it, but please **do not present the project or modified versions as your own original work**.

Please retain appropriate attribution to the original Glox QR project and its creator when redistributing or publishing derived work.

---

<p align="center">
  <strong>GLOX QR</strong>
  <br>
  <sub>Source • Learn • Build • Customize</sub>
</p>
