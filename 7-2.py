#테스트 깃허브에서 추가
import pygame
import sys
import random
import math
from pygame.locals import *

BLACK = (0, 0, 0)
SILVER = (192, 208, 224)
RED = (255, 0, 0)
CYAN = (0, 224, 255)


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
img_shield = pygame.image.load("image/shield.png")

img_explode = [
    None,
    pygame.image.load("image/explosion1.png"),
    pygame.image.load("image/explosion2.png"),
    pygame.image.load("image/explosion3.png"),
    pygame.image.load("image/explosion4.png"),
    pygame.image.load("image/explosion5.png")
]

img_title = [
    pygame.image.load("image/nebula.png"),
    pygame.image.load("image/logo.png")
]

idx = 0
tmr = 0  # 타이머 변수
score = 0
bg_y = 0

ss_x = 0
ss_y = 0
ss_d = 0  # 플레이어 기체의 기울기 변수

ss_shield = 0
ss_muteki = 0

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

EMY_BUULLET = 0 # 적의 탄환 번호 관리 상수
LINE_T = -80
LINE_B = 800
LINE_L = -80
LINE_R = 1040

EFFECT_MAX = 100
eff_no = 0 # 인덱스
eff_p = [0] * ENEMY_MAX
eff_x = [0] * ENEMY_MAX # 폭발연출 X좌표 리스트
eff_y = [0] * ENEMY_MAX # 폭발연출 Y좌표 리스트




def get_dis(x1,y1, x2,y2) : # 두점 사이 거리 계산
    return ((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))

#문자 표시 함수
def draw_text(scrn, txt, x, y, siz, col): #문자표시
    fnt = pygame.font.Font(None, siz)
    sur = fnt.render(txt, True, col)
    x = x - sur.get_width() / 2
    y = y - sur.get_height() / 2
    scrn.blit(sur,[x,y])




def move_starship(scrn, key): # 플레이어 기체 이동
    global  ss_x, ss_y, ss_d, key_spc, key_z, ss_shield, ss_muteki, idx, tmr
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
    if key_z == 1 and ss_shield > 10:
        set_missile(10)
        ss_shield = ss_shield - 10

    if ss_muteki % 2 == 0 :
        scrn.blit(img_sship[3],[ss_x-8,ss_y +40+(tmr % 3)*40])  #(tmr % 3)*2
        scrn.blit(img_sship[ss_d], [ss_x-37 , ss_y-48]) #플레이어 기체 그리기

    if ss_muteki > 0 :
        ss_muteki = ss_muteki - 1
        return
    elif idx == 1:
        for i in range(ENEMY_MAX): # 적기체 와 히트체크
            if emy_f[i] == True :
                w = img_enemy[emy_type[i]].get_width()
                h = img_enemy[emy_type[i]].get_height()
                r = int((w+h) / 4 + (74+96) / 4)
                if get_dis(emy_x[i], emy_y[i], ss_x, ss_y) < r*r:
                    set_effect(ss_x, ss_y)
                    ss_shield = ss_shield - 10
                    if ss_shield <= 0 :
                        ss_shield = 0
                        idx = 2
                        tmr = 0

                    if ss_muteki == 0 :
                        ss_muteki = 60
                    emy_f[i] = False

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
    global  ss_shield, idx, tmr, score
    for i in range(ENEMY_MAX):
        if emy_f[i] == True:
            ang = -90 - emy_a[i]
            png = emy_type[i]
            emy_x[i] = emy_x[i] + emy_speed[i] * math.cos(math.radians(emy_a[i]))
            emy_y[i] = emy_y[i] + emy_speed[i] * math.sin(math.radians(emy_a[i]))

            if emy_type[i] == 1 and emy_y[i] > 360:
                set_enemy(emy_x[i], emy_y[i], 90, 0, 8)
                emy_a[i] = -45
                emy_speed[i] = 16
            if emy_x[i] < LINE_L or LINE_R < emy_x[i] or emy_y[i] < LINE_T or LINE_B < emy_y[i]:
                emy_f[i] = False

            if emy_type[i] != EMY_BUULLET:
                w = img_enemy[emy_type[i]].get_width()
                h = img_enemy[emy_type[i]].get_height()
                r = int((w+h)/4) + 12
                for n in range(MISSILE_MAX):
                    if msl_f[n] == True and get_dis(emy_x[i], emy_y[i], msl_x[n], msl_y[n]) < r*r:
                        msl_f[n] = False
                        set_effect(emy_x[i], emy_y[i])
                        score = score + 100
                        emy_f[i] = False
                        if ss_shield < 100:
                            ss_shield = ss_shield + 1

            img_rz = pygame.transform.rotozoom(img_enemy[png],ang,1.0)
            scrn.blit(img_rz, [emy_x[i] - img_rz.get_width()/2, emy_y[i] - img_rz.get_height()/2])




def set_effect(x,y) : # 폭발 설정
    global  eff_no
    eff_p[eff_no] = 1
    eff_x[eff_no] = x
    eff_y[eff_no] = y
    eff_no = (eff_no + 1) % ENEMY_MAX

def draw_effect(scrn): #폭발 연출
    for i in range(EFFECT_MAX):
        if eff_p[i] > 0:
            scrn.blit(img_explode[eff_p[i]], [eff_x[i] - 48, eff_y[i] - 48])
            eff_p[i] += 1  # eff_p[i] = eff_p[i] + 1
            if eff_p[i] == 6:
                eff_p[i] = 0





def main():
    global bg_y, tmr, idx, score, ss_x, ss_y, ss_d, ss_shield, ss_muteki
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

        if idx == 0: # 타이틀
            img_rz = pygame.transform.rotozoom(img_title[0], -tmr % 360, 1.0)
            screen.blit(img_rz, [480 - img_rz.get_width() / 2, 280 - img_rz.get_height() / 2])
            screen.blit(img_title[1],[70, 160])
            draw_text(screen, "Press [SPACE] to start!", 480, 600, 50, SILVER )
            if key[K_SPACE] == 1:
                idx = 1
                tmr = 0
                ss_x = 480
                ss_y = 600
                ss_d = 0
                ss_shield = 100
                ss_muteki = 0
                for i in range(ENEMY_MAX):
                    emy_f[i] = False
                for i in range(MISSILE_MAX):
                    msl_f[i] = False

        if idx == 1 :   # 게임 플레이 중
            move_starship(screen, key)
            move_missile(screen)
            bring_enemy()
            move_enemy(screen)
            if tmr == 30 * 60 :
                idx = 3
                tmr = 0

        if idx == 2: # 게임오버
            move_missile(screen)
            move_enemy(screen)
            draw_text(screen, "GAME OVER", 480, 300, 80, RED)
            if tmr == 150:
                idx = 0
                tmr = 0

        if idx == 3: # 게임 클리어
            move_starship(screen, key)
            move_missile(screen)
            draw_text(screen, "GAME CLEAR", 480, 300, 80, SILVER )
            if tmr == 150:
                idx = 0
                tmr = 0

        draw_effect(screen)  # 폭발 연출
        draw_text(screen, "SCORE" + str(score), 200, 30, 50, SILVER)
        if idx != 0:  #실드 표시
            screen.blit(img_shield, [40, 680])
            ##40+ss_shield*4 : 사각형의    (100 - ss_shield)*4 : 4각형의 폭
            #pygame.draw.rect(screen, (64, 32, 32),[40+ss_shield*4,680,(100-ss_shield)*4,12 ])
            pygame.draw.rect(screen, (64, 32, 32), [40+ss_shield * 4, 680, (100-ss_shield) * 4, 12])

        pygame.display.update()
        clock.tick(30)



if __name__ == '__main__':
    main()





