import cv2
import numpy as np
import config
from tracker import CentroidTracker
from counter import LineCounter
from logger  import CountLogger


def get_contour_rects(fg_mask):
    """
    Find contours in the foreground mask and return bounding boxes
    for blobs that fall within the configured area range.
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    cleaned = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN,  kernel, iterations=2)
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    rects = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if config.MIN_CONTOUR_AREA <= area <= config.MAX_CONTOUR_AREA:
            x, y, w, h = cv2.boundingRect(cnt)
            rects.append((x, y, x + w, y + h))
    return rects


def draw_overlay(frame, counter, objects):
    h, w = frame.shape[:2]
    line_y = config.LINE_Y

    # Counting line
    cv2.line(frame, (0, line_y), (w, line_y), (0, 255, 255), 2)
    cv2.putText(frame, "COUNT LINE", (10, line_y - 8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)

    # Bounding boxes and IDs
    if config.SHOW_BOUNDING_BOXES or config.SHOW_CENTROIDS or config.SHOW_IDS:
        for object_id, (cx, cy) in objects.items():
            if config.SHOW_CENTROIDS:
                cv2.circle(frame, (cx, cy), 5, (0, 200, 255), -1)
            if config.SHOW_IDS:
                cv2.putText(frame, f"ID {object_id}", (cx - 20, cy - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 200, 255), 1)

    # Stats panel (top-left)
    panel_lines = [
        (f"IN       : {counter.count_in}",  (50, 200, 50)),
        (f"OUT      : {counter.count_out}", (50, 50, 220)),
        (f"OCCUPANCY: {counter.occupancy}", (255, 255, 255)),
    ]
    pad, line_h = 12, 28
    panel_h = pad * 2 + line_h * len(panel_lines)
    panel_w = 240
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (10 + panel_w, 10 + panel_h), (30, 30, 30), -1)
    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)

    for i, (text, color) in enumerate(panel_lines):
        y = 10 + pad + line_h * i + 16
        cv2.putText(frame, text, (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Occupancy alert
    if counter.occupancy > 50:
        cv2.putText(frame, "! HIGH OCCUPANCY", (w // 2 - 130, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    return frame


def main():
    cap = cv2.VideoCapture(config.SOURCE)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  config.FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)

    if not cap.isOpened():
        print(f"[ERROR] Cannot open source: {config.SOURCE}")
        return

    bg_subtractor = cv2.createBackgroundSubtractorMOG2(
        history=config.BG_HISTORY,
        varThreshold=config.BG_THRESHOLD,
        detectShadows=config.DETECT_SHADOWS,
    )

    tracker = CentroidTracker(max_disappeared=config.MAX_DISAPPEARED)
    counter = LineCounter()
    logger  = CountLogger()

    print("[INFO] Press 'q' to quit, 'r' to reset counts.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[INFO] End of stream.")
            break

        frame = cv2.resize(frame, (config.FRAME_WIDTH, config.FRAME_HEIGHT))

        # Foreground mask
        fg_mask = bg_subtractor.apply(frame)

        # Shadow pixels (127) → set to 0 so they don't count as foreground
        if config.DETECT_SHADOWS:
            fg_mask[fg_mask == 127] = 0

        rects   = get_contour_rects(fg_mask)
        objects = tracker.update(rects)
        counter.update(objects)
        logger.tick(counter.count_in, counter.count_out, counter.occupancy)

        frame = draw_overlay(frame, counter, objects)

        cv2.imshow("Visitor Counter", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("r"):
            counter.reset()
            print("[INFO] Counts reset.")

    cap.release()
    logger.close()
    cv2.destroyAllWindows()
    print(f"[INFO] Session ended. IN={counter.count_in}  OUT={counter.count_out}  "
          f"Final occupancy={counter.occupancy}")


if __name__ == "__main__":
    main()
