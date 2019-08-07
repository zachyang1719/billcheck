from ..models import TableSets,RulesForMono
from ..common.base_sql_conn import DataBaseConnection

class MonoComputeCheck:
    def __init__(self, Tid, rules, key, uid): ###传一下uid，后续再改，自动去数据库捞uid
        self.Tid = Tid
        self.rules = rules
        self.key = key
        self.uid = uid

    def check_rules(self):
        db_info = self.get_db_info(self.Tid)
        sql = self.get_sql(db_info)
        conn = DataBaseConnection(host=db_info['host'], port=db_info['port'], user=db_info['user'], passwd= db_info['passwd'], db= db_info['db'], sql=sql)
        data = conn.get_data()  #一个dict
        # print('data {} , type为{}'.format(data,type(data)))
        if data != ():
            check_rules = self.get_rules(db_info)  #一个装有dict的list
            print(check_rules)
            result = self.get_result(check_rules, data[0])
            print(result)
            return result
        else:
            # print('走入正确轨道')
            return None

    def get_result(self, check_rules, data):
        result = []
        for i in check_rules:
            if i is None:
                result.append(2)   #未选择的为记为2
            else:
                fields_factor = i['factors'].split('@')
                actual_amount = data[fields_factor[0]]
                expect_amount = data[i['result']]
                for j in range(len(i['operation'])):
                    if i['operation'][j] == '+':
                        actual_amount += data[fields_factor[j+1]]
                    else:
                        actual_amount -= data[fields_factor[j-1]]
                if actual_amount == expect_amount:
                    result.append(1)    #选择且校验成功的记为1
                else:
                    result.append(0)    #选择但校验失败的记为0
        return result

    def get_rules(self, db_info):
        rules_raw = RulesForMono.objects.filter(related_tables=db_info['Tid'])
        rule_active = self.rules.split(',')
        rules = []
        for i in range(rules_raw.count()):
            if rule_active[i] == '0':
                rules.append(None)
            else:
                rule_raw = rules_raw[i].rules_for_computation
                formula = rule_raw.split('=')
                formula_factors = formula[0]
                formula_result = formula[1]
                operational_symbol = []
                rule = {}
                for j in formula_factors:
                    if j == '+':
                        operational_symbol.append('+')
                        formula_factors = formula_factors.replace("+", '@', 1)  #形如a1@a2@a5
                    elif j == '-':
                        operational_symbol.append('-')
                        formula_factors = formula_factors.replace("-", '@', 1)
                rule['factors'] = formula_factors
                rule['operation'] = operational_symbol
                rule['result'] = formula_result
                rules.append(rule)
        return rules

    def get_db_info(self,Tid):
        table_raw_info = TableSets.objects.filter(Tid=Tid)[0]
        table_info = {}
        table_info['Tid'] = table_raw_info.Tid
        table_info['host'] = table_raw_info.host
        table_info['port'] = table_raw_info.port
        table_info['user'] = table_raw_info.user_name
        table_info['passwd'] = table_raw_info.user_name+'@123'
        table_info['db'] = table_raw_info.instance_name
        table_info['divided'] = table_raw_info.divided
        table_info['table_name'] = table_raw_info.table_name
        table_info['database_name'] = table_raw_info.database_name
        return table_info

    def get_sql(self, db_info):
        # select * from xxx.xxx where xxxxx = key
        if db_info['divided']:
            xx = '0'+str(int(self.uid)//10000000)
            yy = self.uid[-3:-1]
            z = self.uid[-1]
            database_name_pre = db_info['database_name'].split('_')
            database_name = database_name_pre[0]+"_"+xx+"_"+yy+"_"+database_name_pre[1]
            table_name = db_info['table_name']+'_'+z
            db_table_name = database_name+'.'+table_name
        else:
            db_table_name = db_info['database_name']+'.'+db_info['table_name']
        sql = 'SELECT * FROM ' + db_table_name + ' WHERE '+ self.key['key'] + ' = ' + "'" +self.key['value']+ "'"  ###views传进来的key的格式注意下
        return sql