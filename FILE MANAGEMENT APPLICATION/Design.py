import os
import shutil
import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox
import time
import json

# ---------------- THEMES ----------------
LIGHT_THEME = {
    "bg": "#9EDCD0",
    "panel": "#88D5C7",
    "button": "#309D92",
    "text": "#090909",
    "list_bg": "#FFFFFF"
}

DARK_THEME = {
    "bg": "#1e1e1e",
    "panel": "#111827",
    "button": "#1A3C37",
    "text": "#FFFFFF",
    "list_bg": "#1f2933"
}

current_theme = DARK_THEME
current_folder = None

# ---------------- APP SETUP ----------------
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class FileExplorerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("File Explorer")
        self.geometry("1000x580")
        
        self.folder_history = []
        self.current_folder = None
        self.normal_buttons = []
        
        # Initialize UI
        self.setup_ui()

    def choose_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_history.clear()
            self.current_folder = path
            self.path_lbl.configure(text=f"Current Folder: {path}")
            self.load_files()

    def load_files(self):
        self.tree.delete(*self.tree.get_children())
        if not self.current_folder:
            return

        keyword = self.search_var.get().lower()

        for name in os.listdir(self.current_folder):
            if keyword and keyword not in name.lower():
                continue

            full = os.path.join(self.current_folder, name)
            ftype = "Folder" if os.path.isdir(full) else "File"
            size = "-" if ftype == "Folder" else f"{os.path.getsize(full)//1024} KB"
            self.tree.insert("", "end", values=(name, ftype, size))

    def clear_search(self):
        self.search_var.set("")
        self.load_files()

    def selected_path(self):
        sel = self.tree.focus()
        if not sel:
            return None
        return os.path.join(self.current_folder, self.tree.item(sel)["values"][0])

    def open_item(self):
        p = self.selected_path()
        if not p:
            return

        if os.path.isdir(p):
            self.folder_history.append(self.current_folder)
            self.current_folder = p
            self.path_lbl.configure(text=f"Current Folder: {p}")
            self.load_files()
        else:
            os.startfile(p)

    def rename_item(self):
        p = self.selected_path()
        if p:
            new = filedialog.asksaveasfilename(initialdir=self.current_folder)
            if new:
                os.rename(p, new)
                self.load_files()

    def move_item(self):
        p = self.selected_path()
        if p:
            dest = filedialog.askdirectory()
            if dest:
                shutil.move(p, dest)
                self.load_files()

    def go_back(self):
        if not self.folder_history:
            messagebox.showinfo("Back", "No previous folder.")
            return

        self.current_folder = self.folder_history.pop()
        self.path_lbl.configure(text=f"Current Folder: {self.current_folder}")
        self.load_files()

    def delete_item(self):
        p = self.selected_path()
        if p and messagebox.askyesno("Delete", "Confirm delete?"):
            if os.path.isfile(p):
                os.remove(p)
            else:
                shutil.rmtree(p)
            self.load_files()

    # ---------------- SORT LOGIC ----------------
    def sort_items(self):
        if not self.current_folder:
            messagebox.showwarning("No Folder", "Please choose a folder first.")
            return

        start_time = time.time()
        moved_files = {}

        for file in os.listdir(self.current_folder):
            source_path = os.path.join(self.current_folder, file)

            if not os.path.isfile(source_path):
                continue

            name, ext = os.path.splitext(file)
            ext = ext[1:].upper()

            if not ext:
                continue

            folder_path = os.path.join(self.current_folder, ext)

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            destination = os.path.join(folder_path, file)

            try:
                shutil.move(source_path, destination)
                moved_files[file] = folder_path
            except Exception as e:
                messagebox.showerror("Error", f"Failed to move {file}\n{e}")

        if moved_files:
            log_file = os.path.join(self.current_folder, "file_log.json")
            with open(log_file, "w") as f:
                json.dump(moved_files, f, indent=4)

        elapsed = time.time() - start_time
        self.load_files()

        messagebox.showinfo(
            "Sorting Complete",
            f"{len(moved_files)} files sorted in {elapsed:.2f} seconds"
        )

    def undo_sort(self):
        if not self.current_folder:
            return

        log_file = os.path.join(self.current_folder, "file_log.json")

        if not os.path.exists(log_file):
            messagebox.showwarning("Undo", "No previous sort found.")
            return

        with open(log_file, "r") as f:
            moved_files = json.load(f)

        for file, folder in moved_files.items():
            source = os.path.join(folder, file)
            destination = os.path.join(self.current_folder, file)

            if os.path.exists(source):
                shutil.move(source, destination)

        os.remove(log_file)
        self.load_files()

        messagebox.showinfo("Undo Complete", "Files restored successfully.")

    # ---------------- PREVIEW ----------------
    def show_preview(self, event):
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", "end")

        sel = self.tree.focus()
        if not sel:
            return

        name, ftype, size = self.tree.item(sel)["values"]
        full_path = os.path.join(self.current_folder, name)

        info = f"""Name : {name}
            Type : {ftype}
            Size : {size}
            Path :{full_path}
            Date Modified : {time.ctime(os.path.getmtime(full_path))}
            Modified By : {os.getlogin()}
            Created By : {os.getlogin()}
            Author : File Management System
            Contents type : {'Folder' if os.path.isdir(full_path) else 'File'}
            Contents size : {os.path.getsize(full_path)} bytes
            Content created : {time.ctime(os.path.getctime(full_path))}
            Data accessed : {time.ctime(os.path.getatime(full_path))}
            Last saved : {time.ctime(os.path.getctime(full_path))}
            Last opened : {time.ctime(os.path.getatime(full_path))}
            Last Saved By : {os.getlogin()}
            Last saved location : {full_path}
            Last saved Date : {time.ctime(os.path.getmtime(full_path))}
            """
        self.preview_text.insert("end", info)
        self.preview_text.configure(state="disabled")

    # ---------------- THEME ----------------
    def apply_theme(self, theme):
        self.configure(fg_color=theme["bg"])
        self.header.configure(fg_color=theme["panel"])
        self.main.configure(fg_color=theme["bg"])
        self.left.configure(fg_color=theme["panel"])
        self.right.configure(fg_color=theme["bg"])
        self.path_lbl.configure(text_color=theme["text"])

        for b in self.normal_buttons:
            b.configure(fg_color=theme["button"], text_color=theme["text"])

    def toggle_mode(self):
        global current_theme
        if self.mode_switch.get():
            ctk.set_appearance_mode("Dark")
            current_theme = DARK_THEME
        else:
            ctk.set_appearance_mode("Light")
            current_theme = LIGHT_THEME
        self.apply_theme(current_theme)

    def normal_btn(self, text, cmd):
        b = ctk.CTkButton(self.left, text=text, command=cmd)
        b.pack(pady=6, padx=14, fill="x")
        self.normal_buttons.append(b)

    def setup_ui(self):
        # ---------------- HEADER ----------------
        self.header = ctk.CTkFrame(self, height=48)
        self.header.pack(fill="x")

        ctk.CTkLabel(
            self.header, text="📁 File Explorer",
            font=("Segoe UI", 18, "bold")
        ).pack(side="left", padx=18)

        self.mode_switch = ctk.CTkSwitch(self.header, text="Dark Mode", command=self.toggle_mode)
        self.mode_switch.select()
        self.mode_switch.pack(side="right", padx=18)

        # ---------------- MAIN ----------------
        self.main = ctk.CTkFrame(self)
        self.main.pack(fill="both", expand=True, padx=10, pady=10)

        self.left = ctk.CTkFrame(self.main, width=230)
        self.left.pack(side="left", fill="y", padx=(0, 10))

        self.right = ctk.CTkFrame(self.main)
        self.right.pack(side="right", fill="both", expand=True)

        # ---------------- LEFT BUTTONS ----------------
        ctk.CTkButton(
            self.left, text="🗂️ Choose Folder",
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            text_color="white",
            command=self.choose_folder
        ).pack(pady=(14, 8), padx=14, fill="x")

        self.normal_btn("▶ Open", self.open_item)
        self.normal_btn("✏ Rename", self.rename_item)
        self.normal_btn("📦 Move", self.move_item)

        ctk.CTkButton(
            self.left, text="⇅ Sort Files",
            fg_color="#520C7D",
            hover_color="#9038A9",
            command=self.sort_items
        ).pack(pady=(10, 6), padx=14, fill="x")

        ctk.CTkButton(
            self.left, text="↩ Undo Sort",
            fg_color="#520C7D",
            hover_color="#9038A9",
            command=self.undo_sort
        ).pack(pady=(0, 10), padx=14, fill="x")

        ctk.CTkButton(
            self.left,
            text="⬅ Back",
            fg_color="#475569",
            hover_color="#334155",
            command=self.go_back
        ).pack(pady=(6, 6), padx=14, fill="x")

        ctk.CTkButton(
            self.left, text="🗑 Delete",
            fg_color="#7E2626",
            hover_color="#B71C1C",
            command=self.delete_item
        ).pack(pady=(16, 12), padx=14, fill="x")

        # ---------------- RIGHT PANEL ----------------
        self.path_lbl = ctk.CTkLabel(self.right, text="Current Folder: None", anchor="w")
        self.path_lbl.pack(fill="x", padx=10, pady=6)

        # ---------------- SEARCH BAR ----------------
        top_bar = ctk.CTkFrame(self.right, height=42)
        top_bar.pack(fill="x", padx=10, pady=(0, 6))

        self.search_var = ctk.StringVar()

        search_entry = ctk.CTkEntry(
            top_bar,
            placeholder_text="Search files...",
            textvariable=self.search_var
        )
        search_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
        search_entry.bind("<KeyRelease>", lambda e: self.load_files())

        ctk.CTkButton(
            top_bar,
            text="❌ Clear",
            width=70,
            command=self.clear_search
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            top_bar,
            text="🔄 Refresh",
            width=90,
            command=self.load_files
        ).pack(side="right")

        # ---------------- CONTENT ----------------
        content = ctk.CTkFrame(self.right)
        content.pack(fill="both", expand=True, padx=10, pady=10)

        table_frame = ctk.CTkFrame(content)
        table_frame.pack(side="left", fill="both", expand=True, padx=(0, 8))

        preview_frame = ctk.CTkFrame(content, width=240)
        preview_frame.pack(side="right", fill="y")

        # ---------------- TABLE ----------------
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview",
            background=DARK_THEME["list_bg"],
            foreground="white",
            fieldbackground=DARK_THEME["list_bg"],
            rowheight=28
        )

        style.map(
            "Treeview",
            background=[("selected", "#2563eb")],
            foreground=[("selected", "white")]
        )

        cols = ("Name", "Type", "Size")

        tree_scroll = ttk.Scrollbar(table_frame)
        tree_scroll.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            table_frame,
            columns=cols,
            show="headings",
            yscrollcommand=tree_scroll.set
        )

        tree_scroll.config(command=self.tree.yview)

        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="w")

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.show_preview)

        # ---------------- PREVIEW ----------------
        ctk.CTkLabel(
            preview_frame,
            text="📄 Preview",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=(12, 6))

        self.preview_text = ctk.CTkTextbox(preview_frame, wrap="word")
        self.preview_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.preview_text.insert("end", "Select a file to preview details...")
        self.preview_text.configure(state="disabled")

        # ---------------- INIT ----------------
        self.apply_theme(current_theme)

if __name__ == "__main__":
    explorer = FileExplorerApp()
    explorer.mainloop()