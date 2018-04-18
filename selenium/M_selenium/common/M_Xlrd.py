# -*- coding: utf-8 -*-
# By: Mei
import xlrd
from xlutils.copy import copy


class Myxlrd:
    def __init__(self, file_name=None, sheet_id=None):
        if file_name:
            self.file_name = file_name
            self.sheet_id = sheet_id
        else:
            self.file_name = "../dataconfig/1.xlsx"
            self.sheet_id = 0
        self.data = xlrd.open_workbook(self.file_name)
        self.table = self.data.sheet_by_index(0)
    def xl_row(self):
        """获取总行数"""
        return self.table.nrows

    def xl_col(self):
        """获取总列数"""
        return self.table.cols

    def xl_row_value(self,row):
        """读取一整行数据"""
        return self.table.row_values(row)

    def xl_col_value(self,col):
        """获取整列数据"""
        return self.table.col_values(col)

    def xl_cell_value(self,row,col):
        """指定单元格读取"""
        return self.table.cell_value(row,col)

    # 写入数据
    def xl_write_value(self, row, col, value):
        """指定单元格写入"""
        self.data = xlrd.open_workbook(self.file_name)
        write_data = copy(self.data)
        sheet_data = write_data.get_sheet(0)
        sheet_data.write(row, col, value)
        write_data.save(self.file_name)

if __name__ == '__main__':
    sheet = Myxlrd()
    sheet.xl_write_value(1,3,"hao")









