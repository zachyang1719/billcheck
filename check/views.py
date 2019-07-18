from django.shortcuts import render,HttpResponse
from .models import TableSets,RulesForMono
from .compute.cptfunc import MonoComputeCheck
import json

# Create your views here.
def mono_computaion(request):
    table_name = request.GET.get('', '')
    print(request.GET)
    print(table_name)
    if table_name=='':
        table_id=1
        current_queryset = TableSets.objects.filter(Tid=table_id)[0]
        current_table= current_queryset.database_name+'.'+current_queryset.table_name
    else:
        table_info = table_name.split('.')
        print(table_info)
        current_table = '.'.join(table_info)
        table_id = TableSets.objects.filter(database_name=table_info[0], table_name=table_info[1])[0].Tid
    tables = TableSets.objects.all()
    rules = RulesForMono.objects.filter(related_tables=table_id, rule_type='computation')#用request获取related_tables
    rule_list = []
    table_list = []
    for table in tables:
        table_list.append(table.database_name+'.'+table.table_name)
    for rule in rules:
        rule_list.append(rule.rules_for_computation)
    context = {'table_list': table_list,
               'rule_list': rule_list,
               'current_table': current_table,
               }
    return render(request, "monocpt.html", context)

def mono_compute(request):
    table_name = request.GET.get('table','')
    rule_active = request.GET.get('rules','')
    key = request.GET.get('key','')
    uid = request.GET.get('uid','')
    table_info_raw = table_name.split('.')
    Tid = TableSets.objects.filter(database_name=table_info_raw[0], table_name=table_info_raw[1])[0].Tid
    key_info_raw = key.split("=")
    key_info ={}
    key_info['key'] = key_info_raw[0]
    key_info['value'] =key_info_raw[1].strip()
    compute = MonoComputeCheck(Tid=Tid, rules=rule_active, key=key_info, uid=uid)
    results = compute.check_rules()
    print('the results are {}'.format(results))
    # print(type(results))
    rules = RulesForMono.objects.filter(related_tables=Tid, rule_type='computation')
    rule_dict = {}
    rule_list=[]
    for index, rule in enumerate(rules):
        rule_dict['{}'.format(rule.rules_for_computation)] = results[index]
        rule_list.append(rule.rules_for_computation)
    print(rule_dict)
    print(rule_dict.keys())
    for i in rule_dict.keys():
        print (i)
        print(type(i))
    print(json.dumps(rule_dict))
    return render(request, "monocpt_results.html", context={'results': rule_dict})
    # return HttpResponse('This is another milestone,congratulations!')