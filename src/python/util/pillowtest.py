from PIL import Image, ImageDraw, ImageFont


my_image = Image.open("D20K6_1_0_psi2.0.png")

labelfont = ImageFont.truetype('Cambria-Font-For-Windows.ttf', 40)

label = "PSI-up 2.0"

image_editable = ImageDraw.Draw(my_image)

image_editable.text((15,15), label, (255,255,255), font=labelfont)

my_image.save("D20K6_1_0_psi2.0l.png")

