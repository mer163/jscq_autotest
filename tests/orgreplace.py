# -*- coding: UTF-8 -*-
#!/usr/bin/env python

import xlrd

update = r'/Users/admin/Desktop/7.16副标题更新变化.xlsx'
org = r'/Users/admin/Desktop/20180616商品交易--跨境电商版本管理打包数据new.xlsx'

workbook = xlrd.open_workbook(org)
workbook1 = xlrd.open_workbook(update)

orgsheet = workbook.sheet_by_index(0)
updatesheet = workbook1.sheet_by_index(0)

print(orgsheet.name)
print(updatesheet.name)

for i in range(3,orgsheet.nrows):
    print('orgsheet',orgsheet.cell_value(i,0))


    for j in range(updatesheet.nrows):

        updatevalue = updatesheet.cell_value(j,1)
        # print(updatesheet)
        # print(updatesheet.cell_value(i,1))
        try:
            # print('updatesheet',updatevalue.split()[1])
            updatevaluea = updatevalue.split()[1]

            if  updatevaluea == orgsheet.cell(i,0):
                print('update')
            # if updatevalue.split()[1]  is orgsheet.cell_value(i,0):

            #     print('找到orgid')

        except:
            print('error')

        # if orgsheet.cell_value(i, 0) == updatevalue.
    # print(updatevalue.split()[1])



if __name__ == '__main__':
    print('test')