# GloxPrompt DOWNLOAD

<p align="center">
  <strong>Your Ideas. Refined Into Masterpieces.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/GloxPrompt-FF1744?style=for-the-badge&logo=sparkles&logoColor=white">
  <img src="https://img.shields.io/badge/Windows-0078D4?style=for-the-badge&logo=windows&logoColor=white">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/PySide6-41CD52?style=for-the-badge&logo=qt&logoColor=white">
  <img src="https://img.shields.io/badge/OpenRouter-7C3AED?style=for-the-badge">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/AI%20Powered-FF4081?style=flat-square&logo=sparkles&logoColor=white">
  <img src="https://img.shields.io/badge/Multiple%20Models-00B8D4?style=flat-square">
  <img src="https://img.shields.io/badge/Multiple%20Themes-8E5CFF?style=flat-square">
  <img src="https://img.shields.io/badge/Windows%20Executable-FF9800?style=flat-square&logo=windows&logoColor=white">
</p>

---

## 📦 Download

The ready-to-use Windows build of GloxPrompt is available as a ZIP archive.

<p align="center">

<a href="https://www.mediafire.com/file/mrf9ihjdqwp5qug/GloxPrompt.zip/file">

<img src="https://img.shields.io/badge/%E2%AC%87%20DOWNLOAD%20GLOXPROMPT-FF1744?style=for-the-badge&logo=mediafire&logoColor=white">

</a>

</p>

<p align="center">
  <strong>GloxPrompt.zip</strong>
  <br>
  Windows Desktop Application
</p>

---

## 🚀 Running GloxPrompt

### 1. Download

Download the ZIP archive using the button above.

### 2. Extract

Extract `GloxPrompt.zip` anywhere on your computer.

### 3. Configure Your API Key

Before running the application, create a `.env` file according to the included `.env.example`.

Add:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your own OpenRouter API key.

### 4. Launch

Run the executable:

```text
GloxPrompt.exe
```

The application should now open normally.

---

## 🔑 API Configuration

GloxPrompt uses OpenRouter for AI-powered prompt generation.

An API key is required.

Your `.env` configuration should look like:

```env
OPENROUTER_API_KEY=your_api_key_here
```

<p align="center">
  <img src="https://img.shields.io/badge/API%20Required-FF9800?style=for-the-badge">
  <img src="https://img.shields.io/badge/OpenRouter-7C3AED?style=for-the-badge">
</p>

Keep your API key private.

**Never upload your real `.env` file containing your API key to GitHub or any public location.**

---

## ✨ Using GloxPrompt

Once GloxPrompt is running:

```text
Select a model
      ↓
Choose a theme
      ↓
Describe your idea
      ↓
Generate
      ↓
Wait approximately 20–30 seconds
      ↓
Copy your refined prompt
```

Simply describe your idea normally.

You do not need to know advanced prompt engineering.

---

## 🤖 Model Selection

GloxPrompt provides a list of available AI models.

You can select the model you want to use rather than having the application automatically choose one.

Model availability and performance can vary depending on the provider.

Possible differences include:

* Generation speed
* Response quality
* Capabilities
* Availability
* Usage limits
* Pricing

---

## 🎨 Themes

GloxPrompt includes multiple interface themes.

Choose the appearance you prefer and continue generating prompts normally.

<p align="center">
  <img src="https://img.shields.io/badge/Multiple%20Themes-8E5CFF?style=for-the-badge">
  <img src="https://img.shields.io/badge/Personalizable-FF4081?style=for-the-badge">
</p>

---

## ⚡ Generation Time

Typical generation time:

<p align="center">
  <img src="https://img.shields.io/badge/20%E2%80%9330%20Seconds-00C853?style=for-the-badge">
</p>

Generation time can vary depending on the selected model, network connection, API provider and current server conditions.

---

# 💻 Source Code

The GloxPrompt source code is included in the **GloxWidgets** project.

The main source file is:

```text
GloxWidgets/
└── GloxPrompt/
    └── SRC/
        └── gloxprompt.py
```

### Main Source File

`GloxWidgets/GloxPrompt/SRC/gloxprompt.py`

This is the primary Python source file for GloxPrompt.

The downloadable MediaFire package is intended for users who want to run the application without setting up the Python development environment themselves.

---

## 🛠️ Running From Source

If you want to inspect, learn from or run the source code directly, navigate to:

```text
GloxWidgets/GloxPrompt/SRC/
```

and run:

```bash
python gloxprompt.py
```

Make sure the required Python dependencies are installed and that your `.env` configuration is available.

The exact dependency setup may vary depending on the version of the source code.

---

## 📁 Project Location

Within the GloxWidgets repository:

```text
GloxWidgets/
│
└── GloxPrompt/
    │
    └── SRC/
        │
        └── gloxprompt.py
```

The executable release and the source project are separate ways of using GloxPrompt.

**Executable:** for directly running the application.

**Source:** for learning, understanding, development and experimentation.

---

## 🔒 Security

Your API key belongs to you.

Keep your `.env` file private.

Never commit credentials to a public repository.

Use `.env.example` when sharing configuration structure without exposing your actual API key.

If your API key is accidentally exposed, revoke it and generate a new one through your API provider.

---

## 🧩 Troubleshooting

### The `.exe` does not launch

Make sure the ZIP archive has been completely extracted.

Windows Security or another security application may also block an unfamiliar executable.

### Prompt generation does not work

Check:

* Internet connection
* API key
* Selected model
* OpenRouter availability
* Account access
* Available credits where applicable

### The API key is not detected

Make sure your file is named exactly:

```text
.env
```

and contains:

```env
OPENROUTER_API_KEY=your_api_key_here
```

### A selected model is unavailable

Try another model from the available model list.

Model availability can change over time.

---

## 👤 Credits

**AvgLucer | Gaurav W**

**Founder & CEO at Glox Industries**

Created and developed by:

**AvgLucer | Gaurav W**
**Glox Industries**

> **Building Softwares With a New Vision.**

---

## ⚠️ Educational & Usage Warning

<p align="center">
  <img src="https://img.shields.io/badge/Educational%20Use-FF9800?style=for-the-badge&logo=bookstack&logoColor=white">
  <img src="https://img.shields.io/badge/Respect%20The%20Creator-FF1744?style=for-the-badge">
</p>

GloxPrompt is provided for **user, teaching, understanding, learning, experimentation and educational purposes**.

Users are encouraged to explore the application and source code, understand how it works and learn from its implementation.

This project must **not** be falsely presented or claimed as an independently created project by someone who did not originally develop it.

If you use, reference, study or build upon GloxPrompt for educational purposes, please provide appropriate credit to:

**AvgLucer | Gaurav W**
**Founder & CEO, Glox Industries**

Please respect the original creator and the work involved in developing GloxPrompt.

---

<p align="center">
  <img src="https://img.shields.io/badge/Glox%20Industries-111111?style=for-the-badge">
  <img src="https://img.shields.io/badge/Building%20Softwares%20With%20a%20New%20Vision-FF1744?style=for-the-badge">
</p>

<p align="center">
  <strong>Glox Industries</strong>
  <br>
  Building Softwares With a New Vision.
</p>
