import os
from pathlib import Path

desktop_path = Path(os.environ.get("USERPROFILE", "")) / "Desktop"
current_dir = Path(__file__).resolve().parent

vbs_launcher = current_dir / "Launch App.vbs"
icon_path = current_dir / "tn_transport_ai" / "static" / "icons" / "icon-192.png"

vbs_content = f'''Set WshShell = CreateObject("WScript.Shell")
strDesktop = WshShell.SpecialFolders("Desktop")
Set oMyShortcut = WshShell.CreateShortcut(strDesktop & "\\TN Smart Transport AI.lnk")
oMyShortcut.TargetPath = "wscript.exe"
oMyShortcut.Arguments = """{str(vbs_launcher)}"""
oMyShortcut.WorkingDirectory = """{str(current_dir)}"""
oMyShortcut.Description = "Tamil Nadu Smart Transport AI"
oMyShortcut.Save
'''

temp_vbs = current_dir / "_make_shortcut.vbs"
temp_vbs.write_text(vbs_content, encoding="utf-8")

os.system(f'cscript //nologo "{temp_vbs}"')

if temp_vbs.exists():
    temp_vbs.unlink()

print("Shortcut created on Desktop successfully!")
