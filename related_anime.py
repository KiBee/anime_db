import pandas as pd
import sqlalchemy
import csv

st_csv_filename = 'csv\\initial csv\\anime_filtered.csv'

filename = 'csv\\test csv\\animelist_related.csv'

mysql_engine = 'mysql://root@localhost:3306/anime_norm_maria?charset=utf8'
engine = sqlalchemy.create_engine(mysql_engine)

q = """
        SELECT *
        FROM anime_filtered_full
    """
relateds = pd.read_csv(st_csv_filename)
# relateds = pd.read_sql(q, engine)
obj_id = list()
obj = list()
full_filtered_list = list()
table = list()
id_rel = dict([("Adaptation", 1),
                       ("Side story", 2),
                       ("Other", 3),
                       ("Summary", 4),
                       ("Alternative setting", 5),
                       ("Alternative version", 6),
                       ("Parent story", 7),
                       ("Prequel", 8),
                       ("Sequel", 9),
                       ("Full story", 10),
                       ("Spin-off", 11),
                       ("Character", 12)])

for k, v in relateds.iterrows():
    obj_id.append(v.anime_id)

    if v.related != "[]":
        w = list()
        c = list()
        filtered_list = list()
        a = list(map(str, v.related.replace("'", "").split('}]')))

        for i in range(len(a)):
            a[i] = a[i].replace(", ", " ")
            c.append(a[i].split(": [{"))

        for i in range(len(c)):

            c[i][0] = c[i][0].replace('{', "").replace('}', "")
            if c[i][0] == "":
                c.pop(i)
                i -= 1

            if c[i][0][0] == " ":
                c[i][0] = c[i][0][:0] + c[i][0][1:]
            c[i][0].split('}{')

        for i in range(len(c)):
            w.append(c[i])
            w[i][1] = w[i][1].split("} {")
            if w[i][1][0].find("type: anime") != -1:
                for j in range(len(w[i][1])):
                    w[i][1][j] = w[i][1][j].split(" ")[1]
                filtered_list.append(w[i])

        full_filtered_list.append(filtered_list)

    else:
        full_filtered_list.append('empty')

for k in range(len(obj_id)):
    try:
        for i in range(len(full_filtered_list[k])):
            for j in range(len(full_filtered_list[k][i][1])):
                if int(full_filtered_list[k][i][1][j]) != 0:
                    table.append((int(obj_id[k]), int(id_rel.get(full_filtered_list[k][i][0])), int(full_filtered_list[k][i][1][j])))
    except IndexError:
        pass

less = set()
for i in range(len(table) - 1, 0, -1):
    if table[i][2] not in obj_id or table[i][2] == table[i][0]:
        print(table[i][2])
        less.add(table[i][2])
        table.pop(i)

table = sorted(table, key=lambda x: (x[0], x[1], x[2]))
zp = pd.DataFrame(table)
zp.to_csv(filename, header=None, index=False, encoding='utf-8-sig')
zp.rename(columns={0: 'id_anime_object', 1: 'id_relations', 2: 'id_anime_subject'}).to_sql('animelist_related', index=False,  if_exists='append', con=engine)
print('Table Animelist_producer updated')

