import pyglet
from pyglet import shapes
from inputs import *
import threading
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

print(devices.gamepads)

if __name__ == "__main__":
    config = pyglet.gl.Config(sample_buffers=1, samples=8)
    window = pyglet.window.Window(config=config)
    window.set_size(350,150)

batch = pyglet.graphics.Batch()

opacities = [128,255]
normal_buttons = (84,88,90)
AB = (81,70,137)
XY = (167,164,224)
shoulder = (178,180,178)

A,B,X,Y,U,D,L,R,l,r,S,s = [0]*12

def update(dt):
    global A,B,X,Y,U,D,L,R,l,r,S,s
    ok = list()

    #d-pad
    ok.append(shapes.Rectangle(40,0,40,40,color=normal_buttons,batch=batch))
    ok[-1].opacity = opacities[D]
    ok.append(shapes.Rectangle(0,40,40,40,color=normal_buttons,batch=batch))
    ok[-1].opacity = opacities[L]
    ok.append(shapes.Rectangle(40,80,40,40,color=normal_buttons,batch=batch))
    ok[-1].opacity = opacities[U]
    ok.append(shapes.Rectangle(80,40,40,40,color=normal_buttons,batch=batch))
    ok[-1].opacity = opacities[R]
    ok.append(shapes.Rectangle(40,40,40,40,color=normal_buttons,batch=batch))
    ok[-1].opacity = opacities[False]

    #abxy
    ok.append(shapes.Circle(290,20,20,segments=40,color=AB,batch=batch))
    ok[-1].opacity = opacities[B]
    ok.append(shapes.Circle(330,60,20,segments=40,color=AB,batch=batch))
    ok[-1].opacity = opacities[A]
    ok.append(shapes.Circle(250,60,20,segments=40,color=XY,batch=batch))
    ok[-1].opacity = opacities[Y]
    ok.append(shapes.Circle(290,100,20,segments=40,color=XY,batch=batch))
    ok[-1].opacity = opacities[X]

    ok.append(shapes.Rectangle(0,140,60,10,color=shoulder,batch=batch))
    ok[-1].opacity = opacities[l]
    ok.append(shapes.Rectangle(290,140,60,10,color=shoulder,batch=batch))
    ok[-1].opacity = opacities[r]

    ok.append(shapes.Rectangle(140,55,20,10,color=normal_buttons,batch=batch))
    ok[-1].opacity = opacities[s]
    ok.append(shapes.Rectangle(190,55,20,10,color=normal_buttons,batch=batch))
    ok[-1].opacity = opacities[S]

    window.clear()
    batch.draw()

def updatecontrols():
    global A,B,X,Y,U,D,L,R,l,r,S,s
    while True:
        a = get_gamepad()
        for event in a:
            if event.code == "ABS_HAT0X":
                if event.state == 1:
                    R = 1
                    L = 0
                elif event.state == -1:
                    R = 0
                    L = 1
                else:
                    R = 0
                    L = 0
            elif event.code == "ABS_HAT0Y":
                if event.state == 1:
                    D = 1
                    U = 0
                elif event.state == -1:
                    D = 0
                    U = 1
                else:
                    D = 0
                    U = 0
            elif event.code == "BTN_SOUTH":
                B = event.state
            elif event.code == "BTN_EAST":
                A = event.state
            elif event.code == "BTN_WEST":
                Y = event.state
            elif event.code == "BTN_NORTH":
                X = event.state
            elif event.code == "BTN_TL":
                l = event.state
            elif event.code == "BTN_TR":
                r = event.state
            elif event.code == "BTN_START":
                s = event.state
            elif event.code == "BTN_SELECT":
                S = event.state

@window.event
def on_draw():
    pass

if __name__ == "__main__":
    c = threading.Thread(target=updatecontrols)
    c.daemon = True
    c.start()

    pyglet.clock.schedule_interval(update,1/60.0)

    pyglet.app.run()