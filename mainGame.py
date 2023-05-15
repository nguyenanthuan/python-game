import pygame
from sys import exit
from pygame.locals import *
from gameRole import *
import random



pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter Game')


bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
bullet_sound.set_volume(0.3)
enemy1_down_sound.set_volume(0.3)
game_over_sound.set_volume(0.3)

pygame.mixer.music.load('resources/sound/game_music1.mp3')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)


background = pygame.image.load('resources/image/background1.png').convert()
game_over = pygame.image.load('resources/image/gameover.png')

filename = 'resources/image/shoot.png'
plane_img = pygame.image.load(filename)


player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126))
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126))
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
player_pos = [200, 600]
player = Player(plane_img, player_rect, player_pos)


bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)


enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = plane_img.subsurface(enemy1_rect)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))


enemy3_down_sound = pygame.mixer.Sound('resources/sound/enemy3_down.wav')
enemy3_down_sound.set_volume(0.3)
enemy3_rect = pygame.Rect(335, 750, 169, 258)
enemy3_img = plane_img.subsurface(enemy3_rect)
enemy3_down_imgs = []
enemy3_down_imgs.append(plane_img.subsurface(pygame.Rect(0, 486, 165, 261)))
enemy3_down_imgs.append(plane_img.subsurface(pygame.Rect(0, 225, 165, 261)))
enemy3_down_imgs.append(plane_img.subsurface(pygame.Rect(839, 748, 165, 260)))
enemy3_down_imgs.append(plane_img.subsurface(pygame.Rect(165, 486, 165, 261)))
enemy3_down_imgs.append(plane_img.subsurface(pygame.Rect(673, 748, 166, 260)))
enemy3_down_imgs.append(plane_img.subsurface(pygame.Rect(0, 747, 166, 261)))

enemies1 = pygame.sprite.Group()
enemies3 = pygame.sprite.Group()

enemies_down = pygame.sprite.Group()

shoot_frequency = 0
enemy_frequency = 0
t = 100
player_down_index = 16

score = 0

clock = pygame.time.Clock()

running = False

def pause():
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        draw_text_middle('Press C tp continue or Q to quit.', 20, (255, 255, 255), 
                        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)))
        pygame.display.update()
        clock.tick(5)
def main():
    global running
    global shoot_frequency
    global enemy_frequency
    global enemies_down
    global player_down_index
    global score
    global t
    enemy3 = 10
    while running:

        clock.tick(45)


        if not player.is_hit:
            if shoot_frequency % 15 == 0:
                bullet_sound.play()
                player.shoot(bullet_img)
            shoot_frequency += 1
            if shoot_frequency >= 15:
                shoot_frequency = 0

        if enemy_frequency % t == 0:
            enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
            enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
            enemies1.add(enemy1)
        if enemy_frequency % (t+50) == 0:
            enemy3_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
            enemy3 = Enemy(enemy3_img, enemy3_down_imgs, enemy3_pos)
            enemies1.add(enemy3)
        enemy_frequency += 1
        if pygame.time.get_ticks() / 5000 > 0:
            if t  >= 20:
                t-=0.5
        if t <= 20:
            t = 100
        if enemy_frequency >= 200:
            enemy_frequency = 0


        for bullet in player.bullets:
            bullet.move()
            if bullet.rect.bottom < 0:
                player.bullets.remove(bullet)


        for enemy in enemies1:
            enemy.move()

            if pygame.sprite.collide_circle(enemy, player):
                enemies_down.add(enemy)
                enemies1.remove(enemy)
                player.is_hit = True
                game_over_sound.play()
                break
            if enemy.rect.top > SCREEN_HEIGHT:
                enemies1.remove(enemy)

        for enemy in enemies3:
            enemy.move()
            if pygame.sprite.collide_circle(enemy, player):
                enemies_down.add(enemy)
                enemies1.remove(enemy)
                player.is_hit = True
                game_over_sound.play()
                break
            if enemy.rect.top > SCREEN_HEIGHT:
                enemies1.remove(enemy)



        enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
        for enemy_down in enemies1_down:
            enemies_down.add(enemy_down)

        screen.fill(0)
        screen.blit(background, (0, 0))


        if not player.is_hit:
            screen.blit(player.image[player.img_index], player.rect)
            player.img_index = shoot_frequency // 8
        else:
            player.img_index = player_down_index // 8
            screen.blit(player.image[player.img_index], player.rect)
            player_down_index += 1
            if player_down_index > 47:
                running = False



        for enemy_down in enemies_down:
            if enemy_down.down_index == 0:
                enemy1_down_sound.play()
            if enemy_down.down_index > 7:
                enemies_down.remove(enemy_down)
                score += 1000
                continue
            screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
            enemy_down.down_index += 1


        player.bullets.draw(screen)
        enemies1.draw(screen)


        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(str(score), True, (128, 128, 128))
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 10]
        screen.blit(score_text, text_rect)


        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


        key_pressed = pygame.key.get_pressed()

        if not player.is_hit:
            if key_pressed[K_w] or key_pressed[K_UP]:
                player.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                player.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                player.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                player.moveRight()
            if key_pressed[K_p]:
                pause()


font = pygame.font.Font(None, 48)
text = font.render('Score: '+ str(score), True, (255, 0, 0))
text_rect = text.get_rect()
text_rect.centerx = screen.get_rect().centerx
text_rect.centery = screen.get_rect().centery + 24
screen.blit(game_over, (0, 0))
screen.blit(text, text_rect)


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (SCREEN_WIDTH/2 - (label.get_width() / 2), SCREEN_HEIGHT/2 - label.get_height()/2))


pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)).fill((0, 0, 0))
draw_text_middle('Press any key to begin.', 20, (255, 255, 255), pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            running = True
            main()
    pygame.display.update()
