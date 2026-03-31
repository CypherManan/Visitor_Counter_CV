# ─── Camera / video source ────────────────────────────────────────────────────
# Set to 0 for webcam, or a file path like "demo_video.mp4"
SOURCE = 0

# ─── Counting line ────────────────────────────────────────────────────────────
# The line is drawn horizontally across the frame at this Y-position (pixels).
# Adjust based on your camera angle and doorway position.
# A centroid moving from ABOVE the line to BELOW  → counted as IN
# A centroid moving from BELOW the line to ABOVE  → counted as OUT
LINE_Y = 300

# Tolerance band around the line (pixels). Crossing is registered when a
# centroid moves from one side to the other while within this band.
LINE_TOLERANCE = 6

# ─── Background subtractor ────
BG_HISTORY       = 500    # frames used to build background model
BG_THRESHOLD     = 16     # sensitivity — lower = more sensitive
DETECT_SHADOWS   = True   # mark shadows gray instead of white (reduces false hits)

# ─── Contour / blob filtering ────
MIN_CONTOUR_AREA = 1500   # ignore blobs smaller than this (noise, small animals)
MAX_CONTOUR_AREA = 80000  # ignore blobs larger than this (merged crowd)

# ─── Tracker ───
MAX_DISAPPEARED = 40   # frames before a lost track is dropped

# ─── Display ───
SHOW_BOUNDING_BOXES = True
SHOW_CENTROIDS      = True
SHOW_IDS            = True
FRAME_WIDTH         = 640
FRAME_HEIGHT        = 480

# ─── Logging ───
LOG_ENABLED  = True
LOG_PATH     = "output/counts_log.csv"
LOG_INTERVAL = 10   # log a row every N seconds
