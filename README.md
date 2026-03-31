# Contactless Visitor Counter

A real-time people counting system using OpenCV that tracks how many people
enter and exit a space through a camera feed. Designed for temples, shops, and
public venues where occupancy monitoring matters — no internet, no face
recognition, no GPU required.

---

## Problem

During festivals and peak hours, temples and shops in India have no reliable
way to know how many people are inside. Manual counting is error-prone and
adds labour cost. This system uses a standard webcam to count people crossing
a virtual line and displays live occupancy — fully offline and privacy-safe.

---

## How it works

1. A background subtractor (MOG2) separates moving people from the static background.
2. Contours (blobs) are detected and filtered by size to identify people.
3. A centroid tracker assigns a persistent ID to each person across frames.
4. When a centroid crosses the virtual counting line, the direction (IN or OUT) is recorded.
5. Occupancy = IN count − OUT count, displayed live on screen.
6. Counts are logged to a CSV file at a configurable interval.

---

## Setup

```bash
# 1. Clone the repository
git clone https://github.com/your-username/visitor-counter.git
cd visitor-counter

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create the output folder
mkdir output
```

---

## Usage

### With a webcam
```bash
python main.py
```
Make sure `SOURCE = 0` in `config.py`.

### With a video file
Set `SOURCE = "demo_video.mp4"` in `config.py`, then:
```bash
python main.py
```

### Controls
| Key | Action |
|-----|--------|
| `q` | Quit |
| `r` | Reset counts |

---

## Configuration (`config.py`)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `SOURCE` | `0` | Webcam index or video file path |
| `LINE_Y` | `300` | Y-position of the counting line in pixels |
| `LINE_TOLERANCE` | `6` | Pixel band around the line for crossing detection |
| `MIN_CONTOUR_AREA` | `1500` | Minimum blob size (filters out noise) |
| `MAX_CONTOUR_AREA` | `80000` | Maximum blob size (filters merged crowds) |
| `MAX_DISAPPEARED` | `40` | Frames before a lost track is dropped |
| `LOG_INTERVAL` | `10` | Seconds between CSV log entries |

**Tip:** If your camera is mounted high (bird's-eye view), lower `LINE_Y`.
If people are being missed, reduce `MIN_CONTOUR_AREA`.

---

## Output

- Live video window with counting line, bounding boxes, centroid IDs, and the stats panel
- `output/counts_log.csv` — timestamped rows of IN, OUT, and occupancy

---

## Project structure

```
visitor-counter/
├── main.py          ← entry point
├── tracker.py       ← centroid tracker
├── counter.py       ← line crossing logic
├── logger.py        ← CSV logging
├── config.py        ← all tunable parameters
├── requirements.txt
├── output/
│   └── counts_log.csv
└── README.md
```

---

## Limitations

- Works best when people cross the line one at a time
- Merging shadows or very dark environments reduce accuracy
- Accuracy depends on camera angle — overhead or slight angle works best
- Not suitable for dense crowds where blobs merge into each other

---

## Dependencies

- [OpenCV](https://opencv.org/) — video capture, background subtraction, display
- [SciPy](https://scipy.org/) — centroid distance calculation for tracking
- [NumPy](https://numpy.org/) — array operations
