import pygame
import os

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900,500
WIN= pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Clash")

HEALTH_FONT = pygame.font.SysFont('Calisto MT', 40)
WINNER_FONT = pygame.font.SysFont('Copperplate Gothic Bold', 50)

WHITE = (255, 255, 255)
BLACK=(0, 0 ,0)
RED_C=(255, 0, 0)
YELLOW_C=(255, 255 ,0)
FPS = 60
VEL = 5
BULLET_VEL = 8
MAX_BULLET = 3
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2 
BORDER = pygame.Rect(WIDTH//2-5, 0 , 10, HEIGHT)
SPACESHIP_WIDTH , SPACESHIP_HEIGHT = 60 ,40
YELLOW = pygame.image.load(os.path.join('spaceship_yellow.png'))
SPACESHIP1 = pygame.transform.rotate(pygame.transform.scale(YELLOW, (SPACESHIP_WIDTH ,SPACESHIP_HEIGHT)) , 90)
RED = pygame.image.load(os.path.join('spaceship_red.png'))
SPACESHIP2 = pygame.transform.rotate(pygame.transform.scale(RED, (SPACESHIP_WIDTH ,SPACESHIP_HEIGHT)) , 270)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('space1.jpg')) , (WIDTH, HEIGHT))
BULLET_HIT = pygame.mixer.Sound(os.path.join('Grenade+1.mp3'))
BULLET_SHOOT = pygame.mixer.Sound(os.path.join('Gun+Silencer.mp3'))
WINNING = pygame.mixer.Sound(os.path.join('winning.wav'))
BG = pygame.transform.scale(pygame.image.load(os.path.join('BG.png')), (200, 100))
BG_MUSIC= pygame.mixer.Sound(os.path.join('Background.mp3'))


def winner(text):
    win_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(win_text, (WIDTH //2 - win_text.get_width()//2 , HEIGHT//2 -win_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(6000)

def yellow_movement(keys_pressed, yellow):
        if keys_pressed[pygame.K_a] and yellow.x - VEL  > 0:   #Left
            yellow.x -= VEL
        if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  #Right
            yellow.x += VEL
        if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #Up
            yellow.y -= VEL
        if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT -15:  #Down
            yellow.y += VEL
            
def red_movement(keys_pressed, red):
        if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x  + BORDER.width:  #Left
            red.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH :  #Right
            red.x += VEL
        if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  #Up
            red.y -= VEL
        if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15 :  #Down
            red.y += VEL            
           
           
            
def handle_bullets(yellow_bullet, red_bullet, yellow , red):
    for bullet in yellow_bullet:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullet.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullet.remove(bullet)
            
               
    for bullet in red_bullet:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullet.remove(bullet)
        elif bullet.x < 0:
            red_bullet.remove(bullet)    
                        
def draw(yellow, red , yellow_bullet , red_bullet, yellow_health, red_health):
        WIN.blit(SPACE, (0, 0))
        pygame.draw.rect(WIN, BLACK, BORDER)
        WIN.blit(SPACESHIP1, (yellow.x ,yellow.y))
        WIN.blit(SPACESHIP2,(red.x ,red.y))
        WIN.blit(BG,(350,0))
        
        
        red_health_text = HEALTH_FONT.render("Health : " + str(red_health), 1, WHITE)
        yellow_health_text = HEALTH_FONT.render("Health : " + str(yellow_health), 1, WHITE)
        WIN.blit(red_health_text,(WIDTH - red_health_text.get_width() - 10, 10))
        WIN.blit(yellow_health_text,(10, 10))
        
        for bullet in red_bullet:
            pygame.draw.rect(WIN, RED_C, bullet)
            
        for bullet in yellow_bullet:
            pygame.draw.rect(WIN, YELLOW_C, bullet)
            
        pygame.display.update()
        
        
def main():
    yellow=pygame.Rect(100 , 300 ,SPACESHIP_WIDTH ,SPACESHIP_HEIGHT)
    red=pygame.Rect(700 , 300 ,SPACESHIP_WIDTH ,SPACESHIP_HEIGHT)
    clock = pygame.time.Clock()
    BG_MUSIC.play()
    
    yellow_bullet = []
    red_bullet = []
    
    yellow_health=100
    red_health=100
    
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and len(yellow_bullet) < MAX_BULLET:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullet.append(bullet)
                    BULLET_SHOOT.play()
                    
                if event.key == pygame.K_RCTRL and len(red_bullet) < MAX_BULLET:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullet.append(bullet)
                    BULLET_SHOOT.play()
                    
            if event.type == YELLOW_HIT:
                yellow_health -=10
                BULLET_HIT.play()
                    
            if event.type == RED_HIT:
                red_health -= 10
                BULLET_HIT.play()
                
        winner_text = ""
        if yellow_health <= 0:
            winner_text="Player 1 (RED) Winner"
            WINNING.play()
        
        if red_health <= 0:
            winner_text="Player 2 (Yellow) Winner"
            WINNING.play()               
            
        if winner_text != "" :
            winner(winner_text)
            break         
                    
        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed, yellow)
        red_movement(keys_pressed, red)
        handle_bullets(yellow_bullet, red_bullet, yellow, red)
                    
        draw(yellow, red, yellow_bullet, red_bullet, yellow_health, red_health)    
    main()
    
if __name__ == "__main__":
    main()           