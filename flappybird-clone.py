import pygame
import sys
import random

#Initial setup
pygame.init()

#Game window setup
width, height = 350, 622
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

#Game state variables
game_active = False
score = 0
high_score = 0
score_time = True

#Assets loading
#Background and floor
back_img = pygame.transform.scale(pygame.image.load("assets/background-day.png").convert_alpha(), (350, 622))
floor_img = pygame.image.load("assets/base.png").convert_alpha()
floor_x = 0

#Bird sprites
bird_up = pygame.image.load("assets/yellowbird-upflap.png").convert_alpha()
bird_mid = pygame.image.load("assets/yellowbird-midflap.png").convert_alpha()
bird_down = pygame.image.load("assets/yellowbird-downflap.png").convert_alpha()
birds = [bird_up, bird_mid, bird_down]
bird_index = 0
bird_img = birds[bird_index]
bird_rect = bird_img.get_rect(center=(67, height // 2))

#Bird movement
bird_movement = 0
gravity = 0.17

#Pipe setup
pipe_img = pygame.image.load("assets/pipe-green.png").convert_alpha()
pipes = []
pipe_spawn = pygame.USEREVENT + 1
pygame.time.set_timer(pipe_spawn, 1200)
pipe_min = 200 
pipe_max = 450  
pipe_gap_min = 150
pipe_gap_max = 250

#UI images
get_ready_img = pygame.image.load("assets/message.png").convert_alpha()
get_ready_rect = get_ready_img.get_rect(center=(width // 2, height // 2-20))

over_img = pygame.image.load("assets/gameover.png").convert_alpha()
over_rect = over_img.get_rect(center=(width // 2, height // 2))

#Sounds
sound_die = pygame.mixer.Sound("assets/die.wav")
sound_hit = pygame.mixer.Sound("assets/hit.wav")
sound_point = pygame.mixer.Sound("assets/point.wav")
sound_swoosh = pygame.mixer.Sound("assets/swoosh.wav")
sound_wing = pygame.mixer.Sound("assets/wing.wav")

#Fonts
label_font = pygame.font.Font("freesansbold.ttf", 32)

#Bird flap animation timer
bird_flap = pygame.USEREVENT
pygame.time.set_timer(bird_flap, 200)

#Game functions
def draw_floor():
    screen.blit(floor_img, (floor_x, 520))
    screen.blit(floor_img, (floor_x + 448, 520))

def create_pipes():
    bottom_y = random.randint(350, 520)
    top_y = bottom_y - random.randint(pipe_gap_min, pipe_gap_max)
    bottom_pipe = pipe_img.get_rect(midtop=(467, bottom_y))
    top_pipe = pipe_img.get_rect(midbottom=(467, top_y))
    return top_pipe, bottom_pipe

def pipe_animation():
    for pipe in pipes[:]:
        if pipe.top < 0:
            flipped_pipe = pygame.transform.flip(pipe_img, False, True)
            screen.blit(flipped_pipe, pipe)
        else:
            screen.blit(pipe_img, pipe)
        pipe.centerx -= 3
        if pipe.right < 0:
            pipes.remove(pipe)

def check_collision(pipes):
    global game_active
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            sound_hit.play()
            sound_die.play()
            return False
    if bird_rect.top <= 0 or bird_rect.bottom >= 520:
        sound_hit.play()
        sound_die.play()
        return False
    return True

def draw_score(game_state):
    global score, high_score
    if game_state == "game_on":
        score_text = label_font.render(str(score), True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(width // 2, 66))
        screen.blit(score_text, score_rect)
    elif game_state == "game_over":
        score_text = label_font.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(width // 2, 66))
        screen.blit(score_text, score_rect)

        high_score_text = label_font.render(f"High Score: {high_score}", True, (255, 255, 255))
        high_score_rect = high_score_text.get_rect(center=(width // 2, 506))
        screen.blit(high_score_text, high_score_rect)

def score_update():
    global score, score_time, high_score
    if pipes:
        for pipe in pipes:
            if 65 < pipe.centerx < 69 and score_time:
                score += 1
                score_time = False
                sound_point.play()
            if pipe.left <= 0:
                score_time = True
    if score > high_score:
        high_score = score

#Game loop
running = True
while running:
    clock.tick(120)

    #Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_active:
                    game_active = True
                    pipes = []
                    bird_rect = bird_img.get_rect(center=(67, height // 2))
                    bird_movement = -7
                    score_time = True
                    score = 0
                    sound_swoosh.play()
                else:
                    bird_movement = 0
                    bird_movement = -7
                    sound_wing.play()

        if event.type == bird_flap:
            bird_index = (bird_index + 1) % 3
            bird_img = birds[bird_index]
            bird_rect = bird_img.get_rect(center=bird_rect.center)

        if event.type == pipe_spawn and game_active:
            pipes.extend(create_pipes())

    #Drawing and game logic
    screen.blit(back_img, (0, 0))

    if game_active:
        pipe_animation()
        bird_movement += gravity
        bird_rect.centery += bird_movement
        game_active = check_collision(pipes)

        rotated_bird = pygame.transform.rotozoom(bird_img, bird_movement*-6.1, 1)
        screen.blit(rotated_bird, bird_rect)

        score_update()
        draw_score("game_on")

    else:
        if score == 0:
            screen.blit(get_ready_img, get_ready_rect)
        else:
            screen.blit(over_img, over_rect)
            draw_floor()
            draw_score("game_over")

    #Floor movement
    floor_x -= 1
    if floor_x < -448:
        floor_x = 0
    draw_floor()

    #Refresh display
    pygame.display.update()

#Quiting the pygame and sys
pygame.quit()
sys.exit()
