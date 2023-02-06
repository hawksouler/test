from oracle_op import db_conn, db_sousor, db_select, db_close

import sys
from sys import exit

import win32com.client as win32com

# 建立iwbps数据库连接,建立游标
conn_gdh = db_conn('LIUYANG_IWBPS', 'LIUYANG_IWBPS', '192.168.0.3:1521/orcl')
cursor_gdh = db_sousor(conn_gdh)
gdh_index = -1
sign = 1

while gdh_index < 0:
    # 开始查询需要的工程号,并拼接sql语句
    proj_key = input('请输入工程关键字：')
    sql_gdh = "SELECT PROJNO,PROJNAME,PROJADDRESS,CREATEDATE \
                FROM BZ_PROJECT \
                where PROJNAME like  '%{a}%' \
                or PROJADDRESS like '%{b}%'" \
                .format(a=proj_key, b=proj_key)
    data_gdh = db_select(cursor_gdh, sql_gdh)

    while True:
        # 开始查询，并打印列表
        data1 = []
        for i in data_gdh:
            print(str(data_gdh.index(i)), end='. ')
            for j in i:
                print(str(j), end=', ')
            print('\n')

        # 选择需要的工单号，或者继续精确查找
        chioce = input('如能确定项目则选择项目编号，如需继续筛选则继续输入关键字,如需重新查找请按q:')
        if chioce == 'q' or chioce == 'Q':
            break
        elif chioce.isdigit():
            gdh_index = int(chioce)
            gdh = data_gdh[gdh_index][0]
            break
        else:
            for i in range(len(data_gdh)):
                if chioce in data_gdh[i][1] or chioce in data_gdh[i][2]:
                    # print(chioce, type(i), i, type(data1), type(data))
                    data1.append(data_gdh[i])

        data_gdh = data1
cursor_gdh.close()
conn_gdh.close()

# 建立mis数据库连接，建立游标
conn_bsh = db_conn('lymis', 'lyzls', '192.168.0.2:1521/orcl')
cursor_bsh = db_sousor(conn_bsh)
sql_bsh = "SELECT\
    A.BSH, b.hh, b.bzmc, b.zbwz\
    FROM SB_SBDA A, DA_YHBK B, sb_pbmx c\
    WHERE A.SBID = B.SBID and b.sbid = c.sbid\
    AND c.gch = '{gdh}'"\
    .format(gdh=gdh)
data_bsh = db_select(cursor_bsh, sql_bsh)
# print(data_bsh)


x1 = win32com.gencache.EnsureDispatch('Excel.Application')
x1.Visible = False
ss = x1.Workbooks.Add()
x1.Worksheets.Add().Name = gdh
sh = x1.Worksheets(gdh)
i = 0
for d in data_bsh:
    i += 1
    sh.Cells(i, 1).Value = str(d[0])
    sh.Cells(i, 2).Value = str(d[1])
    sh.Cells(i, 3).Value = str(d[2])
    sh.Cells(i, 4).Value = str(d[3])


ss.SaveAs('C:\\Users\\DELL\\Desktop\\{filename}_{address}.xlsx'.format(
    filename=proj_key, address=data_gdh[gdh_index][2]))


x1.Quit()
