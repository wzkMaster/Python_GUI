import sqlite3
import easygui
import sys
import time
import pandas
import update
import visual


def main_menu():
    c1 = easygui.choicebox('请选择你要进行的操作','Main Menu',choices=['修改数据','查询数据','数据可视化'])
    if c1 == '修改数据':
        update.update_data()
    elif c1 == '查询数据':
        select_data()
    elif c1 == '数据可视化':
        visual.visual()
    else:
        sys.exit(0)


def select_data():
    date = time.strftime('%Y/%m/%d',time.localtime(time.time()))
    c1 = easygui.choicebox('请选择你要查看的数据','SELECT',choices=['中国疫情','美国疫情','世界疫情','湖北疫情'])
    if c1 == '中国疫情':
        china(date)
    elif c1 == '美国疫情':
        US(date)
    elif c1 == '世界疫情':
        world(date)
    elif c1 == '湖北疫情':
        hubei()
    else:
        main_menu()
    main_menu()


def US(date):
    cursor = sqlite3.connect('disease.db')
    uss = cursor.execute('SELECT * FROM US_covid19 ORDER BY confirmed DESC')
    us = uss.fetchall()
    data = pandas.DataFrame(us, columns=['地区','确诊','死亡'])
    easygui.msgbox(str(data), '美国疫情')


def china(date):
    cursor = sqlite3.connect('disease.db')
    uss = cursor.execute('SELECT * FROM China_covid19 ORDER BY confirmed DESC')
    us = uss.fetchall()
    data = pandas.DataFrame(us, columns=['地区', '确诊', '治愈', '死亡'])
    easygui.msgbox(str(data), '中国疫情')
    cursor.close()


def world(date):
    cursor = sqlite3.connect('disease.db')
    uss = cursor.execute('SELECT name, confirmed, death, cured FROM global_covid19 ORDER BY confirmed DESC')
    us = uss.fetchall()
    data = pandas.DataFrame(us, columns=['地区', '确诊', '死亡','治愈'])
    easygui.msgbox(str(data), '全球疫情')
    cursor.close()


def hubei():
    cursor = sqlite3.connect('disease.db')
    cities = cursor.execute('SELECT * FROM Hubei ORDER BY confirmed DESC')
    city = cities.fetchall()
    data = pandas.DataFrame(city, columns=['地区', '确诊', '治愈','死亡'])
    easygui.msgbox(str(data), '湖北疫情')
    cursor.close()


pandas.set_option('display.max_rows', None)
main_menu()
