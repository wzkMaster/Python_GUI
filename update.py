import sqlite3
from matplotlib import pyplot
import easygui
import sys
import time
from debug import main_menu


def show_continent_pie():
    cursor = sqlite3.connect('disease.db')
    res = cursor.execute('''SELECT sum(confirmed), continent.name 
                            FROM global_covid19
                            JOIN country ON country.name = global_covid19.name
                            JOIN continent ON continent.continent_id = country.continent_id
                            GROUP BY continent.name''')
    cursor.commit()
    data = res.fetchall()
    region = []
    amount = []
    for record in data:
        region.append(record[1])
        amount.append(record[0])
    cursor.close()
    pyplot.pie(amount, labels=region)
    pyplot.show()


def update_data():
    date = time.strftime('%Y/%m/%d',time.localtime(time.time()))
    c1 = easygui.choicebox('请选择你要修改的数据','Update',choices=['中国疫情','美国疫情','世界疫情','湖北疫情'])
    if c1 == '中国疫情':
        china(date)
        easygui.msgbox('数据操作成功！')
    elif c1 == '美国疫情':
        US(date)
        easygui.msgbox('数据操作成功！')
    elif c1 == '世界疫情':
        world(date)
        easygui.msgbox('数据操作成功！')
    elif c1 == '湖北疫情':
        hubei()
        easygui.msgbox('数据操作成功！')
    else:
        main_menu()
    main_menu()

def US(date):
    cursor = sqlite3.connect('disease.db')
    uss = cursor.execute('SELECT state FROM US_covid19')
    us = uss.fetchall()
    for i in range(len(us)):
        us[i] = us[i][0]
    us.append('America')
    c2 = easygui.choicebox('请选择你要修改数据的州', 'Update US', choices=us)
    cf = easygui.integerbox('请输入确诊人数', '数据输入', lowerbound=0, upperbound=99999999)
    de = easygui.integerbox('请输入死亡人数','数据输入', lowerbound=0, upperbound=99999999)
    if c2 == 'America':
        cursor.execute('INSERT INTO US_timeseries(date ,confirmed, death) VALUES ("{0}", {1}, {2})'
                       .format(date, cf, de))
    elif c2 in us:
        cursor.execute('UPDATE US_covid19 SET confirmed = {0}, death = {1} WHERE state = "{2}"'
                       .format(cf, de, c2))
    else:
        pass
    cursor.commit()


def china(date):
    cursor = sqlite3.connect('disease.db')
    chinad = cursor.execute('SELECT province FROM China_covid19')
    china = chinad.fetchall()
    for i in range(len(china)):
        china[i] = china[i][0]
    china.append('China')
    c2 = easygui.choicebox('请选择你要修改数据的省份', 'Update China', choices=china)
    cf = easygui.integerbox('请输入确诊人数', '数据输入', lowerbound=0, upperbound=99999999)
    if cf is None:
        cf = 0
    de = easygui.integerbox('请输入死亡人数', '数据输入', lowerbound=0, upperbound=99999999)
    if de is None:
        de = 0
    cu = easygui.integerbox('请输入治愈人数', '数据输入', lowerbound=0, upperbound=99999999)
    if cu is None:
        cu = 0
    if cf + de + cu == 0:
        main_menu()
    if c2 == '全国':
        cursor.execute('INSERT INTO China_timeseries(date ,confirmed, cured, death) VALUES ("{0}", {1}, {2}, {3})'
                       .format(date, cf, de, cu))
    elif c2 in china:
        cursor.execute('UPDATE China_covid19 SET confirmed = {0}, death = {1}, cured = {2} WHERE province = "{3}"'
                       .format(cf, de, cu, c2))
    else:
        pass
    cursor.commit()


def world(date):
    cursor = sqlite3.connect('disease.db')
    counss = cursor.execute('SELECT name FROM global_covid19')
    couns = counss.fetchall()
    for i in range(len(couns)):
        couns[i] = couns[i][0]
    couns.append('World')
    c2 = easygui.choicebox('请选择你要修改数据的国家', 'Update World', choices=couns)
    cf = easygui.integerbox('请输入确诊人数', '数据输入', lowerbound=0, upperbound=99999999)
    de = easygui.integerbox('请输入死亡人数', '数据输入', lowerbound=0, upperbound=99999999)
    cu = easygui.integerbox('请输入治愈人数', '数据输入', lowerbound=0, upperbound=99999999)
    if c2 == 'World':
        cursor.execute('INSERT INTO global_timeseries(date ,confirmed, cured, death) VALUES ("{0}", {1}, {2}, {3})'
                       .format(date, cf, de, cu))
    elif c2 in couns:
        cursor.execute('UPDATE global_covid19 SET confirmed = {0}, death = {1}, cured = {2} WHERE name = "{3}"'
                       .format(cf, de, cu, c2))
    else:
        pass
    cursor.commit()


def hubei():
    cursor = sqlite3.connect('disease.db')
    citie = cursor.execute('SELECT city FROM Hubei')
    cities = citie.fetchall()
    for i in range(len(cities)):
        cities[i] = cities[i][0]
    c2 = easygui.choicebox('请选择你要修改数据的省份', 'Update Hubei', choices=cities)
    cf = easygui.integerbox('请输入确诊人数', '数据输入', lowerbound=0, upperbound=99999999)
    de = easygui.integerbox('请输入死亡人数', '数据输入', lowerbound=0, upperbound=99999999)
    cu = easygui.integerbox('请输入治愈人数', '数据输入', lowerbound=0, upperbound=99999999)
    if c2 in cities:
        cursor.execute('UPDATE Hubei SET confirmed = {0}, death = {1}, cured = {2} WHERE city = "{3}"'
                       .format(cf, de, cu, c2))
    else:
        main_menu()
    cursor.commit()

# show_continent_pie()
main_menu()

