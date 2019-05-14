# -*- coding: utf-8 -*-
"""
Created on Mon May 13 23:28:06 2019
@author: walter
"""
import arcade
import numpy as np

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
SCREEN_TITLE = "Pong"

MOVEMENT_SPEED = 2
PADDLE_MOVEMENT_SPEED = 1.25


PLAYER1_UP = arcade.key.W
PLAYER1_DOWN = arcade.key.S


PLAYER2_UP = arcade.key.UP
PLAYER2_DOWN = arcade.key.DOWN


class Paddle:
    def __init__(self, position_x, position_y, change_x, change_y, width, height, color, player_number = 1):

        # Take the parameters of the init function above, and create instance variables out of them.
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.change_y = change_y
        self.width = width
        self.height = height
        self.color = color
        self.player_number = player_number
        self.collision = False
        
        if player_number == 1:
            self.up_key = PLAYER1_UP
            self.down_key = PLAYER1_DOWN
        else:
            self.up_key = PLAYER2_UP
            self.down_key = PLAYER2_DOWN
        
    def draw(self):
        """ Draw the balls with the instance variables we have. """
        arcade.draw_rectangle_filled(self.position_x, self.position_y, self.width, self.height, self.color)
        
    def on_key_press(self, key, modifiers):

        if key == self.up_key:
            self.change_y = PADDLE_MOVEMENT_SPEED
        elif key == self.down_key:
            self.change_y = -PADDLE_MOVEMENT_SPEED
            
    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        if key == self.up_key or key == self.down_key:
            self.change_y = 0

    def update(self):
        # Move the paddle
        self.position_y += self.change_y
        self.position_x += self.change_x

        self.position_x = np.clip(self.position_x, self.width/2, SCREEN_WIDTH - self.width/2)
        self.position_y = np.clip(self.position_y, self.height/2, SCREEN_HEIGHT - self.height/2)
        
        self.top_right_y = self.position_y + self.height/2
        self.top_right_x = self.position_x + self.width/2
        self.bottom_left_x = self.position_x - self.width/2
        self.bottom_left_y = self.position_y - self.height/2
        
class Ball:
   
    def __init__(self, position_x, position_y, change_x, change_y, width, color):

        # Take the parameters of the init function above, and create instance variables out of them.
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.change_y = change_y
        self.width = width
        self.color = color
        self.collision = False
        self.other_collider = None

    def draw(self):
        """ Draw the balls with the instance variables we have. """
        arcade.draw_rectangle_filled(self.position_x, self.position_y, self.width, self.width, self.color)

    def update(self):
        # Move the ball

        # See if the ball hit the edge of the screen. If so, change direction
            
        if self.position_x < self.width/2:
            self.position_x = self.width/2
            self.change_x *= -1
            MyGame.game_over(1)

        if self.position_x > SCREEN_WIDTH - self.width/2:
            self.position_x = SCREEN_WIDTH - self.width/2
            self.change_x *= -1
            MyGame.game_over(2)

        if self.position_y < self.width/2:
            self.position_y = self.width/2
            self.change_y *= -1

        if self.position_y > SCREEN_HEIGHT - self.width/2:
            self.position_y = SCREEN_HEIGHT - self.width/2
            self.change_y *= -1
            
        self.position_y += MOVEMENT_SPEED * self.change_y
        self.position_x += MOVEMENT_SPEED * self.change_x
        
        self.top_right_y = self.position_y + self.width/2
        self.top_right_x = self.position_x + self.width/2
        self.bottom_left_x = self.position_x - self.width/2
        self.bottom_left_y = self.position_y - self.width/2
        
    def check_collision(self, other):
        
        self.collision = not (self.top_right_x < other.bottom_left_x or 
                               self.bottom_left_x > other.top_right_x or 
                               self.top_right_y < other.bottom_left_y or 
                               self.bottom_left_y > other.top_right_y)
        
        if self.collision == True:
            if self.other_collider is None:
                self.change_x *= -1
            self.other_collider = other
        else:
            if self.other_collider == other:
                self.other_collider = None
                
        return self.collision

class MyGame(arcade.Window):
    player1_score = 0
    player2_score = 0
    start_new_round = False
    
    def __init__(self, width, height, title):
        # Call the parent class's init function
        super().__init__(width, height, title)

        # Make the mouse disappear when it is over the window.
        # So we just see our object, not the pointer.
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.ASH_GREY)
        
        MyGame.player1_score = 0
        MyGame.player2_score = 0
        
        self.new_round()
    
    @staticmethod
    def game_over(winner):
        if winner == 1:
            MyGame.player1_score = MyGame.player1_score + 1
        else:
            MyGame.player2_score = MyGame.player2_score + 1
        MyGame.start_new_round = True
        
    def new_round(self):
        MyGame.start_new_round = False
        
        self.ball = Ball(SCREEN_WIDTH/2 + np.random.choice([-10,0,10]), 
                         SCREEN_HEIGHT/2 + + np.random.choice([-10,0,10]), 
                         np.random.choice([-1,1]), 
                         np.random.choice([-1,1]), 
                         16, 
                         arcade.color.WHITE)
        self.paddle1 = Paddle(8, 120, 0, 0, 16, 48, arcade.color.BLUE, 1)
        self.paddle2 = Paddle(SCREEN_WIDTH - 8, 120, 0, 0, 16, 48, arcade.color.RED, 2)

    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()
        self.ball.draw()
        self.paddle1.draw()
        self.paddle2.draw()
        self.ball.check_collision(self.paddle1)
        self.ball.check_collision(self.paddle2)
        
        arcade.draw_text(str(MyGame.player1_score), 10, SCREEN_HEIGHT-25, color=arcade.color.WHITE, font_name="COURIER NEW", font_size=20)
        arcade.draw_text(str(MyGame.player2_score), SCREEN_WIDTH - 50, SCREEN_HEIGHT-25, color=arcade.color.WHITE, font_name="COURIER NEW", font_size=20)
        
    def update(self, delta_time):
        if MyGame.start_new_round == True:
            self.new_round()
            
        self.ball.update()
        self.paddle1.update()
        self.paddle2.update()

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        self.paddle1.on_key_press(key, modifiers)
        self.paddle2.on_key_press(key, modifiers)
        

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        self.paddle1.on_key_release(key, modifiers)
        self.paddle2.on_key_release(key, modifiers)


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
