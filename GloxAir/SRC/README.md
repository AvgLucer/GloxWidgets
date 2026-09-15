# Glox Air — Source

This folder contains the source code for **Glox Air**, a lightweight Windows voice-command application developed by **Glox Industries**.

The main application file is:

```text
gloxair.py
```

## 🎙️ About Glox Air

Glox Air listens for spoken commands, converts the recorded microphone audio into text, and performs supported desktop actions.

The basic flow is:

```text
🎙️ Microphone
      ↓
sounddevice
      ↓
Temporary WAV
      ↓
SpeechRecognition
      ↓
Command Processing
      ↓
Desktop Action
```

## Glox Air also provides local text-to-speech functionality through `pyttsx3`.

## 📁 Source Structure

```text
SRC/
│
├── gloxair.py
├── requirements.txt
└── README.md
```

| File               | Purpose                     |
| ------------------ | --------------------------- |
| `gloxair.py`       | Main Glox Air application   |
| `requirements.txt` | Python package dependencies |
| `README.md`        | Source-code documentation   |

---

## ⚙️ Dependencies

| Package               | Purpose                      |
| --------------------- | ---------------------------- |
| **sounddevice**       | Captures microphone audio    |
| **SpeechRecognition** | Processes speech recognition |
| **pyttsx3**           | Provides text-to-speech      |

The application also uses Python standard-library modules including `tkinter`, `wave`, `threading`, `json`, `subprocess`, `webbrowser`, `tempfile`, and others.

### Python Standard Library

These modules do **not** need to be installed separately:

```text
os
re
json
time
shutil
difflib
ctypes
subprocess
webbrowser
datetime
tempfile
wave
threading
tkinter
```

---

## 📦 Installation

Open a terminal inside the `SRC` directory:

```bash
pip install -r requirements.txt
```

Then run:

```bash
python gloxair.py
```

---

## 🎤 Microphone

Glox Air uses `sounddevice` to record microphone input.

The application records audio as:

```text
Mono
16-bit integer audio
16 kHz sample rate
```

The recorded audio is temporarily written as a WAV file before being passed to the speech-recognition system.

A working microphone is therefore required for voice commands.

---

## 🔊 Text-to-Speech

Glox Air uses **pyttsx3** for text-to-speech.

Speech is generated locally through the installed system speech engine rather than requiring an external AI voice service.

---

## 📴 No FFmpeg

Glox Air's source does **not** require FFmpeg.

Audio recording uses:

```text
sounddevice
      ↓
Python wave
      ↓
WAV
      ↓
SpeechRecognition
```

There is no FFmpeg-based audio conversion pipeline in the source.

---

## 🤖 No Generative AI

Glox Air is **not an AI chatbot** and does not require a generative AI model.

Its purpose is straightforward:

> **Speak. Command. Done.**

The application recognizes supported spoken commands and performs the corresponding desktop actions.

---

## 🖥️ Platform

Glox Air is designed for:

**Windows desktop**

The source contains Windows-oriented functionality for launching applications, handling shortcuts, desktop actions, media controls, and related operations.

---

## 🚀 Running From Source

Clone/download the project and enter the source directory:

```bash
cd SRC
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Glox Air:

```bash
python gloxair.py
```

---

## 👨‍💻 Credits

<p align="center">
  <b>AvgLucer | Gaurav W</b><br>
  CEO & Founder — <b>Glox Industries</b>
</p>

<p align="center">
  Building Softwares With a New Vision.
</p>

---

## ⚠️ Educational & User-Purpose Notice

<table>
<tr>
<td>

### 🟨⚠️ WARNING

**Glox Air source code is provided for user purposes, educational purposes, and teaching purposes only.**

This source is intended for learning, experimentation, software development education, and understanding how desktop voice-command applications are built.

**Do not submit, publish, redistribute, or present this source code as your own original project.**

If you study, modify, reference, or learn from this source, respect the original creator and **AvgLucer | Gaurav W / Glox Industries**.

This project must not be falsely represented as independently created work.

</td>
</tr>
</table>

---

<p align="center">
  <sub>© AvgLucer | Gaurav W — Glox Industries</sub><br>
  <sub>Building Softwares With a New Vision.</sub>
</p>
