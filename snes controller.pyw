import pyglet
from pyglet import shapes
from inputs import *
import multiprocessing
import psutil
import os
import platform
import time

# os specific settings, like dpi awareness and low priority
operatings = platform.system()
lowpriority = 0
if operatings == "Windows":
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
    lowpriority = psutil.IDLE_PRIORITY_CLASS
if operatings == "Linux" or operatings == "Darwin":
    lowpriority = 19

if __name__ == "__main__":
    print(operatings)
    config = pyglet.gl.Config(sample_buffers=1, samples=8)
    window = pyglet.window.Window(config=config)
    window.set_size(350,150)
    manager = multiprocessing.Manager()
    v = list()
    for i in range(12):
        v.append(manager.Value("i",0))
    A,B,X,Y,U,D,L,R,l,r,S,s = v

batch = pyglet.graphics.Batch()

opacities = [128,255]
normal_buttons = (84,88,90)
AB = (81,70,137)
XY = (167,164,224)
shoulder = (178,180,178)



def update(dt):
    global A,B,X,Y,U,D,L,R,l,r,S,s
    ok = list()

    #d-pad
    ok.append(shapes.Rectangle(40,0,40,40,color=normal_buttons,batch=batch))
    ok[-1].opacity = opacities[D.value]
    ok.append(shapes.Rectangle(0,40,40,40,color=normal_buttons,batch=batch))
    ok[-1].opacity = opacities[L.value]
    ok.append(shapes.Rectangle(40,80,40,40,color=normal_buttons,batch=batch))
    ok[-1].opacity = opacities[U.value]
    ok.append(shapes.Rectangle(80,40,40,40,color=normal_buttons,batch=batch))
    ok[-1].opacity = opacities[R.value]
    ok.append(shapes.Rectangle(40,40,40,40,color=normal_buttons,batch=batch))
    ok[-1].opacity = opacities[False]

    #abxy
    ok.append(shapes.Circle(290,20,20,segments=40,color=AB,batch=batch))
    ok[-1].opacity = opacities[B.value]
    ok.append(shapes.Circle(330,60,20,segments=40,color=AB,batch=batch))
    ok[-1].opacity = opacities[A.value]
    ok.append(shapes.Circle(250,60,20,segments=40,color=XY,batch=batch))
    ok[-1].opacity = opacities[Y.value]
    ok.append(shapes.Circle(290,100,20,segments=40,color=XY,batch=batch))
    ok[-1].opacity = opacities[X.value]

    ok.append(shapes.Rectangle(0,140,60,10,color=shoulder,batch=batch))
    ok[-1].opacity = opacities[l.value]
    ok.append(shapes.Rectangle(290,140,60,10,color=shoulder,batch=batch))
    ok[-1].opacity = opacities[r.value]

    ok.append(shapes.Rectangle(140,55,20,10,color=normal_buttons,batch=batch))
    ok[-1].opacity = opacities[s.value]
    ok.append(shapes.Rectangle(190,55,20,10,color=normal_buttons,batch=batch))
    ok[-1].opacity = opacities[S.value]

    window.clear()
    batch.draw()

def updatecontrols(A,B,X,Y,U,D,L,R,l,r,S,s):
    pid = psutil.Process(os.getpid())
    pid.nice(lowpriority)
    while True:
        a = get_gamepad()
        for event in a:
            if event.code == "ABS_HAT0X":
                if event.state == 1:
                    R.value = 1
                    L.value = 0
                elif event.state == -1:
                    R.value = 0
                    L.value = 1
                else:
                    R.value = 0
                    L.value = 0
            elif event.code == "ABS_HAT0Y":
                if event.state == 1:
                    D.value = 1
                    U.value = 0
                elif event.state == -1:
                    D.value = 0
                    U.value = 1
                else:
                    D.value = 0
                    U.value = 0
            elif event.code == "BTN_SOUTH":
                B.value = event.state
            elif event.code == "BTN_EAST":
                A.value = event.state
            elif event.code == "BTN_WEST":
                Y.value = event.state
            elif event.code == "BTN_NORTH":
                X.value = event.state
            elif event.code == "BTN_TL":
                l.value = event.state
            elif event.code == "BTN_TR":
                r.value = event.state
            elif event.code == "BTN_START":
                s.value = event.state
            elif event.code == "BTN_SELECT":
                S.value = event.state


if __name__ == "__main__":
    pid = psutil.Process(os.getpid())
    pid.nice(lowpriority)
    c = multiprocessing.Process(target=updatecontrols,daemon=True,args=(A,B,X,Y,U,D,L,R,l,r,S,s))
    c.start()
    @window.event
    def on_draw():
        pass


    pyglet.clock.schedule_interval(update,1/60.0)

    pyglet.app.run()