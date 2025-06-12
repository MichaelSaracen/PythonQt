from pathlib import Path
import subprocess
from typing import Generator

ui_dirs: Path = Path("App/Gui")
ui_files: Generator = ui_dirs.glob("*.ui")

init_text: str = ""
print("▶️","=" * 10, "Translate Ui - Files to Py - Files", "=" * 10)

for ui_file in ui_files:
    output_py: Path = ui_file.with_name(f"Ui_{ui_file.stem}.py")
    print(f"[+] {ui_file}  {output_py}")
    init_text += f"from .{output_py.stem} import {output_py.stem}\n"
    subprocess.run(["pyside6-uic", ui_file, "-o", output_py])

out_init = ui_dirs / "__init__.py"

print("▶️","»" , "Writing in App/Gui/__init__.py")
out_init.write_text(init_text)
print("▶️","»", "Running main.py\n")
subprocess.run(["python", "main.py"])

