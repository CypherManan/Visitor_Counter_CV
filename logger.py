import csv
import os
import time
import config


class CountLogger:
    """
    Writes occupancy snapshots to a CSV file at a fixed interval.
    Creates the output directory and file (with header) if they don't exist.
    """

    def __init__(self):
        self.enabled       = config.LOG_ENABLED
        self.log_path      = config.LOG_PATH
        self.interval      = config.LOG_INTERVAL
        self._last_log_time = time.time()

        if self.enabled:
            os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
            write_header = not os.path.exists(self.log_path)
            self._file = open(self.log_path, "a", newline="")
            self._writer = csv.writer(self._file)
            if write_header:
                self._writer.writerow(["timestamp", "count_in", "count_out", "occupancy"])
                self._file.flush()

    def tick(self, count_in: int, count_out: int, occupancy: int):
        """Call every frame. Logs a row only when the interval has elapsed."""
        if not self.enabled:
            return
        now = time.time()
        if now - self._last_log_time >= self.interval:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
            self._writer.writerow([timestamp, count_in, count_out, occupancy])
            self._file.flush()
            self._last_log_time = now

    def close(self):
        if self.enabled:
            self._file.close()
