import xlrd
from xlutils.copy import copy


class Myxlrd:
    def __init__(self, file_name=None, sheet_id=None):
        if file_name:
            self.file_name = file_name
            self.sheet_id = sheet_id
        else:
            self.file_name = "../dataconfig/case.xlsx"
            self.sheet_id = 0
        self.data = self.Get_Sheet_Data()

    def Get_Sheet_Data(self):
        """获取sheets的内容"""
        data = xlrd.open_workbook(self.file_name)
        tables = data.sheets()[self.sheet_id]
        return tables


    def Get_All_Lines(self):
        """获取单元格的行数"""
        tables = self.data
        return tables.nrows


    def Get_Only_Value(self, row, col):
        """获取某一个单元格的内容"""
        return self.data.cell_value(row, col)

    # 写入数据
    def Write_Value(self, row, col, value):
        """写入数据"""
        read_data = xlrd.open_workbook(self.file_name)
        write_data = copy(read_data)
        sheet_data = write_data.get_sheet(0)
        sheet_data.write(row, col, value)
        write_data.save(self.file_name)



    def Get_Row_By_Caseid(self, case_id):
        """根据对应的caseid找到对应的行号"""
        num = 0
        clols_data = self.Get_Cols_Data()
        for col_data in clols_data:
            if case_id in col_data:
                return num
            num = num + 1


    def Get_Data_By_Caseid(self, case_id):
        """根据对应的caseid 找到对应行的内容"""
        row_num = self.Get_Row_By_Caseid(case_id)
        rows_data = self.Get_Row_Values(row_num)
        return rows_data

    # 根据行号，找到该行的内容
    def Get_Row_Values(self, row):
        tables = self.data
        row_data = tables.row_values(row)
        return row_data

    # 获取某一列的内容
    def Get_Cols_Data(self, col_id=None):
        if col_id != None:
            cols = self.data.col_values(col_id)
        else:
            cols = self.data.col_values(0)
        return cols


if __name__ == '__main__':
    opers = Myxlrd()
    print(opers.Get_Cols_Data(0))
