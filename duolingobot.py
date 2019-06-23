from googletrans import Translator
import Levenshtein as lvsn
import pyscreenshot as ImageGrab
import re
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

im = ImageGrab.grab(bbox=(100,200,1250,700))
im.save('duolingo.png')

pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.0.0_1/bin/tesseract'

x = pytesseract.image_to_string(Image.open('duolingo.png'))
xlist = x.splitlines()
x = "\n".join([x for x in xlist if len(x) > 0])

f = open("duolingo.txt", "a+b")
f.write(bytes(x, "utf-8"))
f.close()

f = open("duolingo.txt", "r+", encoding='utf-8')
lines = f.readlines()
f.close()
open('duolingo.txt', 'w').close()

trans = Translator()
lc = 0

task = lines[0]
tdist1 = lvsn.distance(task, "Mark the correct meaning")
tdist2 = lvsn.distance(task, "Write this in English")
tdist3 = lvsn.distance(task, "Write this in Spanish")

if tdist1 < tdist2 and tdist1 < tdist3:
    tl = trans.translate(lines[1], dest = 'es').text

    op1 = lines[2]
    op2 = lines[3]
    op3 = lines[4]
    dist1 = lvsn.distance(tl, op1)
    dist2 = lvsn.distance(tl, op2)
    dist3 = lvsn.distance(tl, op3)


    if min(dist1, dist2, dist3) >= 10:
        print("Unsure match")
    if min(dist1, dist2, dist3) == dist1:
        print("[1]")
    elif min(dist1, dist2, dist3) == dist2:
        print("[2]")
    else:
        print("[3]")

elif tdist2 < tdist1 and tdist2 < tdist3:
    tl = trans.translate(lines[1], dest = 'en').text
    tl = re.sub('[^ a-zA-Z0-9]', '', tl)
    print(tl)

else:
    tl = trans.translate(lines[1], dest = 'es').text
    tl = re.sub('[^ a-zA-Z0-9]', '', tl)
    print(tl)



