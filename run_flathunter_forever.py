#!/usr/bin/python
from subprocess import Popen
while True:

    print("\nStarting flathunter.py")
    p = Popen("python flathunter.py", shell=True)
    p.wait()