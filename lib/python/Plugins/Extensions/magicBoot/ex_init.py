#Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/magicBoot/ex_init.py
import sys, magicboot
if len(sys.argv) < 3:
    pass
else:
    magicboot.magicBootMainEx(sys.argv[1], sys.argv[2], sys.argv[3])