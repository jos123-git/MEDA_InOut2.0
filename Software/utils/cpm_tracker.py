from datetime import datetime
from utils import analytics


class CPMTracker:
    def __init__(self):
        # Total session data
        self.keystroke_count = 0
        self.start_time = None
        self.end_time = None
        self.is_tracking = False

        # Time tracking
        self.total_time_seconds = 0
        self.paused_time = 0
        self.pause_start = None

        # 1-minute keystroke tracking
        self.minute_keystrokes = 0
        self.minute_start_time = None

    # ============================================================
    # START
    # ============================================================

    def start(self):
        """Start tracking CPM"""

        self.keystroke_count = 0
        self.start_time = datetime.now()
        self.end_time = None

        self.is_tracking = True

        self.total_time_seconds = 0
        self.paused_time = 0
        self.pause_start = None

        # Start 1-minute interval
        self.minute_keystrokes = 0
        self.minute_start_time = datetime.now()

    # ============================================================
    # STOP
    # ============================================================

    def stop(self):
        """Stop tracking CPM and save remaining keystrokes"""

        if not self.is_tracking:
            return self.get_stats()

        # Save any remaining keystrokes from the current minute
        self._save_minute_log()

        self._calculate_elapsed_time()

        self.end_time = datetime.now()
        self.is_tracking = False

        return self.get_stats()

    # ============================================================
    # PAUSE
    # ============================================================

    def pause(self):
        """Pause CPM tracking"""

        if self.is_tracking and self.pause_start is None:
            self.pause_start = datetime.now()

    # ============================================================
    # RESUME
    # ============================================================

    def resume(self):
        """Resume CPM tracking"""

        if self.is_tracking and self.pause_start:

            pause_duration = (
                datetime.now() - self.pause_start
            ).total_seconds()

            self.paused_time += pause_duration

            self.pause_start = None

            # Start a new 1-minute interval after break
            self.minute_start_time = datetime.now()
            self.minute_keystrokes = 0

    # ============================================================
    # KEYSTROKE
    # ============================================================

    def add_keystroke(self):
        """Record a keystroke"""

        if self.is_tracking and self.pause_start is None:

            # Total session keystrokes
            self.keystroke_count += 1

            # Current 1-minute keystrokes
            self.minute_keystrokes += 1

    # ============================================================
    # 1-MINUTE LOGGING
    # ============================================================

    def check_minute_log(self):
        """
        Check whether 1 minute has passed.

        This method should be called periodically by Tkinter.
        """

        if not self.is_tracking:
            return

        # Don't log while paused
        if self.pause_start is not None:
            return

        if self.minute_start_time is None:
            self.minute_start_time = datetime.now()
            return

        elapsed = (
            datetime.now() - self.minute_start_time
        ).total_seconds()

        if elapsed >= 60:

            self._save_minute_log()

            # Start next minute
            self.minute_start_time = datetime.now()
            self.minute_keystrokes = 0

    # ============================================================
    # SAVE 1-MINUTE KEYSTROKE LOG
    # ============================================================

    def _save_minute_log(self):
        """Save current 1-minute keystroke count to CSV"""

        if self.minute_start_time is None:
            return

        analytics.save_keystroke_log(
            self.minute_start_time,
            self.minute_keystrokes
        )

    # ============================================================
    # ELAPSED TIME
    # ============================================================

    def _calculate_elapsed_time(self):
        """Calculate elapsed time excluding breaks"""

        if self.start_time is None:
            self.total_time_seconds = 0
            return

        end_time = self.end_time or datetime.now()

        elapsed = (
            end_time - self.start_time
        ).total_seconds()

        # If currently paused, include current pause
        # when calculating the amount to exclude.
        current_paused = self.paused_time

        if self.pause_start is not None:
            current_paused += (
                datetime.now() - self.pause_start
            ).total_seconds()

        self.total_time_seconds = elapsed - current_paused

    # ============================================================
    # GET ELAPSED TIME
    # ============================================================

    def get_elapsed_time(self):
        """Get elapsed working time in seconds"""

        self._calculate_elapsed_time()

        return max(0, self.total_time_seconds)

    # ============================================================
    # GET CPM
    # ============================================================

    def get_cpm(self):
        """
        Calculate CPM for the entire session.

        CPM = total keystrokes / total working minutes
        """

        elapsed_minutes = self.get_elapsed_time() / 60.0

        if elapsed_minutes <= 0:
            return 0

        cpm = self.keystroke_count / elapsed_minutes

        return round(cpm, 2)

    # ============================================================
    # GET CURRENT MINUTE CPM
    # ============================================================

    def get_current_minute_cpm(self):
        """
        Return CPM for the current 1-minute interval.
        """

        if not self.is_tracking:
            return 0

        return self.minute_keystrokes

    # ============================================================
    # GET STATS
    # ============================================================

    def get_stats(self):
        """Get comprehensive CPM statistics"""

        self._calculate_elapsed_time()

        elapsed_minutes = self.get_elapsed_time() / 60.0

        cpm = 0

        if elapsed_minutes > 0:
            cpm = self.keystroke_count / elapsed_minutes

        return {
            'keystroke_count': self.keystroke_count,
            'cpm': round(cpm, 2),
            'current_minute_keystrokes': self.minute_keystrokes,
            'elapsed_time': round(self.get_elapsed_time(), 2),
            'elapsed_time_formatted': self._format_time(
                self.total_time_seconds
            ),
            'is_tracking': self.is_tracking
        }

    # ============================================================
    # FORMAT TIME
    # ============================================================

    def _format_time(self, seconds):
        """Format seconds to HH:MM:SS"""

        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    # ============================================================
    # RESET
    # ============================================================

    def reset(self):
        """Reset all tracking data"""

        self.keystroke_count = 0
        self.start_time = None
        self.end_time = None
        self.is_tracking = False

        self.total_time_seconds = 0
        self.paused_time = 0
        self.pause_start = None

        self.minute_keystrokes = 0
        self.minute_start_time = None