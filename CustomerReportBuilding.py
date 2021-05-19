# coding=UTF-8
import csv
import datetime
import os
import re
import shutil
import time
import tkinter
import tkinter.messagebox
from collections import Counter
from os import listdir
from os.path import dirname

import pymysql
import xlrd
import xlwt
from xlutils.copy import copy


class Report:

    def __init__(self, passpath=''):
        self.passpath = passpath

    def csv_read(self, path):
        data = []
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, dialect='excel')
            for row in reader:
                data.append(row)
        return data

    def dict_factorary(self, data):
        get_csv_testitems = []
        get_csv_testitems_result = []
        for row in data:
            get_csv_testitems.append(row[0])
        for row in data:
            get_csv_testitems_result.append(row[1])
        dict_data = dict(zip(get_csv_testitems, get_csv_testitems_result))
        print(dict_data)
        return dict_data

    def writetoexcel(self, dict_data, i=0):
        rb = xlrd.open_workbook(
            os.getcwd() + '\\Test report template Inverter JLR D8.xls', formatting_info=True)
        wb = copy(rb)
        ws = wb.get_sheet(1)

        ############################################################################################################################
        style1 = xlwt.easyxf('font:height 245, name Arial, color-index black;')
        style2 = xlwt.easyxf('font:height 245, name Arial, color-index black;')
        # style = xlwt.easyxf('font:height 240,name Arial, color-index black;align: wrap on, vert centre, horiz center',"borders: top double, bottom double, left double, right double;")
        style = xlwt.easyxf(
            'font:height 245, name Arial, color-index black;align: wrap on, vert centre, horiz center;',
            'General')
        ############################################################################################################################
        border = xlwt.Borders()
        border.left = xlwt.Borders.THIN
        border.top = xlwt.Borders.THIN
        border.right = xlwt.Borders.THIN
        border.bottom = xlwt.Borders.THIN
        style.borders = border
        style1.borders = border

        pattern = xlwt.Pattern()  # Create the Pattern
        # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 3

        pattern2 = xlwt.Pattern()  # Create the Pattern
        # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
        pattern2.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern2.pattern_fore_colour = 1

        # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
        # style1 = xlwt.XFStyle()  # Create the Pattern
        style1.pattern = pattern  # Add Pattern to Style
        # style1.alignment.wrap = 1  # 自动换行
        style1.alignment.horz = 0x02
        style1.alignment.vert = 0x01

        style2.borders = border
        style2.pattern = pattern2  # Add Pattern to Style
        # style1.alignment.wrap = 1  # 自动换行
        style2.alignment.horz = 0x02
        style2.alignment.vert = 0x01
        ########################################################################################################################
        # ws.write_merge(2, 8, 0, 3, 'Second Merge', style)  # Merges row 1 through 2's columns 0 through 3.
        ########################################################################################################################

        ws.write(0, 4+i, dict_data['Serial Number'], style)
        ws.write(5, 4+i, dict_data['FPGA version'], style)
        ws.write(6, 4+i, dict_data['MCU version'], style)
        ws.write(15, 4+i, dict_data['Sleep Power Current Measure'], style)
        ws.write(18, 4+i, 'OK', style)
        ws.write(16, 4+i, dict_data['Standby Power Current Measure'], style)
        ws.write(19, 4+i, 'OK', style)
        ws.write(45, 4+i, dict_data['Read FTEAEXC_UResExcAvg'], style)
        ws.write(20, 4+i, 'OK', style)
        ws.write(30, 4+i, dict_data['Read MAIN_VSIRxsGridVoltW'], style)
        ws.write(21, 4+i, 'OK', style)
        ws.write(24, 4+i, dict_data['Read T_Iuvw3_U16[0]'], style)
        ws.write(22, 4+i, 'OK', style)
        ws.write(25, 4+i, dict_data['Read T_Iuvw3_U16[1]'], style)
        ws.write(48, 4+i, 'OK', style)
        ws.write(26, 4+i, dict_data['Read T_Iuvw3_U16[2]'], style)
        ws.write(49, 4+i, 'OK', style)
        ws.write(27, 4+i, dict_data['Read FS_IbatHV_U16'], style)
        ws.write(50, 4+i, 'OK', style)
        ws.write(28, 4+i, dict_data['Read HV_FS_FaultLevel_U16'], style)
        ws.write(57, 4+i, 'OK', style)
        ws.write(29, 4+i, dict_data['Read FSEABHV_UbatHV'], style)
        ws.write(62, 4+i, 'OK', style)
        ws.write(1, 4+i, dict_data['LAB'], style)
        ##########################################################################
        ws.write(32, 4+i, dict_data['Read FSMAPMT_PmTemp'], style)
        ws.write(64, 4+i, 'OK', style)
        ws.write(33, 4+i, dict_data['Read FSMADBT_DboardTemp'], style)
        ws.write(76, 4+i, 'OK', style1)
        ws.write(34, 4+i, dict_data['Read FSMACBT_CboardTempHV'], style)
        ws.write(35, 4+i, dict_data['Read FSMACBT_CboardTempLV'], style)
        ws.write(36, 4+i, dict_data['Read FSMAICT_CoolingTemp'], style)
        ws.write(37, 4+i, dict_data['Read FSMAMST_StatorTemp1'], style)
        ws.write(38, 4+i, dict_data['Read FSMAMST_StatorTemp2'], style)

        #################################reslover##################################
        ws.write(40, 4+i, dict_data['Resolver excitation'], style)
        ws.write(41, 4+i, dict_data['Read FT_ResolverSin_U16 Max'], style)
        ws.write(42, 4+i, dict_data['Read FT_ResolverSin_U16 Min'], style)
        ws.write(43, 4+i, dict_data['Read FT_ResolverCos_U16 Max'], style)
        ws.write(44, 4+i, dict_data['Read FT_ResolverCos_U16 Min'], style)
        ws.write(47, 4+i, dict_data['Switch Measure Current'], style)
        ws.write(53, 4+i, dict_data['Active discharge 450V to 60V'], style)
        ws.write(55, 4+i, dict_data['Passive discharge 450V to 60V'], style)
        ws.write(
            57, 4+i, dict_data['Read MAIN_MSGu8InverterHVILStatus'], style)
        ws.write(59, 4+i, dict_data['Read Dcs_bMot Measure Current'], style)
        ws.write(60, 4+i, dict_data['Read Pls_bMot Measure Current'], style)
        ws.write(51, 4+i, 'Not Tested', style2)
        ###########################################################################
        ws.write(66, 4+i, dict_data['Read FSMABLV_UbatLVCorGainC'], style)
        ws.write(67, 4+i, dict_data['Read FSMABLV_UbatLVCorOffsetC'], style)
        ws.write(68, 4+i, dict_data['Read HV_CorGainC'], style)
        ws.write(69, 4+i, dict_data['Read HV_CorOffsetC'], style)
        ws.write(70, 4+i, dict_data['Read FTEAMPI_A2DGainIsuLC'], style)
        ws.write(71, 4+i, dict_data['Read FTEAMPI_A2DGainIsvLC'], style)
        ws.write(72, 4+i, dict_data['Read FTEAMPI_A2DGainIswLC'], style)
        ws.write(73, 4+i, dict_data['Read SAMTLCS_A2DGainIsuLC'], style)
        ws.write(74, 4+i, dict_data['Read SAMTLCS_A2DGainIsvLC'], style)
        ws.write(75, 4+i, dict_data['Read SAMTLCS_A2DGainIswLC'], style)
        wb.save(os.getcwd() + '\\Test report template Inverter JLR D8.xls')

    def getColumnIndex(self, table, columnName):
        columnIndex = None
        for i in range(table.ncols):
            if(table.cell_value(0, i) == columnName):
                columnIndex = i
                break
        return columnIndex

    def WriteHipotData_ToCustomerReport(self, Hipot_Data_Dict=''):
        data = xlrd.open_workbook(
            os.getcwd() + '\\Test report template Inverter JLR D8.xls', formatting_info=True)
        table = data.sheet_by_index(1)
        SerialNumber = Hipot_Data_Dict['Serial Number']
        SN_column = self.getColumnIndex(table, SerialNumber)
        # print(SN_column)
        if SN_column != None:
            wb = copy(data)
            ws = wb.get_sheet(1)
            ############################################################################################################################
            style1 = xlwt.easyxf(
                'font:height 245, name Arial, color-index black;')
            style2 = xlwt.easyxf(
                'font:height 245, name Arial, color-index black;')
            # style = xlwt.easyxf('font:height 240,name Arial, color-index black;align: wrap on, vert centre, horiz center',"borders: top double, bottom double, left double, right double;")
            style = xlwt.easyxf(
                'font:height 245, name Arial, color-index black;align: wrap on, vert centre, horiz center;',
                'General')
            ############################################################################################################################
            border = xlwt.Borders()
            border.left = xlwt.Borders.THIN
            border.top = xlwt.Borders.THIN
            border.right = xlwt.Borders.THIN
            border.bottom = xlwt.Borders.THIN
            style.borders = border
            style1.borders = border

            pattern = xlwt.Pattern()  # Create the Pattern
            # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
            pattern.pattern = xlwt.Pattern.SOLID_PATTERN
            pattern.pattern_fore_colour = 3

            pattern2 = xlwt.Pattern()  # Create the Pattern
            # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
            pattern2.pattern = xlwt.Pattern.SOLID_PATTERN
            pattern2.pattern_fore_colour = 1

            # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
            # style1 = xlwt.XFStyle()  # Create the Pattern
            style1.pattern = pattern  # Add Pattern to Style
            # style1.alignment.wrap = 1  # 自动换行
            style1.alignment.horz = 0x02
            style1.alignment.vert = 0x01

            style2.borders = border
            style2.pattern = pattern2  # Add Pattern to Style
            # style1.alignment.wrap = 1  # 自动换行
            style2.alignment.horz = 0x02
            style2.alignment.vert = 0x01
            ########################################################################################################################
            # ws.write_merge(2, 8, 0, 3, 'Second Merge', style)  # Merges row 1 through 2's columns 0 through 3.
            ########################################################################################################################
            ws.write(9, SN_column, Hipot_Data_Dict['Leakage Current'], style)
            ws.write(10, SN_column,
                     Hipot_Data_Dict['Isulation Resistance'], style)
            wb.save(os.getcwd() + '\\Test report template Inverter JLR D8.xls')
        else:
            now = datetime.datetime.now()
            f = open('error list.csv', 'a', encoding="utf-8")
            f.write(SerialNumber + ',' + str(now) + '\n')
            f.close()


class CSV_List(object):

    def __init__(self, passpath=''):
        self.passpath = passpath

    def list_sort(self, lt, key=None, reverse=False):
        for i in range(len(lt) - 1):
            for j in range(len(lt) - 1 - i):
                if lt[j] > lt[j + 1]:
                    lt[j], lt[j + 1] = lt[j + 1], lt[j]
        return lt

    def find_repeat_csv(self, repeat_string=''):
        time_list = []
        pathlist = os.listdir(self.passpath)
        for i, filename in enumerate(pathlist):
            pathx = self.passpath + "/" + filename
            result = pathx.find(repeat_string)
            # print(pathx)
            if result != -1:
                stringToint = int(pathx[-19:-4].replace('_', ''))
                # print(stringToint)
                time_list.append(stringToint)
        # print(time_list)
        return time_list

    def find_repeat_string(self):
        new_list = []
        pathlist = os.listdir(self.passpath)
        for i, filename in enumerate(pathlist):
            pathx = self.passpath + "/" + filename
            new_list.append(pathx[0:-21])
            # print(new_list)          #C:/python37/projects/LogReport/PASS/Hipot_!193250055!_V29113441
            b = dict(Counter(new_list))
            repeat_list = []
            for key, value in b.items():
                if value > 1:  # 只展示重复元素
                    repeat_list.append(key)
        # print (repeat_list)
        return repeat_list

    def get_repeat_list(self):
        #######################筛选出重复的测试报告###########################################
        pathlist = os.listdir(self.passpath)
        Repeat_data = self.find_repeat_string()
        # print(Repeat_data)
        each_repeat_list = []
        for each in Repeat_data:
            # print(each[-24:])          #EOL_!200050051!_V29113441
            repeat_data_list = list(
                filter(lambda x: re.search(each[-24:], x) != None, pathlist))
            each_repeat_list.append(repeat_data_list)
        # print(each_repeat_list)     #分别列出重复的数组
        repeat_list = sum(each_repeat_list, [])  # 取得嵌套列表生产新的list
        # print(repeat_list)
        return repeat_list

    def get_separatedCSV(self, number=0):
        pathlist = os.listdir(self.passpath)
        objectCSVfile = list(filter(lambda x: re.search(
            str(number)[-6:], x) != None, pathlist))  # [191228092543]
        return objectCSVfile

    def get_nonrepeateCSV(self):
        pathlist = os.listdir(self.passpath)
        getrepeatlist = self.get_repeat_list()
        repeat_string = self.find_repeat_string()
        # print(getrepeatlist)   #['EOL_!193520016!_V29113441__20191228_092542.csv', 'EOL_!193520016!_V29113441__20191228_092543.csv']
        total_tracenumber_list = []
        for each in repeat_string:
            get_tracenumber_list = self.find_repeat_csv(each)
            total_tracenumber_list.append(get_tracenumber_list)
        # print(total_tracenumber_list)     #[[191228092542, 191228092543]]
        tracenumber_list = []
        for each in total_tracenumber_list:
            each_tracenumber = self.list_sort(each)[-1]  # 获取最新的测试报告时间
            # print(each_tracenumber)
            tracenumber_list.append(each_tracenumber)
        # print(tracenumber_list)      #[191228092543]
        get_total_selectedCSV = []
        for each in tracenumber_list:
            getseparatedCSV = self.get_separatedCSV(each)
            # print(getseparatedCSV)   #['EOL_!193520016!_V29113441__20191228_092543.csv']
            get_total_selectedCSV.append(getseparatedCSV)
        # print(get_total_selectedCSV)   #[['EOL_!193520016!_V29113441__20191228_092543.csv']]
        get_each_selectedCSV = []
        for each in get_total_selectedCSV:
            for i in each:
                get_each_selectedCSV.append(i)
        # print(get_each_selectedCSV)     #['EOL_!193280029!_V29113441__20191227_225433.csv', 'EOL_!193520016!_V29113441__20191228_092543.csv']
        Final_CSV_List = list(set(pathlist) ^ set(
            getrepeatlist)) + get_each_selectedCSV
        # print(Final_CSV_List)
        return Final_CSV_List

##########################################处理报告函数###################################################


def Customer_Report(passpath=''):
    del_ini = []
    del_ini = os.listdir(passpath)
    for f in del_ini:
        if f.endswith('.ini'):
            os.remove(os.path.join(passpath, f))
    csv_list = CSV_List(passpath)
    Final_CSV_List = csv_list.get_nonrepeateCSV()
    from db import Db
    db = Db()
    for i, filename in enumerate(Final_CSV_List):
        pathx = passpath + "/" + filename
        report = Report(passpath)
        data = report.csv_read(pathx)
        data_combine = report.dict_factorary(data)
        try:
            report.writetoexcel(data_combine, i)
        except KeyError as e:
            print(e)
            tkinter.messagebox.showinfo(
                "Warnning", filename + "测试项目缺少或丢失!")

            return False
        db.mysqldata(filename, data_combine)


def GRR_Data(passpath=''):
    del_ini = []
    del_ini = os.listdir(passpath)
    for f in del_ini:
        if f.endswith('.ini'):
            os.remove(os.path.join(passpath, f))
    pathlist = os.listdir(passpath)
    from db import Db
    db = Db()
    for i, filename in enumerate(pathlist):
        pathx = passpath + "/" + filename
        report = Report(passpath)
        data = report.csv_read(pathx)
        data_combine = report.dict_factorary(data)
        try:
            report.writetoexcel(data_combine, i)
        except KeyError as e:
            print(e)
            tkinter.messagebox.showinfo(
                "Warnning", filename + "测试项目缺少或丢失!")
            return False
        db.mysqldata(filename, data_combine)


def HipotData_To_Report(passpath=''):
    del_ini = []
    del_ini = os.listdir(passpath)
    for f in del_ini:
        if f.endswith('.ini'):
            os.remove(os.path.join(passpath, f))
    csv_list = CSV_List(passpath)
    Final_CSV_List = csv_list.get_nonrepeateCSV()
    for i, filename in enumerate(Final_CSV_List):
        pathx = passpath + "/" + filename
        report = Report(passpath)
        data = report.csv_read(pathx)
        data_combine = report.dict_factorary(data)
        try:
            report.WriteHipotData_ToCustomerReport(data_combine)
        except KeyError as e:
            print(e)
            tkinter.messagebox.showinfo(
                "Warnning", filename + "测试项目缺少或丢失!")
            return False
        # print(data_combine)


if __name__ == '__main__':
    Customer_Report('C:/python37/projects/LogReport/new')
    # HipotData_To_Report('C:/python37/projects/LogReport/PASS-Hipot')
    # db = Db()
    # db.create_mysqldatabasetable()
