import sys, pygame, random
import pygame.freetype


width, height = (500, 500)
black = (0,0,0)
white = (255, 255, 255)
green = (0,255,0)
brown = (210, 105, 30)


class Ball(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface([20,20])
        self.image.fill(green)
        self.rect = self.image.get_rect()

        self.pos = pos
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        self.grav = 5 # Gravity
        self.lift  = -40 # Force applied to rect when jumping
        self.vel = [0, 0] # x, y
    
    # Translate position into rectangle position
    def render(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def update(self):
        # Vertical movement
        self.vel[1] -= self.grav * 0.95
        self.pos[1] -= self.vel[1]

        # Horizontal movement
        self.pos[0] -= self.vel[0]
        self.vel[0] *=  0.8 # De accelerate horizontal movement

        # Limit horizontal acceleration
        if abs(self.vel[0]) > 15:
            if self.vel[0] < 0:
                self.vel[0] == -15
            elif self.vel[0] > 0:
                self.vel[0] == 15

        # Limit veritcal movement
        if abs(self.vel[1]) > 15:
            if self.vel[1] < 0:
                self.vel[1] == -15
                

        # Bounds
        if not player_has_jumped:
            if self.pos[1] > 400 - 20:
                    self.vel[1] = 0  
                    self.pos[1] = 400 - 20
        
        
        if self.pos[0] < 0: 
            self.pos[0] = 0
        elif self.pos[0] > width - 20:
            self.pos[0] = width - 20

    # Basic movements controls
    def jump(self):
        #self.pos[1] -= 20
        self.vel[1] -= self.lift


    def move_left(self):
        self.vel[0] += 5
    
    def move_right(self): 
        self.vel[0] -= 5

    def check_for_gameover(self):
        if self.rect.y  > 500:
            return True

class Boards(pygame.sprite.Sprite):
    board_height = 8
    def __init__(self, pos_y):
        super().__init__()
        self.length = random.randint(75, 150)
        self.image = pygame.Surface((self.length, Boards.board_height))
        self.image.fill(brown)
        self.rect = self.image.get_rect()

        self.y_gap = pos_y
        self.x = int(random.randrange(0, width-self.length)) 
        self.y = pos_y

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y - self.y_gap - 10 # Minus 10 just generate out of picture

    def move(self):
        self.y += game_speed

def main():
    
    screen = pygame.display.set_mode((width, height))

    pygame.freetype.init()
    game_font = pygame.freetype.SysFont("Arial", 24)
    all_sprites_list = pygame.sprite.Group()
    board_sprites_list = pygame.sprite.Group()
    Clock = pygame.time.Clock()

    ball = Ball([width/2, 400 - 20])
    
    all_sprites_list.add(ball)
    
    board_height_counter = 1
    global player_has_jumped
    global game_speed
    game_speed = 2
    game_score = 0

    player_has_jumped = False

    # Game loop
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                   ball.jump()
                   player_has_jumped = True
                   game_score += 1

        # Smooth movement left and right
        if pygame.key.get_pressed()[97]:
            ball.move_left()
        elif pygame.key.get_pressed()[100]:
            ball.move_right()
        
        
        screen.fill(white) # Draw white background

        all_sprites_list.draw(screen)
        
        ball.update()
        ball.render()

        if ball.check_for_gameover():
            game_speed = 0
            board_sprites_list.empty()
            game_font.render_to(screen, (200, 250), 'GAME OVER!')


        if not player_has_jumped:
            pygame.draw.line(screen, black, (0, 400), (width, 400)) # Base line

        # Generate random boards 
        if board_height_counter > 0:
            y = random.randrange(100,120,3)
            board_sprites_list.add(Boards(y))
            board_height_counter -= y 

        board_sprites_list.draw(screen)
        board_sprites_list.update()

        # Collioson detection between player and boards
        for board in board_sprites_list:
            board.move()
            if pygame.sprite.collide_rect(ball, board):
                ball.pos[1] = board.rect.y - 17
                ball.vel[1] = 0                    
            

        board_height_counter += game_speed
        
        game_font.render_to(screen, (400, 450), 'Score: ' + str(game_score))

        pygame.display.flip()

        Clock.tick(30)


if __name__ == '__main__':
    main()