from pygame import *
from math import sqrt
from random import randint
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

gray = (211, 211, 211)
white = (255, 255, 255)

screen = display.set_mode((1024, 768))
background = image.load("images/background.png")
screen.blit(background, (0, 0))

canvasRect = Rect(122, 51, 1024-122*2, 768-61*2)  # blank canvas
draw.rect(screen, (255, 255, 255), canvasRect)

init()  # initializes text and music
myfont = font.SysFont('Helvetica', 12)  # text font

mixer.music.load("sounds/megalovania.mp3")  # music
mixer.music.play(-1)

# rect for where all stickers are
draw.rect(screen, (30, 30, 30), (902, 75, 122, 596))

# --------------------------------IMAGES AND RECTS---------------------------------

spectrum = transform.smoothscale(image.load("images/spectrum.jpg"), (115, 115))
screen.blit(spectrum, (4, 560))
colour = (0)  # colour starts black

pencilRect = Rect(3, 51, 56, 56)
pencil = transform.smoothscale(image.load("images/pencil.png"), (50, 50))
pencilselect = transform.smoothscale(
    image.load("images/pencilselect.png"), (50, 50))

eraserRect = Rect(3, 115, 56, 56)
eraser = transform.smoothscale(image.load("images/eraser.png"), (46, 46))
eraserselect = transform.smoothscale(
    image.load("images/eraserselect.png"), (46, 46))

removeRect = Rect(5, 14, 30, 30)
remove = transform.smoothscale(image.load(
    "images/remove.png"), (1100//52, 1303//52))
removeselect = transform.smoothscale(image.load(
    "images/removeselect.png"), (1100//52, 1303//52))

saveRect = Rect(5, 728, 35, 35)
save = transform.smoothscale(image.load("images/save.png"), (28, 28))
saveselect = transform.smoothscale(
    image.load("images/saveselect.png"), (28, 28))

openRect = Rect(45, 728, 35, 35)
openfile = transform.smoothscale(image.load("images/open.png"), (29, 29))
openfileselect = transform.smoothscale(
    image.load("images/openselect.png"), (29, 29))

paintRect = Rect(62, 51, 56, 56)
paint = transform.smoothscale(image.load(
    "images/paint.png"), (514//12, 626//12))
paintselect = transform.smoothscale(image.load(
    "images/paintselect.png"), (514//12, 626//12))

pickerRect = Rect(62, 115, 56, 56)
picker = transform.smoothscale(image.load("images/picker.png"), (54, 54))
pickerselect = transform.smoothscale(
    image.load("images/pickerselect.png"), (54, 54))

lineRect = Rect(3, 179, 56, 56)

fRect = Rect(3, 243, 56, 56)
unfRect = Rect(62, 243, 56, 56)

fCirc = Rect(3, 307, 56, 56)
unfCirc = Rect(62, 307, 56, 56)

polyRect = Rect(62, 179, 56, 56)
polygon = transform.smoothscale(image.load(
    "images/polygon.png"), (600//13, 600//13))
polyselect = transform.smoothscale(image.load(
    "images/polyselect.png"), (600//13, 600//13))
polypoints = []  # for each polygon point
polyredos = []  # adds to this list when undoing

undoRect = Rect(40, 14, 30, 30)
undo = transform.smoothscale(image.load("images/undo.png"), (26, 26))
undoselect = transform.smoothscale(
    image.load("images/undoselect.png"), (26, 26))

redoRect = Rect(75, 14, 30, 30)
redo = transform.smoothscale(image.load("images/redo.png"), (26, 26))
redoselect = transform.smoothscale(
    image.load("images/redoselect.png"), (26, 26))

sansRect = Rect(918, 95-40, 92, 115)
sans = transform.scale(image.load("images/sans.png"), (1024//13, 1346//13))

undyneRect = Rect(918, 220-40, 92, 130)
undyne = transform.scale(image.load("images/undyne.png"), (284//3, 366//3))

papyrusRect = Rect(918, 360-40, 92, 115)
papyrus = transform.scale(image.load(
    "images/papyrus.png"), (710//10, 1050//10))

friskRect = Rect(918, 445, 92, 115)
frisk = transform.scale(image.load("images/frisk.png"), (470//4, 389//4))

floweyRect = Rect(918, 570, 92, 115)
flowey = transform.smoothscale(image.load(
    "images/flowey.png"), (543//7, 568//7))

sprayRect = Rect(3, 371, 56, 56)
spray = transform.smoothscale(image.load("images/spray.png"), (50, 50))
sprayselect = transform.smoothscale(
    image.load("images/sprayselect.png"), (50, 50))

fillRect = Rect(62, 371, 56, 56)
fill = transform.smoothscale(image.load("images/fill.png"), (65, 65))
fillselect = transform.smoothscale(
    image.load("images/fillselect.png"), (65, 65))

# ---------------------------------------------------------------------------------------

tool = 'pencil'  # tool starts as this
lastpos = None  # to allow pencil and paintbrush to work
undos = [screen.subsurface(canvasRect).copy()]  # first element is blank canvas
redos = []

size = 4  # size starts as 4
sRect1 = Rect(10-4, 700-13, 26, 26)  # size rects
sRect2 = Rect(35-7, 700-13, 26, 26)
sRect3 = Rect(67-10, 700-13, 26, 26)
sRect4 = Rect(106-13, 700-13, 26, 26)
canCount = 0

running = True
while running:
    mx, my = mouse.get_pos()  # mouse location
    leftclick = False
    rightclick = False
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == MOUSEBUTTONDOWN:
            back = screen.copy()  # for dragging
            if e.button == 1:
                start = e.pos  # keep track of where first clicking
                canCount = 0
        if e.type == MOUSEBUTTONUP:
            lastpos = None  # becomes none when not clicking
            if e.button == 1:
                leftclick = True  # when mouse is up after clicking
                # fill and polygon require adding to undo after their actions, picker doesn't draw
                if canvasRect.collidepoint(mx, my) and tool != 'picker' and tool != 'fill' and tool != 'polygon':
                    # copies only whats on the canvas
                    undos.append(screen.subsurface(canvasRect).copy())
                    # canCount = 1
                elif canvasRect.collidepoint(mx, my) == 0 and canCount == 1 and tool != 'picker' and tool != 'fill' and tool != 'polygon':
                    canCount = 0
                    undos.append(screen.subsurface(canvasRect).copy())
            if e.button == 3:
                rightclick = True  # for completing polygon

    mb = mouse.get_pressed()  # press

    draw.rect(screen, colour, (95, 530, 25, 25))  # colour display
    # colour display outline
    draw.rect(screen, (255, 255, 255), (95, 530, 25, 25), 2)

    screen.blit(remove, (9, 16))  # remove all icon
    draw.rect(screen, gray, removeRect, 3)

    rgb = myfont.render(str(colour), False, (255, 255, 255)
                        )  # displaying rgb values
    # adds black rect to allow rgb to change
    draw.rect(screen, (0), (0, 535, 95, 25))
    screen.blit(rgb, (0, 535))

    draw.rect(screen, gray, saveRect, 3)
    screen.blit(save, (8, 731))

    draw.rect(screen, gray, openRect, 3)
    screen.blit(openfile, (48, 731))

    draw.rect(screen, gray, undoRect, 3)
    screen.blit(undo, (42, 15))

    draw.rect(screen, gray, redoRect, 3)
    screen.blit(redo, (77, 15))

    if spectrum.get_rect(topleft=(4, 560)).collidepoint(mx, my):
        if mb[0] == 1:
            colour = screen.get_at((mx, my))  # rgba value of mouse location

    if tool != 'picker':  # for not highlighting at first
        draw.rect(screen, gray, pickerRect, 3)
        screen.blit(picker, (63, 116))
    if pickerRect.collidepoint(mx, my):
        draw.rect(screen, white, pickerRect, 3)
        screen.blit(pickerselect, (63, 116))
        if leftclick:
            tool = 'picker'  # highlights (this all repeats for all tools)

    if tool != 'sans':
        draw.rect(screen, gray, sansRect, 3)
        screen.blit(sans, (924, 100-40))
    if sansRect.collidepoint(mx, my):
        draw.rect(screen, white, sansRect, 3)
        screen.blit(sans, (924, 100-40))
        if leftclick:
            tool = 'sans'

    if tool != 'undyne':
        draw.rect(screen, gray, undyneRect, 3)
        screen.blit(undyne, (920, 225-40))
    if undyneRect.collidepoint(mx, my):
        draw.rect(screen, white, undyneRect, 3)
        screen.blit(undyne, (920, 225-40))
        if leftclick:
            tool = 'undyne'

    if tool != 'papyrus':
        draw.rect(screen, gray, papyrusRect, 3)
        screen.blit(papyrus, (928, 365-40))
    if papyrusRect.collidepoint(mx, my):
        draw.rect(screen, white, papyrusRect, 3)
        screen.blit(papyrus, (928, 365-40))
        if leftclick:
            tool = 'papyrus'

    if tool != 'frisk':
        draw.rect(screen, gray, friskRect, 3)
        screen.blit(frisk, (910, 445))
    if friskRect.collidepoint(mx, my):
        draw.rect(screen, white, friskRect, 3)
        screen.blit(frisk, (910, 445))
        if leftclick:
            tool = 'frisk'

    if tool != 'flowey':
        draw.rect(screen, gray, floweyRect, 3)
        screen.blit(flowey, (925, 585))
    if floweyRect.collidepoint(mx, my):
        draw.rect(screen, white, floweyRect, 3)
        screen.blit(flowey, (925, 585))
        if leftclick:
            tool = 'flowey'

    # --------------SIZE-----------------------------------------------------------------------------

    if tool == 'eraser' or tool == 'paint' or tool == 'line' or tool == 'unfrect' or tool == 'unfcirc' or tool == 'spray':  # only these tools change sizes
        if size != 4:
            draw.circle(screen, gray, (10, 700), 4)
        if sRect1.collidepoint(mx, my) or size == 4:
            draw.circle(screen, white, (10, 700), 4)
            if leftclick:
                size = 4

        if size != 7:
            draw.circle(screen, gray, (35, 700), 7)
        if sRect2.collidepoint(mx, my) or size == 7:
            draw.circle(screen, white, (35, 700), 7)
            if leftclick:
                size = 7

        if size != 10:
            draw.circle(screen, gray, (67, 700), 10)
        if sRect3.collidepoint(mx, my) or size == 10:
            draw.circle(screen, white, (67, 700), 10)
            if leftclick:
                size = 10

        if size != 13:
            draw.circle(screen, gray, (106, 700), 13)
        if sRect4.collidepoint(mx, my) or size == 13:
            draw.circle(screen, white, (106, 700), 13)
            if leftclick:
                size = 13

    # puts black areas over circles when other tools selected
    if tool != 'eraser' and tool != 'paint' and tool != 'line' and tool != 'unfrect' and tool != 'unfcirc' and tool != 'spray':
        draw.circle(screen, (0), (10, 700), 4)
        draw.circle(screen, (0), (35, 700), 7)
        draw.circle(screen, (0), (67, 700), 10)
        draw.circle(screen, (0), (106, 700), 13)
    # --------------SIZE----------------------------------------------------------------------------------------------------------------------------------------

    if tool != 'pencil':
        draw.rect(screen, gray, pencilRect, 3)
        screen.blit(pencil, (6, 54))
    if pencilRect.collidepoint(mx, my) or tool == 'pencil':
        draw.rect(screen, white, pencilRect, 3)
        screen.blit(pencilselect, (6, 54))
        if leftclick:
            tool = 'pencil'

    if tool != 'eraser':
        draw.rect(screen, gray, eraserRect, 3)
        screen.blit(eraser, (7, 119))
    if eraserRect.collidepoint(mx, my):
        draw.rect(screen, white, eraserRect, 3)
        screen.blit(eraserselect, (7, 119))
        if leftclick:
            tool = 'eraser'

    if tool != 'paint':
        draw.rect(screen, gray, paintRect, 3)
        screen.blit(paint, (69, 54))
    if paintRect.collidepoint(mx, my):
        draw.rect(screen, white, paintRect, 3)
        screen.blit(paintselect, (69, 54))
        if leftclick:
            tool = 'paint'

    if tool != 'line':
        draw.rect(screen, gray, lineRect, 3)
        draw.line(screen, gray, (13, 229), (49, 185), 8)
    if lineRect.collidepoint(mx, my):
        draw.rect(screen, white, lineRect, 3)
        draw.line(screen, white, (13, 229), (49, 185), 8)
        if leftclick:
            tool = 'line'

    if tool != 'unfrect':
        draw.rect(screen, gray, unfRect, 3)
        draw.rect(screen, gray, (69, 255, 42, 32), 3)
    if unfRect.collidepoint(mx, my):
        draw.rect(screen, white, unfRect, 3)
        draw.rect(screen, white, (69, 255, 42, 32), 3)
        if leftclick:
            tool = 'unfrect'

    if tool != 'frect':
        draw.rect(screen, gray, fRect, 3)
        draw.rect(screen, gray, (10, 255, 42, 32))
    if fRect.collidepoint(mx, my):
        draw.rect(screen, white, fRect, 3)
        draw.rect(screen, white, (10, 255, 42, 32))
        if leftclick:
            tool = 'frect'

    if tool != 'fcirc':
        draw.rect(screen, gray, fCirc, 3)
        draw.ellipse(screen, gray, (10, 314, 42, 42))
    if fCirc.collidepoint(mx, my):
        draw.rect(screen, white, fCirc, 3)
        draw.ellipse(screen, white, (10, 314, 42, 42))
        if leftclick:
            tool = 'fcirc'

    if tool != 'unfcirc':
        draw.rect(screen, gray, unfCirc, 3)
        draw.ellipse(screen, gray, (69, 314, 42, 42), 3)
    if unfCirc.collidepoint(mx, my):
        draw.rect(screen, white, unfCirc, 3)
        draw.ellipse(screen, white, (69, 314, 42, 42), 3)
        if leftclick:
            tool = 'unfcirc'

    if tool != 'polygon':
        draw.rect(screen, gray, polyRect, 3)
        screen.blit(polygon, (67, 184))
        del polypoints[:]
        del polyredos[:]
    if polyRect.collidepoint(mx, my):
        draw.rect(screen, white, polyRect, 3)
        screen.blit(polyselect, (67, 184))
        if leftclick:
            tool = 'polygon'

    if tool != 'spray':
        draw.rect(screen, gray, sprayRect, 3)
        screen.blit(spray, (4, 374))
    if sprayRect.collidepoint(mx, my):
        draw.rect(screen, white, sprayRect, 3)
        screen.blit(sprayselect, (4, 374))
        if leftclick:
            tool = 'spray'

    if tool != 'fill':
        draw.rect(screen, gray, fillRect, 3)
        screen.blit(fill, (56, 366))
    if fillRect.collidepoint(mx, my):
        draw.rect(screen, white, fillRect, 3)
        screen.blit(fillselect, (56, 366))
        if leftclick:
            tool = 'fill'

    if removeRect.collidepoint(mx, my):
        screen.blit(removeselect, (9, 16))
        draw.rect(screen, white, removeRect, 3)
        if leftclick:
            # makes canvas white (removes all)
            draw.rect(screen, (255, 255, 255), canvasRect)

    if saveRect.collidepoint(mx, my):
        draw.rect(screen, white, saveRect, 3)
        screen.blit(saveselect, (8, 731))
        if leftclick:
            result = asksaveasfilename()  # save prompt
            if result:  # only if result is entered (same for open tool)
                image.save(screen.subsurface(canvasRect), result)

    if openRect.collidepoint(mx, my):
        draw.rect(screen, white, openRect, 3)
        screen.blit(openfileselect, (48, 731))
        if leftclick:
            result = askopenfilename(
                filetypes=[("Picture files", "*.png;*.jpg")])
            if result:
                # adds image that was loaded
                screen.blit(image.load(result), (122, 51))

    if undoRect.collidepoint(mx, my):
        draw.rect(screen, white, undoRect, 3)
        screen.blit(undoselect, (42, 15))
        if leftclick:
            if len(undos) >= 2:  # the undos must be at or over 2 because it already starts at 1
                if len(polypoints) > 0:
                    # this is for continuing polygon when undoing
                    polyredos.append(polypoints[-1])
                    del polypoints[-1]
                # second last undo is blitted
                screen.blit(undos[-2], (122, 51))
                # need to add last undo to redo for reuse
                redos.append(undos[-1])
                del undos[-1]  # undo is in redo, so need to delete last one

    if redoRect.collidepoint(mx, my):
        draw.rect(screen, white, redoRect, 3)
        screen.blit(redoselect, (77, 15))
        if leftclick:
            if len(redos) >= 1:  # starts at 0, so should be at or over 1
                if len(polypoints) > 0:
                    # polygon can then be continued
                    polypoints.append(polyredos[-1])
                    del polyredos[-1]
                screen.blit(redos[-1], (122, 51))
                undos.append(redos[-1])  # same done to undo function
                del redos[-1]

    if len(redos) >= 1:  # this deletes all redos if the list has anything in it and you click
        if canvasRect.collidepoint(mx, my):
            if leftclick and tool != 'picker':
                del redos[:]
            # can only delete all redos if the polygon is closed by rightclicking
            if rightclick and tool == 'polygon' and len(polypoints >= 3):
                del redos[:]

# -----------------------------------DRAWING--------------------------------
    if canvasRect.collidepoint(mx, my):
        screen.set_clip(canvasRect)  # only draw on canvas
        if mb[0] == 1:
            canCount = 1
            if tool == 'picker':
                # rgba values of mouse location
                colour = screen.get_at((mx, my))

            if tool == 'pencil':
                if lastpos is not None:  # happens only when mouse button is down
                    draw.line(screen, colour, lastpos, (mx, my), 1)
                lastpos = mx, my  # old mouse location to stop dashed line

            if tool == 'eraser':
                if lastpos is not None:
                    # distance between last position and current
                    dist = sqrt((my-lastpos[1])**2+(mx-lastpos[0])**2)
                    distx = mx-lastpos[0]  # only distance between x's
                    disty = my-lastpos[1]  # only distance between y's
                    for i in range(int(dist)):
                        x = int(lastpos[0]+i/dist*distx)
                        y = int(lastpos[1]+i/dist*disty)
                        # creates circles between each position where they're missing
                        draw.circle(screen, white, (x, y), size)
                    draw.circle(screen, white, (mx, my),
                                size)  # initial circles
                lastpos = mx, my

            # ------------------STICKERS---------------------------------------------------------------------------

            if tool == 'sans':
                screen.blit(back, (0, 0))  # copy of the screen
                # sticker in center of cursor
                screen.blit(sans, (mx-sans.get_size()
                            [0]//2, my-sans.get_size()[1]//2))

            if tool == 'undyne':
                screen.blit(back, (0, 0))
                screen.blit(undyne, (mx-undyne.get_size()
                            [0]//2, my-undyne.get_size()[1]//2))

            if tool == 'papyrus':
                screen.blit(back, (0, 0))
                screen.blit(papyrus, (mx-papyrus.get_size()
                            [0]//2, my-papyrus.get_size()[1]//2))

            if tool == 'frisk':
                screen.blit(back, (0, 0))
                screen.blit(frisk, (mx-frisk.get_size()
                            [0]//2, my-frisk.get_size()[1]//2))

            if tool == 'flowey':
                screen.blit(back, (0, 0))
                screen.blit(flowey, (mx-flowey.get_size()
                            [0]//2, my-flowey.get_size()[1]//2))

            # ---------------------------------------------------------------------------------------------------

            if tool == 'paint':  # all functions same as eraser except there is colour
                if lastpos is not None:
                    dist = sqrt((my-lastpos[1])**2+(mx-lastpos[0])**2)
                    distx = mx-lastpos[0]
                    disty = my-lastpos[1]
                    for i in range(int(dist)):
                        x = int(lastpos[0]+i/dist*distx)
                        y = int(lastpos[1]+i/dist*disty)
                        draw.circle(screen, colour, (x, y), size)
                    draw.circle(screen, colour, (mx, my), size)
                lastpos = mx, my

            # same as eraser, though starting position (when first clicking) is instead used and screen is copied
            if tool == 'line':
                screen.blit(back, (0, 0))
                dist = sqrt((my-start[1])**2+(mx-start[0])**2)
                distx = mx-start[0]
                disty = my-start[1]
                for i in range(int(dist)):
                    x = int(start[0]+i/dist*distx)
                    y = int(start[1]+i/dist*disty)
                    draw.circle(screen, colour, (x, y), size)

            if tool == 'unfrect':
                screen.blit(back, (0, 0))
                # draw polygon is better because each point is specified
                draw.polygon(screen, colour, [
                             (start), (mx, start[1]), (mx, my), (start[0], my)], size)

            if tool == 'frect':
                screen.blit(back, (0, 0))
                draw.polygon(screen, colour, [
                             (start), (mx, start[1]), (mx, my), (start[0], my)])

            if tool == 'fcirc':
                screen.blit(back, (0, 0))
                # ellipse at start with width and height distance between mouse and start
                ellipseRect = Rect(start[0], start[1],
                                   mx-start[0], my-start[1])
                ellipseRect.normalize()  # corrects negative values
                draw.ellipse(screen, colour, ellipseRect)

            if tool == 'unfcirc':
                screen.blit(back, (0, 0))
                ellipseRect = Rect(start[0], start[1],
                                   mx-start[0], my-start[1])
                ellipseRect.normalize()
                if ellipseRect.height < size*2 or ellipseRect.width < size*2:
                    draw.ellipse(screen, colour, ellipseRect)
                else:
                    draw.ellipse(screen, colour, ellipseRect, size)

            if tool == 'spray':
                if lastpos is not None:
                    dist = sqrt((my-lastpos[1])**2+(mx-lastpos[0])**2)
                    distx = mx-lastpos[0]
                    disty = my-lastpos[1]
                    for i in range(int(dist)):
                        x = int(lastpos[0]+i/dist*distx)
                        y = int(lastpos[1]+i/dist*disty)
                        orx, ory = randint(
                            x-size, x+size), randint(y-size, y+size)
                        screen.set_at((orx, ory), colour)
                    randx, randy = randint(
                        mx-size, mx+size), randint(my-size, my+size)
                    if (mx-randx)**2+(my-randy)**2 <= size**2:
                        screen.set_at((randx, randy), colour)
                lastpos = mx, my

        if tool == 'polygon':
            if leftclick:
                polypoints.append((mx, my))
                if len(polypoints) > 1:
                    draw.line(screen, colour,
                              (polypoints[len(polypoints)-2]), (mx, my))
                    undos.append(screen.subsurface(canvasRect).copy())
            if rightclick:
                if len(polypoints) >= 3:
                    draw.line(screen, colour, (polypoints[-1]), polypoints[0])
                    undos.append(screen.subsurface(canvasRect).copy())
                    del polypoints[:]  # fix for undo and redo

        if tool == 'fill' and leftclick:
            theStack = [(mx, my)]
            oldColor = screen.get_at((mx, my))
            while screen.get_at((mx, my)) != colour:
                while len(theStack) > 0:
                    mx, my = theStack.pop()
                    if screen.get_at((mx, my)) != oldColor:
                        continue
                    screen.set_at((mx, my), colour)
                    theStack.append((mx + 1, my))  # right
                    theStack.append((mx - 1, my))  # left
                    theStack.append((mx, my + 1))  # down
                    theStack.append((mx, my - 1))  # up
                undos.append(screen.subsurface(canvasRect).copy())

        screen.set_clip(None)
    else:
        if tool == 'pencil' or tool == 'eraser' or tool == 'paint' or tool == 'spray':
            lastpos = None

# -----------------------------------DRAWING--------------------------------

    display.flip()


quit()
