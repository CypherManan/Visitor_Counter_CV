import config


class LineCounter:
    """
    Tracks each person's centroid across frames and detects when they
    cross the horizontal counting line defined in config.LINE_Y.

    Direction logic:
        Previous centroid ABOVE line (cy < LINE_Y) and
        current centroid BELOW line  (cy > LINE_Y)  → IN

        Previous centroid BELOW line (cy > LINE_Y) and
        current centroid ABOVE line  (cy < LINE_Y)  → OUT
    """

    def __init__(self):
        self.count_in  = 0
        self.count_out = 0
        self._previous = {}   # object_id -> last known cy

    @property
    def occupancy(self):
        return max(0, self.count_in - self.count_out)

    def update(self, objects: dict):
        """
        objects: OrderedDict from CentroidTracker  {id: (cx, cy)}
        Call this every frame after the tracker update.
        """
        line_y = config.LINE_Y
        tol    = config.LINE_TOLERANCE

        for object_id, (cx, cy) in objects.items():
            if object_id not in self._previous:
                self._previous[object_id] = cy
                continue

            prev_cy = self._previous[object_id]

            # Only register a crossing when the centroid is near the line
            if abs(cy - line_y) <= tol:
                if prev_cy < line_y and cy >= line_y:
                    self.count_in += 1
                elif prev_cy > line_y and cy <= line_y:
                    self.count_out += 1

            self._previous[object_id] = cy

        # Clean up IDs that the tracker has dropped
        active_ids = set(objects.keys())
        stale_ids  = set(self._previous.keys()) - active_ids
        for sid in stale_ids:
            del self._previous[sid]

    def reset(self):
        self.count_in  = 0
        self.count_out = 0
        self._previous.clear()
