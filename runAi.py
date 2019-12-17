import pygame
import random

interval = 35
pos = [([-1] * 16) for i in range(16)]  # 15*15的数组初始化为-1 为棋盘
aiMap = []

sizeqizi = 30
is_aifirst = True  # 是否为ai先手
user = True  # 白棋先手为True
firstUser = True
winblack, winwhite = 0, 0
winstaus = False
step = 1
weights = [[1, 50, 62, 900], [10, 60, 300, 900]]  # weights[0] 死权值  weights[1]活权值  ！！修改后要修改judge_down_win


# 初始化棋盘
def pro_init(rightfont, screen, font, bg):
    global pos, step, aiMap
    step = 1
    aiMap = [({"l": 0, "r": 0, "u": 0, "d": 0, "lu": 0, "ru": 0, "ld": 0, "rd": 0},
              {"l": 0, "r": 0, "u": 0, "d": 0, "lu": 0, "ru": 0, "ld": 0, "rd": 0},
              {"l": 0, "r": 0, "u": 0, "d": 0, "lu": 0, "ru": 0, "ld": 0, "rd": 0},
              {"l": 0, "r": 0, "u": 0, "d": 0, "lu": 0, "ru": 0, "ld": 0, "rd": 0},
              {"l": 0, "r": 0, "u": 0, "d": 0, "lu": 0, "ru": 0, "ld": 0, "rd": 0},
              {"l": 0, "r": 0, "u": 0, "d": 0, "lu": 0, "ru": 0, "ld": 0, "rd": 0},
              {"l": 0, "r": 0, "u": 0, "d": 0, "lu": 0, "ru": 0, "ld": 0, "rd": 0},
              {"l": 0, "r": 0, "u": 0, "d": 0, "lu": 0, "ru": 0, "ld": 0, "rd": 0},
              {"l": 0, "r": 0, "u": 0, "d": 0, "lu": 0, "ru": 0, "ld": 0, "rd": 0},
              {"l": 0, "r": 0, "u": 0, "d": 0, "lu": 0, "ru": 0, "ld": 0, "rd": 0},
              {"l": 0, "r": 0, "u": 0, "d": 0, "lu": 0, "ru": 0, "ld": 0, "rd": 0},
              {"l": 0, "r": 0, "u": 0, "d": 0, "lu": 0, "ru": 0, "ld": 0, "rd": 0},
              {"l": 0, "r": 0, "u": 0, "d": 0, "lu": 0, "ru": 0, "ld": 0, "rd": 0},
              {"l": 0, "r": 0, "u": 0, "d": 0, "lu": 0, "ru": 0, "ld": 0, "rd": 0},
              {"l": 0, "r": 0, "u": 0, "d": 0, "lu": 0, "ru": 0, "ld": 0, "rd": 0},
              {"l": 0, "r": 0, "u": 0, "d": 0, "lu": 0, "ru": 0, "ld": 0, "rd": 0}) for i in range(16)]

    pos = [([-1] * 16) for i in range(16)]
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
    # firstUser = not firstUser
    user = firstUser


# 添加一个棋子并处理
def add_piece_handle(indexx, indexy):
    global user
    if 0 <= indexx < 15 and 0 <= indexy < 15 and pos[indexx][indexy] == -1:
        add_piece(indexx, indexy)  # 下棋

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


# dis={"x","y"}
def changedis(dis):
    if dis["x"] == 0:
        if dis["y"] == 1:  # up
            return "d"
        else:  # down
            return "u"
    elif dis["x"] == 1:
        if dis["y"] == 1:  # right up
            return "rd"
        elif dis["y"] == 0:  # right
            return "r"
        else:  # right down
            return "ru"
    else:  # x == -1
        if dis["y"] == 1:  # left up
            return "ld"
        elif dis["y"] == 0:  # left
            return "l"
        else:  # left down
            return "lu"


# 得到posx.posy的dis方向上的权值 dis={"x","y"} ai_down=True为玩家
def get_weight(posx, posy, dis, length, ai_down=True):
    global aiMap
    if not 0 <= posx <= 15 or not 0 <= posy <= 15:
        return

    # if length <= 0:
    #     aiMap[posx][posy][changedis(dis)] = 0
    #     return
    rootx = posx + dis["x"] * (length + 1)
    rooty = posy + dis["y"] * (length + 1)
    # print((rootx,rooty))
    # 死
    if (not 0 <= rooty <= 15 or not 0 <= rootx <= 15) or pos[rootx][rooty] != -1:
        if length == 1:  # 死1 权值为
            aiMap[posx][posy][changedis(dis)] = weights[0][0]
        elif length == 2:  # 死2 权值为
            aiMap[posx][posy][changedis(dis)] = weights[0][1]
        elif length == 3:  # 死3 权值为
            aiMap[posx][posy][changedis(dis)] = weights[0][2]
        elif length == 4:  # 死4 权值为
            aiMap[posx][posy][changedis(dis)] = weights[0][3] if ai_down else 10000

    else:
        if length == 1:  # 活1 权值
            aiMap[posx][posy][changedis(dis)] = weights[1][0]
        elif length == 2:  # 活2 权值为
            aiMap[posx][posy][changedis(dis)] = weights[1][1] if ai_down else 150
        elif length == 3:  # 活3 权值为
            aiMap[posx][posy][changedis(dis)] = weights[1][2] if ai_down else 500
        elif length == 4:  # 活4 权值为
            aiMap[posx][posy][changedis(dis)] = weights[1][3] if ai_down else 10000
    # print((posx, posy))
    # print(aiMap[posx][posy])
    return


# 赋值数组权值 tmp_user = True为玩家
def init_weight(posx, posy, tmp, tmp_user=True):
    # print("\n\n")
    same = {"l": digui(-1, 0, posx, posy, tmp, 0),
            "r": digui(1, 0, posx, posy, tmp, 0),
            "d": digui(0, 1, posx, posy, tmp, 0),
            "u": digui(0, -1, posx, posy, tmp, 0),
            "ru": digui(1, -1, posx, posy, tmp, 0),
            "rd": digui(1, 1, posx, posy, tmp, 0),
            "ld": digui(-1, 1, posx, posy, tmp, 0),
            "lu": digui(-1, -1, posx, posy, tmp, 0)
            }

    get_weight(posx - same["l"] - 1, posy, {"x": 1, "y": 0},
               same["l"] + same["r"] + 1, tmp_user)  # 赋值当前棋的aiMap左侧权值 ,目标点的右侧
    get_weight(posx + same["r"] + 1, posy, {"x": -1, "y": 0},
               same["l"] + same["r"] + 1, tmp_user)  # 赋值当前棋的aiMap右侧权值 ,目标点的左侧
    get_weight(posx, posy - same["u"] - 1, {"x": 0, "y": 1},
               same["u"] + same["d"] + 1, tmp_user)  # 赋值当前棋的aiMap上侧权值 ,目标点的下侧
    get_weight(posx, posy + same["d"] + 1, {"x": 0, "y": -1},
               same["u"] + same["d"] + 1, tmp_user)  # 赋值当前棋的aiMap下侧权值 ,目标点的上侧
    get_weight(posx + same["ru"] + 1, posy - same["ru"] - 1, {"x": -1, "y": 1},
               same["ru"] + same["ld"] + 1, tmp_user)  # 赋值当前棋的aiMap右上侧权值 ,目标点的左下侧
    get_weight(posx - same["ld"] - 1, posy + same["ld"] + 1, {"x": 1, "y": -1},
               same["ru"] + same["ld"] + 1, tmp_user)  # 赋值当前棋的aiMap左下侧权值 ,目标点的右上侧
    get_weight(posx + same["rd"] + 1, posy + same["rd"] + 1, {"x": -1, "y": -1},
               same["rd"] + same["lu"] + 1, tmp_user)  # 赋值当前棋的aiMap右下侧权值 ,目标点的左上侧
    get_weight(posx - same["lu"] - 1, posy - same["lu"] - 1, {"x": 1, "y": 1},
               same["rd"] + same["lu"] + 1, tmp_user)  # 赋值当前棋的aiMap右上侧权值 ,目标点的左下侧


def ai_downed_wight(posx, posy, cdis, length):
    global aiMap
    if not 0 <= posx < 15 or not 0 <= posy < 15:
        return
    if length == 1:  # 死1 权值为 1
        aiMap[posx][posy][cdis] = weights[0][0]
    elif length == 2:  # 死2 权值为 50
        aiMap[posx][posy][cdis] = weights[0][1]
    elif length == 3:  # 死3 权值为 61
        aiMap[posx][posy][cdis] = weights[0][2]
    elif length == 4:  # 死4 权值为 900
        aiMap[posx][posy][cdis] = weights[0][3]
    return 0


# ai下完之后处理影响的白棋权值    tmp ai棋色
def handle_ai_down(posx, posy, tmp):
    global aiMap
    same = {"l": digui(-1, 0, posx, posy, not tmp, 0),
            "r": digui(1, 0, posx, posy, not tmp, 0),
            "d": digui(0, 1, posx, posy, not tmp, 0),
            "u": digui(0, -1, posx, posy, not tmp, 0),
            "ru": digui(1, -1, posx, posy, not tmp, 0),
            "rd": digui(1, 1, posx, posy, not tmp, 0),
            "ld": digui(-1, 1, posx, posy, not tmp, 0),
            "lu": digui(-1, -1, posx, posy, not tmp, 0)
            }
    ai_downed_wight(posx, posy - same["u"] - 1, "d", same["u"])  # up
    ai_downed_wight(posx, posy + same["d"] + 1, "u", same["d"])  # down
    ai_downed_wight(posx - same["l"] - 1, posy, "r", same["l"])  # left
    ai_downed_wight(posx + same["r"] + 1, posy, "l", same["r"])  # right

    ai_downed_wight(posx + same["ru"] + 1, posy - same["ru"] - 1, "ld", same["ru"])  # right up
    ai_downed_wight(posx - same["ld"] - 1, posy + same["ld"] + 1, "ru", same["ld"])  # left down
    ai_downed_wight(posx + same["rd"] + 1, posy + same["rd"] + 1, "lu", same["rd"])  # right down
    ai_downed_wight(posx - same["lu"] - 1, posy - same["lu"] - 1, "rd", same["lu"])  # left p


# 比较两个aiMap大小 返回true为a>b
def cmp(a, b):
    fa, fb = False, False
    ta = a["l"] + a["r"] + a["u"] + a["d"] + a["ru"] + a["rd"] + a["lu"] + a["ld"]  # 权值
    tb = b["l"] + b["r"] + b["u"] + b["d"] + b["ru"] + b["rd"] + b["lu"] + b["ld"]
    # 计算是否必须
    if a["l"] >= 200 or a["r"] >= 200 or a["u"] >= 200 or a["d"] >= 200 or a["lu"] >= 200 or a["ld"] >= 200 or a[
        "ru"] >= 200 or a["rd"] >= 200:
        fa = True
    if b["l"] >= 200 or b["r"] >= 200 or b["u"] >= 200 or b["d"] >= 200 or b["lu"] >= 200 or b["ld"] >= 200 or b[
        "ru"] >= 200 or b["rd"] >= 200:
        fb = True
    if fa == fb:  # 同要必须或者不必须则返回权值大的
        if ta == tb:
            return random.randint(0, 1)
        return ta > tb
    return fa == True  # 返回必须的


# 通过权值 获取到长度(1~4)  死为- 活为+
def get_length_by_weight(w):
    if w == 0:
        return 0
    for u in range(2):
        for j in range(4):
            if w == weights[u][j]:
                return j + 1 if u == 1 else -(j + 1)
    return 0


# 输入两个方向的权重 得到同方向上面的棋数量，死为- 活为正
def get_length_by_line_weight(w1, w2):
    a = get_length_by_weight(w1)
    b = get_length_by_weight(w2)
    if a < 0 or b < 0:
        return -(abs(a) + abs(b))
    else:
        return a + b


# 判断两个坐标是否为同颜色， 不相同或者空则为False 超范围也为False
def judge_same_color(x1, y1, x2, y2):
    if not 0 <= x1 <= 14 or not 0 <= y1 <= 14 or not 0 <= x2 <= 14 or not 0 <= y2 <= 14:
        return False
    return pos[x1][y1] == pos[x2][y2]


# 得到颜色， 超过则为-2 无为-1
def get_type_pos(x, y):
    if not 0 <= x <= 14 or not 0 <= y <= 14:
        return -2
    else:
        return pos[x][y]


# 判断下这个位置是否一定赢 True为一定赢 2为必胜但需要下一步
def judge_down_win(posx, posy):
    # if posx == 6 and posy == 7:
    #     a = 1
    # 八个方向的棋子数量
    type_true = [[0, 0, 0, 0], [0, 0, 0, 0]]
    type_false = [[0, 0, 0, 0], [0, 0, 0, 0]]

    # 同行双方向必胜棋
    if judge_same_color(posx - 1, posy, posx + 1, posy):  # 无需判断 ==0情况
        # 相同方向
        line = get_length_by_line_weight(aiMap[posx][posy]["l"], aiMap[posx][posy]["r"])
        if pos[posx - 1][posy]:
            type_true[(0 if line < 0 else 1)][abs(line) - 1] += 1
        else:
            type_false[(0 if line < 0 else 1)][abs(line) - 1] += 1

        if aiMap[posx][posy]["l"] + aiMap[posx][posy]["r"] >= 63:
            return True
    else:
        qi0 = get_type_pos(posx - 1, posy)
        qi1 = get_type_pos(posx + 1, posy)
        len0 = get_length_by_weight(aiMap[posx][posy]["l"])
        len1 = get_length_by_weight(aiMap[posx][posy]["r"])
        if qi0 == True:
            type_true[0 if len0 < 0 else 1][abs(len0) - 1] += 1
        elif qi0 == False:
            type_false[0 if len0 < 0 else 1][abs(len0) - 1] += 1
        if qi1 == True:
            type_true[0 if len1 < 0 else 1][abs(len1) - 1] += 1
        elif qi1 == False:
            type_false[0 if len1 < 0 else 1][abs(len1) - 1] += 1
        if abs(len0) == 4 or abs(len1) == 4:
            return True
        # if len0 == 3 or len1 == 3:
        #     return 2

    if judge_same_color(posx, posy - 1, posx, posy + 1):
        # 相同方向
        line = get_length_by_line_weight(aiMap[posx][posy]["d"], aiMap[posx][posy]["u"])
        if pos[posx][posy - 1]:
            type_true[(0 if line < 0 else 1)][abs(line) - 1] += 1
        else:
            type_false[(0 if line < 0 else 1)][abs(line) - 1] += 1

        if aiMap[posx][posy]["d"] + aiMap[posx][posy]["u"] >= 63:
            return True
    else:
        qi0 = get_type_pos(posx, posy - 1)
        qi1 = get_type_pos(posx, posy + 1)
        len0 = get_length_by_weight(aiMap[posx][posy]["u"])
        len1 = get_length_by_weight(aiMap[posx][posy]["d"])
        if qi0 == True:
            type_true[0 if len0 < 0 else 1][abs(len0) - 1] += 1
        elif qi0 == False:
            type_false[0 if len0 < 0 else 1][abs(len0) - 1] += 1
        if qi1 == True:
            type_true[0 if len1 < 0 else 1][abs(len1) - 1] += 1
        elif qi1 == False:
            type_false[0 if len1 < 0 else 1][abs(len1) - 1] += 1
        if abs(len0) == 4 or abs(len1) == 4:
            return True
        # if len0 == 3 or len1 == 3:
        #     return 2

    if judge_same_color(posx + 1, posy - 1, posx - 1, posy + 1):
        # 相同方向
        line = get_length_by_line_weight(aiMap[posx][posy]["ld"], aiMap[posx][posy]["ru"])
        if pos[posx + 1][posy - 1]:
            type_true[(0 if line < 0 else 1)][abs(line) - 1] += 1
        else:
            type_false[(0 if line < 0 else 1)][abs(line) - 1] += 1

        if aiMap[posx][posy]["ld"] + aiMap[posx][posy]["ru"] >= 63:
            return True
    else:
        qi0 = get_type_pos(posx + 1, posy - 1)
        qi1 = get_type_pos(posx - 1, posy + 1)
        len0 = get_length_by_weight(aiMap[posx][posy]["ru"])
        len1 = get_length_by_weight(aiMap[posx][posy]["ld"])
        if qi0 == True:
            type_true[0 if len0 < 0 else 1][abs(len0) - 1] += 1
        elif qi0 == False:
            type_false[0 if len0 < 0 else 1][abs(len0) - 1] += 1
        if qi1 == True:
            type_true[0 if len1 < 0 else 1][abs(len1) - 1] += 1
        elif qi1 == False:
            type_false[0 if len1 < 0 else 1][abs(len1) - 1] += 1
        if abs(len0) == 4 or abs(len1) == 4:
            return True
        # if len0 == 3 or len1 == 3:
        #     return 2

    if judge_same_color(posx - 1, posy - 1, posx + 1, posy + 1):
        # 相同方向
        line = get_length_by_line_weight(aiMap[posx][posy]["lu"], aiMap[posx][posy]["rd"])
        if pos[posx + 1][posy + 1]:
            type_true[(0 if line < 0 else 1)][abs(line) - 1] += 1
        else:
            type_false[(0 if line < 0 else 1)][abs(line) - 1] += 1

        if aiMap[posx][posy]["lu"] + aiMap[posx][posy]["rd"] >= 63:
            return True
    else:
        qi0 = get_type_pos(posx - 1, posy - 1)
        qi1 = get_type_pos(posx + 1, posy + 1)
        len0 = get_length_by_weight(aiMap[posx][posy]["lu"])
        len1 = get_length_by_weight(aiMap[posx][posy]["rd"])
        if qi0 == True:
            type_true[0 if len0 < 0 else 1][abs(len0) - 1] += 1
        elif qi0 == False:
            type_false[0 if len0 < 0 else 1][abs(len0) - 1] += 1
        if qi1 == True:
            type_true[0 if len1 < 0 else 1][abs(len1) - 1] += 1
        elif qi1 == False:
            type_false[0 if len1 < 0 else 1][abs(len1) - 1] += 1
        if abs(len0) == 4 or abs(len1) == 4:
            return True
        # if len0 == 3 or len1 == 3:
        #     return 2

    # 多行必胜棋
    if type_true[0][2] > 0 and (type_true[1][1] > 0 or type_true[0][2] > 1):  # 死三和活二  和双死三（活三、活四和死四已经检查过了）
        return 2
    if type_true[1][1] > 1:  # 两个活二
        return 2

    if type_false[1][1] > 1:  # 两个活二
        return 2
    if type_false[0][2] > 0 and (type_false[1][1] > 0 or type_false[0][2] > 1):
        return 2
    return False


# 两个方向的weight 死棋为正数 没有为0
def judeg_down_temp(w1, w2):
    if w1 + w2 == weights[0][0] + weights[0][1]:  # 判断是否左右为死一死二
        return True
    elif w1 + w2 == weights[0][0] + weights[0][0]:  # 两个都为死一
        return True
    elif w1 == 0 or w2 == 0:
        if w1 == weights[0][2] or w2 == weights[0][2]:  # 有一个为死三
            return True
        if w1 == weights[0][0] or w2 == weights[0][0]:  # 有一个为死一
            return True
        if w1 == weights[0][1] or w2 == weights[0][1]:  # 有一个为死二
            return True
    return False


# 判断下这个位置是否无用
def judge_down_disable(posx, posy):
    flag = 0

    if posx == 0 or posx == 14 or pos[posx - 1][posy] == pos[posx + 1][posy]:
        if judeg_down_temp(0 if posx == 0 else aiMap[posx][posy]["l"], 0 if posx == 14 else aiMap[posx][posy]["r"]):
            flag += 2
    elif pos[posx - 1][posy] != pos[posx + 1][posy] or pos[posx - 1][posy] != -1 and pos[posx + 1][posy] != -1:
        if judeg_down_temp(aiMap[posx][posy]["l"], 0):
            flag += 1
        if judeg_down_temp(aiMap[posx][posy]["r"], 0):
            flag += 1

    if posy == 0 or posy == 14 or pos[posx][posy - 1] == pos[posx][posy + 1]:
        if judeg_down_temp(0 if posy == 0 else aiMap[posx][posy]["u"], 0 if posy == 14 else aiMap[posx][posy]["d"]):
            flag += 2
    elif pos[posx][posy - 1] != pos[posx + 1][posy + 1] and pos[posx][posy - 1] != -1 and pos[posx + 1][posy + 1] != -1:
        if judeg_down_temp(aiMap[posx][posy]["u"], 0):
            flag += 1
        if judeg_down_temp(aiMap[posx][posy]["d"], 0):
            flag += 1

    if posy == 0 or posy == 14 or posx == 0 or posx == 14 or pos[posx + 1][posy - 1] == pos[posx - 1][posy + 1]:
        w1 = (0 if (posx == 14 or posy == 0) else aiMap[posx][posy]["ru"])
        w2 = (0 if (posx == 0 or posy == 14) else aiMap[posx][posy]["ld"])
        if judeg_down_temp(w1, w2):
            flag += 2
    elif pos[posx + 1][posy - 1] != pos[posx - 1][posy + 1] and pos[posx + 1][posy - 1] != -1 and pos[posx - 1][
        posy + 1] != -1:
        if judeg_down_temp(aiMap[posx][posy]["ru"], 0):
            flag += 1
        if judeg_down_temp(aiMap[posx][posy]["ld"], 0):
            flag += 1

    if posy == 0 or posy == 14 or posx == 0 or posx == 14 or pos[posx - 1][posy - 1] == pos[posx + 1][posy + 1]:
        w1 = (0 if (posx == 0 or posy == 0) else aiMap[posx][posy]["lu"])
        w2 = (0 if (posx == 14 or posy == 14) else aiMap[posx][posy]["rd"])
        if judeg_down_temp(w1, w2):
            flag += 2
    elif pos[posx - 1][posy - 1] != pos[posx + 1][posy + 1] and pos[posx - 1][posy - 1] != -1 and pos[posx + 1][
        posy + 1] != -1:
        if judeg_down_temp(aiMap[posx][posy]["rd"], 0):
            flag += 1
        if judeg_down_temp(aiMap[posx][posy]["lu"], 0):
            flag += 1
    return flag >= 8


# 得到最适合下棋的位置  可用优先队列减低时间复杂度 return {"x","y"}
def get_down_max_pos():
    temp = {"x": -1, "y": -1}
    f = False
    for i in range(15):
        for j in range(15):
            if pos[i][j] == -1:
                if temp["x"] < 0:
                    temp["x"] = i
                    temp["y"] = j
                retmp = judge_down_win(i, j)
                if retmp == 2:
                    print("retmp: " + str(retmp))
                    temp["x"] = i
                    temp["y"] = j

                    print(temp)
                    f = True
                if retmp == True:
                    temp["x"] = i
                    temp["y"] = j
                    print(temp)
                    print("TRUE")
                    return temp
                if not f and not judge_down_disable(i, j) and cmp(aiMap[i][j], aiMap[temp["x"]][temp["y"]]):
                    temp["x"] = i
                    temp["y"] = j

    return temp


# 输入用户最后下棋的位置 得到ai落子位置
def get_down_ai(userx, usery, tmp):
    init_weight(userx, usery, tmp)  # AI初始化 test
    return get_down_max_pos()


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
indexx, indexy = 7, 7

if is_aifirst:
    user = not user
    add_piece_handle(indexx, indexy)  # 落子
    init_weight(indexx, indexy, not user)  # AI初始化 test

while True:
    if user != firstUser:
        handle_ai_down(indexx, indexy, not user)  # 玩家落子后处理，处理对ai棋的影响，传入颜色为ai棋色
        init_weight(indexx, indexy, True)  # 玩家下棋后处理权重
        downai = get_down_max_pos()

        add_piece_handle(downai["x"], downai["y"])  # ai落子
        handle_ai_down(downai["x"], downai["y"], not user)  # 落子后处理，处理对用户棋的影响，传入颜色为ai棋色
        init_weight(downai["x"], downai["y"], not user, False)  # 处理weight对于ai的影响

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        # user==firstUser玩家下棋
        if event.type == pygame.MOUSEBUTTONDOWN and user == firstUser:
            # 获得鼠标位置
            x, y = pygame.mouse.get_pos()
            # judge replay
            if judge_replay(x, y):
                pro_init(rightfont, screen, font, bg)
                winstaus = False
                continue
            # judge first
            if judge_first(x, y):
                user = firstUser
                pro_init(rightfont, screen, font, bg)
                winstaus = False

            if winstaus:
                continue

            indexx = find_pos(x)
            indexy = find_pos(y)
            add_piece_handle(indexx, indexy)

        if event.type == pygame.KEYDOWN and winstaus:
            user = firstUser
            pro_init(rightfont, screen, font, bg)
            winstaus = False

    pygame.display.update()
# update Commodity set Stock = Stock+1
# select Id from Orders where `Status`= 1 and TIMESTAMPDIFF(HOUR,CreateTime,now())>3
# update Commodity,(select CommodityId,count(CommodityId) as number from Orders where `Status`= 6 and TIMESTAMPDIFF(HOUR,CreateTime,now())>3 group by CommodityId) a  set  Commodity.Stock=Commodity.Stock+a.number where Id=a.CommodityId
# CREATE PROCEDURE delete_order()
# delete from shop.Orders where shop.Orders.`Status`=6 and TIMESTAMPDIFF(HOUR,shop.Orders.CreateTime,now())>3;
