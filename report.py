import csv
import os,re



class Report:

    def __init__(self, path=''):
        self.path = path

    def csv_read(self,path=''):
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
        return dict_data

    def FindOneRecode(self,i,path=''):
        with open(path,'r') as csvfile: 
            reader = csv.reader(csvfile)
            for j,rows in enumerate(reader):    
                if j ==i:   
                    result = rows
                    return result[1]
    
    def SaveToDb(self):
        from db import Db
        db = Db()
        pathlist = os.listdir(self.path)
        for i, filename in enumerate(pathlist):
            each_path = self.path + "/" + filename
            fail_each_path = each_path + "/" + "FAIL"
            pass_each_path = each_path + "/" + "PASS"
            for fail_dir_path,subpaths,fail_files in os.walk(fail_each_path,False):
                for failCount,file in enumerate(fail_files):
                    fail_file_path=os.path.join(fail_dir_path,file)
                    # /home/ubuntu/project/29113425/2021-4-12/FAIL/EOL_!210240019!_V29113441__20210412_093728.csv
                    # print(file)
                    # findStringList = re.compile(r'!.*!').findall(fail_file_path)
                    # print(findStringList)
                    # print(failCount)
                    # print(fail_file_path)
                    data = self.csv_read(fail_file_path)
                    for each_list in data:
                        for each in enumerate(each_list):   
                            if 'Failed' in each:    
                                db.mysql_insert_fail_data(file,each_list)

            for pass_dir_path,subpaths,pass_files in os.walk(pass_each_path,False):
                for passCount,file in enumerate(pass_files):
                    pass_file_path=os.path.join(pass_dir_path,file)
                    data = self.csv_read(pass_file_path)
                    data_combine = self.dict_factorary(data)
                    db.mysqldata(file, data_combine)
        

if __name__ == '__main__':  
    report = Report('/home/ubuntu/project/29113425')
    report.SaveToDb()