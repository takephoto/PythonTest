
import xlrd

if __name__ == '__main__':


    data = xlrd.open_workbook('test.xlsx')
    table = data.sheets()[0]
