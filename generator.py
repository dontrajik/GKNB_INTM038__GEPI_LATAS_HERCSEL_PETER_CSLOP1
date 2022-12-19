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
        draw.line((x1, x2, y1, y2), width=randint(1, 30), fill=(
            randint(0, 255), randint(0, 255), randint(0, 255)))

    img2 = Image.open("barcode.png").convert("RGBA")
    barcodeWhere = Image.open("barcode.png").convert("RGBA")
    draw2 = ImageDraw.Draw(barcodeWhere)
    draw2.rectangle([(0, 0), barcodeWhere.size], fill=(255, 255, 255))
    barcodeWhere.save("asd.png", 'PNG')

    angle = randint(0, 360)
    img2 = img2.rotate(angle, expand=1)
    barcodeWhere = barcodeWhere.rotate(angle, expand=1)
    w = randint(0, 512-img2.size[0])
    h = randint(0, 512-img2.size[1])
    img.paste(img2, (w, h), img2)

    savename = "{}_{}_{}_{}_{}.png".format(
        w, h, img2.size[0], img2.size[1], angle)
    img.save(savename, 'PNG')
    draw.rectangle([(0, 0), img.size], fill=(0, 0, 0))
    img.paste(barcodeWhere, (w, h), barcodeWhere)

    savename = "{}_{}_{}_{}_{}_test.png".format(
        w, h, img2.size[0], img2.size[1], angle)
    img = img.convert("RGB")
    img.save(savename, 'PNG')

    os.system("rm new_code.svg barcode.png asd.png")
