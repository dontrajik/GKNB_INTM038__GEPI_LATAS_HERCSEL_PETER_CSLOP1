def generateRandomPicture(noise):
    from PIL import Image, ImageDraw
    from barcode import EAN13
    from random import randint
    import os
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPM

    number = '5901234123457'
    my_code = EAN13(number)

    my_code.save("new_code")

    renderPM.drawToFile(svg2rlg("new_code.svg"), "barcode.png", fmt='PNG')

    r, g, b = randint(0, 255), randint(0, 255), randint(0, 255)

    img = Image.new('RGB', (512, 512), (r, g, b))

    draw = ImageDraw.Draw(img)
    for i in range(noise):
        x1 = randint(0, 512)
        x2 = randint(0, 512)
        y1 = randint(0, 512)
        y2 = randint(0, 512)
        draw.line((x1, x2, y1, y2), width=randint(1, 30), fill=(randint(0, 255), randint(0, 255), randint(0, 255)))

    img2 = Image.open("barcode.png").convert("RGB")
    img2 = img2.rotate(randint(0, 360), expand=1, fillcolor=(r, g, b))
    w = randint(0, 512-img2.size[0])
    h = randint(0, 512-img2.size[1])
    img.paste(img2, (w, h))

    img.save(''+str(w) + "_" + str(h)+".png", 'PNG')

    os.system("rm new_code.svg barcode.png ")
