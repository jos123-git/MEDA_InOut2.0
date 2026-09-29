from tkinter import *
import tkinter.font as tkFont
import config as cfg

from utils.logger import (
    start_logger,
    stop_logger,
    log_event,
    set_keystroke_callback
)

from utils.screenshot import take_screenshot
from utils.cpm_tracker import CPMTracker

from utils.analytics import (
    ensure_csv_files,
    save_attendance,
    save_break
)

from utils.email_sender import send_cpm_report

from datetime import datetime
from tkinter import messagebox


# ============================================================
# STATES
# ============================================================

is_TimeIn = False
is_Break = False
was_logging = False
running = True

cpm_tracker = CPMTracker()

break_count = 0
total_break_time = 0
break_start_time = None

# Used to control attendance.csv updates
last_attendance_update = None


# ============================================================
# OPEN DASHBOARD
# ============================================================

def open_dashboard():

    global is_TimeIn
    global is_Break
    global was_logging
    global cpm_tracker
    global running
    global break_count
    global total_break_time
    global break_start_time
    global last_attendance_update

    # ========================================================
    # RESET STATES WHEN OPENING DASHBOARD
    # ========================================================

    is_TimeIn = False
    is_Break = False
    was_logging = False
    running = True

    break_count = 0
    total_break_time = 0
    break_start_time = None

    last_attendance_update = None

    cpm_tracker = CPMTracker()

    # ========================================================
    # CREATE CSV FILES
    # ========================================================

    ensure_csv_files()

    # ========================================================
    # MAIN WINDOW
    # ========================================================

    app = Tk()
    app.title("MEDA: InOut Dashboard")
    app.geometry("600x700")
    app.configure(bg=cfg.bg_primary)

    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=1)

    # ========================================================
    # FONTS
    # ========================================================

    titleFont = tkFont.Font(
        root=app,
        weight=cfg.weight,
        size=cfg.titleFontSize,
        family=cfg.fontfamily
    )

    statsFont = tkFont.Font(
        root=app,
        family=cfg.fontfamily,
        size=14,
        weight="bold"
    )

    labelFont = tkFont.Font(
        root=app,
        family=cfg.fontfamily,
        size=10
    )

    # ========================================================
    # HELPER FUNCTIONS
    # ========================================================

    def apply_button_style(
        button,
        bg_color=cfg.btn_bg_default,
        fg_color=cfg.btn_fg_default
    ):
        """Apply consistent button styling."""

        button.config(
            bg=bg_color,
            fg=fg_color,
            font=cfg.font_button,
            relief=FLAT,
            padx=10,
            pady=8,
            cursor="hand2"
        )

    def apply_label_style(
        label,
        fg_color=cfg.fg_primary
    ):
        """Apply consistent label styling."""

        label.config(
            bg=cfg.bg_primary,
            fg=fg_color,
            font=labelFont
        )

    # ========================================================
    # LOG DISPLAY
    # ========================================================

    def log_message(message):
        """Display message in the system message list."""

        timestamp = datetime.now().strftime("%H:%M:%S")

        systemMessage.insert(
            0,
            f"{timestamp} | {message}"
        )

    # ========================================================
    # CPM UPDATE + 1-MINUTE KEYSTROKE LOGGING
    # ========================================================

    def update_cpm_display():

        global last_attendance_update

        if not running:
            return

        try:

            if app.winfo_exists():

                # ------------------------------------------------
                # ONLY TRACK WHILE WORKING
                # ------------------------------------------------

                if is_TimeIn and not is_Break:

                    # Check if a 1-minute keystroke interval
                    # has completed.
                    cpm_tracker.check_minute_log()

                    # Get current CPM statistics
                    stats = cpm_tracker.get_stats()

                    # ------------------------------------------------
                    # UPDATE ATTENDANCE EVERY 60 SECONDS
                    # ------------------------------------------------

                    current_time = datetime.now()

                    if (
                        last_attendance_update is None
                        or (
                            current_time - last_attendance_update
                        ).total_seconds() >= 60
                    ):

                        save_attendance(
                            cpm_tracker.start_time,
                            current_time,
                            stats["elapsed_time"]
                        )

                        last_attendance_update = current_time

                        log_message(
                            "Attendance updated"
                        )

                    # ------------------------------------------------
                    # UPDATE CPM DISPLAY
                    # ------------------------------------------------

                    cpm_label.config(
                        text=(
                            f"CPM: {stats['cpm']} | "
                            f"Keystrokes: {stats['keystroke_count']} | "
                            f"Time: {stats['elapsed_time_formatted']}"
                        ),
                        fg=cfg.text_info
                    )

                # ------------------------------------------------
                # RUN AGAIN
                # ------------------------------------------------

                if running:

                    app.after(
                        cfg.cpm_display_interval * 1000,
                        update_cpm_display
                    )

        except Exception:
            pass

    # ========================================================
    # AUTO SCREENSHOT
    # ========================================================

    def auto_screenshot():

        # Screenshot monitoring disabled
        if not cfg.screenshot_enabled:
            return

        # Screenshot only while Time-In and not on break
        if is_TimeIn and not is_Break:

            take_screenshot()

            app.after(
                cfg.screenshot_interval * 1000,
                auto_screenshot
            )

        elif running:

            app.after(
                1000,
                auto_screenshot
            )

    # ========================================================
    # TIME-IN / TIME-OUT
    # ========================================================

    def toggle_time():

        global is_TimeIn
        global is_Break
        global was_logging
        global break_count
        global total_break_time
        global break_start_time
        global last_attendance_update

        # ====================================================
        # TIME-IN
        # ====================================================

        if not is_TimeIn:

            # ------------------------------------------------
            # Update button
            # ------------------------------------------------

            timeBtn.config(
                text="⏹ Time-Out",
                bg=cfg.color_success,
                fg="white"
            )

            log_message("Time-In")
            log_event("Time-In")

            # ------------------------------------------------
            # Start CPM tracking
            # ------------------------------------------------

            cpm_tracker.start()

            # ------------------------------------------------
            # CREATE ATTENDANCE RECORD IMMEDIATELY
            # ------------------------------------------------

            save_attendance(
                cpm_tracker.start_time
            )

            # Reset attendance update timer
            last_attendance_update = datetime.now()

            log_message(
                "Attendance Time-In recorded"
            )

            # ------------------------------------------------
            # Start keyboard activity monitoring
            # ------------------------------------------------

            set_keystroke_callback(
                cpm_tracker.add_keystroke
            )

            # ------------------------------------------------
            # Start general logger
            # ------------------------------------------------

            start_logger()

            # ------------------------------------------------
            # Enable break button
            # ------------------------------------------------

            breakBtn.config(
                state="normal"
            )

            is_TimeIn = True
            is_Break = False

            cpm_label.config(
                fg=cfg.text_success
            )

            log_message(
                "CPM tracking started"
            )

        # ====================================================
        # TIME-OUT
        # ====================================================

        else:

            confirm = messagebox.askyesno(
                "Confirm",
                "Are you sure you want to Time-Out?"
            )

            if not confirm:
                return

            # ------------------------------------------------
            # Record ending time
            # ------------------------------------------------

            end_time = datetime.now()

            # ------------------------------------------------
            # Stop CPM tracker
            #
            # This also saves remaining keystrokes
            # from the current minute.
            # ------------------------------------------------

            stats = cpm_tracker.stop()

            # ------------------------------------------------
            # Get Time-In
            # ------------------------------------------------

            start_time = cpm_tracker.start_time

            # ------------------------------------------------
            # Save FINAL attendance information
            # ------------------------------------------------

            if start_time:

                save_attendance(
                    start_time,
                    end_time,
                    stats["elapsed_time"]
                )

                log_message(
                    "Final attendance saved"
                )

            # ------------------------------------------------
            # Update UI
            # ------------------------------------------------

            timeBtn.config(
                text="▶ Time-In",
                bg=cfg.btn_bg_default,
                fg=cfg.btn_fg_default
            )

            log_message(
                f"Time-Out | Final CPM: {stats['cpm']}"
            )

            log_event("Time-Out")

            # ------------------------------------------------
            # Stop logger
            # ------------------------------------------------

            stop_logger()

            # ------------------------------------------------
            # Disable break button
            # ------------------------------------------------

            breakBtn.config(
                state="disabled"
            )

            # ------------------------------------------------
            # Reset states
            # ------------------------------------------------

            is_TimeIn = False
            is_Break = False
            was_logging = False

            break_count = 0
            total_break_time = 0
            break_start_time = None

            last_attendance_update = None

            # ------------------------------------------------
            # Display final session information
            # ------------------------------------------------

            cpm_label.config(
                text=(
                    f"Session Complete | "
                    f"CPM: {stats['cpm']} | "
                    f"Total Keystrokes: "
                    f"{stats['keystroke_count']}"
                ),
                fg=cfg.text_success
            )

            # ------------------------------------------------
            # Reset tracker for next session
            # ------------------------------------------------

            cpm_tracker.reset()

    # ========================================================
    # BREAK
    # ========================================================

    def toggle_break():

        global is_Break
        global was_logging
        global break_count
        global total_break_time
        global break_start_time

        # ====================================================
        # START BREAK
        # ====================================================

        if not is_Break:

            confirm = messagebox.askyesno(
                "Confirm",
                "Start break?"
            )

            if not confirm:
                return

            # ------------------------------------------------
            # Update button
            # ------------------------------------------------

            breakBtn.config(
                bg=cfg.color_warning,
                fg="white",
                text="⏵ Resume"
            )

            log_message("Break started")
            log_event("Break Start")

            # ------------------------------------------------
            # Remember logging state
            # ------------------------------------------------

            was_logging = is_TimeIn

            # ------------------------------------------------
            # Pause CPM
            # ------------------------------------------------

            cpm_tracker.pause()

            # ------------------------------------------------
            # Stop keyboard/general logging
            # ------------------------------------------------

            stop_logger()

            # ------------------------------------------------
            # Record break start
            # ------------------------------------------------

            break_start_time = datetime.now()

            break_count += 1

            is_Break = True

            cpm_label.config(
                fg=cfg.text_warning
            )

        # ====================================================
        # END BREAK
        # ====================================================

        else:

            confirm = messagebox.askyesno(
                "Confirm",
                "End break?"
            )

            if not confirm:
                return

            # ------------------------------------------------
            # Record break end
            # ------------------------------------------------

            if break_start_time:

                break_end_time = datetime.now()

                break_duration = (
                    break_end_time - break_start_time
                ).total_seconds()

                total_break_time += break_duration

                # --------------------------------------------
                # Save break.csv
                # --------------------------------------------

                save_break(
                    break_start_time,
                    break_end_time
                )

                log_message(
                    "Break saved"
                )

                break_start_time = None

            # ------------------------------------------------
            # Update button
            # ------------------------------------------------

            breakBtn.config(
                bg=cfg.btn_bg_default,
                fg=cfg.btn_fg_default,
                text="☕ Break"
            )

            log_message("Break ended")
            log_event("Break End")

            # ------------------------------------------------
            # Resume tracking
            # ------------------------------------------------

            if was_logging:

                cpm_tracker.resume()

                start_logger()

            is_Break = False

            cpm_label.config(
                fg=cfg.text_info
            )

    # ========================================================
    # INSTRUCTIONS
    # ========================================================

    def instruction():

        screenshot_status = (
            "Enabled"
            if cfg.screenshot_enabled
            else "Disabled"
        )

        text = (
            "⏱ TIME-IN\n"
            "     Starts logging and CPM tracking\n"
            "     Attendance is recorded immediately\n\n"

            "☕ BREAK\n"
            "     Pauses logging & screenshots\n"
            "     and preserves the CPM session\n\n"

            "⏹ TIME-OUT\n"
            "     Stops logging and screenshots\n"
            "     and saves final attendance statistics\n\n"

            "📊 CPM ANALYTICS\n"
            "     Keystrokes are saved every minute\n"
            "     in keystroke.csv\n\n"

            "📋 ATTENDANCE ANALYTICS\n"
            "     Attendance is created at Time-In\n"
            "     and updated every minute\n"
            "     Final values are saved at Time-Out\n\n"

            "☕ BREAK ANALYTICS\n"
            "     Every completed break is saved\n"
            "     in break.csv\n\n"

            f"📸 SCREENSHOT MONITORING\n"
            f"     Status: {screenshot_status}\n\n"

            "🚪 LOGOUT\n"
            "     Exit dashboard and return to login"
        )

        messagebox.showinfo(
            "Instructions",
            text
        )

    # ========================================================
    # SEND REPORT
    # ========================================================

    def send_report():

        success, message = send_cpm_report()

        if success:

            messagebox.showinfo(
                "Success",
                message
            )

            log_message(message)

        else:

            messagebox.showerror(
                "Error",
                message
            )

            log_message(
                f"Report send failed: {message}"
            )

    # ========================================================
    # LOGOUT
    # ========================================================

    def logout():

        global running
        global is_TimeIn
        global is_Break

        confirm = messagebox.askyesno(
            "Confirm",
            "Are you sure you want to logout?"
        )

        if not confirm:
            return

        # ------------------------------------------------
        # Stop background tasks
        # ------------------------------------------------

        running = False

        # ------------------------------------------------
        # Stop general logger
        # ------------------------------------------------

        stop_logger()

        # ------------------------------------------------
        # Stop CPM tracker
        # ------------------------------------------------

        if is_TimeIn:

            cpm_tracker.stop()

        is_TimeIn = False
        is_Break = False

        # ------------------------------------------------
        # Close dashboard
        # ------------------------------------------------

        app.destroy()

    # ========================================================
    # UI LAYOUT
    # ========================================================

    # ========================================================
    # HEADER
    # ========================================================

    header_frame = Frame(
        app,
        bg=cfg.bg_secondary,
        height=80
    )

    header_frame.grid(
        row=0,
        column=0,
        columnspan=2,
        sticky="ew",
        padx=0,
        pady=0
    )

    header_frame.grid_propagate(False)

    title_label = Label(
        header_frame,
        text="MEDA: InOut",
        font=titleFont,
        bg=cfg.bg_secondary,
        fg=cfg.color_info
    )

    title_label.pack(
        pady=cfg.pady
    )

    subtitle_label = Label(
        header_frame,
        text="Time & Activity Tracker with CPM Analytics",
        font=(cfg.fontfamily, 9),
        bg=cfg.bg_secondary,
        fg=cfg.fg_primary
    )

    subtitle_label.pack(
        pady=2
    )

    # ========================================================
    # MAIN CONTROL FRAME
    # ========================================================

    control_frame = Frame(
        app,
        bg=cfg.bg_primary
    )

    control_frame.grid(
        row=1,
        column=0,
        columnspan=2,
        sticky="ew",
        padx=cfg.padx,
        pady=cfg.pady
    )

    # ========================================================
    # TIME BUTTON
    # ========================================================

    timeBtn = Button(
        control_frame,
        text="▶ Time-In",
        command=toggle_time
    )

    apply_button_style(
        timeBtn,
        cfg.btn_bg_default
    )

    timeBtn.grid(
        row=0,
        column=0,
        padx=cfg.padx,
        pady=cfg.pady,
        sticky="ew"
    )

    control_frame.grid_columnconfigure(
        0,
        weight=1
    )

    # ========================================================
    # BREAK BUTTON
    # ========================================================

    breakBtn = Button(
        control_frame,
        text="☕ Break",
        command=toggle_break,
        state="disabled"
    )

    apply_button_style(
        breakBtn,
        cfg.btn_bg_default
    )

    breakBtn.grid(
        row=0,
        column=1,
        padx=cfg.padx,
        pady=cfg.pady,
        sticky="ew"
    )

    control_frame.grid_columnconfigure(
        1,
        weight=1
    )

    # ========================================================
    # CPM DISPLAY FRAME
    # ========================================================

    cpm_frame = Frame(
        app,
        bg=cfg.bg_secondary,
        relief=FLAT,
        padx=10,
        pady=10
    )

    cpm_frame.grid(
        row=2,
        column=0,
        columnspan=2,
        sticky="ew",
        padx=cfg.padx,
        pady=cfg.pady
    )

    cpm_label = Label(
        cpm_frame,
        text="Ready to start...",
        font=statsFont,
        bg=cfg.bg_secondary,
        fg=cfg.text_info
    )

    cpm_label.pack(
        side=LEFT,
        padx=cfg.padx
    )

    # ========================================================
    # SYSTEM MESSAGE FRAME
    # ========================================================

    msg_frame = Frame(
        app,
        bg=cfg.bg_primary
    )

    msg_frame.grid(
        row=3,
        column=0,
        columnspan=2,
        sticky="nsew",
        padx=cfg.padx,
        pady=cfg.pady
    )

    msg_label = Label(
        msg_frame,
        text="Activity Log",
        font=(cfg.fontfamily, 10, "bold"),
        bg=cfg.bg_primary,
        fg=cfg.color_info
    )

    msg_label.pack(
        anchor="w",
        pady=(0, 5)
    )

    systemMessage = Listbox(
        msg_frame,
        height=15,
        width=cfg.lbWidth,
        bg=cfg.bg_secondary,
        fg=cfg.fg_primary,
        font=cfg.font_mono,
        relief=FLAT,
        bd=0
    )

    systemMessage.pack(
        fill=BOTH,
        expand=True
    )

    systemMessage.insert(
        0,
        "Welcome to MEDA: InOut Dashboard"
    )

    # ========================================================
    # SCROLLBAR
    # ========================================================

    scrollbar = Scrollbar(
        msg_frame,
        command=systemMessage.yview,
        bg=cfg.bg_secondary
    )

    scrollbar.pack(
        side=RIGHT,
        fill=Y
    )

    systemMessage.config(
        yscrollcommand=scrollbar.set
    )

    app.grid_rowconfigure(
        3,
        weight=1
    )

    # ========================================================
    # FOOTER CONTROL FRAME
    # ========================================================

    footer_frame = Frame(
        app,
        bg=cfg.bg_primary
    )

    footer_frame.grid(
        row=4,
        column=0,
        columnspan=3,
        sticky="ew",
        padx=cfg.padx,
        pady=cfg.pady
    )

    # ========================================================
    # INSTRUCTIONS BUTTON
    # ========================================================

    infoBtn = Button(
        footer_frame,
        text="ℹ Instructions",
        command=instruction
    )

    apply_button_style(
        infoBtn,
        cfg.color_info
    )

    infoBtn.grid(
        row=0,
        column=0,
        padx=cfg.padx,
        pady=cfg.pady,
        sticky="ew"
    )

    footer_frame.grid_columnconfigure(
        0,
        weight=1
    )

    # ========================================================
    # SEND REPORT BUTTON
    # ========================================================

    sendBtn = Button(
        footer_frame,
        text="📧 Send Report",
        command=send_report
    )

    apply_button_style(
        sendBtn,
        cfg.color_secondary
    )

    sendBtn.grid(
        row=0,
        column=1,
        padx=cfg.padx,
        pady=cfg.pady,
        sticky="ew"
    )

    footer_frame.grid_columnconfigure(
        1,
        weight=1
    )

    # ========================================================
    # LOGOUT BUTTON
    # ========================================================

    logoutBtn = Button(
        footer_frame,
        text="🚪 Logout",
        command=logout
    )

    apply_button_style(
        logoutBtn,
        cfg.color_danger
    )

    logoutBtn.grid(
        row=0,
        column=2,
        padx=cfg.padx,
        pady=cfg.pady,
        sticky="ew"
    )

    footer_frame.grid_columnconfigure(
        2,
        weight=1
    )

    # ========================================================
    # START BACKGROUND TASKS
    # ========================================================

    auto_screenshot()
    update_cpm_display()

    # ========================================================
    # START APPLICATION
    # ========================================================

    app.mainloop()