"""
Remake of the veritcal stack demo from the box2d testbed.
"""

from world import World
from world_constants import WorldConstants

import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse

import pymunk
from pymunk import Vec2d
import pymunk.pyglet_util

class Main(pyglet.window.Window):
    def __init__(self):
        pyglet.window.Window.__init__(self, width=600, height=600, vsync=False)
        self.set_caption('Vertical stack from box2d')


        wc = WorldConstants()
        self.world = World(wc)

        pyglet.clock.schedule_interval(self.update, 1/600.0)
        self.fps_display = pyglet.clock.ClockDisplay()

        self.text = pyglet.text.Label('Press space to fire bullet',
                          font_size=10,
                          x=10, y=400)

    def update(self,dt):
        self.world.update()


    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            pyglet.app.exit()
        elif symbol == key.UP:
            direction = Vec2d(1, 0).rotated(self.me.angle)
            self.me.apply_impulse(direction*1000, (0, 0))
        elif symbol == key.LEFT:
            self.me.angle += 0.3
        elif symbol == key.RIGHT:
            self.me.angle -= 0.3
        elif symbol == pyglet.window.key.P:
            pass


    def on_draw(self):
        self.clear()
        self.text.draw()
        self.fps_display.draw()
        pymunk.pyglet_util.draw(self.world.space)

if __name__ == '__main__':
    main = Main()
    pyglet.app.run()