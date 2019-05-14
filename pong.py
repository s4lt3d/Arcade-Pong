# -*- coding: utf-8 -*-
"""
Created on Mon May 13 23:28:06 2019
@author: walte
"""

import arcade
import numpy as np

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
SCREEN_TITLE = "Pong"

MOVEMENT_SPEED = 3


class Paddle(arcade.Sprite):
    def __init__(self, position_x, position_y, change_x, change_y, width, height, color):
        
        super().__init__()
        # Take the parameters of the init function above, and create instance variables out of them.
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.change_y = change_y
        self.width = width
        self.height = height
        self.color = color
        

    def draw(self):
        """ Draw the balls with the instance variables we have. """
        arcade.draw_rectangle_filled(self.position_x, self.position_y, self.width, self.height, self.color)
        
    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.change_x = MOVEMENT_SPEED
        elif key == arcade.key.UP:
            self.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.change_y = -MOVEMENT_SPEED
            
    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.change_x = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.change_y = 0

    def update(self):
        # Move the paddle
        self.position_y += self.change_y
        self.position_x += self.change_x

        self.position_x = np.clip(self.position_x, self.width/2, SCREEN_WIDTH - self.width/2)
        self.position_y = np.clip(self.position_y, self.height/2, SCREEN_HEIGHT - self.height/2)
        
class Ball:
    def __init__(self, position_x, position_y, change_x, change_y, radius, color):
        
        super().__init__()
        
        # Take the parameters of the init function above, and create instance variables out of them.
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.change_y = change_y
        self.radius = radius
        self.color = color

    def draw(self):
        """ Draw the balls with the instance variables we have. """
        arcade.draw_circle_filled(self.position_x, self.position_y, self.radius, self.color)

    def update(self):
        # Move the ball

        # See if the ball hit the edge of the screen. If so, change direction
        if self.position_x < self.radius:
            self.position_x = self.radius
            self.change_x *= -1

        if self.position_x > SCREEN_WIDTH - self.radius:
            self.position_x = SCREEN_WIDTH - self.radius
            self.change_x *= -1

        if self.position_y < self.radius:
            self.position_y = self.radius
            self.change_y *= -1

        if self.position_y > SCREEN_HEIGHT - self.radius:
            self.position_y = SCREEN_HEIGHT - self.radius
            self.change_y *= -1
            
        self.position_y += self.change_y
        self.position_x += self.change_x


class MyGame(arcade.Window):

    def __init__(self, width, height, title):

        # Call the parent class's init function
        super().__init__(width, height, title)

        # Make the mouse disappear when it is over the window.
        # So we just see our object, not the pointer.
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.ASH_GREY)

        # Create our ball
        self.ball = Ball(50, 50, 1, 1, 15, arcade.color.AUBURN)
        self.paddle = Paddle(100, 100, 0, 0, 15, 15, arcade.color.BLUE)

    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()
        self.ball.draw()
        self.paddle.draw()

    def update(self, delta_time):
        self.ball.update()
        self.paddle.update()

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        self.paddle.on_key_press(key, modifiers)
        

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        self.paddle.on_key_release(key, modifiers)


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
