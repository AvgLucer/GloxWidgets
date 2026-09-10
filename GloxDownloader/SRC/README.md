

<h1 align="center">GloxDownloader - Source</h1>

<p align="center">
  <b>Lightweight • Customizable • Open Source Media Downloader</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/PySide6-GUI-41CD52?style=for-the-badge&logo=qt&logoColor=white">
  <img src="https://img.shields.io/badge/yt--dlp-Downloader-FF0000?style=for-the-badge">
  <img src="https://img.shields.io/badge/FFmpeg-Optional-007808?style=for-the-badge&logo=ffmpeg&logoColor=white">
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Themes-8-8A2BE2?style=flat-square">
  <img src="https://img.shields.io/badge/Formats-MP4%20%7C%20MP3-orange?style=flat-square">
  <img src="https://img.shields.io/badge/Quality-Up%20to%204K-blue?style=flat-square">
  <img src="https://img.shields.io/badge/Ads-None-success?style=flat-square">
</p>

---

## 📌 About

**GloxDownloader** is a lightweight desktop media downloader built with **Python, PySide6, and yt-dlp**.

It provides a simple frameless interface for downloading publicly accessible media from supported platforms while giving the user control over:

* Video quality
* Output format
* Application theme
* Window opacity
* Download location

The application is designed to stay compact, customizable, and free from unnecessary interface elements.

> **Glox Industries — Building Softwares With a New Vision.**

---

## ✨ Features

| Feature                          | Details                                                                                     |
| -------------------------------- | ------------------------------------------------------------------------------------------- |
| 📥 **Media Downloads**           | Download publicly accessible media through yt-dlp.                                          |
| 🌐 **Multi-Platform Support**    | Supports YouTube, YouTube Shorts, Instagram, Facebook, and other sites supported by yt-dlp. |
| 🎬 **MP4 Downloads**             | Download video in MP4 when available.                                                       |
| 🎵 **MP3 Downloads**             | Extract audio and save it as MP3.                                                           |
| 💎 **4K Support**                | Supports video quality up to 2160p when the source provides it.                             |
| 🖥️ **2K Support**               | Supports up to 1440p.                                                                       |
| 📺 **1080p Support**             | Full HD video downloads.                                                                    |
| 📱 **720p Support**              | HD video downloads.                                                                         |
| 📼 **360p Support**              | Lower-resolution downloads for smaller files.                                               |
| ⚡ **Live Progress**              | Displays download progress and download speed.                                              |
| 🔄 **Processing Status**         | Shows when yt-dlp/FFmpeg is processing the downloaded media.                                |
| 🎨 **8 Themes**                  | Includes eight built-in background themes.                                                  |
| 🔳 **Opacity Control**           | Change application opacity from 70% to 100%.                                                |
| 💾 **Saved Preferences**         | Selected theme and opacity are saved between sessions.                                      |
| 📂 **Dedicated Download Folder** | Downloads are automatically stored inside `GDownloads`.                                     |
| 📁 **Open Download Folder**      | Quickly open `GDownloads` from the right-click menu.                                        |
| 🖱️ **Draggable Window**         | Move the frameless application freely around the desktop.                                   |
| 📌 **Always on Top**             | Keeps the downloader above other windows.                                                   |
| 🪟 **Frameless UI**              | Custom rounded desktop interface without the standard Windows title bar.                    |
| 🧵 **Background Downloads**      | Downloading runs through a worker thread so the UI remains responsive.                      |
| 🛡️ **Windows Filenames**        | Uses yt-dlp's Windows filename handling for downloaded files.                               |
| ⚙️ **FFmpeg Detection**          | Automatically searches for local or system FFmpeg installations.                            |
| 🔧 **FFprobe Detection**         | Detects FFprobe when available.                                                             |

---

## 🌐 Supported Platforms

GloxDownloader uses **yt-dlp**, meaning platform support depends on the sites supported by the installed yt-dlp version.

Built-in intended support includes:

| Platform                               | Support |
| -------------------------------------- | ------- |
| ▶️ **YouTube**                         | ✅       |
| ▶️ **YouTube Shorts**                  | ✅       |
| 📸 **Instagram**                       | ✅       |
| 📘 **Facebook**                        | ✅       |
| 🌐 **Other yt-dlp supported websites** | ✅*      |

* Support depends on whether the website and media are publicly accessible and supported by the installed yt-dlp version.

---

## 🎬 Video Qualities

For MP4 downloads, GloxDownloader provides the following quality selections:

| Selection | Maximum Video Height |
| --------- | -------------------: |
| **4K**    |                2160p |
| **2K**    |                1440p |
| **1080p** |                1080p |
| **720p**  |                 720p |
| **360p**  |                 360p |

When FFmpeg is available, GloxDownloader can combine separate video and audio streams when necessary.

Without FFmpeg, it falls back to formats that are already available as compatible MP4 video.

---

## 🎵 Audio / MP3

Selecting **MP3** uses yt-dlp's best available audio stream and FFmpeg's audio extraction functionality.

The resulting audio is configured for:

**MP3 — 192 kbps**

> **FFmpeg is required for MP3 conversion.**

If FFmpeg cannot be detected, GloxDownloader displays an error explaining that `ffmpeg.exe` is required.

---

## 🎨 Themes

GloxDownloader currently contains **8 built-in themes**.

| Theme                | Style          | Background |
| -------------------- | -------------- | ---------- |
| 🤍 **Crystal Cream** | Warm / Premium | `#E9E0D4`  |
| 🌑 **Midnight**      | Deep Dark      | `#111217`  |
| 🌊 **Ocean**         | Cool / Soft    | `#D5E4E7`  |
| 💜 **Lavender**      | Soft Purple    | `#DCD4E9`  |
| ⚫ **Graphite**       | Neutral Dark   | `#18191B`  |
| 🌿 **Sage**          | Natural Green  | `#DCE4D9`  |
| 🌹 **Rose**          | Warm Pink      | `#E9D9DC`  |
| 🩸 **Blood Red**     | Dark Red       | `#211416`  |

Themes modify the application's:

* Background
* Panels
* Cards
* Text
* Muted text
* Accent colors
* Secondary accent
* Borders
* Buttons
* Progress bar
* Input fields
* Dropdown menus

---

## 🔳 Opacity

The application supports seven opacity levels.

|  Setting |       Window Opacity |
| -------: | -------------------: |
|  **70%** |   Highly transparent |
|  **75%** |          Transparent |
|  **80%** | Slightly transparent |
|  **85%** |    Mild transparency |
|  **90%** |          Near opaque |
|  **95%** |  Almost fully opaque |
| **100%** |         Fully opaque |

Opacity can be changed through the application's **right-click context menu**.

---

## 🖱️ Right-Click Menu

Right-clicking the application opens the customization menu.

```text
Background / Theme
├── Crystal Cream
├── Midnight
├── Ocean
├── Lavender
├── Graphite
├── Sage
├── Rose
└── Blood Red

Opacity
├── 70%
├── 75%
├── 80%
├── 85%
├── 90%
├── 95%
└── 100%

Open GDownloads

Quit GloxDownloader
```

This provides quick access to appearance customization without adding extra controls to the main interface.

---

## 💾 Configuration

GloxDownloader automatically stores the selected:

* Theme
* Window opacity

inside:

```text
~/.gloxdownloader/config.json
```

Example configuration:

```json
{
    "theme": "Crystal Cream",
    "opacity": 94
}
```

The application loads these preferences when it starts.

---

## 📂 Download Location

Downloaded files are stored inside:

```text
GDownloads/
```

The folder is automatically created beside the Python source file if it does not already exist.

Expected structure:

```text
GloxDownloader/
│
├── gloxdownloader.py
├── ffmpeg.exe
├── ffprobe.exe
└── GDownloads/
```

The application also provides an **Open GDownloads** option through the right-click menu.

---

## ⚙️ FFmpeg

FFmpeg is **optional for basic compatible downloads**, but it is important for features such as:

* MP3 extraction
* Merging separate video and audio streams
* Higher-quality downloads where video/audio are provided separately

GloxDownloader searches for FFmpeg in:

```text
GloxDownloader/
    ffmpeg.exe
```

```text
GloxDownloader/
    bin/
        ffmpeg.exe
```

It also checks the current working directory and the system `PATH`.

FFprobe is similarly detected from local locations or the system `PATH`.

---

## 🛠️ Requirements

### Python Packages

Install the required packages with:

```bash
pip install PySide6 yt-dlp
```

### Required

* Python 3.x
* PySide6
* yt-dlp

### Optional

* `ffmpeg.exe`
* `ffprobe.exe`

---

## ▶️ Running From Source

Clone/download the repository and place the source inside your project folder.

Install dependencies:

```bash
pip install PySide6 yt-dlp
```

Then run:

```bash
python gloxdownloader.py
```

---

## 🧵 Background Download Architecture

Downloads are handled using a dedicated worker:

```text
GloxDownloader
      │
      ▼
   QThread
      │
      ▼
DownloadWorker
      │
      ▼
    yt-dlp
      │
      ▼
   FFmpeg
```

The worker communicates with the interface through Qt signals:

| Signal     | Purpose                              |
| ---------- | ------------------------------------ |
| `progress` | Updates the progress bar.            |
| `status`   | Updates the current download status. |
| `finished` | Reports success or failure.          |

This prevents the downloader operation from blocking the main GUI thread.

---

## 📊 Download Status

During a download, the application can display:

```text
Preparing download...
```

```text
Downloading • 5.2 MB/s
```

```text
Processing...
```

and finally:

```text
✓ Download complete
```

If something goes wrong, the interface reports:

```text
Download failed
```

while retaining the detailed error message in the status tooltip and console.

---

## 🪟 Interface

GloxDownloader uses a custom **470 × 575 px** frameless widget.

The interface includes:

* Glox `G` logo
* Application title
* URL input
* Quality selector
* Format selector
* Download button
* Progress bar
* Status indicator
* Download-folder information
* Glox Industries footer
* Custom close button

The window can be freely dragged around the desktop and remains on top of other windows.

---

## 🧩 Technology Stack

| Technology               | Purpose                                      |
| ------------------------ | -------------------------------------------- |
| **Python**               | Core application language                    |
| **PySide6**              | Desktop GUI framework                        |
| **yt-dlp**               | Media extraction and downloading             |
| **FFmpeg**               | Media processing, merging and MP3 extraction |
| **Qt Signals / QThread** | Background download processing               |
| **JSON**                 | Persistent application configuration         |

---

## 📁 Source Structure

```text
GloxDownloader/
│
├── gloxdownloader.py
│
├── ffmpeg.exe          # Optional
├── ffprobe.exe         # Optional
│
└── GDownloads/         # Download destination
```

Application configuration is stored separately in:

```text
~/.gloxdownloader/
└── config.json
```

---

## 📥 Download

Looking for the ready-to-use version instead of the source code?

Check:

**[DOWNLOAD.md](DOWNLOAD.md)**

---

## ⚠️ Usage Notice

GloxDownloader is provided for **educational, teaching, learning, development, and user purposes only**.

Only download content that you have permission to download and use the software in accordance with the terms and policies of the platforms you access.

GloxDownloader does not bypass private content restrictions or authentication requirements.

---

## 🤝 Contributing

Contributions and improvements are welcome.

You can:

* Improve the interface
* Add new themes
* Improve error handling
* Improve download handling
* Optimize the source
* Fix bugs
* Add supported functionality
* Submit pull requests

---

## 👨‍💻 Credits

**GloxDownloader** is developed under **Glox Industries**.

**Founder & CEO:** AvgLucer | Gaurav W

> **Glox Industries**
> *Building Softwares With a New Vision.*

---

<p align="center">
  <b>Glox Industries</b>
  <br>
  Building Softwares With a New Vision.
</p>

<p align="center">
  Open Source • Zero Ads • No Unnecessary Bloat
</p>
