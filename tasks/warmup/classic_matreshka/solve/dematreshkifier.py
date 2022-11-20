#!/usr/bin/env python3
import subprocess, re, time, os
for i in range(1000,0,-1):
    zipfile_info = subprocess.run(["zipnote", f"matreshka_{i}.zip"], capture_output=True, text=True)
    zipfile_password = re.findall(r"Password for this zip archive is: ([A-Z0-9]*)\n", zipfile_info.stdout)[0]
    unzip_info = subprocess.run(["unzip", "-P", zipfile_password, f"matreshka_{i}.zip"], capture_output=True, text=True)
    os.remove(f"matreshka_{i}.zip")

