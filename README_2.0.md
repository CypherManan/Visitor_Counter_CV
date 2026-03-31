# 🏛️ Contactless Visitor Counter

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Real-time people counting using a webcam — no GPU, no internet, no face recognition.**

*Built for temples, shops, and public venues where occupancy monitoring matters.*

</div>

---

## 📌 The Problem

During festivals like Navratri and Diwali, temples and shops across India face dangerous overcrowding — with no easy way to know how many people are inside at any given moment. Manual counting is unreliable and labour-intensive.

This project solves that with a simple webcam-based system that:
- Counts people **entering** and **exiting** through any doorway
- Shows **live occupancy** (IN − OUT) directly on screen
- Logs data to a **CSV file** for reporting
- Runs entirely **offline** on a basic laptop

---

## 🎥 How It Works

```
Webcam Frame
     │
     ▼
┌─────────────────────┐
│  Background         │  MOG2 separates moving people
│  Subtraction (MOG2) │  from the static background
└─────────────────────┘
     │
     ▼
┌─────────────────────┐
│  Morphological      │  Cleans noise, fills gaps
│  Cleaning           │  in the foreground mask
└─────────────────────┘
     │
     ▼
┌─────────────────────┐
│  Contour Detection  │  Finds person-sized blobs
│  (findContours)     │  and extracts bounding boxes
└─────────────────────┘
     │
     ▼
┌─────────────────────┐
│  Centroid Tracker   │  Assigns persistent IDs
│                     │  to each person across frames
└─────────────────────┘
     │
     ▼
┌─────────────────────┐
│  Line Crossing      │  Detects direction (IN / OUT)
│  Detection          │  when centroid crosses the line
└─────────────────────┘
     │
     ▼
  Dashboard + CSV Log
```

---

## 🗂️ Project Structure

```
visitor-counter/
│
├── main.py          ← Entry point — runs the full pipeline
├── tracker.py       ← Centroid tracker (ID assignment & persistence)
├── counter.py       ← Line crossing logic (IN / OUT detection)
├── logger.py        ← CSV file logging
├── config.py        ← All settings in one place
├── requirements.txt ← Python dependencies
│
└── output/
    └── counts_log.csv   ← Auto-generated session log
```

---

## ⚙️ Setup

### Prerequisites

- Python 3.10 or higher
- A webcam (or a `.mp4` video file for testing)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/visitor-counter.git
cd visitor-counter

# 2. (Recommended) Create a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create the output folder
mkdir output
```

---

## ▶️ Running the Project

### With your webcam (default)

Make sure `SOURCE = 0` in `config.py`, then:

```bash
python main.py
```

### With a video file (for testing)

Set `SOURCE = "demo_video.mp4"` in `config.py`, then:

```bash
python main.py
```

### Keyboard controls

| Key | Action |
|-----|--------|
| `q` | Quit the application |
| `r` | Reset all counts to zero |

---

## 🖥️ What You'll See

Once running, a window opens showing your camera feed with:

- 🟡 **Yellow line** — the virtual counting boundary
- 🟠 **Bounding boxes** — around each detected person
- 🔵 **Centroid dots** — the tracked centre point of each person
- 📊 **Stats panel** (top-left corner):

```
IN       : 14
OUT      : 9
OCCUPANCY: 5
```

A `! HIGH OCCUPANCY` alert appears on screen if count exceeds 50.

---

## 🛠️ Configuration

All settings live in `config.py` — no need to touch any other file.

| Parameter | Default | What it controls |
|-----------|---------|-----------------|
| `SOURCE` | `0` | Webcam index (`0`, `1`) or video file path |
| `LINE_Y` | `300` | Y-pixel position of the counting line |
| `LINE_TOLERANCE` | `6` | Pixel band to prevent double-counting |
| `MIN_CONTOUR_AREA` | `1500` | Minimum blob size — filters out noise |
| `MAX_CONTOUR_AREA` | `80000` | Maximum blob size — filters merged crowds |
| `BG_HISTORY` | `500` | Frames used to build the background model |
| `BG_THRESHOLD` | `16` | Sensitivity — lower = more sensitive |
| `MAX_DISAPPEARED` | `40` | Frames before a lost track is dropped |
| `LOG_INTERVAL` | `10` | Seconds between CSV log entries |

### Tuning tips

> **Camera mounted high (bird's-eye)?** → Lower `LINE_Y`

> **People being missed?** → Reduce `MIN_CONTOUR_AREA` to `800`

> **Too many false detections?** → Increase `BG_THRESHOLD` to `25`

> **Webcam not found?** → Try `SOURCE = 1` instead of `0`

---

## 📄 Output Log

Every session writes to `output/counts_log.csv`:

```
timestamp,count_in,count_out,occupancy
2026-03-31 10:00:00,3,1,2
2026-03-31 10:00:10,5,2,3
2026-03-31 10:00:20,8,4,4
```

You can open this in Excel or plot it with matplotlib for a full occupancy report.

---

## ⚠️ Known Limitations

| Situation | Impact |
|-----------|--------|
| Two people walking very close together | May be counted as one (undercount) |
| Very dark or rapidly changing lighting | Reduces detection accuracy |
| Camera not stable (handheld) | Background model breaks down |
| Dense crowds | Blobs merge; not suitable for 10+ people at once |

This system is designed for **single-file or low-density** entry points. For high-density crowd scenarios, a YOLO-based detector is more appropriate.

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `opencv-python` | ≥ 4.8 | Frame capture, background subtraction, display |
| `scipy` | ≥ 1.11 | Centroid distance matrix for tracking |
| `numpy` | ≥ 1.24 | Array operations |

Install all at once:
```bash
pip install -r requirements.txt
```

---

## 🚀 Future Improvements

- [ ] YOLO-based person detector for better accuracy in crowds
- [ ] Flask/Streamlit web dashboard for remote monitoring
- [ ] SMS/WhatsApp alert when occupancy exceeds a threshold
- [ ] Raspberry Pi deployment for a self-contained door unit
- [ ] Multi-line support for complex venue layouts

---

## 📃 License

This project is open source under the [MIT License](LICENSE).

---

<div align="center">
Made with OpenCV · Built for VITyarthi · No GPU required
</div>
