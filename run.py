import pygame

interval = 35
pos = [([-1] * 15) for i in range(15)]  # 15*15的数组初始化为-1 为棋盘
sizeqizi = 30
user = True  # 白棋先手为True 玩家一定为先手
firstUser = True
winblack, winwhite = 0, 0
winstaus = False
step = 1


# 初始化棋盘
def pro_init(rightfont, screen, font, bg):
    global pos, step
    step = 1

    pos = [([-1] * 15) for i in range(15)]
    screen.blit(bg, (0, 0))  # 绘制背景

    pygame.draw.circle(screen, (0, 0, 0), (50 + interval * 3, 50 + interval * 3), 4, 3)  # 绘制圆点
    pygame.draw.circle(screen, (0, 0, 0), (50 + interval * 11, 50 + interval * 3), 4, 3)  # 绘制圆点
    pygame.draw.circle(screen, (0, 0, 0), (50 + interval * 3, 50 + interval * 11), 4, 3)  # 绘制圆点
    pygame.draw.circle(screen, (0, 0, 0), (50 + interval * 11, 50 + interval * 11), 4, 3)  # 绘制圆点
    pygame.draw.circle(screen, (0, 0, 0), (50 + interval * 7, 50 + interval * 7), 4, 3)  # 绘制圆点

    score = rightfont.render("White Score : " + str(winwhite), True, (255, 0, 0))
    screen.blit(score, (600, 100))  # 绘制分数
    score = rightfont.render("Black Score : " + str(winblack), True, (255, 0, 0))
    screen.blit(score, (600, 150))  # 绘制分数
    pygame.draw.rect(screen, (255, 255, 255), (622, 445, 85, 28))
    replay = rightfont.render("Replay", True, (255, 0, 0))
    screen.blit(replay, (630, 450))  # 绘制重新开始
    pygame.draw.rect(screen, (255, 255, 255), (592, 295, 140, 28))
    first = rightfont.render("First :  " + ("White" if user else "Black"), True, (255, 0, 0))
    screen.blit(first, (600, 300))  # 绘制先手信息

    for i in range(15):  # 调整尺寸
        t = i * interval
        text = font.render(str(i + 1), True, (0, 0, 0))  # 数字
        screen.blit(text, (25, 45 + t))
        text = font.render(chr(i + 65), True, (0, 0, 0))  # 字母
        screen.blit(text, (45 + t, 25))

        pygame.draw.line(screen, (0, 0, 0), (50, 50 + t), (540, 50 + t), 1)  # 横线
        pygame.draw.line(screen, (0, 0, 0), (50 + t, 50), (50 + t, 540), 1)


# 判断是否点击先手
def judge_first(x, y):
    return 600 < x < 660 and 300 < y < 340


# exit
def code_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


# 判断x,y是否为重新开始
def judge_replay(x, y):
    return 700 > x > 630 and 490 > y > 450


# 找到点
def find_pos(n):
    p = (n - 50 + interval // 2) // 35
    return p


# 递归判断是否为同一棋子
def digui(disx, disy, posx, posy, tmp, cnt):
    if cnt >= 4:  # 超过4连珠直接返回
        return cnt
    posx = posx + disx
    posy = posy + disy
    if 0 <= posx < 15 and 0 <= posy < 15 and pos[posx][posy] == tmp:
        return digui(disx, disy, posx, posy, tmp, cnt + 1)
    return cnt


# 判胜 传入最后输入的棋子 以及最后下棋的user状态 返回true则代表user赢
def judge_win(posx, posy, tmp):
    urbias = 1  # 右上斜线
    ulbias = 1  # 左上斜线
    level = 1  # 水平
    vertical = 1  # 垂直

    ulbias += digui(1, -1, posx, posy, tmp, 0) + digui(-1, 1, posx, posy, tmp, 0)
    urbias += digui(-1, -1, posx, posy, tmp, 0) + digui(1, 1, posx, posy, tmp, 0)
    level += digui(-1, 0, posx, posy, tmp, 0) + digui(1, 0, posx, posy, tmp, 0)
    vertical += digui(0, -1, posx, posy, tmp, 0) + digui(0, 1, posx, posy, tmp, 0)
    if ulbias >= 5 or urbias >= 5 or level >= 5 or vertical >= 5:
        return True
    return False


# 添加一个棋子
def add_piece(indexx, indexy):
    global step
    # -- 数字
    offset = 3
    if step // 10 > 9:
        offset = 9
    elif step // 10 >= 1:
        offset = 6
    # -- 数字

    posx = 50 + indexx * interval - (sizeqizi + 1) // 2
    posy = 50 + indexy * interval - (sizeqizi + 1) // 2
    screen.blit((white if user else black), (posx, posy))
    pos[indexx][indexy] = user
    if user:
        text = font.render(str(step), True, (0, 0, 0))  # 数字
    else:
        text = font.render(str(step), True, (255, 255, 255))  # 数字
    screen.blit(text, (50 - offset + indexx * interval, 45 + indexy * interval))
    step += 1


# 胜利处理
def win_handle(winuser):
    global winstaus, winwhite, winblack, user, firstUser
    music2.play()  # 获胜音乐
    win = winfont.render(winuser + " win !!!", True, (255, 0, 0))  # 赢
    screen.blit(win, (255, 255))
    winstaus = True
    if user:
        winwhite += 1
    else:
        winblack += 1
    firstUser = not firstUser
    user = firstUser


# 添加一个棋子并处理
def add_piece_handle(indexx, indexy):
    global user
    if 0 <= indexx < 15 and 0 <= indexy < 15 and pos[indexx][indexy] == -1:
        add_piece(indexx, indexy)

        # 判断胜利
        if judge_win(indexx, indexy, user):
            win_handle(("White" if user else "Black"))
            return
        # 和棋判断先手
        if step >= 255:
            win_handle(("White" if firstUser else "Black"))
            return
        # 没有胜利
        user = not user
        music1.play()  # 下棋音乐
    return


pygame.init()
screen = pygame.display.set_mode((780, 600))
# 背景
bg = pygame.image.load("bg.jpg")
bg = pygame.transform.scale(bg, (780, 600))
# 文字
font = pygame.font.SysFont("", 20)
# win 文字
winfont = pygame.font.SysFont("", 70, True)
# right 文字
rightfont = pygame.font.SysFont("", 30)
# 音乐
music1 = pygame.mixer.Sound("m1.wav")
music2 = pygame.mixer.Sound("m2.wav")
# 初始化棋子
white = pygame.image.load("white.png")
white = pygame.transform.scale(white, (sizeqizi, sizeqizi))
black = pygame.image.load("black.png")
black = pygame.transform.scale(black, (sizeqizi, sizeqizi))

pro_init(rightfont, screen, font, bg)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        # user==firstUser玩家下棋
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 获得鼠标位置
            x, y = pygame.mouse.get_pos()
            # judge replay
            if judge_replay(x, y):
                pro_init(rightfont, screen, font, bg)
                winstaus = False
                continue
            # judge first
            if judge_first(x, y):
                firstUser = not firstUser
                user = firstUser
                pro_init(rightfont, screen, font, bg)
                winstaus = False

            if winstaus:
                continue

            indexx = find_pos(x)
            indexy = find_pos(y)
            add_piece_handle(indexx, indexy)

        if event.type == pygame.KEYDOWN and winstaus:
            firstUser = not firstUser
            user = firstUser
            pro_init(rightfont, screen, font, bg)
            winstaus = False

    pygame.display.update()
