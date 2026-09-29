from tkinter import *
import tkinter.font as tkFont
import config as cfg
from dashboard import open_dashboard

def show_login():
    root = Tk()
    root.title("MEDA: InOut - Login")
    root.geometry("450x500")
    root.configure(bg=cfg.bg_primary)
    root.resizable(False, False)

    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    titleFont = tkFont.Font(
        root=root,
        weight=cfg.weight,
        size=cfg.titleFontSize,
        family=cfg.fontfamily
    )

    subtitleFont = tkFont.Font(
        root=root,
        family=cfg.fontfamily,
        size=10,
        slant="italic"
    )

    labelFont = tkFont.Font(
        root=root,
        family=cfg.fontfamily,
        size=10
    )

    # ===== HELPER FUNCTIONS =====
    def apply_button_style(button, bg_color=cfg.color_info):
        """Apply consistent button styling"""
        button.config(
            bg=bg_color,
            fg="white",
            font=(cfg.fontfamily, 11, "bold"),
            relief=FLAT,
            padx=20,
            pady=10,
            cursor="hand2",
            activebackground=cfg.btn_bg_active
        )

    def on_entry_focus_in(event, entry):
        """Handle entry focus in"""
        if entry.get() == entry.placeholder:
            entry.delete(0, END)
            entry.config(fg=cfg.fg_primary)

    def on_entry_focus_out(event, entry):
        """Handle entry focus out"""
        if entry.get() == "":
            entry.insert(0, entry.placeholder)
            entry.config(fg=cfg.fg_primary)

    def login():
        user_val = user_entry.get()
        pass_val = pass_entry.get()

        # Treat placeholder text as empty
        if user_val == user_entry.placeholder:
            user_val = ""
        if pass_val == pass_entry.placeholder:
            pass_val = ""

        if user_val == "" and pass_val == "":
            root.destroy()
            open_dashboard()
            show_login()
        else:
            status_label.config(text="✗ Invalid login", fg=cfg.color_danger)

    # ===== HEADER FRAME =====
    header_frame = Frame(root, bg=cfg.bg_secondary, height=100)
    header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=0)
    header_frame.grid_propagate(False)

    title_label = Label(
        header_frame, 
        text="🕐 MEDA: InOut", 
        font=titleFont, 
        bg=cfg.bg_secondary, 
        fg=cfg.color_info
    )
    title_label.pack(pady=10)

    subtitle_label = Label(
        header_frame, 
        text="Time & Activity Tracking System", 
        font=subtitleFont, 
        bg=cfg.bg_secondary, 
        fg=cfg.fg_primary
    )
    subtitle_label.pack(pady=(0, 10))

    # ===== LOGIN FORM FRAME =====
    form_frame = Frame(root, bg=cfg.bg_primary)
    form_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=25, pady=20)
    root.grid_rowconfigure(1, weight=1)

    # Username
    user_label = Label(form_frame, text="Username", font=labelFont, bg=cfg.bg_primary, fg=cfg.fg_primary)
    user_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

    user_entry = Entry(
        form_frame,
        font=(cfg.fontfamily, 11),
        bg=cfg.bg_secondary,
        fg=cfg.fg_primary,
        relief=FLAT,
        bd=0,
        insertbackground=cfg.color_info
    )
    user_entry.placeholder = "Enter username"
    user_entry.insert(0, user_entry.placeholder)
    user_entry.config(fg=cfg.fg_primary)
    user_entry.bind("<FocusIn>", lambda e: on_entry_focus_in(e, user_entry))
    user_entry.bind("<FocusOut>", lambda e: on_entry_focus_out(e, user_entry))
    user_entry.grid(row=1, column=0, sticky="ew", pady=(0, 20))
    form_frame.grid_columnconfigure(0, weight=1)

    # Password
    pass_label = Label(form_frame, text="Password", font=labelFont, bg=cfg.bg_primary, fg=cfg.fg_primary)
    pass_label.grid(row=2, column=0, sticky="w", pady=(0, 5))

    pass_entry = Entry(
        form_frame,
        font=(cfg.fontfamily, 11),
        bg=cfg.bg_secondary,
        fg=cfg.fg_primary,
        show="*",
        relief=FLAT,
        bd=0,
        insertbackground=cfg.color_info
    )
    pass_entry.placeholder = "Enter password"
    pass_entry.insert(0, pass_entry.placeholder)
    pass_entry.config(show="", fg=cfg.fg_primary)

    def pass_focus_in(event):
        if pass_entry.get() == pass_entry.placeholder:
            pass_entry.delete(0, END)
            pass_entry.config(show="*")

    def pass_focus_out(event):
        if pass_entry.get() == "":
            pass_entry.insert(0, pass_entry.placeholder)
            pass_entry.config(show="")

    pass_entry.bind("<FocusIn>", pass_focus_in)
    pass_entry.bind("<FocusOut>", pass_focus_out)
    pass_entry.grid(row=3, column=0, sticky="ew", pady=(0, 20))

    # Login Button
    login_btn = Button(form_frame, text="🔓 Login", command=login)
    apply_button_style(login_btn)
    login_btn.grid(row=4, column=0, sticky="ew", pady=10)

    # Status Label
    status_label = Label(form_frame, text="", font=(cfg.fontfamily, 9), bg=cfg.bg_primary, fg=cfg.fg_primary)
    status_label.grid(row=5, column=0, sticky="ew", pady=(10, 0))

    # ===== FOOTER FRAME =====
    footer_frame = Frame(root, bg=cfg.bg_secondary, height=30)
    footer_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=0, pady=0)
    footer_frame.grid_propagate(False)

    footer_label = Label(
        footer_frame,
        text="Leave fields empty to demo the application",
        font=(cfg.fontfamily, 8),
        bg=cfg.bg_secondary,
        fg=cfg.fg_primary
    )
    footer_label.pack(pady=5)

    root.mainloop()

# start app
show_login()