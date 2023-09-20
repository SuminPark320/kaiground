from tkinter import *
from tkinter import ttk
import tkinter.font
import math

from PIL import ImageTk, Image
import tkinter.messagebox, tkinter.simpledialog

import random
import pyperclip as clip


item_list = ["비타민", "단검", "대검", "포탈", "방탄복", "소화제", "포식자", "루나코인"]
def item_price(turn):
    pricelist=[100, 100, 150, 250, 350, 350]
    predator_price=(850,950,800,1000,900) # determine the price for 1, 3, 5, 7, 9 turn.
    lunacoin_price=(400,540,600,200,370) # determine the price for 1, 3, 5, 7, 9 turn.
    pricelist.append(predator_price[turn])
    pricelist.append(lunacoin_price[turn])
    return pricelist
user_items = []
user_items_name = []
other_items = []
player_list = []
player_list_other = []
explosion_list = []
budget = 1000

#variables
player_display_object_list = [] # append the oval object

class Table :
    def __init__(self,num,point,item,death):
        self.num = num
        self.point = point
        self.item = item
        self.death = death
table = []

# Coin and Item
class CNI :
    def __init__(self,coin,item):
        self.coin=coin
        self.item=item
cni = CNI(budget,"")


# initialize the graphics
root = Tk()


# setting font
turn_font=tkinter.font.Font(family='MS Serif', size=15, weight='bold')
table_font=tkinter.font.Font(family='MS Serif', size=14)
lbl_font=tkinter.font.Font(family='MS Serif', size=20, weight='bold')

root.option_add("*Font", table_font)
screen_width=root.winfo_screenwidth()
screen_height=root.winfo_screenheight()

width_resize=screen_width-350
height_resize=screen_height


# import map image
img=Image.open("map_revision_1.png")
mag1_img=Image.open("mag_1_tran.png")
mag2_img=Image.open("mag_2_tran.png")
explosion=Image.open("explosion2.png")
explosion_TK=ImageTk.PhotoImage(explosion)
img_TK=ImageTk.PhotoImage(img)
width = img_TK.width()
height = img_TK.height()
exp_w= explosion_TK.width()
exp_h= explosion_TK.height()

resize_ratio=min(width_resize*0.9/width,height_resize*0.9/height)
width=int(width*resize_ratio)
height=int(height*resize_ratio)
exp_w=int(exp_w*resize_ratio)
exp_h=int(exp_h*resize_ratio)

img=img.resize((width,height),Image.ANTIALIAS)
mag1_img=mag1_img.resize((width,height),Image.ANTIALIAS)
mag2_img=mag2_img.resize((width,height),Image.ANTIALIAS)
explosion=explosion.resize((exp_w*3,exp_h*3),Image.ANTIALIAS)

img=ImageTk.PhotoImage(img)
mag1_img=ImageTk.PhotoImage(mag1_img)
mag2_img=ImageTk.PhotoImage(mag2_img)
explosion=ImageTk.PhotoImage(explosion)


frm = Canvas(root, width=width, height=height)
frm.pack(side='left')
tab = Canvas(root, height=height, width=500, bg='white')
tab.pack(side='right')


# score table
style = ttk.Style()
style.configure("Treeview", font=table_font)
lbl = Label(tab, text="우리팀 현재 현황", bg='white', font=lbl_font)
lbl.pack()

treeview=ttk.Treeview(tab, columns= ["one", "two", "three","four"], displaycolumns=["one", "two", "three","four"])
treeview.pack()

treeview.column("#1", width=100, anchor = "center")
treeview.heading("one",text="플레이어 번호",anchor="center")

treeview.column("#2", width = 100, anchor="center")
treeview.heading("two", text="점수", anchor="center")

treeview.column("#3", width =180, anchor="center")
treeview.heading("three", text="장착한 아이템",anchor="center")

treeview.column("#4", width =100, anchor="center")
treeview.heading("four", text="소멸여부",anchor="center")

treeview["show"] = "headings" # 컬럼 제목만 보이게

treelist = []
for i in range(10) :
    pp = Table(i+1,0,"","")
    table.append(pp)
    treelist.append((i+1,0,"",""))
for i in range(len(treelist)):
    treeview.insert("","end", text=i, values=treelist[i],iid=str(i)+"번")

lbl1 = Label(tab, text="보유한 코인과 아이템", bg='white', font=lbl_font)
lbl1.pack()

treeview1=ttk.Treeview(tab, columns= ["one", "two"], displaycolumns=["one", "two"])
treeview1.pack()

treeview1.column("#1", width=130, anchor = "center")
treeview1.heading("one",text="코인",anchor="center")

treeview1.column("#2", width = 350, anchor="center")
treeview1.heading("two", text="보유한 아이템", anchor="center")

treeview1["show"] = "headings" # 컬럼 제목만 보이게

treelist1 = [(budget, "")]
treeview1.insert("","end", text=i, values=treelist1[0],iid=str(0)+"번")



background = frm.create_image(int(width/2), int(height/2), image=img)
turn_text = frm.create_text(width-90, 20, fill="black", text="플레이어 배치", font=turn_font)


root.title('창글리 경쟁 2조 흡수 게임')
root.state('zoomed')

class Building:
    def __init__(self, num, name, distance, position):
        self.players = []
        self.num = num
        self.name = name
        self.distance = distance
        self.special = 0
        self.position = position

    def append_player(self, player):
        self.players.append(player)
    
    def remove_player(self, player):
        self.players.remove(player)
    
    def move_distance(self, next):
        return self.distance[next-1]
    
    def players_name(self):
        result = []
        for p in self.players:
            if p.team == "my":
                result.append("%s 플레이어%d(%d)" %(p.team, p.key, p.score))
            else:
                result.append("%s 플레이어%d" %(p.team, p.key))
        return result

building_list = []
if True:
    building_list.append(Building(1, "북측기숙사", [0, 1, 1, 1, 2, 2, 3, 4, 5, 6, 6, 6, 6, 7, 7, 6, 3, 4, 5, 5], (225, 92)))
    building_list.append(Building(2, "기계공학동", [1, 0, 1, 2, 3, 2, 3, 4, 5, 6, 6, 6, 6, 7, 7, 6, 3, 4, 5, 5], (173, 191)))
    building_list.append(Building(3, "태울관", [1, 1, 0, 1, 2, 1, 2, 3, 4, 5, 5, 5, 5, 6, 6, 5, 2, 3, 4, 4], (295, 185)))
    building_list.append(Building(4, "카이마루", [1, 2, 1, 0, 1, 1, 2, 3, 4, 5, 5, 5, 5, 6, 6, 5, 2, 3, 4, 4], (352, 132)))
    building_list.append(Building(5, "산업디자인학과동", [2, 3, 2, 1, 0, 1, 2, 3, 4, 5, 5, 5, 5, 6, 6, 5, 2, 3, 4, 4], (464, 172)))
    building_list.append(Building(6, "스포츠컴플렉스", [2, 2, 1, 1, 1, 0, 1, 2, 3, 4, 4, 4, 4, 5, 5, 4, 1, 2, 3, 3], (400, 240)))
    building_list.append(Building(7, "창의학습관", [3, 3, 2, 2, 2, 1, 0, 1, 2, 3, 3, 3, 3, 4, 4, 3, 1, 1, 2, 2], (424, 384)))
    building_list.append(Building(8, "자연과학동", [4, 4, 3, 3, 3, 2, 1, 0, 1, 3, 4, 4, 4, 3, 3, 2, 2, 2, 3, 3], (584, 419)))
    building_list.append(Building(9, "의과학연구센터", [5, 5, 4, 4, 4, 3, 2, 1, 0, 2, 5, 4, 3, 2, 2, 1, 3, 3, 3, 4], (674, 407)))
    building_list.append(Building(10, "정보전자공학동", [6, 6, 5, 5, 5, 4, 3, 3, 2, 0, 3, 2, 1, 1, 2, 1, 4, 2, 1, 2], (653, 520)))
    building_list.append(Building(11, "학생회관", [6, 6, 5, 5, 5, 4, 3, 4, 5, 3, 0, 1, 2, 4, 5, 4, 4, 2, 2, 1], (161, 554)))
    building_list.append(Building(12, "응용공학동", [6, 6, 5, 5, 5, 4, 3, 4, 4, 2, 1, 0, 1, 3, 4, 3, 4, 2, 2, 1], (171, 640)))
    building_list.append(Building(13, "산업경영학동", [6, 6, 5, 5, 5, 4, 3, 4, 3, 1, 2, 1, 0, 2, 3, 2, 4, 2, 1, 1], (478, 608)))
    building_list.append(Building(14, "나노종합기술원", [7, 7, 6, 6, 6, 5, 4, 3, 2, 1, 4, 3, 2, 0, 1, 1, 5, 4, 3, 4], (693, 579)))
    building_list.append(Building(15, "바이오모델시스템파크", [7, 7, 6, 6, 6, 5, 4, 3, 2, 2, 5, 4, 3, 1, 0, 1, 5, 4, 3, 4], (826, 595)))
    building_list.append(Building(16, "파팔라도메디컬센터", [6, 6, 5, 5, 5, 4, 3, 2, 1, 1, 4, 3, 2, 1, 1, 0, 4, 3, 2, 3], (1002, 550)))
    building_list.append(Building(17, "본관", [3, 3, 2, 2, 2, 1, 1, 2, 3, 4, 4, 4, 4, 5, 5, 4, 0, 2, 3, 3], (316, 349)))
    building_list.append(Building(18, "학술문화관", [4, 4, 3, 3, 3, 2, 1, 2, 3, 2, 2, 2, 2, 4, 4, 3, 2, 0, 1, 1], (460, 452)))
    building_list.append(Building(19, "KI빌딩", [5, 5, 4, 4, 4, 3, 2, 3, 3, 1, 2, 2, 1, 3, 3, 2, 3, 1, 0, 1], (464, 542)))
    building_list.append(Building(20, "오리연못", [5, 5, 4, 4, 4, 3, 2, 3, 4, 2, 1, 1, 1, 4, 4, 3, 3, 1, 1, 0], (322, 564)))

class Player:
    def __init__(self, team, key, score, place, item = None):
        self.team = team
        self.key = key
        self.score = score
        self.place = place
        self.item = item
        self.state = 1
        self.shield = 0
        self.multi = 1.0
    
    def set_item(self, item):
        old_item = self.item
        if old_item == 4: #방탄복
            self.shield = 0
        elif old_item == 0: #비타민
            self.minus_score(1)
        self.item = item
        if self.team == "my":
            table[self.key - 1].item = item_list[item]
            treeview.item(str(self.key - 1) + "번", values=(table[self.key - 1].num, table[self.key - 1].point, table[self.key - 1].item, table[self.key - 1].death))
        if item == 0: #비타민
            self.plus_score(1)
            if self.team == "my":
                print("<비타민>을 사용하여 플레이어 %d의 점수가 %d가 되었습니다. <비타민> 해제할 시 점수가 다시 내려갑니다.\n" %(self.key, self.score))
                info("아이템: 비타민", "<비타민>을 사용하여 플레이어 %d의 점수가 %d가 되었습니다.\n<비타민> 해제할 시 점수가 다시 내려갑니다." % (self.key, self.score))
        elif item == 3: #포탈
            while True:
                try:
                    b = int(tkinter.simpledialog.askstring("아이템: 포탈", "플레이어 %d에게 <포탈>을 사용하였습니다.\n어디로 이동하시겠습니까?"%self.key))
                    if b > 20 or b < 1:
                        print("건물을 잘못 입력하였습니다. 다시 입력해주세요.")
                        tkinter.messagebox.showwarning("아이템: 포탈", "건물을 잘못 입력하였습니다.\n다시 입력해주세요.")
                    else :
                        break
                except ValueError:
                    print("건물을 잘못 입력하였습니다. 다시 입력해주세요.")
                    tkinter.messagebox.showwarning("아이템: 포탈", "건물을 잘못 입력하였습니다.\n다시 입력해주세요.")
            self.moveto(b)
            print("플레이어 %d를 %s로 이동하였습니다. <포탈>은 소멸되었습니다.\n" %(self.key, building_list[b-1].name))
            info("아이템: 포탈", "플레이어 %d를 %s로 이동하였습니다.\n<포탈>은 소멸되었습니다." %(self.key, building_list[b-1].name))
            self.item = None
            if self.team == "my" :
                table[self.key-1].item = ""
                treeview.item(str(self.key-1)+"번",values=(table[self.key-1].num,table[self.key-1].point,table[self.key-1].item,table[self.key-1].death))
        elif item == 4: #방탄복
            if self.team == "my":
                print("플레이어 %d에게 <방탄복>을 장착하였습니다. 장착하고 있는 동안 한 번의 상대팀 흡수를 방어할 수 있습니다.\n" %self.key)
                info("아이템: 방탄복", "플레이어 %d에게 <방탄복>을 장착하였습니다.\n장착하고 있는 동안 한 번의 상대팀 흡수를 방어할 수 있습니다."%self.key)
            self.shield = 1


    
    def moveto(self, n_place):
        cur_place = self.place
        self.place = n_place
        building_list[cur_place - 1].remove_player(self)
        building_list[n_place - 1].append_player(self)
        clear_player()
        show_player()
    
    def minus_score(self, s):
        global building_list
        self.score = self.score - s
        print("%s 플레이어 %d이(가) 점수 %d를 잃었습니다." %(self.team, self.key, s))
        if self.score <= 0:
            print("%s 플레이어 %d이(가) 점수를 잃어 소멸하였습니다." %(self.team, self.key))
            info("소멸", "%s 플레이어 %d이(가) 점수를 잃어 소멸하였습니다." %(self.team, self.key))
            self.state = 0
            self.score = 0
            building_list[self.place - 1].remove_player(self)
            if self.team == "my" :
                table[self.key-1].point = 0
                table[self.key-1].item = "-"
                table[self.key-1].death = "O"
                treeview.item(str(self.key-1)+"번",values=(table[self.key-1].num,table[self.key-1].point,table[self.key-1].item,table[self.key-1].death))
        if self.team == "my" :
            table[self.key-1].point = self.score
            treeview.item(str(self.key-1)+"번",values=(table[self.key-1].num,table[self.key-1].point,table[self.key-1].item,table[self.key-1].death))
        clear_player()
        show_player()
    
    def plus_score(self, s):
        self.score = self.score + s
        print("플레이어 %d이(가) 점수 %d를 얻었습니다.\n" %(self.key, s))
        if self.team == "my" :
            table[self.key-1].point = self.score
            treeview.item(str(self.key-1)+"번",values=(table[self.key-1].num,table[self.key-1].point,table[self.key-1].item,table[self.key-1].death))
        clear_player()
        show_player()

def cur_position():
    print("\n현재 배치")
    for b in building_list:
        if b.players != []:
            print(b.num, b.name, ":", b.players_name())
    clear_player()
    show_player()

def cur_items():
    if user_items == []:
        print("현재 보유한 아이템이 없습니다.")
    else:
        print_items = []
        for i in user_items:
            print_items.append(item_list[i])
        print("현재 보유한 아이템은", print_items, "입니다.\n")


special_building = []
def special(l):
    global special_building
    for i in special_building:
        building_list[i].special = 0
    special_building = []
    if len(l) == 5:
        for m in l:
            special_building.append(m)
            building_list[m].special = len(special_building)
    elif len(l) == 4:
        for m in l:
            special_building.append(m)
            building_list[m].special = len(special_building) + 1
    elif len(l) == 2:
        for m in l:
            special_building.append(m)
            building_list[m].special = len(special_building) + 3
    print("스페셜존이 리셋되었습니다.")

def special_print():
    global special_building
    special_building.sort()
    l = []
    for n in special_building:
        l.append((building_list[n].num, building_list[n].name))
    print("스페셜존 :", l, "\n")

def special_building_show():
    for index, building in enumerate(building_list):
        if building.special == 0:
            create_circle(building_list[index].position[0]*resize_ratio, building_list[index].position[1]*resize_ratio, 15, "black", "black", frm)
        else:
            create_circle(building_list[index].position[0]*resize_ratio, building_list[index].position[1]*resize_ratio, 15, "yellow", "yellow", frm)
        clear_player()
        show_player()

def info(title,text):
    tkinter.messagebox.showinfo(title,text)

def compete():
    global explosion_list, explosion
    for b in building_list:
        if len(b.players) > 1:
            my_score = 0
            other_score = 0
            my_team = []
            other_team = []
            for p in b.players:
                if p.team == "my":
                    my_score = my_score + p.score
                    my_team.append(p)
                else :
                    other_score = other_score + p.score
                    other_team.append(p)
            if (len(my_team) != 0) and (len(other_team) != 0):
                print("%d %s에서 경쟁이 발생하였습니다." %(b.num, b.name))
                boom = frm.create_image(int(b.position[0]*resize_ratio), int(b.position[1]*resize_ratio), image=explosion)
                explosion_list.append(boom)
                info("경쟁 발생!", "%d %s에서 경쟁이 발생하였습니다." %(b.num, b.name))
                my_str = "my 플레이어 "
                other_str = "other 플레이어 "
                for p in my_team:
                    my_str = my_str + str(p.key) + ", "
                for p in other_team:
                    other_str = other_str + str(p.key) + ", "
                print("[" + my_str[:-2] + "] vs [" + other_str[:-2] + "]")
                # 아이템 사용
                sending_message = ""
                except_item_my = []
                except_item_other = []
                for p in my_team:
                    if p.item in [1, 2, 5, 6, 7]:
                        while True:
                            use_item = tkinter.messagebox.askquestion("아이템 사용","플레이어 %d에게 <%s>가 장착되어 있습니다.\n이번 경쟁에서 사용하시겠습니까?" %(p.key, item_list[p.item]))
                            if use_item == "yes":
                                table[p.key - 1].item = ""
                                treeview.item(str(p.key - 1) + "번", values=(table[p.key - 1].num, table[p.key - 1].point, table[p.key - 1].item,table[p.key - 1].death))
                                if (p.item == 1 or p.item == 2) : #단검, 대검
                                    sending_message = sending_message + str(p.key) + " " + str(p.item) + "/"
                                    print("상대팀에게 <%s>를 사용하였습니다." %item_list[p.item])
                                    info("아이템: 단검, 대검","상대팀에게 <%s>를 사용하였습니다." %item_list[p.item])
                                    other_score = other_score - p.item
                                elif p.item == 5: #소화제
                                    sending_message = sending_message + str(p.key) + " " + str(p.item) + "/"
                                    print("플레이어 %d이(가) <%s>를 사용하여 경쟁에서 승리할 시 점수를 2배로 얻을 수 있습니다." %(p.key, item_list[p.item]))
                                    info("아이템: 소화제", "플레이어 %d이(가) <%s>를 사용하여 경쟁에서 승리할 시 점수를 2배로 얻을 수 있습니다." %(p.key, item_list[p.item]))
                                    p.multi = p.multi * 2.0
                                elif p.item == 6 or p.item == 7: #포식자, 루나코인
                                    sending_message = sending_message + str(p.key) + " " + str(p.item) + "/"
                                    except_item_my.append(p.item)
                                    print("플레이어 %d이(가) <%s>를 사용하였습니다." %(p.key, item_list[p.item]))
                                    info("아이템: 포식자, 루나코인", "플레이어 %d이(가) <%s>를 사용하였습니다." %(p.key, item_list[p.item]))
                                p.item = None
                                break
                            elif use_item == "no":
                                break
                            else:
                                print("다시 입력해주세요.")
                                continue
                print("상대팀한테 아래의 메세지를 전달해주세요")
                print(sending_message)
                if sending_message != "":
                    clip.copy(sending_message)
                    tkinter.messagebox.showinfo("우리팀 코드", sending_message + '\n\n' + "상대팀한테 위의 메세지를 전달해주세요.\n(클립보드에 복사 되었습니다)")
                else:
                    tkinter.messagebox.showinfo("우리팀 코드", "상대팀한테 전달할 메세지가 없습니다.")
                l = tkinter.simpledialog.askstring("상대팀 코드", "상대팀이 사용한 아이템이 있다면\n전달받은 값을 입력해주세요.",show='*')
                l = l.split("/")
                for a in l[:-1]:
                    a = a.split(" ")
                    a[0] = int(a[0])
                    a[1] = int(a[1])
                    p = player_list_other[a[0] - 1]
                    if a[1] == 1 or a[1] == 2: #단검, 대검
                        print("상대팀이 우리팀에게 <%s>를 사용하였습니다." %item_list[a[1]])
                        info("아이템: 단검, 대검", "상대팀이 우리팀에게 <%s>를 사용하였습니다." %item_list[a[1]])
                        my_score = my_score - a[1]
                    elif a[1] == 5: #소화제
                        print("상대팀 플레이어 %d이(가) <%s>를 사용하여 경쟁에서 승리할 시 점수를 2배로 얻습니다." %(a[0], item_list[a[1]]))
                        info("아이템: 소화제", "상대팀 플레이어 %d이(가) <%s>를 사용하여 경쟁에서 승리할 시 점수를 2배로 얻습니다." %(a[0], item_list[a[1]]))
                        p.multi = p.multi * 2.0
                    elif a[1] == 6 or a[1] == 7: #포식자, 루나코인
                        except_item_other.append(a[1])
                        print("상대팀 플레이어 %d이(가) <%s>를 사용하였습니다." %(a[0], item_list[a[1]]))
                        info("아이템: 포식자, 루나코인", "상대팀 플레이어 %d이(가) <%s>를 사용하였습니다." %(a[0], item_list[a[1]]))
                    p.item = None
                
                while (6 in except_item_my) and (6 in except_item_other):
                    print("두 팀 모두 <포식자>를 사용하였습니다. 아이템은 소멸됩니다.")
                    info("아이템: 포식자, 루나코인", "두 팀 모두 <포식자>를 사용하였습니다. 아이템은 소멸됩니다.")
                    except_item_my.remove(6)
                    except_item_other.remove(6)
                
                while (7 in except_item_my) and (7 in except_item_other):
                    print("두 팀 모두 <루나코인>을 사용하였습니다. 아이템은 소멸됩니다.")
                    info("아이템: 포식자, 루나코인", "두 팀 모두 <루나코인>를 사용하였습니다. 아이템은 소멸됩니다.")
                    except_item_my.remove(7)
                    except_item_other.remove(7)
                
                if 6 in except_item_my:
                    print("축하합니다. 상대팀을 이겼습니다.")
                    info("승패 결과", "축하합니다. 상대팀을 이겼습니다.")
                    other_str = "other 플레이어 "
                    for p in other_team:
                        if p.shield == 0:
                            other_str = other_str + str(p.key) + ", "
                            p.state = 0
                            building_list[p.place - 1].remove_player(p)
                        else :
                            print("상대팀 플레이어 %d이(가) <방탄복>을 사용하여 살아남았습니다." %p.key)
                            info("예외", "상대팀 플레이어 %d이(가) <방탄복>을 사용하여 살아남았습니다." %p.key)
                            p.multi = 1.0
                            p.item = None
                            p.shield = 0
                            other_score -= p.score
                    if other_str != "other 플레이어 ":
                        gs = other_score / (2 * len(my_team))
                        print("상대팀 %s은(는) 소멸하였습니다. 상대 플레이어를 흡수하여 %s이(가) 점수 %d를 얻었습니다." %(other_str[:-2], my_str[:-2], gs))
                        info("소멸", "상대팀 %s은(는) 소멸하였습니다. 상대 플레이어를 흡수하여 %s이(가) 점수 %d를 얻었습니다." %(other_str[:-2], my_str[:-2], gs))
                        for p in my_team:
                            p.score = p.score + int(p.multi * gs)
                            table[p.key - 1].point = p.score
                            treeview.item(str(p.key - 1) + "번", values=(table[p.key - 1].num, table[p.key - 1].point, table[p.key - 1].item, table[p.key - 1].death))
                            if p.multi != 1.0:
                                print("플레이어 %d이(가) 기존 점수의 %f배를 획득하였습니다." %(p.key, p.multi))
                                info("흡수 점수 예외", "플레이어 %d이(가) 기존 점수의 %f배를 획득하였습니다." %(p.key, p.multi))
                                p.multi = 1.0
                    print("\n")
                elif 6 in except_item_other:
                    print("상대팀에게 흡수당했습니다.")
                    info("승패결과", "상대팀에게 흡수당했습니다.")
                    my_str = "my 플레이어 "
                    for p in my_team:
                        if p.shield == 0:
                            my_str = my_str + str(p.key) + ", "
                            p.state = 0
                            building_list[p.place - 1].remove_player(p)
                            table[p.key - 1].point = 0
                            table[p.key - 1].item = "-"
                            table[p.key - 1].death = "O"
                            treeview.item(str(p.key - 1) + "번", values=(table[p.key - 1].num, table[p.key - 1].point, table[p.key - 1].item,table[p.key - 1].death))
                        else:
                            print("플레이어 %d이(가) <방탄복>을 사용하여 살아남았습니다." %p.key)
                            info("예외", "플레이어 %d이(가) <방탄복>을 사용하여 살아남았습니다." %p.key)
                            p.multi = 1.0
                            p.item = None
                            p.shield = 0
                            my_score -= p.score
                            table[p.key - 1].item = ""
                            treeview.item(str(p.key - 1) + "번", values=(
                            table[p.key - 1].num, table[p.key - 1].point, table[p.key - 1].item,table[p.key - 1].death))
                    if my_str != "my 플레이어 ":
                        gs = my_score / (2 * len(other_team))
                        print("%s이(가) 소멸하였습니다.상대 플레이어는 점수 %d를 얻었습니다." %(my_str[:-2], gs))
                        info("소멸", "%s이(가) 소멸하였습니다.상대 플레이어는 점수 %d를 얻었습니다." %(my_str[:-2], gs))
                        for p in other_team:
                            p.score = p.score + int(p.multi * gs)
                            if p.multi != 1.0:
                                print("상대팀 플레이어 %d은(는) 기존 점수의 %f배를 획득하였습니다." %(p.key, p.multi))
                                p.multi = 1.0
                    print("\n")
                elif ((7 not in except_item_my) and (7 not in except_item_other) and (my_score > other_score)) or ((7 in except_item_my) and (my_score < other_score)) or ((7 in except_item_other) and (my_score < other_score)):
                    print("축하합니다. 상대팀을 이겼습니다.")
                    info("승패 결과", "축하합니다. 상대팀을 이겼습니다.")
                    other_str = "other 플레이어 "
                    for p in other_team:
                        if p.shield == 0:
                            other_str = other_str + str(p.key) + ", "
                            p.state = 0
                            building_list[p.place - 1].remove_player(p)
                        else :
                            print("상대팀 플레이어 %d이(가) <방탄복>을 사용하여 살아남았습니다." %p.key)
                            info("예외", "상대팀 플레이어 %d이(가) <방탄복>을 사용하여 살아남았습니다." %p.key)
                            p.multi = 1.0
                            p.item = None
                            p.shield = 0
                            other_score -= p.score
                    if other_str != "other 플레이어 ":
                        gs = other_score / (2 * len(my_team))
                        print("상대팀 %s은(는) 소멸하였습니다. 상대 플레이어를 흡수하여 %s이(가) 점수 %d를 얻었습니다." %(other_str[:-2], my_str[:-2], gs))
                        info("소멸", "상대팀 %s은(는) 소멸하였습니다. 상대 플레이어를 흡수하여 %s이(가) 점수 %d를 얻었습니다." %(other_str[:-2], my_str[:-2], gs))
                        for p in my_team:
                            p.score = p.score + int(p.multi * gs)
                            table[p.key - 1].point = p.score
                            treeview.item(str(p.key - 1) + "번", values=(table[p.key - 1].num, table[p.key - 1].point, table[p.key - 1].item, table[p.key - 1].death))
                            if p.multi != 1.0:
                                print("플레이어 %d이(가) 기존 점수의 %f배를 획득하였습니다." %(p.key, p.multi))
                                info("흡수 점수 예외", "플레이어 %d이(가) 기존 점수의 %f배를 획득하였습니다." %(p.key, p.multi))
                                p.multi = 1.0
                    print("\n")
                elif (my_score < other_score) or ((7 in except_item_my) and (my_score > other_score)) or ((7 in except_item_other) and (my_score > other_score)):
                    print("상대팀에게 흡수당했습니다.")
                    info("승패결과", "상대팀에게 흡수당했습니다.")
                    my_str = "my 플레이어 "
                    for p in my_team:
                        if p.shield == 0:
                            my_str = my_str + str(p.key) + ", "
                            p.state = 0
                            building_list[p.place - 1].remove_player(p)
                            table[p.key - 1].point = 0
                            table[p.key - 1].item = "-"
                            table[p.key - 1].death = "O"
                            treeview.item(str(p.key - 1) + "번", values=(table[p.key - 1].num, table[p.key - 1].point, table[p.key - 1].item,table[p.key - 1].death))
                        else:
                            print("플레이어 %d이(가) <방탄복>을 사용하여 살아남았습니다." %p.key)
                            info("예외", "플레이어 %d이(가) <방탄복>을 사용하여 살아남았습니다." %p.key)
                            p.multi = 1.0
                            p.item = None
                            p.shield = 0
                            my_score -= p.score
                            table[p.key - 1].item = ""
                            treeview.item(str(p.key - 1) + "번", values=(
                            table[p.key - 1].num, table[p.key - 1].point, table[p.key - 1].item,table[p.key - 1].death))
                    if my_str != "my 플레이어 ":
                        gs = my_score / (2 * len(other_team))
                        print("%s이(가) 소멸하였습니다.상대 플레이어는 점수 %d를 얻었습니다." %(my_str[:-2], gs))
                        info("소멸", "%s이(가) 소멸하였습니다.상대 플레이어는 점수 %d를 얻었습니다." %(my_str[:-2], gs))
                        for p in other_team:
                            p.score = p.score + int(p.multi * gs)
                            if p.multi != 1.0:
                                print("상대팀 플레이어 %d은(는) 기존 점수의 %f배를 획득하였습니다." %(p.key, p.multi))
                                p.multi = 1.0
                    print("\n")
                else :
                    for p in my_team:
                        p.multi = 1.0
                    for p in other_team:
                        p.multi = 1.0
                    print("무승부입니다.\n")
                    info("무승부", "무승부입니다.")
    clear_player()
    show_player()

def create_circle(x, y, r, fill, outline, canvasName): #center coordinates, radius
    x0 = int(x - r)
    y0 = int(y - r)
    x1 = int(x + r)
    y1 = int(y + r)
    return canvasName.create_oval(x0, y0, x1, y1, fill=fill, outline=outline)


def circle_radius(score):
    return 6*math.sqrt(score)


def show_player():
    global player_display_object_list
    for building in building_list:
        my_list = []
        other_list = []
        for index, player in enumerate(building.players):
            if player.team == "my":
                my_list.append(player)
            elif player.team == "other":
                other_list.append(player)
        # display red team
        for index, player in enumerate(my_list):
            if player.item != None:  # if item placed
                my_man = create_circle(resize_ratio*(building.position[0] - len(my_list) * 20 / 2 + index * 20), resize_ratio*(building.position[1]-10), circle_radius(player.score + 1), "magenta", "white", frm)
                my_man_text = frm.create_text(resize_ratio*(building.position[0] - len(my_list) * 20 / 2 + index * 20), resize_ratio*(building.position[1]-10), fill="white", text=str(player.key))
            else:
                my_man = create_circle(resize_ratio*(building.position[0] - len(my_list) * 20 / 2 + index * 20), resize_ratio*(building.position[1] - 10), circle_radius(player.score + 1), "red", "white", frm)
                my_man_text = frm.create_text(resize_ratio*(building.position[0] - len(my_list) * 20 / 2 + index * 20), resize_ratio*(building.position[1] - 10), fill="white", text=str(player.key))
            player_display_object_list.append(my_man)
            player_display_object_list.append(my_man_text)
        # display blue team
        for index, player in enumerate(other_list):
            o_man = create_circle(resize_ratio*(building.position[0] - len(other_list) * 20 / 2 + index * 20), resize_ratio*(building.position[1] + 10), 10, "blue", "white", frm)
            o_man_text = frm.create_text(resize_ratio*(building.position[0] - len(other_list) * 20 / 2 + index * 20), resize_ratio*(building.position[1] + 10), fill="white", text=str(player.key))
            player_display_object_list.append(o_man)
            player_display_object_list.append(o_man_text)



def clear_player():
    global player_display_object_list
    for obj in player_display_object_list:
        frm.delete(obj)


sending_message = ""
#초기 세팅
coin = budget
print("플레이어의 점수와 초기 위치를 입력해주세요.")
tkinter.messagebox.showinfo("플레이어 초기 위치", "플레이어의 점수와 초기 위치를 입력해주세요")
score_check = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
for i in range(1, 11):
    while True:
        try:
            score = tkinter.simpledialog.askinteger("플레이어 %d"%i, "플레이어 %d의 점수를\n입력해주세요. : " %i)
            if score in score_check:
                score_check.remove(score)
                break
            else:
                print("점수를 잘못 입력하였습니다. 다시 입력해주세요.")
                tkinter.messagebox.showwarning("플레이어 %d"%i, "점수를 잘못 입력하였습니다.\n다시 입력해주세요.")
        except ValueError:
            print("점수를 잘못 입력하였습니다. 다시 입력해주세요.")
            tkinter.messagebox.showwarning("플레이어 %d" % i, "점수를 잘못 입력하였습니다.\n다시 입력해주세요.")
    while True:
        try:
            place = tkinter.simpledialog.askinteger("플레이어 %d"%i, "플레이어 %d의 초기 위치를 어디로 설정할까요?\n건물 번호를 입력해주세요." %i)
            if place > 20 or place < 1:
                print("건물을 잘못 입력하였습니다. 다시 입력해주세요.")
                tkinter.messagebox.showwarning("플레이어 %d" % i, "건물을 잘못 입력하였습니다.\n다시 입력해주세요.")
            else:
                break
        except ValueError:
            print("건물을 잘못 입력하였습니다. 다시 입력해주세요.")
            tkinter.messagebox.showwarning("플레이어 %d" % i, "건물을 잘못 입력하였습니다.\n다시 입력해주세요.")
    cur_player = Player("my", i, score, place)
    player_list.append(cur_player)
    building_list[place-1].append_player(cur_player)
    table[i - 1].point = score
    treeview.item(str(i - 1) + "번",values=(table[i - 1].num, table[i - 1].point, table[i - 1].item, table[i - 1].death))
    clear_player()
    show_player()
for p in player_list:
    sending_message = sending_message +str(p.score) + " " + str(p.place) + "/"
print("\n상대팀한테 아래의 메세지를 전달해주세요.")
print(sending_message)
clip.copy(sending_message)
tkinter.messagebox.showinfo("우리팀 코드", sending_message+'\n\n'+"상대팀한테 위의 메세지를 전달해주세요.\n(클립보드에 복사 되었습니다)")

while True :
        l = tkinter.simpledialog.askstring("상대팀 코드", "상대팀한테\n전달받은 값을 입력해주세요.",show='*')
        if (l != None) and (len(l) > 10) :
            break

#l = tkinter.simpledialog.askstring("상대팀 코드", "상대팀한테\n전달받은 값을 입력해주세요.",show='*')
l = l.split("/")
for i in range(1, 11):
    a = l[i - 1].split(" ")
    cur_player = Player("other", i, int(a[0]), int(a[1]))
    player_list_other.append(cur_player)
    building_list[cur_player.place - 1].append_player(cur_player)
cur_position()
clear_player()
show_player()
frm.delete(turn_text)

#게임 시작
for i in range(1, 11):
    sending_message = ""
    print("\n%d번째 턴입니다!\n" %i)
    frm.delete(turn_text)
    turn_text = frm.create_text(width - 70, 20, fill="black", text=str(i)+"번째 턴", font=turn_font)
    if i == 1: special([0, 6, 12, 2, 5])
    elif i == 4: special([15, 5, 11, 8, 1])
    elif i == 7: special([12, 16, 8, 3])

    special_print()
    special_building_show()

    if i == 4 or i == 5:
        print("%d턴 뒤에 자기장이 나타납니다.\n" %(7 - i))
        tkinter.messagebox.showwarning("자기장 주의", "%d턴 뒤에\n자기장이 나타납니다." %(7 - i))
    elif i >= 6 and i < 9:
        print("현재 자기장 : 1 북측기숙사, 2 기계공학동, 11 학생회관, 12 응용공학동, 14 나노종합기술원, 15 바이오모델시스템파크, 16 파팔라도")
        if i == 6:
            mag_1 = frm.create_image(int(width / 2), int(height / 2), image=mag1_img)
            tkinter.messagebox.showerror("자기장 경고", "자기장 구역이\n생겼습니다")
        else:
            print("%d턴 뒤에 자기장이 추가됩니다." %(10 - i))
            tkinter.messagebox.showwarning("자기장 주의", "%d턴 뒤에\n자기장이 추가됩니다." % (10 - i))
        for p in player_list:
            if (p.state == 1) and (p.place in [1, 2, 11, 12, 14, 15, 16]):
                print("플레이어 %d이(가) 자기장 영역에 있습니다." %p.key)
                p.minus_score(1)
        for p in player_list_other:
            if (p.state == 1) and (p.place in [1, 2, 11, 12, 14, 15, 16]):
                print("상대 플레이어 %d이(가) 자기장 영역에 있습니다." %p.key)
                p.minus_score(1)
        print("\n")
    
    elif i >= 9:
        print("현재 자기장 : 1 북측기숙사, 2 기계공학동, 3 태울관, 4 카이마루, 9 의과학연구센터, 11 학생회관, 12 응용공학동, 14 나노종합기술원, 15 바이오모델시스템파크, 16 파팔라도, 20 오리연못")
        if i == 9:
            frm.delete(mag_1)
            mag_2 = frm.create_image(int(width / 2), int(height / 2), image=mag2_img)
            tkinter.messagebox.showerror("자기장 경고", "자기장 구역이\n바뀌었습니다")
        for p in player_list:
            if (p.state == 1) and (p.place in [1, 2, 3, 4, 9, 11, 12, 14, 15, 16, 20]):
                print("플레이어 %d이(가) 자기장 영역에 있습니다." %p.key)
                p.minus_score(i - 8)
        for p in player_list_other:
            if (p.state == 1) and (p.place in [1, 2, 3, 4, 9, 11, 12, 14, 15, 16, 20]):
                print("상대 플레이어 %d이(가) 자기장 영역에 있습니다." %p.key)
                p.minus_score(i - 8)
        print("\n")
    
    #상점 이용
    if i%2 == 1:
        index=i//2
        item_list_str = "비타민(100): 장착하고 있는 동안 점수 1 높여줌"+"\n"+"단검(100): 경쟁 시 상대 총 점수 -1"+"\n"+"대검(150): 경쟁 시 상대 총 점수 -2"+"\n"+"포탈(250): 장착 즉시 원하는 건물로 이동"+"\n"+"방탄복(350): 한 번의 흡수 방어"+"\n"+"소화제(300): 상대팀 흡수 시 얻는 점수 2배"+"\n"+"포식자(" + str(item_price(index)[6]) + "): 점수와 관계없이 상대팀 흡수"+"\n"+"루나코인(" + str(item_price(index)[7]) + "): 흡수 결과 반대로 뒤집음"
        while True:
            if coin < 100:
                print("현재 보유한 코인은 %d입니다. 아이템 상점을 이용할 수 없습니다." %coin)
                tkinter.messagebox.showwarning("아이템 상점", "현재 보유한 코인은 %d입니다.\n아이템 상점을 이용할 수 없습니다." %coin)
                break
            market = tkinter.messagebox.askquestion("아이템 상점", "현재 보유한 코인은 %d입니다.\n아이템 상점을 이용하겠습니까?" %coin)
            if market == "yes":
                new_item = tkinter.simpledialog.askstring("아이템 상점", "어떤 아이템을 구입하겠습니까?\n\n"+item_list_str+"\n\n아이템 이름을 입력해주세요.")
                if new_item == None:
                    yesno=tkinter.messagebox.askquestion("아이템 상점", "아이템을 구매하지 않으시겠습니까?\n상점으로 다시 되돌아 올 수 없습니다.")
                    if yesno == 'yes':
                        tkinter.messagebox.showwarning("아이템 상점","상점에서 빠져나왔습니다!")
                        break
                while not new_item in item_list:
                    new_item = tkinter.simpledialog.askstring("아이템 상점", "아이템을 잘못 입력하였습니다.\n\n"+item_list_str+"\n\n다시 입력해주세요.")
                price = item_price(index)[item_list.index(new_item)]
                if coin < price :
                    print("코인이 부족합니다. 현재 보유 코인 : %d / <%s> 가격 : %d" %(coin, new_item, price))
                    tkinter.messagebox.showwarning("아이템 상점", "코인이 부족합니다.\n현재 보유 코인 : %d / <%s> 가격 : %d" %(coin, new_item, price))
                else :
                    coin = coin - price
                    user_items.append(item_list.index(new_item))
                    user_items_name.append(new_item)
                    print("감사합니다. <%s>을(를) 구입하였습니다. %d 코인이 남았습니다." %(new_item, coin))
                    tkinter.messagebox.showinfo("아이템 상점", "감사합니다.\n<%s>을(를) 구입하였습니다.\n%d 코인이 남았습니다." %(new_item, coin))
                    cur_items()
                    cni.coin = coin
                    cni.item = ""
                    for i in user_items_name :
                        cni.item = cni.item + "\n" + i
                    treeview1.item(str(0) + "번", values=(cni.coin, cni.item))
            elif market == "no":
                print("상점 이용을 종료하였습니다.")
                cur_items()
                break
            else :
                continue

    #미니게임
    if i == 2 or i == 6:
        print("미니게임 턴입니다. 미니게임을 진행해주세요.")
        while True:
            mini = tkinter.messagebox.askquestion("미니게임", "미니게임을 성공하였나요?")
            if  mini == "yes" :
                num = random.randrange(2, 6)
                user_items.append(num)
                user_items_name.append(item_list[num])
                print("<%s> 아이템을 획득하였습니다.\n" %item_list[num])
                cni.item = ""
                for i in user_items_name :
                    cni.item = cni.item + "\n" + i
                treeview1.item(str(0) + "번", values=(cni.coin, cni.item))
                tkinter.messagebox.showinfo("미니게임", "<%s> 아이템을 획득하였습니다.\n" %item_list[num])
                break
            elif mini == "no" :
                break
            else :
                continue
    
    #플레이어 행동
    j = 5
    while j > 0:
        while True:
            try:
                action = tkinter.simpledialog.askstring("\n%d번째 행동"%(6-j), "행동 명령어를 규칙에 맞게 입력해주세요. ex) M 1 13 또는 I 3")
                action = action.split(" ")
                # 이동
                if action[0] == "M":
                    action[1] = int(action[1])
                    action[2] = int(action[2])
                    player_n = action[1]
                    if (player_n > 0) and (player_n <= 10) and (player_list[player_n - 1].state != 0):
                        player = player_list[player_n - 1]
                        cur_place = player.place
                        next_place = action[2]
                        if (next_place > 0) and (next_place <= 20):
                            d = building_list[cur_place - 1].move_distance(next_place)
                            if d != 0:
                                if j >= d:
                                    j = j - d
                                    player.moveto(next_place)
                                    print("플레이어 %d을(를) %s(으)로 이동하였습니다." %(player_n, building_list[player.place - 1].name))
                                    sending_message = sending_message + "M " + str(player_n) + " " + str(player.place) + "/"
                                    special_n = building_list[player.place - 1].special
                                    clear_player()
                                    show_player()
                                    #스페셜존
                                    if special_n != 0:
                                        if special_n <= 3:
                                            print("축하합니다! 코인 존입니다. 스페셜존 이용권을 사용하시겠습니까?")
                                            if tkinter.messagebox.askyesno("코인 존 미션", "축하합니다! 코인 존입니다.\n스페셜존 이용권을 사용하시겠습니까?"):
                                                coin = coin + 50 * (special_n + 1)
                                                print("%d 코인을 얻어 현재 %d 코인입니다." %(50 * (special_n + 1), coin))
                                                cni.coin = coin
                                                treeview1.item(str(0) + "번", values=(cni.coin, cni.item))
                                                tkinter.messagebox.showinfo("코인 존 미션", "%d 코인을 얻어 현재 %d 코인입니다." %(50 * (special_n + 1), coin))
                                            else:
                                                tkinter.messagebox.showwarning("코인 존 미션", "미션에 실패하여\n코인이 지급되지 않았습니다.")

                                        else:
                                            print("축하합니다! 점수 +존입니다. 스페셜존 이용권을 사용하시겠습니까?")
                                            if tkinter.messagebox.askyesno("점수 +존 미션", "축하합니다! 점수 +존입니다.\n스페셜존 이용권을 사용하시겠습니까?"):
                                                player.plus_score(1 * (special_n - 3))
                                                # table[player_n - 1].point += 1*(special_n-3)
                                                treeview.item(str(player_n - 1) + "번", values=(table[player_n - 1].num, table[player_n - 1].point, table[player_n - 1].item,table[player_n - 1].death))
                                                sending_message = sending_message + "P " + str(player_n) + " " + str(1 * (special_n - 3)) + "/"
                                                tkinter.messagebox.showinfo("점수 +존 미션", "%d 점을 얻어 현재 %d 점입니다." %(1 * (special_n - 3), player.score))
                                            else:
                                                tkinter.messagebox.showwarning("점수 +존 미션", "미션에 실패하여\n점수가 지급되지 않았습니다.")
                                        print("\n")
                                        special_building.remove(player.place - 1)
                                        building_list[player.place - 1].special = 0
                                        special_building_show()
                                        sending_message = sending_message + "S " + str(player.place - 1) + "/"
                                    clear_player()
                                    show_player()
                                    break
                                else:
                                    print("거리가 너무 멉니다. %d칸 이내로 이동해주세요." %j)
                                    tkinter.messagebox.showwarning("플레이어 이동", "거리가 너무 멉니다.\n%d칸 이내로 이동해주세요." %j)
                            else:
                                print("현재 위치로는 이동할 수 없습니다." )
                                tkinter.messagebox.showwarning("플레이어 이동", "현재 위치로는 이동할 수 없습니다." )
                        else: 
                            print("건물을 잘못 입력하였습니다. 다시 입력해주세요.")
                            tkinter.messagebox.showwarning("플레이어 이동", "건물을 잘못 입력하였습니다.\n다시 입력해주세요.")
                    else:
                        print("플레이어를 잘못 입력하였습니다. 다시 입력해주세요.")
                        tkinter.messagebox.showwarning("플레이어 이동", "플레이어를 잘못 입력하였습니다.\n다시 입력해주세요.")
                # 아이템 장착
                elif action[0] == "I":
                    if len(user_items) == 0:
                        print("보유한 아이템이 없습니다.")
                        tkinter.messagebox.showwarning("아이템 장착", "보유한 아이템이 없습니다.")
                        continue
                    action[1] = int(action[1])
                    player_n = action[1]
                    if (player_n > 0) and (player_n <= 10) and (player_list[player_n - 1].state != 0):
                        print("현재 보유하고 있는 아이템 목록입니다.")
                        user_items_str = ''
                        for k in range(len(user_items)):
                            print(k, ":", item_list[user_items[k]])
                            user_items_str= user_items_str+'\n'+str(k)+' : '+item_list[user_items[k]]
                            print(user_items_str)
                        player = player_list[player_n - 1]
                        item_n = tkinter.simpledialog.askinteger("아이템 장착", "플레이어 %d에게 어떤 아이템을 장착할까요?\n"%player_n+user_items_str+"\n번호를 입력해주세요.")
                        if item_n >= len(user_items) or item_n < 0:
                            print("아이템 번호를 잘못 입력하였습니다. 다시 입력해주세요.")
                            tkinter.messagebox.showwarning("아이템 장착", "아이템 번호를 잘못 입력하였습니다.\n다시 입력해주세요.")
                            continue
                        player.set_item(user_items[item_n])
                        user_items_name.remove(item_list[user_items[item_n]])
                        cni.item = ""
                        for i in user_items_name :
                            cni.item = cni.item + "\n" + i
                        treeview1.item(str(0) + "번", values=(cni.coin, cni.item))
                        clear_player()
                        show_player()
                        if user_items[item_n] == 3: #포탈
                            sending_message = sending_message + "M " + str(player_n) + " " + str(player.place) + "/"
                            special_n = building_list[player.place - 1].special
                            if special_n != 0:
                                if special_n <= 3:
                                    print("축하합니다! 코인 존입니다. 스페셜존 이용권을 사용하시겠습니까?")
                                    if tkinter.messagebox.askyesno("코인 존 미션", "축하합니다! 코인 존입니다.\n스페셜존 이용권을 사용하시겠습니까?"):
                                        coin = coin + 50 * (special_n + 1)
                                        cni.coin = coin
                                        treeview1.item(str(0) + "번", values=(cni.coin, cni.item))
                                        print("%d 코인을 얻어 현재 %d 코인입니다." % (50 * (special_n + 1), coin))
                                        tkinter.messagebox.showinfo("코인 존 미션",
                                                                    "%d 코인을 얻어 현재 %d 코인입니다." % (50 * (special_n + 1), coin))
                                    else:
                                        tkinter.messagebox.showwarning("코인 존 미션", "미션에 실패하여\n코인이 지급되지 않았습니다.")
                                elif special_n <= 5:
                                    print("축하합니다! 점수 +존입니다. 스페셜존 이용권을 사용하시겠습니까?")
                                    if tkinter.messagebox.askyesno("점수 +존 미션", "축하합니다! 점수 +존입니다.\n스페셜존 이용권을 사용하시겠습니까?"):
                                        player.plus_score(1 * (special_n - 3))
                                        table[player_n-1].point+=1*(special_n-3)
                                        treeview.item(str(player_n-1)+"번",values=(table[player_n-1].num,table[player_n-1].point,table[player_n-1].item,table[player_n-1].death))
                                        sending_message = sending_message + "P " + str(player_n) + " " + str(1 * (special_n - 3)) + "/"
                                    else:
                                        tkinter.messagebox.showwarning("점수 +존 미션", "미션에 실패하여\n점수가 지급되지 않았습니다.")
                                    print("\n")
                                special_building.remove(player.place - 1)
                                building_list[player.place - 1].special = 0
                                sending_message = sending_message + "S " + str(player.place - 1) + "/"
                        else:
                            sending_message = sending_message + "I " + str(player_n) + " " + str(user_items[item_n]) + "/"
                        del user_items[item_n]
                        j = j - 1
                        break
                    else:
                        print("플레이어를 잘못 입력하였습니다. 다시 입력해주세요.")
                        tkinter.messagebox.showwarning("아이템 장착", "플레이어를 잘못 입력하였습니다.\n다시 입력해주세요.")
                else:
                    print("행동 입력이 잘못되었습니다. 다시 입력해주세요.")
                    tkinter.messagebox.showwarning("행동", "행동 입력이 잘못되었습니다.\n다시 입력해주세요.")
            except:
                print("행동 입력이 잘못되었습니다. 다시 입력해주세요.")
                tkinter.messagebox.showwarning("행동", "행동 입력이 잘못되었습니다.\n다시 입력해주세요.")
    
    print("상대팀한테 아래의 메세지를 전달해주세요.")
    print(sending_message)
    clip.copy(sending_message)
    tkinter.messagebox.showinfo("우리팀 코드", sending_message + '\n\n' + "상대팀한테 위의 메세지를 전달해주세요.\n(클립보드에 복사 되었습니다)")
    while True :
        l = tkinter.simpledialog.askstring("상대팀 코드", "상대팀한테\n전달받은 값을 입력해주세요.",show='*')
        if (l != None) and (len(l) > 5) and ((l[0] =='M') or (l[0] =='I')):
            break
    #l = tkinter.simpledialog.askstring("상대팀 코드", "상대팀한테\n전달받은 값을 입력해주세요.",show='*')
    l = l.split("/")
    for a in l:
        a = a.split(" ")
        if a[0] == "M":
            player = player_list_other[int(a[1]) - 1]
            next_place = int(a[2])
            player.moveto(next_place)
            print("상대팀이 플레이어 %d을(를) %s(으)로 이동하였습니다." %(player.key, building_list[player.place - 1].name))
        elif a[0] == "I":
            player = player_list_other[int(a[1]) - 1]
            player.set_item(int(a[2]))
            print("상대팀이 플레이어 %d에게 아이템을 장착하였습니다." %player.key)
        elif a[0] == "S":
            if int(a[1]) in special_building:
                special_building.remove(int(a[1]))
                building_list[int(a[1])].special = 0
                print("상대팀이 스페셜존 %d %s의 미션을 성공하였습니다. 스페셜존은 소멸되었습니다." %(building_list[int(a[1])].num, building_list[int(a[1])].name))
        elif a[0] == "D":
            player = player_list_other[int(a[1]) - 1]
            player.state = 0
            building_list[player.place - 1].remove_player(player)
            print("상대팀의 플레이어 %d가 점수를 잃어 소멸하였습니다." %player.key)
        elif a[0] == "P":
            player = player_list_other[int(a[1]) - 1]
            player.plus_score(int(a[2]))
    print("\n")
    compete()
    for e in explosion_list:
        frm.delete(e)
    clear_player()
    show_player()
    score_my = 0
    score_other = 0
    for p in player_list:
        if p.state != 0 :
            score_my += p.score
    for p in player_list_other:
        if p.state != 0 :
            score_other += p.score
    if score_my == 0 or score_other == 0:
        break
    cur_position()

if score_my > score_other:
    print("게임에서 승리하였습니다.")
    tkinter.messagebox.showinfo("승리", "우리팀 점수 %d vs 상대팀 점수 %d\n게임에서 승리하였습니다." %(score_my, score_other))
elif score_my < score_other:
    print("게임에서 패배하였습니다.")
    tkinter.messagebox.showerror("패배","우리팀 점수 %d vs 상대팀 점수 %d\n게임에서 패배하였습니다." %(score_my, score_other))
else:
    print("점수가 동일합니다. 무승부입니다.")
    tkinter.messagebox.showinfo("무승부","우리팀 점수 %d vs 상대팀 점수 %d\n무승부입니다." %(score_my, score_other))
root.mainloop()