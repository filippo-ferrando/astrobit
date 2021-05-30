import pygame
from random import randrange
from tkinter import Tk

# get pc screen size
root = Tk()
monitor_width = root.winfo_screenwidth()
monitor_height = root.winfo_screenheight()

# pygame init
pygame.init()

# window
window_w = int(monitor_width/1.8)
window_h = int(monitor_height/1.8)
window = pygame.display.set_mode((window_w,window_h))
pygame.display.set_caption("Space War")

# other setups
fps = pygame.time.Clock()
closed = False
game_started = False
died = False
won = False

# colors
white = (255,255,255)
black = (0,0,0)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)

# background image and music
background = pygame.image.load("assets/backgrounds/space.png")
background = pygame.transform.scale(background,(window_w,window_h))
#pygame.mixer.music.load("audio/musics/game.wav") #--> .mp3 unrecognized format in py 3.8
#pygame.mixer.music.play(-1)

# texts
#-------------------------------------------------------------------
# space war text
centerFont = pygame.sysfont.SysFont("Bahnscrift",(window_w+window_h)//20)
spacewar_text = centerFont.render("Space War",True,blue)
spacewar_textRect = spacewar_text.get_rect()
spacewar_textRect.center = (window_w//2,(window_h//2)-50)

# press start text
centerFont2 = pygame.sysfont.SysFont("Bahnscrift",(window_w+window_h)//30)
pressStart_text = centerFont2.render("press 'H' to start the adventure...",True,white)
pressStart_textRect = pressStart_text.get_rect()
pressStart_textRect.center = (window_w//2,(window_h//2)+50)

# how to play text
centerFont3 = pygame.sysfont.SysFont("Bahnscrift",(window_w+window_h)//50)
howtoplay_text = centerFont3.render("movement --> UP and DOWN | fire --> SPACE",True,white)
howtoplay_textRect = howtoplay_text.get_rect()
howtoplay_textRect.center = (window_w//2,(window_h//2)+150)
#-------------------------------------------------------------------

# player
class Player:
    def __init__(self):
        self.normal_image = pygame.image.load("assets/spacecrafts/player/normal.png")
        self.hit_image = pygame.image.load("assets/spacecrafts/player/hit.png")
        self.normal_image = pygame.transform.scale(self.normal_image,(window_w//12,window_h//8))
        self.hit_image = pygame.transform.scale(self.hit_image,(window_w//12,window_h//8))
        self.image = self.normal_image
        self.rect = self.image.get_rect()
        self.rect.centery = window_h//2
        self.timedelay = 0
        self.score = 0
        self.level = 1
        self.levellock = 1
        self.maxlevel = 3
        self.reach_score = 500
        self.powerup = 0
        self.p_time = 0
        self.max_health = 100
        self.hitted = 0
        self.healthbar_width = 100
        self.healthbar_height = 12
        self.healthbar_ratio = self.max_health/self.healthbar_width
        self.health = self.max_health

    def draw(self):
        window.blit(self.image,self.rect)

        for asteroid in asteroids:
            if self.rect.colliderect(asteroid.rect):
                self.image = self.hit_image
                self.timedelay += 1
                self.hitted = 1
                if self.timedelay > 4:
                    self.health -= 30//(asteroid.size/6)
                    asteroids.remove(asteroid)
                    del asteroid
                    self.image = self.normal_image
                    self.hitted = 0
                    self.timedelay = 0
                    break

        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                self.image = self.hit_image
                self.timedelay += 1
                self.hitted = 1
                if self.timedelay > 4:
                    if enemy.which == 1:
                        self.health -= 20
                    elif enemy.which == 2:
                        self.health -= 15
                    elif enemy.which == 3:
                        self.health -= 25
                    enemies.remove(enemy)
                    del enemy
                    self.image = self.normal_image
                    self.hitted = 0
                    self.timedelay = 0
                    break

        for bullet in enemy_bullets:
            if self.rect.colliderect(bullet.rect):
                self.image = self.hit_image
                self.timedelay += 1
                self.hitted = 1
                if self.timedelay > 4:
                    self.health -= 10
                    enemy_bullets.remove(bullet)
                    del bullet
                    self.image = self.normal_image
                    self.hitted = 0
                    self.timedelay = 0
                    break

    def draw_health(self):
        if self.health > self.max_health:
            self.health = self.max_health
        if self.health < 0:
            self.health = 0

        hpFont = pygame.sysfont.SysFont("Franklin Gothic",25)
        hp_text = hpFont.render("HP:",True,green)

        amount = int(self.health / self.healthbar_ratio)
        window.blit(hp_text,(5,7))
        pygame.draw.rect(window, green, (45, 10, amount, self.healthbar_height))
        if self.hitted == 0:
            pygame.draw.rect(window, white, (45, 10, self.healthbar_width, self.healthbar_height), 2)
        else:
            pygame.draw.rect(window, red, (45, 10, self.healthbar_width, self.healthbar_height), 2)

    def draw_score(self):
        hpFont = pygame.sysfont.SysFont("Franklin Gothic",25)
        score_text = hpFont.render("Score:",True,(100,100,255))
        scoreNum_text = hpFont.render(str(self.score),True,(100,100,255))
        window.blit(score_text,(5,30))
        window.blit(scoreNum_text,(60,31))

    def draw_level(self):
        hpFont = pygame.sysfont.SysFont("Franklin Gothic",25)
        level_text = hpFont.render("Level:",True,(150,150,150))
        levelNum_text = hpFont.render(str(self.level),True,(150,150,150))
        window.blit(level_text,(5,52))
        window.blit(levelNum_text,(60,53))

    def movement(self):
        if keys[pygame.K_UP]:
            self.rect.y -= 3
        if keys[pygame.K_DOWN]:
            self.rect.y += 3

        if keys[pygame.K_RIGHT]:
            self.rect.x += 6
        if keys[pygame.K_LEFT]:
            self.rect.x -= 6

        if self.rect.bottom > window_h:
            self.rect.bottom = window_h
        if self.rect.y < 0:
            self.rect.y = 0

    def fire(self):
        new_playerbullet = Playerbullet(self.powerup)
        player_bullets.append(new_playerbullet)

    def power_up(self):
        if self.powerup != 0:
            self.p_time += 1
            if self.p_time == 400:
                self.powerup = 0
                self.p_time = 0

        if self.powerup == 1:
            hpFont = pygame.sysfont.SysFont("Franklin Gothic", 25)
            power_text = hpFont.render("Strong bullets", True, red)
            window.blit(power_text,(15,window_h-30))

        for powerup in powerups:
            if player.rect.colliderect(powerup.rect):
                if powerup.power == "strong_bullet":
                    self.powerup = 1
                powerups.remove(powerup)
                del powerup

player = Player()

# bullet
player_bullets = []
class Playerbullet:
    def __init__(self,powertype):
        self.rect = pygame.Rect(player.rect.right,player.rect.centery,20,5)
        self.power = powertype

    def draw(self):
        if self.power == 0:
            color = yellow
        elif self.power == 1:
            color = red
        pygame.draw.rect(window,color,self.rect)

        if self.rect.x > window_w:
            player_bullets.remove(self)
            del self

    def movement(self):
        self.rect.x += 20

enemy_bullets = []
class Enemybullet:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,20,5)

    def draw(self):
        pygame.draw.rect(window,(255,0,255),self.rect)

        if self.rect.x > window_w:
            enemy_bullets.remove(self)
            del self

    def movement(self):
        self.rect.x -= 7

# asteroid
asteroids = []
a_spawndelay = 0
class Asteroid:
    def __init__(self,which,speed,ytime,size):
        self.normal_image = pygame.image.load(f"assets/asteroids/asteroid{which}/normal.png")
        self.hit_image = pygame.image.load(f"assets/asteroids/asteroid{which}/hit.png")
        self.normal_image = pygame.transform.scale(self.normal_image,(window_w//(size+2),window_h//size))
        self.hit_image = pygame.transform.scale(self.hit_image, (window_w//(size+2),window_h//size))
        self.image = self.normal_image
        self.rect = self.image.get_rect()
        self.rect.x = window_w
        self.rect.y = randrange(-30,window_h+30)
        self.size = size
        self.health = 70 // self.size
        self.timedelay = 0
        self.ytime_delay = 0
        self.speed = speed
        self.time_delay = 0
        self.ytime = ytime
        if self.rect.y > window_h/2:
            self.direction = 0
        else:
            self.direction = 1

    def draw(self):
        window.blit(self.image,self.rect)

        for bullet in player_bullets:
            if self.rect.colliderect(bullet.rect):
                self.image = self.hit_image
                self.timedelay += 1
                if self.timedelay > 4:
                    if bullet.power == 0:
                        self.health -= 1
                    elif bullet.power == 1:
                        self.health -= 2
                    player_bullets.remove(bullet)
                    del bullet
                    self.image = self.normal_image
                    self.timedelay = 0
                    break

        if self.rect.right < 0:
            asteroids.remove(self)
            del self

        elif self.health < 1:
            player.score += int(100//(self.size/3))
            asteroids.remove(self)
            del self

    def movement(self):
        self.rect.x -= self.speed

        self.ytime_delay += 1
        if self.ytime_delay > self.ytime:
            self.ytime_delay = 0
            if self.direction == 0:
                self.rect.y -= 1
            elif self.direction == 1:
                self.rect.y += 1

# powerups
powerups = []
p_spawndelay = 0
class Powerup:
    def __init__(self,which):
        self.image = pygame.image.load(f"assets/powerups/{which}/normal.png")
        self.image = pygame.transform.scale(self.image,(window_w//24,window_h//12))
        self.rect = self.image.get_rect()
        self.rect.x = window_w
        self.rect.centery = randrange(50,window_h-50)
        self.power = which

    def draw(self):
        window.blit(self.image,self.rect)

        if self.rect.right < 0:
            powerups.remove(self)
            del self

    def movement(self):
        self.rect.x -= 3

# enemies
enemies = []
e_spawndelay = 0
class Enemy:
    def __init__(self,which):
        self.normal_image = pygame.image.load(f"assets/spacecrafts/enemy{which}/normal.png")
        self.normal_image = pygame.transform.scale(self.normal_image,(window_w//12,window_h//8))
        self.hit_image = pygame.image.load(f"assets/spacecrafts/enemy{which}/hit.png")
        self.hit_image = pygame.transform.scale(self.hit_image,(window_w//12,window_h//8))
        self.image = self.normal_image
        self.rect = self.image.get_rect()
        self.rect.x = window_w
        self.rect.centery = randrange(50,window_h-50)
        self.which = which
        self.timedelay = 0
        # enemy attributes
        if self.which == 1:
            self.speed = 2
            self.health = 10

        elif self.which == 2:
            self.speed = 4
            self.health = 8

        elif self.which == 3:
            self.speed = 3
            self.health = 12

        # bullet spawn delay
        self.b_spawndelay = 0

    def draw(self):
        window.blit(self.image,self.rect)
        for bullet in player_bullets:
            if self.rect.colliderect(bullet.rect):
                self.image = self.hit_image
                self.timedelay += 1
                if self.timedelay > 4:
                    if bullet.power == 0:
                        self.health -= 1
                    elif bullet.power == 1:
                        self.health -= 2
                    player_bullets.remove(bullet)
                    del bullet
                    self.image = self.normal_image
                    self.timedelay = 0
                    break

        if self.rect.right < 0:
            enemies.remove(self)
            del self

        elif self.health < 1:
            player.score += 75
            enemies.remove(self)
            del self

    def movement(self):
        self.rect.x -= self.speed

    def attack(self):
        if self.which == 1:
            self.b_spawndelay += 1
            if self.b_spawndelay == 100:
                self.b_spawndelay = 0
                new_enemybullet = Enemybullet(self.rect.left,self.rect.centery)
                enemy_bullets.append(new_enemybullet)

# boss
class Boss:
    def __init__(self):
        self.normal_image = pygame.image.load("assets/spacecrafts/boss/normal.png")
        self.normal_image = pygame.transform.scale(self.normal_image,(window_w//10,window_h//6))
        self.hit_image = pygame.image.load("assets/spacecrafts/boss/hit.png")
        self.hit_image = pygame.transform.scale(self.hit_image, (window_w // 10, window_h // 6))
        self.image = self.normal_image
        self.rect = self.image.get_rect()
        self.rect.x = window_w
        self.rect.centery = window_h//2
        self.max_health = 75
        self.b_spawndelay = 0
        self.b_maxtime = 60
        self.hitted = 0
        self.timedelay = 0
        self.healthbar_width = 100
        self.healthbar_height = 12
        self.healthbar_ratio = self.max_health / self.healthbar_width
        self.health = self.max_health

    def draw(self):
        window.blit(self.image,self.rect)

    def draw_health(self):
        if self.health > self.max_health:
            self.health = self.max_health
        if self.health < 0:
            self.health = 0

        hpFont = pygame.sysfont.SysFont("Franklin Gothic",25)
        hp_text = hpFont.render("BOSS:",True,(220,0,220))

        amount = int(self.health / self.healthbar_ratio)
        window.blit(hp_text,(window_w-self.healthbar_width-70,10))
        pygame.draw.rect(window, (220,0,220), (window_w-self.healthbar_width-10,10 , amount, self.healthbar_height))
        if self.hitted == 0:
            pygame.draw.rect(window, white, (window_w-self.healthbar_width-10,10 ,self.healthbar_width, self.healthbar_height), 2)
        else:
            pygame.draw.rect(window, red, (window_w-self.healthbar_width-10,10, self.healthbar_width, self.healthbar_height), 2)

    def show_myself(self):
        if not self.rect.right < window_w:
            self.draw()
            self.rect.x -= 1

    def movement(self):
        self.rect.y += randrange(-5,6)

        for bullet in player_bullets:
            if self.rect.colliderect(bullet.rect):
                self.image = self.hit_image
                self.timedelay += 1
                self.hitted = 1
                if self.timedelay > 4:
                    if bullet.power == 0:
                        self.health -= 1
                    elif bullet.power == 1:
                        self.health -= 2
                    player_bullets.remove(bullet)
                    del bullet
                    self.image = self.normal_image
                    self.hitted = 0
                    self.timedelay = 0
                    break

    def fire(self):
        self.b_spawndelay += 1
        if self.b_spawndelay == self.b_maxtime:
            self.b_spawndelay = 0
            self.b_maxtime = randrange(20,90,10)
            new_enemybullet = Enemybullet(self.rect.left, self.rect.centery)
            enemy_bullets.append(new_enemybullet)

levelshow_td = 0

# game loop
while not closed:
    fps.tick(60)
    keys = pygame.key.get_pressed()

    window.blit(background,(0,0))

    if not game_started:
        window.blit(spacewar_text,spacewar_textRect)
        window.blit(pressStart_text,pressStart_textRect)
        window.blit(howtoplay_text,howtoplay_textRect)

        if keys[pygame.K_h]:
            game_started = True

    elif game_started:
        # level up codes
        if player.score >= player.reach_score:
            player.levellock = 1
            player.level += 1
            levelshow_td = 0
            if player.level == 2:
                player.reach_score = 1250

            if player.level == player.maxlevel:
                player.reach_score = 99999999

        # display level on the screen center
        if player.levellock == 1:
            levelshow_td += 1
            if levelshow_td > 200:
                player.levellock = 0

                if player.level == player.maxlevel:
                    boss = Boss()
            else:
                player.image = player.normal_image
                player.health = player.max_health
                player.timedelay = 0
                if player.level < player.maxlevel:
                    level_text = centerFont2.render(
                        f"Level: {player.level}/{player.maxlevel} - Reach {player.reach_score} score", True, white)
                else:
                    level_text = centerFont2.render(
                        f"Level: {player.level}/{player.maxlevel} - destroy the BOSS", True, white)
                level_textRect = level_text.get_rect()
                level_textRect.center = (window_w // 2, window_h // 2)
                window.blit(level_text, level_textRect)

        # revive powerups
        if player.levellock == 0:
            p_spawndelay += 1
            if 0 < player.level < player.maxlevel+1:
                if p_spawndelay > 1200:
                    p_spawndelay = 0
                    new_powerup = Powerup("strong_bullet")
                    powerups.append(new_powerup)

            for powerup in powerups:
                powerup.draw()
                powerup.movement()
        else:
            p_spawndelay = 0
            for powerup in powerups:
                powerups.remove(powerup)
                del powerup

        # revive bullets
        for bullet in player_bullets:
            bullet.draw()
            bullet.movement()

        for bullet in enemy_bullets:
            bullet.draw()
            bullet.movement()

        # revive enemies
        if player.levellock == 0:
            e_spawndelay += 1
            if player.level == 1:
                if e_spawndelay > 600:
                    e_spawndelay = 0
                    new_enemy = Enemy(randrange(1,3))
                    enemies.append(new_enemy)

            if player.level == 2:
                if e_spawndelay > 480:
                    e_spawndelay = 0
                    new_enemy = Enemy(randrange(1,4))
                    enemies.append(new_enemy)

            for enemy in enemies:
                enemy.draw()
                enemy.movement()
                enemy.attack()
        else:
            e_spawndelay = 0
            for enemy in enemies:
                enemies.remove(enemy)
                del enemy

        # revive player
        player.draw()
        player.draw_health()
        player.draw_score()
        player.draw_level()
        player.movement()
        player.power_up()

        if player.health < 1:
            closed = True
            died = True

        # revive boss
        if player.levellock == 0:
            if player.level == player.maxlevel:
                boss.draw()
                boss.show_myself()
                if boss.rect.right <= window_w:
                    boss.movement()
                    boss.fire()
                    boss.draw_health()

                if boss.health < 1:
                    player.score += 1000
                    closed = True
                    won = True

        # revive asteroids
        if player.levellock == 0:
            a_spawndelay += 1
            if player.level == 1:
                if a_spawndelay == 160:
                    a_spawndelay = 0
                    new_asteroid = Asteroid(which=randrange(1,3),size=randrange(6,13),speed=randrange(1,4),ytime=randrange(0,6))
                    asteroids.append(new_asteroid)

            if player.level == 2:
                if a_spawndelay == 100:
                    a_spawndelay = 0
                    new_asteroid = Asteroid(which=randrange(1,3),size=randrange(5,12),speed=randrange(2,4),ytime=randrange(0,6))
                    asteroids.append(new_asteroid)

            for asteroid in asteroids:
                asteroid.draw()
                asteroid.movement()
        else:
            a_spawndelay = 0
            for asteroid in asteroids:
                asteroids.remove(asteroid)
                del asteroid



    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            closed = True

        if game_started:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.fire()

pygame.mixer.music.stop()

if died:
    closed = False
    while not closed:
        window.fill(black)

        gameover_text = centerFont.render("GAME OVER",True,white)
        gameover_textRect = gameover_text.get_rect()
        gameover_textRect.center = (window_w//2,(window_h//2)-50)
        window.blit(gameover_text,gameover_textRect)

        died_text = centerFont3.render("You died", True, white)
        died_textRect = died_text.get_rect()
        died_textRect.center = (window_w// 2,(window_h//2))
        window.blit(died_text,died_textRect)

        hpFont = pygame.sysfont.SysFont("Franklin Gothic", 35)
        score_text = hpFont.render("Score:", True, (100, 100, 255))
        score_textRect = score_text.get_rect()
        score_textRect.center = ((window_w//2)-40,(window_h//2)+75)
        scoreNum_text = hpFont.render(str(player.score), True, (100, 100, 255))
        scoreNum_textRect = scoreNum_text.get_rect()
        scoreNum_textRect.center = ((window_w//2)+40,(window_h//2)+75)
        window.blit(score_text,score_textRect)
        window.blit(scoreNum_text,scoreNum_textRect)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closed = True

if won:
    closed = False
    while not closed:
        window.fill(white)
        hpFont = pygame.sysfont.SysFont("Franklin Gothic", 35)
        youwin_text = centerFont.render("YOU WON THE GAME",True,black)
        youwin_textRect = youwin_text.get_rect()
        youwin_textRect.center = ((window_w // 2), (window_h // 2))
        score_text = hpFont.render("Score:", True, (100, 100, 255))
        score_textRect = score_text.get_rect()
        score_textRect.center = ((window_w // 2) - 40, (window_h // 2) + 75)
        scoreNum_text = hpFont.render(str(player.score), True, (100, 100, 255))
        scoreNum_textRect = scoreNum_text.get_rect()
        scoreNum_textRect.center = ((window_w // 2) + 40, (window_h // 2) + 75)
        window.blit(youwin_text,youwin_textRect)
        window.blit(score_text, score_textRect)
        window.blit(scoreNum_text, scoreNum_textRect)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closed = True

pygame.quit()
quit()
