import datetime
import sqlite3
from threading import RLock

from DBUtils.PooledDB import PooledDB, SharedDBConnection

LOCK = RLock()
POOL = PooledDB(
    creator=sqlite3,  # 使用链接数据库的模块
    maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
    maxshared=3,  # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
    setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    ping=0,
    # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
    database='posts.db')  # 需要手动创建一个db文件


class Db:

    def __init__(self):
        # 检测当前正在运行连接数的是否小于最大链接数，如果不小于则：等待或报raise TooManyConnections异常
        # 否则
        # 则优先去初始化时创建的链接中获取链接 SteadyDBConnection。
        # 然后将SteadyDBConnection对象封装到PooledDedicatedDBConnection中并返回。
        # 如果最开始创建的链接没有链接，则去创建一个SteadyDBConnection对象，再封装到PooledDedicatedDBConnection中并返回。
        # 一旦关闭链接后，连接就返回到连接池让后续线程继续使用。
        # print(th, '链接被拿走了', conn1._con)
        # print(th, '池子里目前有', pool._idle_cache, '\r\n')

        self.conn = POOL.connection()

        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d
        self.conn.row_factory = dict_factory
        self.cursor = self.conn.cursor()

    def fetch_one(self, sql):
        with LOCK:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            self.conn.close()
            return result

    def fetch_all(self, sql):
        with LOCK:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.conn.close()
            return result

    def get_measure_value(self, log_name, test_item):
        with LOCK:
            data = self.fetch_all(
                "select * from loglist where PPID='%s'" % log_name)
            get_csv_testitems = []
            get_csv_testitems_result = []
            for row in data:
                get_csv_testitems.append(row[2])
            for row in data:
                get_csv_testitems_result.append(row[3])
            data_combine = dict(
                zip(get_csv_testitems, get_csv_testitems_result))
            return data_combine[test_item]

    def from_logname_get_allvalue(self, log_name):
        with LOCK:
            data = self.fetch_all(
                "select * from loglist where PPID='%s'" % log_name)
            return data

    def from_db_get_select_testitem(self, name):
        with LOCK:
            data = self.fetch_all(
                "select * from loglist where TestItem='%s'" % name)
            return data

    def create_mysqldatabasetable(self):
        conn = sqlite3.connect('posts.db')  # 手动先创建一个posts.db文件
        cur = conn.cursor()
        sql = 'create table loglist(ID INTEGER PRIMARY KEY AUTOINCREMENT, PPID varchar(30), TestItem varchar(30), MeasureValue varchar(30), Result varchar(30), DateTime varchar(30))'
        cur.execute(sql)

    def mysqldata(self, log_name, dict_data):
        with LOCK:
            now = datetime.datetime.now()
            # sql = "INSERT into loglist(ID,PPID,TestItem,MeasureValue,Result,DateTime) values(%s,%s,%s,%s,%s,%s)"
            sql = "INSERT into EolPassList(ID,PPID,TestItem,MeasureValue,Result,DateTime) values(?,?,?,?,?,?)"
            val_eol = (
                (None, log_name, 'Sleep Power Current Measure',
                 dict_data['Sleep Power Current Measure'], 'PASS', now),
                (None, log_name, 'Standby Power Current Measure',
                 dict_data['Standby Power Current Measure'], 'PASS', now),
                (None, log_name, 'Read FTEAEXC_UResExcAvg',
                 dict_data['Read FTEAEXC_UResExcAvg'], 'PASS', now),
                (None, log_name, 'Read MAIN_VSIRxsGridVoltW',
                 dict_data['Read MAIN_VSIRxsGridVoltW'], 'PASS', now),
                (None, log_name, 'Read T_Iuvw3_U16[0]',
                 dict_data['Read T_Iuvw3_U16[0]'], 'PASS', now),
                (None, log_name, 'Read T_Iuvw3_U16[1]',
                 dict_data['Read T_Iuvw3_U16[1]'], 'PASS', now),
                (None, log_name, 'Read T_Iuvw3_U16[2]',
                 dict_data['Read T_Iuvw3_U16[2]'], 'PASS', now),
                (None, log_name, 'Read FS_IbatHV_U16',
                 dict_data['Read FS_IbatHV_U16'], 'PASS', now),
                (None, log_name, 'Read HV_FS_FaultLevel_U16',
                 dict_data['Read HV_FS_FaultLevel_U16'], 'PASS', now),
                (None, log_name, 'Read FSEABHV_UbatHV',
                 dict_data['Read FSEABHV_UbatHV'], 'PASS', now),
                (None, log_name, 'Read FSMAPMT_PmTemp',
                 dict_data['Read FSMAPMT_PmTemp'], 'PASS', now),
                (None, log_name, 'Read FSMADBT_DboardTemp',
                 dict_data['Read FSMADBT_DboardTemp'], 'PASS', now),
                (None, log_name, 'Read FSMACBT_CboardTempHV',
                 dict_data['Read FSMACBT_CboardTempHV'], 'PASS', now),
                (None, log_name, 'Read FSMACBT_CboardTempLV',
                 dict_data['Read FSMACBT_CboardTempLV'], 'PASS', now),
                (None, log_name, 'Read FSMAICT_CoolingTemp',
                 dict_data['Read FSMAICT_CoolingTemp'], 'PASS', now),
                (None, log_name, 'Read FSMAMST_StatorTemp1',
                 dict_data['Read FSMAMST_StatorTemp1'], 'PASS', now),
                (None, log_name, 'Read FSMAMST_StatorTemp2',
                 dict_data['Read FSMAMST_StatorTemp2'], 'PASS', now),
                (None, log_name, 'Resolver excitation',
                 dict_data['Resolver excitation'], 'PASS', now),
                (None, log_name, 'Read FT_ResolverSin_U16 Max',
                 dict_data['Read FT_ResolverSin_U16 Max'], 'PASS', now),
                (None, log_name, 'Read FT_ResolverSin_U16 Min',
                 dict_data['Read FT_ResolverSin_U16 Min'], 'PASS', now),
                (None, log_name, 'Read FT_ResolverCos_U16 Max',
                 dict_data['Read FT_ResolverCos_U16 Max'], 'PASS', now),
                (None, log_name, 'Read FT_ResolverCos_U16 Min',
                 dict_data['Read FT_ResolverCos_U16 Min'], 'PASS', now),
                (None, log_name, 'Switch Measure Current',
                 dict_data['Switch Measure Current'], 'PASS', now),
                (None, log_name, 'Active discharge time',
                 dict_data['Active discharge 450V to 60V'], 'PASS', now),
                (None, log_name, 'Passive discharge time',
                 dict_data['Passive discharge 450V to 60V'], 'PASS', now),
                (None, log_name, 'Read Dcs_bMot Current',
                 dict_data['Read Dcs_bMot Measure Current'], 'PASS', now),
                (None, log_name, 'Read Pls_bMot Current',
                 dict_data['Read Pls_bMot Measure Current'], 'PASS', now),
                (None, log_name, 'Read Interlock status',
                 dict_data['Read MAIN_MSGu8InverterHVILStatus'], 'PASS', now),
                (None, log_name, 'FSMABLV_UbatLVCorGainC',
                 dict_data['Read FSMABLV_UbatLVCorGainC'], 'PASS', now),
                (None, log_name, 'FSMABLV_UbatLVCorOffsetC',
                 dict_data['Read FSMABLV_UbatLVCorOffsetC'], 'PASS', now),
                (None, log_name, 'HV_CorGainC',
                 dict_data['Read HV_CorGainC'], 'PASS', now),
                (None, log_name, 'HV_CorOffsetC',
                 dict_data['Read HV_CorOffsetC'], 'PASS', now),
                (None, log_name, 'FTEAMPI_A2DGainIsuLC',
                 dict_data['Read FTEAMPI_A2DGainIsuLC'], 'PASS', now),
                (None, log_name, 'FTEAMPI_A2DGainIsvLC',
                 dict_data['Read FTEAMPI_A2DGainIsvLC'], 'PASS', now),
                (None, log_name, 'FTEAMPI_A2DGainIswLC',
                 dict_data['Read FTEAMPI_A2DGainIswLC'], 'PASS', now),
                (None, log_name, 'SAMTLCS_A2DGainIsuLC',
                 dict_data['Read SAMTLCS_A2DGainIsuLC'], 'PASS', now),
                (None, log_name, 'SAMTLCS_A2DGainIsvLC',
                 dict_data['Read SAMTLCS_A2DGainIsvLC'], 'PASS', now),
                (None, log_name, 'SAMTLCS_A2DGainIswLC', dict_data['Read SAMTLCS_A2DGainIswLC'], 'PASS', now))

            self.cursor.executemany(sql, val_eol)
            self.conn.commit()

    def mysql_insert_fail_data(self, log_name, list_data):
        with LOCK:
            now = datetime.datetime.now()
            # sql = "INSERT into loglist(ID,PPID,TestItem,MeasureValue,Result,DateTime) values(%s,%s,%s,%s,%s,%s)"
            sql = "INSERT into EolFailList(ID,PPID,TestItem,MeasureValue,Result,DateTime) values(?,?,?,?,?,?)"
            val_eol = (
                (None, log_name, list_data[0],
                 list_data[1], 'Failed', now))

            self.cursor.execute(sql, val_eol)
            self.conn.commit()



if __name__ == '__main__':
    db = Db()
    # result = db.get_measure_value('EOL_!192780029!_V29113441__20191229_040551.csv','Sleep Power Current Measure')
    # print(result)
    # print(db.from_logname_get_allvalue('EOL_!192780029!_V29113441__20191229_040551.csv'))
    print(db.from_db_get_select_testitem('SAMTLCS_A2DGainIsuLC'))
