# pong
# ball spawns in middle and bounces off each players paddle 
# a point is awarded if the ball touches the other players wall behind the paddle
# game ends at 11 points
# 'w' and 's' are used as up and down for player 1
# 'i' and 'k' are used as up and down for player 2

# I used the pygame library as well knowledge that I learned in class to complete this project

import pygame



def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((1000, 700))
   # set the title of the display window
   pygame.display.set_caption('Pong')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit() 




class Game:
   # An object in this class represents a complete game.

   def __init__(self, surface):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object

      # === objects that are part of every game that we will discuss
      self.surface = surface
      self.bg_color = pygame.Color('black')
      
      self.FPS = 80
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      
      # === game specific objects
      self.ball = Ball('white', 10, [500, 350], [4, 2], self.surface)
      
      self.paddle_1 = Paddle('white', [150, 350], 10, 80, 5, self.surface)
      self.player1_score = 0
      self.paddle_2 = Paddle('white', [850, 350], 10, 80, 5, self.surface)
      self.player2_score = 0
      
      
      self.p1_up = False
      self.p1_down = False
      self.p2_up = False
      self.p2_down = False      
      
      
   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.

      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()
         self.draw() 
                 
         if self.continue_game:
            self.update()
            
         self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled
      
      
      
      
      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
         elif event.type == pygame.KEYDOWN:
            
               if event.key == pygame.K_w:
                  self.p1_up = True
               elif event.key == pygame.K_s:
                  self.p1_down = True
               elif event.key == pygame.K_i:
                  self.p2_up = True
               elif event.key == pygame.K_k:
                  self.p2_down = True
                  
         elif event.type == pygame.KEYUP:
            
            if event.key == pygame.K_w:
               self.p1_up = False
            elif event.key == pygame.K_s:
               self.p1_down = False
            elif event.key == pygame.K_i:
               self.p2_up = False
            elif event.key == pygame.K_k:
               self.p2_down = False                  
               
     

   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      
      self.surface.fill(self.bg_color) # clear the display surface first
      self.ball.draw()
      self.paddle_1.draw()
      self.paddle_2.draw()
      self.draw_score()
      pygame.display.update() # make the updated surface appear on the display

   def update(self):
      # Update the game objects for the next frame.
      # - self is the Game to update
           
      self.ball.move()
      # moves paddles up and down
      if self.p1_up:
         self.paddle_1.move_up()
      if self.p1_down:
         self.paddle_1.move_down()
      if self.p2_up:
         self.paddle_2.move_up()
      if self.p2_down:
         self.paddle_2.move_down() 
       # bounces the ball off of the paddles 
      if self.ball.velocity[0] < 0:
         self.paddle_1.collide_ball(self.ball)
      elif self.ball.velocity[0] > 0:
         self.paddle_2.collide_ball(self.ball)
      # updates the games score
      self.update_score()
      # determines if a player is at 11 points and ends the game
      self.game_over()

   def draw_score(self):
         # draws each players score in each respective corner
         player1_score = str(self.player1_score)
         player2_score = str(self.player2_score)
         font_size = 100
         fg_color = pygame.Color('white') 
         
         
         
         font = pygame.font.SysFont('',font_size) # SysFont is a function
         
         player1_text_box = font.render(player1_score,True,fg_color,None)
         player2_text_box = font.render(player2_score,True,fg_color,None)
         
         screen_width = self.surface.get_width()
         box_width = player2_text_box.get_width()
         location = screen_width - box_width
         self.surface.blit(player1_text_box,(0,0))
         self.surface.blit(player2_text_box,(location,0))
   
   
   def update_score(self):
      # increases the each plyers score when they win a point
      
      if self.ball.center[0] < self.ball.radius:
         self.player2_score += 1
      elif self.ball.center[0] + self.ball.radius > 1000:
         self.player1_score += 1
      
   def game_over(self):
      # stops the game if a player reaches 11 points
      if self.player1_score == 11 or self.player2_score == 11:
         self.continue_game = False
   
      
class Ball:
   # An object in this class represents a Dot that moves 
   
   def __init__(self, ball_color, ball_radius, ball_center, ball_velocity, surface):
      # Initialize a ball.
      # - self is the ball to initialize
      # - color is the pygame.Color of the ball
      # - center is a list containing the x and y int
      #   coords of the center of the ball
      # - radius is the int pixel radius of the ball
      # - velocity is a list containing the x and y components
      # - surface is the window's pygame.Surface object

      self.color = pygame.Color(ball_color)
      self.radius = ball_radius
      self.center = ball_center
      self.velocity = ball_velocity
      self.surface = surface
      
   def move(self):
      # Change the location of the ball by adding the corresponding 
      # speed values to the x and y coordinate of its center
      # - self is the ball
      size = self.surface.get_size()
      for i in range(0,2):
         self.center[i] = (self.center[i] + self.velocity[i])
         if self.center[i] < self.radius or self.center[i] + self.radius > size[i]:
            # we need to do something --- > bounce off the edges of the window
            self.velocity[i] = -self.velocity[i]
            
   
   def draw(self):
      # Draw the ball on the surface
      # - self is the ball
      
      pygame.draw.circle(self.surface, self.color, self.center, self.radius)

class Paddle:
   # an object in this class represents a paddle
   
   def __init__(self, paddle_color, top_left, width, hight, paddle_velocity, surface):
      # Initialie a paddle
      
      self.color = pygame.Color(paddle_color)
      self.top_left = top_left
      self.width = width
      self.hight = hight
      self.surface = surface
      self.velocity = paddle_velocity
      
      self.paddle = pygame.Rect(self.top_left[0], self.top_left[1], self.width, self.hight)
   
   def draw(self):
      # draw the paddle on the surface
      # self is paddle
      
      pygame.draw.rect(self.surface, self.color, self.paddle)
      
   def move_up(self):
      # moves the paddles up based on the key input from player
      # and stops the paddle if its going too high
      if self.paddle.top > 0:
         self.paddle.top = self.paddle.top - self.velocity
         
   def move_down(self):
      # moves the paddle down based 
      # and stops if paddle goes too low
      if self.paddle.top < 700 - self.hight:
         self.paddle.top = self.paddle.top + self.velocity
      

   def collide_ball(self, ball):
      # determines if the ball is bouncing off the paddles
      if self.paddle.collidepoint(ball.center):
         ball.velocity[0] = -ball.velocity[0]
      
   
   
   

   
main()