import re
import datetime
from bs4 import BeautifulSoup
from ics import Calendar, Event

##check your HTML file name to make sure this program can work in a proper way
with open("学生课表查询.html", "rb") as f:
    html = f.read().decode("utf8")
    f.close()

soup = BeautifulSoup(html,"html.parser")

##please replace the date with the real date your term starts
term_start_time = datetime.datetime.strptime('2020-09-7 00:00:00+0800',
                                             '%Y-%m-%d %H:%M:%S%z')

count = 0

info = []

weekday_T = ('星期一','星期二','星期三','星期四','星期五','星期六','星期日')

start_h = (0,8,8,10,10,12,12,14,14,16,16,18,18,19)
end_h = (0,8,9,10,11,12,13,14,15,16,17,18,19,20)
start_m = (0,0,55,0,55,0,55,0,55,0,55,0,55,0)
end_m = (0,45,40,45,40,45,40,45,40,45,40,45,40,45)


class_locates = soup.find_all(lambda tag: tag.name in ['font'] and tag['color']=='blue' or tag.name in ['span'] )
for locate in class_locates:
    if locate.get_text()!='' and locate.get_text()!='蓝色为已选上':
        if(locate.get_text()=='星期一') : count+=1
        if(locate.get_text()=='实验课表') : count=0
        if(count>=2) : info.append(locate.get_text())


x = 0
weekday = 0

c = Calendar()

def add_course(time,name,weeks,weekflag,local,remark):
    if(len(weeks)!=2):
        for week in weeks:
            e = Event()
            e.name = name
            e.location = local
            e.description = remark
            offset = datetime.timedelta(days=(int(week)-1)*7+weekday,hours=start_h[int(time[0])],minutes=start_m[int(time[0])])
            e.begin = term_start_time + offset
            #print(term_start_time + offset)
            offset = datetime.timedelta(days=(int(week)-1)*7+weekday,hours=end_h[int(time[1])],minutes=end_m[int(time[1])])
            e.end = term_start_time + offset
            #print(term_start_time + offset)
            c.events.add(e)
        print("成功导入：",name,time,weeks,weekflag,local,remark)
    else:
        week_cur = int(weeks[0])
        week_end = int(weeks[1])
        while week_cur <= week_end:
            e = Event()
            e.name = name
            e.location = local
            e.description = remark
            offset = datetime.timedelta(days=(week_cur-1)*7+weekday,hours=start_h[int(time[0])],minutes=start_m[int(time[0])])
            e.begin = term_start_time + offset
            #print(term_start_time + offset)
            offset = datetime.timedelta(days=(week_cur-1)*7+weekday,hours=end_h[int(time[1])],minutes=end_m[int(time[1])])
            e.end = term_start_time + offset
            #print(term_start_time + offset)
            if(weekflag):week_cur+=2
            else:week_cur+=1
            c.events.add(e)
        print("成功导入：",name,time,weeks,weekflag,local)

while x<len(info):
    if(info[x] in weekday_T):
        weekday = weekday_T.index(info[x])
        #print(info[x])
        x+=1
    else: 
        time = re.findall(r"\d+",info[x])
        name = info[x+1]
        weeks = re.findall(r"\d+",info[x+3])
        weekflag = 0
        if(info[x+3].find('单')!=-1) : weekflag = 1
        if(info[x+3].find('双')!=-1) : weekflag = 2
        local = info[x+4]
        remark = info[x+8]
        #print(info[x+3])
        x+=13
        #print(weekflag)
        #print(time,name,weeks,local,remark)
        add_course(time,name,weeks,weekflag,local,remark)
        while(x<len(info) and not(info[x] in weekday_T) and info[x].find('-')==-1):
            name = info[x]
            weeks = re.findall(r"\d+",info[x+2])
            weekflag = 0
            if(info[x+2].find('单')!=-1) : weekflag = 1
            if(info[x+2].find('双')!=-1) : weekflag = 2
            local = info[x+3]
            remark = info[x+7]
            x+=12
            add_course(time,name,weeks,weekflag,local,remark)

with open('sjtu.ics', 'w', encoding='utf-8') as my_file:
    my_file.writelines(c)