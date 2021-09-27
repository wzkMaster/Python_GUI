import pandas
import sqlite3

def create_tables():
    cursor = sqlite3.connect('disease.db')
    cursor.execute('CREATE TABLE country (continent_id int, name VARCHAR(100) PRIMARY KEY, '
                   'FOREIGN KEY (continent_id) REFERENCES continent(continent_id))')
    cursor.execute('CREATE TABLE continent (continent_id int PRIMARY KEY, name VARCHAR(100))')
    cursor.execute('CREATE TABLE SARS (id INTEGER PRIMARY KEY AUTOINCREMENT ,date date, infected int, Mortality int)')
    cursor.execute('CREATE TABLE global_covid19 (name VARCHAR(100) PRIMARY KEY, confirmed int ,cured int, death int)')
    cursor.execute('CREATE TABLE global_timeseries (id INTEGER PRIMARY KEY AUTOINCREMENT , date date, confirmed int, cured int,death int)')
    cursor.execute('CREATE TABLE China_covid19 (province VARCHAR(20) PRIMARY KEY ,confirmed int, cured int, death int)')
    cursor.execute('CREATE TABLE China_timeseries (date date PRIMARY KEY, confirmed int, cured int, death int)')
    cursor.execute('CREATE TABLE Hubei (city VARCHAR(100) PRIMARY KEY, confirmed int, cured int, death int )')
    cursor.execute('CREATE TABLE US_covid19 (state VARCHAR(100) PRIMARY KEY, confirmed int, death int)')
    cursor.execute('CREATE TABLE US_timeseries (date date PRIMARY KEY , confirmed int, death int)')
    cursor.commit()
    cursor.close()


def insert_country_data():
    cursor = sqlite3.connect('disease.db')
    country_data = pandas.read_csv('data/country.csv')
    country_data = country_data.loc[0:210, ['continent_id', 'name']]
    continent_data = {0: 'Unkown',1: 'Asia', 2: "Europe", 3: 'Africa', 4: 'Oceania', 6: 'North America', 7: 'South America'}
    for i in range(211):
       id = country_data.loc[i, 'continent_id']
       name = country_data.loc[i, 'name']
       cursor.execute('INSERT INTO country (continent_id, name) VALUES ({0}, "{1}")'.format(id, name))
    cursor.commit()
    for i, j in continent_data.items():
        cursor.execute('INSERT INTO continent (continent_id, name) VALUES ({0}, "{1}")'.format(i, j))
    cursor.commit()
    cursor.close()


def insert_sars():
    cursor = sqlite3.connect('disease.db')
    SARS_data = pandas.read_csv('data/sars_final.csv')
    for record in SARS_data.values[:, 1:4]:
        if record[0][8] == '上':
            cursor.execute(
                'INSERT INTO SARS (date, infected, Mortality) VALUES ("{0}", {1}, {2})'.format(record[0][:8], record[1],
                                                                                               record[2]))
        cursor.execute(
            'INSERT INTO SARS (date, infected, Mortality) VALUES ("{0}", {1}, {2})'.format(record[0][:9], record[1], record[2]))
    cursor.commit()
    cursor.close()


def insert_world():
    cursor = sqlite3.connect('disease.db')
    world_data = pandas.read_csv('data/DXYArea.csv')
    already = []
    for record in world_data.values[3850:4804, [1, 3, 5, 7, 9, 10]]:
        if record[1] == record[2] and record[1] not in already:
            cursor.execute(
                'INSERT INTO global_covid19 (name, confirmed, cured, death) VALUES ("{0}", {1}, {2}, {3})'.format(
                    record[1], record[3], record[4], record[5]))
            already.append(record[1])
        else:
            pass
    cursor.commit()
    cursor.close()


def insert_China():
    cursor = sqlite3.connect('disease.db')
    confirmed = pandas.read_csv('data/time_series_covid19_confirmed_global.csv')
    death = pandas.read_csv('data/time_series_covid19_deaths_global.csv')
    cured = pandas.read_csv('data/time_series_covid19_recovered_global.csv')
    data = [confirmed.values[51:82, [0, 120]],death.values[51:82, 120],cured.values[42:73,120]]
    print(data)
    for i in range(31):
        cursor.execute(
            'INSERT INTO China_covid19 (province, confirmed, cured, death) VALUES ("{0}", {1}, {2}, {3})'.format(
                data[0][i][0], data[0][i][1], data[2][i], data[1][i]))
    cursor.commit()
    cursor.close()


def insert_hubei():
    cursor = sqlite3.connect('disease.db')
    data = pandas.read_csv('data/DXYArea.csv')
    for record in data.values[7078:7095, [11,14,16,17]]:
        cursor.execute('INSERT INTO Hubei (city, confirmed, cured, death) VALUES ("{0}", {1}, {2}, {3})'.format(record[0],record[1],record[2],record[3]))
    cursor.commit()
    cursor.close()


def insert_China_time():
    cursor = sqlite3.connect('disease.db')
    data = pandas.read_csv('data/ncov.csv')
    for record in data.values[:117,[0, 1, 2 , 8, 11]]:
        cursor.execute(
           'INSERT INTO China_timeseries (date , confirmed, cured, death) VALUES ("{0}", {1}, {2}, {3})'.format(
               record[0], record[2], record[1], record[4], record[3]))
    cursor.commit()
    cursor.close()


def insert_US():
    cursor = sqlite3.connect('disease.db')
    data = pandas.read_csv('data/us-states.csv')
    for record in data.values[4086:4140,[1,3,4]]:
        cursor.execute(
            'INSERT INTO US_covid19 (state, confirmed, death) VALUES ("{0}", {1}, {2})'.format(
                record[0], record[1], record[2]))
    cursor.commit()
    cursor.close()


def insert_US_time():
    cursor = sqlite3.connect('disease.db')
    data = pandas.read_csv('data/us.csv')
    for record in data.values:
        cursor.execute(
            'INSERT INTO US_timeseries (date, confirmed, death) VALUES ("{0}", {1}, {2})'.format(
                record[0], record[1], record[2]))
    cursor.commit()
    cursor.close()


def insert_world_time():
    cursor = sqlite3.connect('disease.db')
    confirmed = pandas.read_csv('data/time_series_covid19_confirmed_global.csv')
    death = pandas.read_csv('data/time_series_covid19_deaths_global.csv')
    cured = pandas.read_csv('data/time_series_covid19_recovered_global.csv')
    for i in range(4, 128):
        cursor.execute('INSERT INTO global_timeseries (date, confirmed, cured, death) VALUES ("{0}", {1}, {2}, {3})'.format(
            confirmed.columns[i], confirmed.values[-1, i], cured.values[-1, i], death.values[-1, i]))
    cursor.commit()
    cursor.close()


def create_view():
    cursor = sqlite3.connect('disease.db')
    cursor.execute('''CREATE VIEW continent_covid19 AS 
                            SELECT sum(confirmed), continent.name 
                            FROM global_covid19
                            JOIN country ON country.name = global_covid19.name
                            JOIN continent ON continent.continent_id = country.continent_id
                            GROUP BY continent.name''')
    cursor.execute('''CREATE view sars_covid 
                        AS 
                        SELECT infected, mortality, confirmed, death
                        FROM sars s
                        JOIN global_timeseries g
                        ON s.id = g.id''')
    cursor.commit()


create_tables()
insert_country_data()
insert_sars()
insert_world()
insert_China_time()
insert_US_time()
insert_China()
insert_hubei()
insert_US()
insert_world_time()
create_view()