import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

SERIES_MAP = {
    "Q100": "DHC-8-100",
    "Q200": "DHC-8-200",
    "Q300": "DHC-8-300",
}

PATTERN = re.compile(
    r'^(Q100|Q200|Q300)\.AIPC\[\d+\]\.AIPC(.*?)(\.[^.]+)?$',
    re.IGNORECASE
)

class RenamerGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("DHC-8 AIPC Renamer")
        self.root.geometry("1000x600")

        self.folder_path = ""

        self.copy_type = tk.StringVar()
        self.copy_type.set("Pre Authored Copy")

        top = tk.Frame(root)
        top.pack(fill="x", padx=10, pady=10)

        tk.Button(
            top,
            text="Select Folder",
            command=self.select_folder
        ).pack(side="left")

        tk.Label(
            top,
            text="Rename Type:"
        ).pack(side="left", padx=15)

        ttk.Combobox(
            top,
            textvariable=self.copy_type,
            values=[
                "Pre Authored Copy",
                "Proposed Authored Copy"
            ],
            width=30,
            state="readonly"
        ).pack(side="left")

        tk.Button(
            top,
            text="Preview",
            command=self.load_preview
        ).pack(side="left", padx=10)

        self.tree = ttk.Treeview(
            root,
            columns=("old", "new"),
            show="headings"
        )

        self.tree.heading("old", text="Original File")
        self.tree.heading("new", text="New File")

        self.tree.column("old", width=400)
        self.tree.column("new", width=550)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Button(
            root,
            text="Rename Files",
            bg="green",
            fg="white",
            command=self.rename_files
        ).pack(pady=10)

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        self.load_preview()

    def build_new_name(self, filename):

        match = PATTERN.match(filename)

        if not match:
            return None

        series = match.group(1).upper()
        ata = match.group(2)
        ext = match.group(3) or ""

        return (
            f"{self.copy_type.get()} "
            f"{SERIES_MAP[series]} "
            f"AIPC {ata}{ext}"
        )

    def load_preview(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        if not self.folder_path:
            return

        for file in os.listdir(self.folder_path):

            new_name = self.build_new_name(file)

            if new_name:
                self.tree.insert(
                    "",
                    "end",
                    values=(file, new_name)
                )

    def rename_files(self):

        count = 0

        for row in self.tree.get_children():

            old_name, new_name = self.tree.item(row)["values"]

            old_path = os.path.join(
                self.folder_path,
                old_name
            )

            new_path = os.path.join(
                self.folder_path,
                new_name
            )

            if os.path.exists(old_path):
                os.rename(old_path, new_path)
                count += 1

        messagebox.showinfo(
            "Completed",
            f"{count} files renamed."
        )

        self.load_preview()

root = tk.Tk()
app = RenamerGUI(root)
root.mainloop()