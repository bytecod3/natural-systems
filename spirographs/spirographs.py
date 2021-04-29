import argparse
from datetime import datetime
import random
import turtle
from math import *
from PIL import Image


class Spiro:
    # constructor
    def __init__(self, xc, yc, col, R, r, l):
        self.t = turtle.Turtle()    # create a turtle object
        self.t.shape('turtle')  # set the cursor shape
        self.step = 5  # set the step in degrees
        self.drawingComplete = False  # set the drawing complete flag

        self.setparams(xc, yc, col, R, r, l)  # set the parameters
        self.restart()

    def setparams(self, xc, yc, col, R, r, l):
        # the spirograph parameters
        self.xc = xc
        self.yc = yc
        self.col = col
        self.R = int(R)
        self.r = int(r)
        self.l = l

        gcdVal = gcd(self.r, self.R) # reduce r/R to the smallest fraction
        self.nRot = self.r//gcdVal
        self.k = r/float(R)  # get the ratio of the radii
        self.t.color(*col)  # set the color
        self.a = 0  # store the current angle

    def restart(self):
        # restart the drawing
        self.drawingComplete = False
        self.t.showturtle()  # show turtle
        self.t.up()  # go to the first point
        R, k, l = self.R, self.k, self.l
        a = 0.0
        x = R * ((1-k) * cos(a) + l * k * cos(((1-k) / k) * a))
        y = R * ((1-k) * sin(a) - l * k * sin(((1-k) / k) * a))

        self.t.setpos(self.xc + x, self.yc + y)
        self.t.down()

    def draw(self):
        # draw the rest of the points
        R, k, l = self.R, self.k, self.l
        for i in range(0, 360*self.nRot + 1, self.step):
            a = radians(i)
            x = R * ((1 - k) * cos(a) + l * k * cos(((1 - k) / k) * a))
            y = R * ((1 - k) * sin(a) - l * k * sin(((1 - k) / k) * a))
            self.t.setpos(self.xc + x, self.yc + y)

        self.t.hideturtle()  # drawing is done so hide the cursor

    def update(self):
        if self.drawingComplete: return # skip the rest of the code if drawing done

        self.a += self.step # increment th angle
        R, k, l = self.R, self.k, self.l  # draw a step
        a = radians(self.a)  # set the angle
        x = R * ((1 - k) * cos(a) + l * k * cos(((1 - k) / k) * a))
        y = R * ((1 - k) * sin(a) - l * k * sin(((1 - k) / k) * a))
        self.t.setpos(self.xc + x, self.yc + y)

        if self.a > 360*self.nRot:
            self.drawingComplete = True  # update the flag if drawing is complete
            self.t.hideturtle()

    def clear(self):
        # clear everything
        self.t.clear()


class SpiroAnimator:
    # class for animating spiros
    def __init__(self, N):
        self.deltaT = 10  # set the timer in milliseconds
        self.width = turtle.window_width()
        self.height = turtle.window_height()

        # create the spiro objects
        self.spiros = []

        for i in range(N):
            rparams = self.genRandomParams()  # generate random parameters
            spiro = Spiro(*rparams)
            self.spiros.append(spiro)

        # call timer
        turtle.ontimer(self.update, self.deltaT)

    def genRandomParams(self):
        width, height = self.width, self.height
        R = random.randint(50, min(width, height)//2)
        r = random.randint(10, 9*R//10)
        l = random.uniform(0.1, 0.9)
        xc = random.randint(-width//2, width//2)
        yc = random.randint(-height//2, height//2)

        col = (
            random.random(),
            random.random(),
            random.random()
        )

        return (xc, yc, col, R, r, l)

    def restart(self):
        # restart spiro drawing
        for spiro in self.spiros:
            spiro.clear()  # clear
            rparams = self.genRandomParams()  # generate random parameters
            spiro.setparams(*rparams)
            spiro.restart()  # restart spiro

    def update(self):
        # update all spiros
        nComplete = 0
        for spiro in self.spiros:
            # update
            spiro.update()
            if spiro.drawingComplete:  # count completed spiros
                nComplete += 1

        if nComplete == len(self.spiros):  # restart is all spiros are complete
            self.restart()

        turtle.ontimer(self.update, self.deltaT)

    def toggleTurtles(self):
        # toggle turtle cursor on or off
        for spiro in self.spiros:
            if spiro.t.isvisible():
                spiro.t.hideturtle()
            else:
                spiro.t.showturtle()


# save drawings as PNG files
def saveDrawing():
    turtle.hideturtle()  # hide turtle cursor
    dateStr = (datetime.now()).strftime("%d%b%Y-%H%M%S")
    filename = 'spiro-' + dateStr
    print('Saving drawing to %s.eps/png' % filename)

    canvas = turtle.getcanvas()  # get the tkinter canvas
    canvas.postscript(file = filename + '.eps')  # save image as postscript image

    # use Pillow module to convert image to png
    img = Image.open(filename + '.eps')
    img.save(filename + '.png', 'png')

    turtle.showturtle()

def main():
    # use sys.argv if needed
    print('Generating spirographs...')

    # create parser
    descStr = """This program draws Spirographs using the turtle module. If no arguments are passed, the program draws 
                random spirographs.
                
                Terminology:
                R -> radius of outer circle
                r -> radius of inner circle
                l -> ratio of hole distance to r
            """

    parser = argparse.ArgumentParser(description= descStr)

    # add expected arguments
    parser.add_argument('--sparams', nargs=3, dest='sparams', required=False, help='The three arguments in sparams: '
                                                                                   'R, r, l')
    args = parser.parse_args()  # parse args
    turtle.shape('turtle')  # set the cursor shape to turtle
    # turtle.title("Spirographs")
    turtle.onkey(saveDrawing, 's')
    turtle.listen()  # start listening
    turtle.hideturtle()  # hide the main cursor

    # check for any parameters sent to --sparams and draw the spirograph
    if args.sparams:
        params = [float(x) for x in args.sparams]
        # draw the spirograph with the given parameters
        col = (0.0, 0.0, 0.0)
        spiro = Spiro(0, 0, col, *params)
        spiro.draw()
    else:
        spiroAnim = SpiroAnimator(4)    # create an animator object
        turtle.onkey(spiroAnim.toggleTurtles, "t")
        turtle.onkey(spiroAnim.restart, "space")  # add a key handler to restart the animation

    # start the turtle mainloop
    turtle.mainloop()


if __name__ == '__main__':
    main()










