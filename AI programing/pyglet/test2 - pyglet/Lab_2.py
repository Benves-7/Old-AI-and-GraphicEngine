import pyglet
from JsonLoader import *

JsonLoader.LoadInJson()

window = pyglet.window.Window(JsonLoader.Data["windowspecs"]["width"], JsonLoader.Data["windowspecs"]["height"])

def Update(*args):
	print("hi.")



@window.event
def on_click():
    print("ops")


pyglet.clock.schedule_interval(Update, 1/60)
pyglet.app.run()
