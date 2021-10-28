#테스트 깃허브에서 추가
import pygame
import sys
import random
import math
from pygame.locals import *

img_galaxy = pygame.image.load("image/galaxy.png")
img_sship = [
    pygame.image.load("image/starship.png"),
    pygame.image.load("image/starship_l.png"),
    pygame.image.load("image/starship_r.png"),
    pygame.image.load("image/starship_burner.png")
]

img_enemy = [
    pygame.image.load("image/enemy0.png"),
    pygame.image.load("image/enemy1.png")
]



img_weapon = pygame.image.load("image/bullet.png")

tmr = 0  # 타이머 변수
bg_y = 0

ss_x = 480
ss_y = 360
ss_d = 0  # 플레이어 기체의 기울기 변수
key_spc = 0
key_z = 0 # z키를 눌렀을때 사용하는 변수


MISSILE_MAX = 200
msl_no = 0
msl_f = [False] * MISSILE_MAX
msl_x = [0] * MISSILE_MAX
msl_y = [0] * MISSILE_MAX
msl_a = [0] * MISSILE_MAX

ENEMY_MAX = 100
emy_no = 0
emy_f = [False] * ENEMY_MAX
emy_x = [0] * ENEMY_MAX
emy_y = [0] * ENEMY_MAX
emy_a = [0] * ENEMY_MAX  #적의 비행 각도 리스트
emy_type = [0] * ENEMY_MAX # 적의 종류 리스트
emy_speed = [0] * ENEMY_MAX #적 속도 리스트

LINE_T = -80
LINE_B = 800
LINE_L = -80
LINE_R = 1040


def move_starship(scrn, key): # 플레이어 기체 이동
    global  ss_x, ss_y, ss_d, key_spc, key_z
    ss_d = 0
    if key[K_UP] == 1:
        ss_y = ss_y - 20
        if ss_y < 80:
            ss_y = 80

    if key[K_DOWN] == 1:
        ss_y = ss_y + 20
        if ss_y > 640:
            ss_y = 640

    if key[K_LEFT] == 1:
        ss_d = 1
        ss_x = ss_x - 20
        if ss_x < 40:
            ss_x = 40

    if key[K_RIGHT] == 1:
        ss_d = 2
        ss_x = ss_x + 20
        if ss_x > 920:
            ss_x = 920


    key_spc = (key_spc+1) * key[K_SPACE]
    print(key_spc)
    if key_spc % 5 == 1:
        set_missile(0)

    key_z = (key_z+1) * key[K_z]
    if key_z == 1:
        set_missile(10)

    scrn.blit(img_sship[3],[ss_x-8,ss_y +40+(tmr % 3)*40])  #(tmr % 3)*2

    scrn.blit(img_sship[ss_d], [ss_x-37 , ss_y-48]) #플레이어 기체 그리기

def set_missile(typ): #플레이어 기체 발사 탄환 설정
    global msl_no
    if typ == 0 :
        msl_f[msl_no] = True
        msl_x[msl_no] = ss_x
        msl_y[msl_no] = ss_y-50
        msl_a[msl_no] = 270
        msl_no = (msl_no + 1) % MISSILE_MAX
    if typ == 10 :
        for a in range(160,390,10):
            msl_f[msl_no] = True
            msl_x[msl_no] = ss_x
            msl_y[msl_no] = ss_y - 50
            msl_a[msl_no] = a
            msl_no = (msl_no + 1) % MISSILE_MAX


def move_missile(scrn): #탄환 이동
    for i in range(MISSILE_MAX):
        if msl_f[i] == True:

            msl_x[i] = msl_x[i] + 36 * math.cos(math.radians(msl_a[i]))
            msl_y[i] = msl_y[i] + 36 * math.sin(math.radians(msl_a[i]))
            img_rz = pygame.transform.rotozoom(img_weapon, -90 - msl_a[i], 1.0)
            scrn.blit(img_rz, [msl_x[i] - img_rz.get_width()/2, msl_y[i] - img_rz.get_height() /2 ])
            if msl_y[i] < 0 or msl_x[i] < 0 or msl_x[i] > 960:
                msl_f[i] = False


def bring_enemy(): #적기체 등장
    if tmr % 30 == 0:
        set_enemy(random.randint(20, 940), LINE_T, 90, 1, 6)

def set_enemy(x, y, a, ty, sp):
    global  emy_no
    while True :
        if emy_f[emy_no] == False :
            emy_f[emy_no] = True
            emy_x[emy_no] = x
            emy_y[emy_no] = y
            emy_a[emy_no] = a
            emy_type[emy_no] = ty
            emy_speed[emy_no] = sp
            break

        emy_no = (emy_no+1) % ENEMY_MAX

def move_enemy(scrn) :
    for i in range(ENEMY_MAX):
        if emy_f[i] == True:
            ang = -90 - emy_a[i]
            png = emy_type[i]
            emy_x[i] = emy_x[i] + emy_speed[i] * math.cos(math.radians(emy_a[i]))
            emy_y[i] = emy_y[i] + emy_speed[i] * math.sin(math.radians(emy_a[i]))
            #계속 작성해야함.......







def main():
    global bg_y, tmr
    pygame.init()
    pygame.display.set_caption("Pygame 사용법")
    screen = pygame.display.set_mode((960, 720))
    clock = pygame.time.Clock()
    ang = 0

    while True:
        tmr = tmr + 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    screen = pygame.display.set_mode((960,720), pygame.FULLSCREEN )
                if event.key == pygame.K_F2 or event.key == pygame.K_ESCAPE:
                    screen = pygame.display.set_mode((960,720))

        screen.blit(img_galaxy, [0,0])

        # 배경 스크롤
        bg_y = (bg_y + 16) % 720
        screen.blit(img_galaxy, [0, bg_y - 720])
        screen.blit(img_galaxy, [0, bg_y])

        key = pygame.key.get_pressed()
        move_starship(screen, key)
        move_missile(screen)
        bring_enemy()


        pygame.display.update()
        clock.tick(30)







if __name__ == '__main__':
    main()





