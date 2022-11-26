# Vikram Anantha
# Jul 29 2021
# Creating a QR Code for class signups
# HELM Learning
# https://www.geeksforgeeks.org/python-generate-qr-code-using-pyqrcode-module/

import pyqrcode
import png


qr = pyqrcode.create("http://signup.helmlearning.com/class-signup.html?class=HTML")
qr.png('dumpsterfiles/interest_qr.png', scale=6, quiet_zone=1)