import csv
import os
from datetime import datetime
import config as cfg

analytics_folder = cfg.analytics_folder_name
os.makedirs(analytics_folder, exist_ok=True)


# ============================================================
# FILE PATHS
# ============================================================

def get_attendance_file():
    return os.path.join(analytics_folder, "attendance.csv")


def get_keystroke_file():
    return os.path.join(analytics_folder, "keystroke.csv")


def get_break_file():
    return os.path.join(analytics_folder, "break.csv")


# ============================================================
# CREATE CSV FILES
# ============================================================

def ensure_csv_files():
    """Create all CSV files with their headers if they don't exist."""

    # ---------------- ATTENDANCE ----------------
    attendance_file = get_attendance_file()

    if not os.path.exists(attendance_file):
        with open(attendance_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Date',
                'Start_Time',
                'End_Time',
                'Total_Time_Minutes',
                'Total_Time_Formatted'
            ])

    # ---------------- KEYSTROKE ----------------
    keystroke_file = get_keystroke_file()

    if not os.path.exists(keystroke_file):
        with open(keystroke_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Date',
                'Time_Start',
                'Number_of_Keystrokes'
            ])

    # ---------------- BREAK ----------------
    break_file = get_break_file()

    if not os.path.exists(break_file):
        with open(break_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Date',
                'Time_Start',
                'Time_End',
                'Total_Break_Time_Minutes'
            ])


# ============================================================
# ATTENDANCE
# ============================================================

def save_attendance(start_time, end_time=None, elapsed_seconds=None):
    """
    Create or update the current attendance session.

    Time-In:
        save_attendance(start_time)

    While working / Time-Out:
        save_attendance(start_time, end_time, elapsed_seconds)
    """

    ensure_csv_files()

    attendance_file = get_attendance_file()

    # --------------------------------------------------------
    # TIME-IN
    # --------------------------------------------------------

    if end_time is None:
        with open(attendance_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            writer.writerow([
                start_time.strftime("%Y-%m-%d"),
                start_time.strftime("%H:%M:%S"),
                "",
                "",
                ""
            ])

        return

    # --------------------------------------------------------
    # UPDATE CURRENT ATTENDANCE
    # --------------------------------------------------------

    total_minutes = elapsed_seconds / 60.0

    hours = int(elapsed_seconds // 3600)
    minutes = int((elapsed_seconds % 3600) // 60)
    seconds = int(elapsed_seconds % 60)

    total_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    # Read existing CSV
    with open(attendance_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    target_date = start_time.strftime("%Y-%m-%d")
    target_start = start_time.strftime("%H:%M:%S")

    # Find the current unfinished session
    found = False

    for i in range(1, len(rows)):

        if (
            rows[i][0] == target_date
            and rows[i][1] == target_start
            and rows[i][2] == ""
        ):
            rows[i][2] = end_time.strftime("%H:%M:%S")
            rows[i][3] = round(total_minutes, 2)
            rows[i][4] = total_formatted

            found = True
            break

    # Write updated CSV
    if found:
        with open(attendance_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

# ============================================================
# KEYSTROKE
# ============================================================

def save_keystroke_log(time_start, keystroke_count):
    """
    Save keystroke count for a 1-minute interval.

    Args:
        time_start: datetime representing the beginning of the interval
        keystroke_count: number of keystrokes detected
    """

    ensure_csv_files()

    keystroke_file = get_keystroke_file()

    with open(keystroke_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        writer.writerow([
            time_start.strftime("%Y-%m-%d"),
            time_start.strftime("%H:%M:%S"),
            keystroke_count
        ])


# ============================================================
# BREAK
# ============================================================

def save_break(time_start, time_end):
    """
    Save one completed break.

    Args:
        time_start: datetime when break started
        time_end: datetime when break ended
    """

    ensure_csv_files()

    break_file = get_break_file()

    break_seconds = (time_end - time_start).total_seconds()
    break_minutes = break_seconds / 60.0

    with open(break_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        writer.writerow([
            time_start.strftime("%Y-%m-%d"),
            time_start.strftime("%H:%M:%S"),
            time_end.strftime("%H:%M:%S"),
            round(break_minutes, 2)
        ])