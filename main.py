import pygame, random

pygame.init()

WIDTH = 800
HEIGHT = 400
FPS = 60
CLOCK = pygame.time.Clock()

BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
RED = (220, 20, 60)
GREEN = (50, 205, 50)

display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eat The Bee")
display_surface.fill(WHITE)

LIFE = 5
SCORE = 0
VELOCITY = 10
BEE_SPEED_STARTING = 3
BEE_SPEED = BEE_SPEED_STARTING

score_font = pygame.font.Font('Roboto-Black.ttf', 32)
score_text = score_font.render("Score: " + str(SCORE), True, GREEN, None)
score_text_rect = score_text.get_rect()
score_text_rect.centerx = WIDTH // 2
score_text_rect.y = 10

life_font = pygame.font.Font('Roboto-Black.ttf', 32)
life_text = life_font.render("Life: " + str(LIFE), True, RED, None)
life_text_rect = life_text.get_rect()
life_text_rect.topleft = (10, 10)

game_end_font = pygame.font.Font('Roboto-Black.ttf', 42)
game_end_text = game_end_font.render("Game Over. Press Space to restart", True, RED, None)
game_end_text_rect = game_end_text.get_rect()
game_end_text_rect.center = (WIDTH // 2, HEIGHT // 2)

bird = pygame.image.load("bird.png")
bird_rect = bird.get_rect()
bird_rect.x = 10
bird_rect.y = HEIGHT // 2

bee = pygame.image.load("bee.png")
bee_rect = bee.get_rect()
bee_rect.x = WIDTH - 40
bee_rect.y = random.randint(48, (HEIGHT - bird_rect[3]))

pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1, 0)

eat_sound = pygame.mixer.Sound("eat.mp3")
die_sound = pygame.mixer.Sound("die.mp3")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if LIFE <= 0:
        display_surface.blit(game_end_text, game_end_text_rect)
        pygame.display.update()
        pygame.mixer.music.stop()

        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        LIFE = 5
                        SCORE = 0
                        BEE_SPEED = BEE_SPEED_STARTING
                        bird_rect.y = HEIGHT // 2
                        pygame.mixer.music.play(-1, 0)
                        is_paused = False

                if event.type == pygame.QUIT:
                    running = False
                    is_paused = False
                    pygame.quit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and bird_rect.y > 48:
        bird_rect.y -= VELOCITY
    if keys[pygame.K_DOWN] and bird_rect.y < HEIGHT - bird_rect[3]:
        bird_rect.y += VELOCITY

    bee_rect.x -= BEE_SPEED
    if bee_rect.x < 0:
        bee_rect.x = WIDTH - 40
        bee_rect.y = random.randint(48, (HEIGHT - bird_rect[3]))
        LIFE -= 1
        life_text = score_font.render("Life: " + str(LIFE), True, RED, None)
        die_sound.play()

    if bird_rect.colliderect(bee_rect):
        SCORE += 1
        BEE_SPEED += .5
        score_text = score_font.render("Score: " + str(SCORE), True, GREEN, None)
        bee_rect.x = WIDTH - 40
        bee_rect.y = random.randint(48, (HEIGHT - bird_rect[3]))
        eat_sound.play()

    display_surface.fill(WHITE)
    display_surface.blit(score_text, score_text_rect)
    display_surface.blit(life_text, life_text_rect)
    pygame.draw.line(display_surface, GRAY, (0, 48), (WIDTH, 48), 1)
    display_surface.blit(bird, bird_rect)
    display_surface.blit(bee, bee_rect)

    pygame.display.update()
    CLOCK.tick(FPS)

pygame.quit()