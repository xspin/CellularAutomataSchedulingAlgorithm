#-*- coding: UTF-8 -*-
import random, Data

all_class = Data.all_class
all_lesson = Data.all_lesson


###初始化数据###############################
def location_init():
    """构造位置表"""

    location = {}
    for i, lessons in enumerate(all_lesson):
        for l in lessons:
            if l[0] not in location:
                location[l[0]] = {all_class[i]:[]}
            else:
                location[l[0]][all_class[i]] = []
    return location

def lessons_init():
    all_table = []
    teacheres = [[[l[0], l[1]] for l in les] for les in all_lesson]

    for i, cnum in enumerate(all_class):
        one_table = [['nil' for section in range(4)] for week in range(5)]

        for teach in teacheres[i]:
            for num in range(teach[1]):

                cod = [random.randint(0,4), random.randint(0, 3)]
                while one_table[cod[0]][cod[1]]!='nil':
                    cod = [random.randint(0,4), random.randint(0, 3)]

                one_table[cod[0]][cod[1]] = teach[0]
                location[teach[0]][cnum].append(cod)

        all_table.append(one_table)

    return all_table

location = location_init()
all_table = lessons_init()
##########################################


###数据操作#################################
def operate(act1,act2='',ele='',cod='',cnum=''):
    """数据操作接口"""

    def cheak_index(cod):
        if cod=='':
            return "I don't care that right now"
        elif ((0<=cod[0]<=4) and (0<=cod[1]<=3))==False:
            return 'IndexError'

    def write_class(ele,cod,cnum):
        """把元素写入总课程表"""

        week, section = cod
        class_index   = all_class.index(cnum)
        all_table[class_index][week][section] = ele

    def write_location(ele,cod,cnum):
        """把元素位置写入位置表"""

        if ele!='nil':
            location[ele][cnum] = [cod]
        else:
            """都是空了为什么要更新它的位置？无视无视＝ ＝"""
            pass

    def read_class(cod,cnum):
        """读取总课程表"""

        week, section = cod
        class_index   = all_class.index(cnum)
        ele = all_table[class_index][week][section]
        return ele

    def read_location(act='',ele=''):
        """读取位置表"""

        if ele=='':
            for key in location:
                yield key
        elif act=='time':
            for t in location[ele].values():
                yield t
        elif act=='class':
            for cnum in location[ele]:
                yield cnum
        else:
            raise IOError

    if act1=='cheak-index':
        return cheak_index(cod)
    else:
        if act1=='w-class':
            write_class(ele, cod, cnum)
        elif act1=='w-location':
            write_location(ele, cod, cnum)
        elif act1=='r-class':
            return read_class(cod, cnum)
        elif act1=='r-location':
            return read_location(act2, ele)
        else:
            raise IOError
##########################################


###核心算法#################################
def update(ele,cnum,cod_now,cod_aim):
    """更新元素信息操作"""

    ele_aim = operate('r-class', cod=cod_aim, cnum=cnum)

    operate('w-class', ele=ele, cod=cod_aim, cnum=cnum)
    operate('w-location', ele=ele, cod=cod_aim, cnum=cnum)
    operate('w-class', ele=ele_aim, cod=cod_now, cnum=cnum)
    operate('w-location', ele=ele_aim, cod=cod_now, cnum=cnum)

def judge(act,ele=''):
    """检查数据合法性"""

    def get_info(act,ele):
        if act=='time':
            raw_time  = list(operate('r-location', 'time', ele))
            ripe_time = [t for time in raw_time for t in time]              #重整化列表以判断时间是否重复
            return [raw_time, ripe_time]

        elif act=='class':
            class_num = operate('r-location', 'class', ele)
            return list(class_num)


    def law_1(ele):
        """基本法则：老师课程不能冲突"""
        class_num           = get_info('class', ele)
        raw_time, ripe_time = get_info('time', ele)

        for l in ripe_time:                                                   #判断所有的时间是否有重复的代码
            if ripe_time.count(l)>1:                                          #得到下标以确定班级编号
                index = [i for i, x in enumerate(raw_time) if l in x][0]
                return [l, class_num[index]]

        return 'Right!'

    def state():
        """检查所有数据的状态"""
        for ele in operate('r-location'):
            if law_1(ele)!='Right!':
                return ele
        return 'All Right!'

    if act=='state':
        return state()
    elif act=='law_1':
        return law_1(ele)
    else:
        return IOError

def navigate(act,cod):
    """生成移动所需坐标"""

    navigation = {'left'  : [cod[0]-1, cod[1]],
                  'right' : [cod[0]+1, cod[1]],
                  'up'    : [cod[0], cod[1]-1],
                  'down'  : [cod[0], cod[1]+1]}

    back_navig = {'b-left'  : [cod[0]+1, cod[1]],
                  'b-right' : [cod[0]-1, cod[1]],
                  'b-up'    : [cod[0], cod[1]+1],
                  'b-down'  : [cod[0], cod[1]-1]}

    if act=='map':
        return navigation
    elif act=='rondom':
        return [random.randint(0,4), random.randint(0, 3)]
    elif act[:1]!='b':
        return navigation[act]
    elif act[:1]=='b':
        return back_navig[act]

def move(act,cod,ele,cnum):
    cod_now = cod
    cod_aim = navigate(act,cod)
    update(ele, cnum, cod_now, cod_aim)

def weight(ele,cod,cnum):
    """给出权重最低的移动方向"""

    ###初始化所需数据############################
    maps = navigate('map',cod=cod)                                                  #导航表
    time_lst = [t for time in operate('r-location', 'time', ele) for t in time]     #时间表
    price_list = {'conflict' : 10,                                                  #权值
                  'so_tried' :  5,
                  '????????' :  0}
    ##########################################

    def get_info(way=''):
        """返回移动后的权重"""

        if way!='':
            move(way, cod, ele, cnum)

        conflict_num = time_lst.count(cod)-1
        value = conflict_num*price_list['conflict']

        if way!='':
            move('b-'+way, maps[way], ele, cnum)

        return value

    remain_weight = get_info()

    for way in maps:
        if operate('cheak-index', cod=maps[way])=='IndexError':
            pass
        else:
            move_weight = get_info(way)
            if move_weight>=remain_weight:
                good_way = 'rondom'
            else:
                good_way = way

    return good_way

def tactic(ele,error_cod,cnum):

    good_way = weight(ele,error_cod,cnum)

    # output('other', ele+'  is  '+good_way)

    # output('one', cnum)

    move(good_way, error_cod, ele, cnum)

    # output('one', cnum)

def evolve():
    output('clear')
    i = 0
    while judge('state', location)!='All Right!':
        print(i)
        i += 1
        for ele in operate('r-location'):
            if judge('law_1', ele)!='Right!':
                error_cod, cnum = judge('law_1', ele)
                tactic(ele, error_cod, cnum)
##########################################


###输出####################################
def output(act,cnum=''):
    def table():
        f = open('log', 'a')
        for index, classes in enumerate(all_table):
            f.write(all_class[index]+'\n')
            for l in classes:
                string = str(l)
                f.write(string+'\n')
            f.write('\n')
        f.write('-'*42+'\n')
        f.close()

    def one(cnum):
        f = open('log', 'a')
        f.write(cnum+'\n')
        index = all_class.index(cnum)
        for l in all_table[index]:
            string = str(l)
            f.write(string+'\n')
        f.write('-'*42+'\n\n')
        f.close()

    def other(cnum):
        f = open('log', 'a')
        f.write('\n'+str(cnum)+'\n')
        f.close()

    def clear():
        f = open('log','w')
        f.close()

    if act=='table':
        table()
    elif act=='one':
        one(cnum)
    elif act=='other':
        other(cnum)
    elif act=='clear':
        clear()
##########################################


###运行算法#################################
evolve()
print('Yes')
output('table')
##########################################


