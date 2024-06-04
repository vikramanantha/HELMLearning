# Vikram Anantha
# Jul 29 2021
# Creating a QR Code for class signups
# HELM Learning
# https://www.geeksforgeeks.org/python-generate-qr-code-using-pyqrcode-module/

import pyqrcode
import png

website = "http://signup.helmlearning.com?geometry"
stored = 'dumpsterfiles/homepage_qr.png'


qr = pyqrcode.create(website)
qr.png(stored, scale=7, quiet_zone=1)
print("Created!")
print("Website: %s" % website)
print("Saved:   %s" % stored)