from matplotlib import pyplot as plt
import sqlite3
import easygui


def visual():
   cursor = sqlite3.connect('disease.db')
   plt.rcParams['font.sans-serif'] = ['SimHei']
   choices = ['新冠与非典对比','全球前10感染国家病例数量对比','查看各大洲病例分布状况','中国病例分布状况','湖北病例分布状况']
   c = easygui.choicebox('选择你想要的功能', '数据可视化', choices=choices)
   if c == choices[0]:
       res = cursor.execute('SELECT * FROM sars_covid')
       data = res.fetchall()
       s_d = []
       s_c = []
       c_c = []
       c_d = []
       x = []
       for i in range(len(data)):
           s_d.append(data[i][1])
           s_c.append(data[i][0])
           c_c.append(data[i][2])
           c_d.append(data[i][3])
           x.append(i)
       plt.plot(x, s_c)
       plt.plot(x, s_d)
       plt.xlabel("疫情爆发天数", fontsize=10)
       plt.ylabel("确诊/死亡人数", fontsize=10)
       plt.savefig('sars.jpg')
       plt.plot(x, c_c)
       plt.plot(x, c_d)
       plt.savefig('covid.jpg')
       easygui.buttonbox('Here is the graph', choices=['点击按钮或图片返回主菜单', '', ''], images=['sars.jpg','covid.jpg'])
   elif c == choices[1]:
       data = cursor.execute("SELECT name, confirmed FROM global_covid19 ORDER BY confirmed DESC LIMIT 10")
       data = data.fetchall()
       region = []
       amount = []
       for record in data:
           region.append(record[1])
           amount.append(record[0])
       plt.barh(amount, region)
       plt.savefig('world.jpg')
       easygui.buttonbox('Here is the graph',choices=['点击按钮或图片返回主菜单','',''],image='world.jpg')
   elif c == choices[2]:
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
       plt.pie(amount, labels=region)
       plt.savefig('continent.jpg')
       easygui.buttonbox('Here is the graph',choices=['点击按钮或图片返回主菜单','',''],image='continent.jpg')
   elif c==choices[3]:
       data = cursor.execute("SELECT province, confirmed FROM china_covid19 ORDER BY confirmed DESC")
       data = data.fetchall()
       region = []
       amount = []
       for record in data:
           region.append(record[1])
           amount.append(record[0])
       plt.barh(amount, region)
       plt.savefig('china.jpg')
       easygui.buttonbox('Here is the graph', choices=['点击按钮或图片返回主菜单', '', ''], image='china.jpg')
   elif c == choices[4]:
       data = cursor.execute("SELECT city, confirmed FROM hubei ORDER BY confirmed DESC")
       data = data.fetchall()
       region = []
       amount = []
       for record in data:
           region.append(record[1])
           amount.append(record[0])
       plt.barh(amount, region)
       plt.savefig('hubei.jpg')
       easygui.buttonbox('Here is the graph', choices=['点击按钮或图片返回主菜单', '', ''], image='hubei.jpg')

