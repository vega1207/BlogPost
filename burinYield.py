import csv
import os
import re

class BurinYield:

    def __init__(self, path=''):
        self.path = path
    
    def yieldRate(self):
        # ['20210517', '20210516']
        pathlist = os.listdir(self.path)
        for i, filename in enumerate(pathlist):
            #/home/ubuntu/project/OP1300/20210516
            each_path = self.path + "/" + filename
            # print(each_path)
            fail_each_path = each_path + "/" + "Failed"
            pass_each_path = each_path + "/" + "Passed"
            # print(fail_each_path)
            for fail_dir_path,subpaths,fail_files in os.walk(fail_each_path,False):
                for failCount,file in enumerate(fail_files):
                    fail_file_path=os.path.join(fail_dir_path,file)
                    # /home/ubuntu/project/OP1300/20210517/Failed/PSA_!211190090!V29102835_20210517050505_2.csv
                    # print(fail_file_path)
                    # findStringList = re.compile(r'!.*!').findall(fail_file_path)
                    # print(findStringList)
                    # print(failCount)

            for pass_dir_path,subpaths,pass_files in os.walk(pass_each_path,False):
                for passCount,file in enumerate(pass_files):
                    pass_file_path=os.path.join(pass_dir_path,file)
                    # /home/ubuntu/project/OP1300/20210517/Failed/PSA_!211190090!V29102835_20210517050505_2.csv
                    # print(pass_file_path)
                    # print(passCount)
            # print(passCount,failCount)
            yield_rate = ("%.2f"%((passCount+1)/((passCount+1) +(failCount+1))*100))
            Yield = str(yield_rate)+"%"  
            print(Yield) 
            print(filename)
            # self.save_to_csv(filename,str(yield_rate),'YieldRate.csv')
        return filename,Yield

    def FindOneRecode(i,path=''):
        with open(path,'r') as csvfile: 
            reader = csv.reader(csvfile)
            for j,rows in enumerate(reader):    
                if j ==i:   
                    result = rows
                    return result[1]


    def save_to_csv(self,TestDate='',rate='', csv_name="None.csv"):
        f = open(csv_name, 'a')
        f.write(TestDate + ',' + rate + ',' +'\n')
        f.close()



if __name__ == '__main__':  
    burinYield = BurinYield('/home/ubuntu/project/OP1300')
    results = burinYield.yieldRate()            

    # pathlist = os.listdir('./PASS')
    # for each_file in pathlist:
    #     try:
    #         base_dir = os.path.dirname(__file__) + '\\PASS' +'\\' + each_file +'\\' + 'PASS'
    #         # print(base_dir)   # d:\projects\PSAReadLog\PASS-\2020-9-1\PASS
    #         for filename in os.listdir(base_dir):
    #             try:
    #                 assert  filename.endswith('.csv')
    #                 pathx = base_dir + '\\' + filename 
    #                 results = FindOneRecode(506,pathx)   
    #                 if results is None:
    #                     pass
    #                 else:
    #                     save_to_csv(filename[5:14],results,filename[26:34],'FindOneData.csv')   
    #             except AssertionError:
    #                 pass
    #     except FileNotFoundError:
    #         pass



