import os
import re

folder = r"C:\PDFs"

series_map = {
    "Q100": "DHC-8-100",
    "Q200": "DHC-8-200",
    "Q300": "DHC-8-300",
}

pattern = re.compile(
    r'^(Q100|Q200|Q300)\.AIPC\[\d+\]\.AIPC(.*?)(\.pdf)?$',
    re.IGNORECASE
)

for filename in os.listdir(folder):
    match = pattern.match(filename)

    if match:
        series = match.group(1)
        ata = match.group(2)

        ext = ".pdf" if filename.lower().endswith(".pdf") else ""

        new_name = (
            f"Pre Authored Copy "
            f"{series_map[series]} "
            f"AIPC {ata}{ext}"
        )

        old_path = os.path.join(folder, filename)
        new_path = os.path.join(folder, new_name)

        os.rename(old_path, new_path)

        print(f"{filename} -> {new_name}")