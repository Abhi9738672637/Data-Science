
import os
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Aircraft Mapping
SERIES_MAP = {
    "Q100": "DHC-8-100",
    "Q200": "DHC-8-200",
    "Q300": "DHC-8-300"
}

# Example:
# Q100.AIPC[79].AIPC26-12-00-05.pdf
PATTERN = re.compile(
    r'^(Q100|Q200|Q300)\.AIPC\[\d+\]\.AIPC(.*?)(\.[^.]+)?$',
    re.IGNORECASE
)


class RenamerGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("DHC-8 Document Renamer")
        self.root.geometry("1200x700")

        self.folder_path = ""

        self.copy_type = tk.StringVar(value="Pre Authored Copy")

        top_frame = tk.Frame(root)
        top_frame.pack(fill="x", padx=10, pady=10)

        tk.Button(
            top_frame,
            text="Select Folder",
            command=self.select_folder
        ).pack(side="left")

        tk.Label(
            top_frame,
            text="Copy Type:"
        ).pack(side="left", padx=(30, 5))

        ttk.Combobox(
            top_frame,
            textvariable=self.copy_type,
            values=[
                "Pre Authored Copy",
                "Proposed Authored Copy"
            ],
            width=25,
            state="readonly"
        ).pack(side="left")

        tk.Button(
            top_frame,
            text="Refresh Preview",
            command=self.load_preview
        ).pack(side="left", padx=15)

        self.tree = ttk.Treeview(
            root,
            columns=("Old", "New"),
            show="headings"
        )

        self.tree.heading("Old", text="Current File Name")
        self.tree.heading("New", text="New File Name")

        self.tree.column("Old", width=450)
        self.tree.column("New", width=650)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Button(
            root,
            text="Rename Files",
            bg="green",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.rename_files
        ).pack(pady=10)

    def select_folder(self):
        folder = filedialog.askdirectory()

        if folder:
            self.folder_path = folder
            self.load_preview()

    def build_new_name(self, filename):

        match = PATTERN.match(filename)

        if not match:
            return None

        series = match.group(1).upper()
        ata = match.group(2)
        ext = match.group(3) or ""

        aircraft = SERIES_MAP.get(series)

        return (
            f"{self.copy_type.get()} "
            f"{aircraft} "
            f"AIPC {ata}{ext}"
        )

    def load_preview(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.folder_path:
            return

        for filename in os.listdir(self.folder_path):

            new_name = self.build_new_name(filename)

            if new_name:
                self.tree.insert(
                    "",
                    "end",
                    values=(filename, new_name)
                )

    def rename_files(self):

        if not self.folder_path:
            messagebox.showwarning(
                "Warning",
                "Please select a folder first."
            )
            return

        count = 0

        for item in self.tree.get_children():

            old_name, 