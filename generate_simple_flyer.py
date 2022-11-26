# Vikram Anantha
# Jul 29 2021
# Creating Simple Flyer for teachers
# HELM Learning

from tkinter import *
from PIL import ImageTk, Image
from PIL import ImageGrab, ImageFont
import helper_functions as hf
import os

fontfam = "dumpsterfiles/productsans.ttf"
fontfambold = "dumpsterfiles/productsans-bold.ttf"

# tk = Tk()
# canvas = Canvas(tk, width=800, height=800, bg="#642c94")
# canvas.pack()

# canvas.create_text(400, 200, text="Want to Learn\n%s\nfor FREE?" % classname, font=(fontfam, 110, "bold"), fill="white", justify="center")

# hf.generate_qrcode(classname)

# image = Image.open('dumpsterfiles/%s_qrcode.png' % classname.lower()) # this stores the image into a variable
# image = image.resize((250, 250), Image.ANTIALIAS) # resizes the image to be 400x200
# image = ImageTk.PhotoImage(image) # doesn't really matter, just do it
# canvas.create_image(805, 800, anchor=SE, image=image)

# canvas.create_text(440, 676, text="Find more\ndetails for the\n%s\nclass at HELM\nto learn for\nFREE!" % classname, fill="white", font=(fontfam, 33), justify="left")

# canvas.create_text(675, 520, text="signup.helmlearning.com?\n%s" % classname, font=(fontfam, 20), justify="center", fill="white")

# image2 = Image.open('logo.png') # this stores the image into a variable
# image2 = image2.resize((270, 90), Image.ANTIALIAS) # resizes the image to be 400x200
# image2 = ImageTk.PhotoImage(image2) # doesn't really matter, just do it
# canvas.create_image(0, 800, anchor=SW, image=image2)

# canvas.postscript(file = 'dumpsterfiles/%s_simple_flyer.ps' % classname, colormode='color')
# img = Image.open('dumpsterfiles/%s_simple_flyer.esp' % classname)
# img.save('%s_simple_flyer.png' % classname, 'png')

from PIL import Image, ImageDraw

def make_simple_flyer(classname):
    output = hf.generate_simple_flyer(classname)
    add_to_sharing_mats(classname, filename='%s Simple Flyer.png', fileloc=output)

def make_async_flyer(classname):
    output = "dumpsterfiles/%s_async_flyer.png" % classname.lower().replace(" ", "-")
    im = Image.new('RGBA', (600, 600), (99, 44, 148, 255))
    draw = ImageDraw.Draw(im) 

    w, h = draw.textsize("Want to learn\n%s\nat your own pace?" % classname, font=ImageFont.truetype(fontfambold, 60))
    draw.text(((600-w)/2, 10), "Want to learn\n%s\nat your own pace?" % classname, align="center", fill="white", font=ImageFont.truetype(fontfambold, 60))
    # print(w)
    # if (w > 800):
    #     fontsize = 85
    #     w, h = draw.textsize("Want to Learn\n%s\nfor FREE?" % classname, font=ImageFont.truetype(fontfambold, 85))
    # else:
    #     fontsize = 110
    # draw.text(((800-w)/2, 50), "Want to Learn\n%s\nfor FREE?" % classname, align="center", fill="white", font=ImageFont.truetype(fontfambold, fontsize))
    # w, h = draw.textsize("%s" % classname, font=ImageFont.truetype(fontfam, 110))
    # draw.text(((800-w)/2, 50+103), "%s" % classname, fill="white", font=ImageFont.truetype(fontfam, 110))
    # w, h = draw.textsize("for FREE?", font=ImageFont.truetype(fontfam, 110))
    # draw.text(((800-w)/2, 50+2*103), "for FREE?", fill="white", font=ImageFont.truetype(fontfam, 110))

    w, h = draw.textsize("Receive FREE class resources created\nby qualified teachers at HELM Learning\nused to teach %s" % classname, font=ImageFont.truetype(fontfambold, 30))
    # print(w)
    draw.text((300-(w/2), 260), "Receive FREE class resources created\nby qualified teachers at HELM Learning\nused to teach %s" % classname, fill="white", font=ImageFont.truetype(fontfambold, 30), align='center')

    # if (not os.path.exists('dumpsterfiles/%s_qrcode.png')):
    hf.generate_qrcode(classname)

    im2 = Image.open('dumpsterfiles/%s_qrcode.png' % classname.lower().replace(" ", "-"))
    im2 = im2.resize((200, 200), Image.BOX)
    im.paste(im2, (400, 400))

    w,h = draw.textsize("signup.helmlearning.com?%s" % classname.lower().replace(" ", "-"), font=ImageFont.truetype(fontfambold, 20))
    draw.text(((400-w)/2, 420), "Scan the QR code or go to", fill="white", font=ImageFont.truetype(fontfam, 20), align="left")
    draw.text(((400-w)/2, 440), "signup.helmlearning.com?%s" % classname.lower().replace(" ", "-"), fill="white", font=ImageFont.truetype(fontfambold, 20), align="left")

    im2 = Image.open('logo.png')
    im2 = im2.resize((210, 70), Image.BOX)
    im.paste(im2, (0, 530), im2)

    # im.show()
    im.save(output)
    print("Async Flyer Created for the %s class (in the folder %s" % (classname, output))

    add_to_sharing_mats(classname)

def make_flyer_v2(classname):
    output = hf.generate_flyer_v2(classname)
    add_to_sharing_mats(classname, filename='%s Flyer V2.png', fileloc=output)

def add_to_sharing_mats(classname, filename="%s Async Flyer.png", fileloc="dumpsterfiles/%s_async_flyer.png"):
    if "%s" in fileloc: fileloc = fileloc % classname.lower().replace(" ", "-")
    cnx, cursor = hf.start()
    cursor.execute("select sharing_mats from classes where short_name = '%s'" % classname)
    sharing_mats = cursor.fetchall()[0][0]

    hf.upload_file_to_folder(filename % classname, fileloc, sharing_mats[39:-12])


class_name = input("For which class? ")
make_simple_flyer(class_name)
# make_flyer_v2(class_name)
# hf.generate_simple_flyer("AMC8")