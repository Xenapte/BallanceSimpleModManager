import sys
import tkinter as tk
import tkinter.font as tkfont
from tkinter import filedialog, messagebox
from glob import glob
from os import path, rename

window = tk.Tk()
window.title("Ballance Mod Manager")

def center_main():
  window.tk.eval(f'tk::PlaceWindow {window._w} center')

center_main()

header_font = tkfont.Font(family="Times New Roman", size=14)
text_font = tkfont.Font(family="Arial", size=11)
sidenote_font = tkfont.Font(family="Tahoma", size=8)

tk.Label(window, text="Mods to keep", font=header_font).pack(anchor=tk.CENTER)

base_directory = filedialog.askdirectory(title="Choose the Ballance directory")
mods_directory_name = "/ModLoader/Mods" # to make this fool-proof
if path.isdir(base_directory + mods_directory_name):
  base_directory = base_directory + mods_directory_name
tk.Label(window, text=base_directory, font=sidenote_font).pack(anchor=tk.W)
base_directory += "/"

files: list[dict[str, tk.BooleanVar]] = []

def move_file():
  for file in files:
    try:
      if file["enabled"].get():
        rename(base_directory + file["basename"] + "-d", base_directory + file["basename"])
      else:
        rename(base_directory + file["basename"], base_directory + file["basename"] + "-d")
    except FileExistsError:
      print("File already exists")
    except FileNotFoundError:
      pass

for fn in glob(base_directory + "/*.bmod*"):
  basename = path.basename(fn)
  name, ext = path.splitext(basename)
  enabled = tk.BooleanVar()
  if ext == ".bmod" or ext == ".bmodp":
    enabled.set(True)
  elif ext == ".bmod-d" or ext == ".bmodp-d":
    enabled.set(False)
    basename = name + ext.replace("-d", "")
  else:
    continue
  tk.Checkbutton(window, text=basename, font=text_font, onvalue=True, offvalue=False, variable=enabled, command=move_file).pack(anchor=tk.W)
  files.append({"basename": basename, "enabled": enabled})

tk.Label(window, text="Created by BallanceBug\nwith Tkinter, 2023-10-01.", font=sidenote_font).pack(anchor=tk.E)

center_main()

if not files:
  messagebox.showerror("Error", "No mod files found in the selected directory!")
  window.quit()
  sys.exit(1)
window.mainloop()

