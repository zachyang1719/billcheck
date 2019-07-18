from django.db import models

# Create your models here.

class TableSets(models.Model):
    Tid = models.AutoField(primary_key=True)
    instance_name = models.CharField(max_length=15)
    database_name = models.CharField(max_length=40)
    table_name = models.CharField(max_length=45)
    user_name = models.CharField(max_length=15)
    divided = models.BooleanField(default=False)
    host = models.CharField(max_length=20, blank=False, default='0.0.0.0')
    port = models.IntegerField(default=20025)
    create_time = models.DateTimeField(auto_now_add=True)
    last_modify_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}.{}[{}]".format(self.database_name, self.table_name,self.instance_name)

    class Meta:
        db_table = 'table_sets'
        unique_together = ('database_name','table_name')


class RulesForMono(models.Model):
    # rule_type = models.IntegerField(default=0) #规则类型，0代表单库表数据校对，1表示单表状态维度校验，以后可再增加
    rule_type = models.CharField(max_length=15, choices=(('computation', '单库表数据校对'),('observation', '单表状态维度校验')), default='computation')
    rules_for_computation = models.TextField(max_length=100, null=True, blank=True)
    fields_for_observation = models.TextField(max_length=100, null=True, blank=True)
    related_tables = models.ForeignKey(TableSets, on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True)
    last_modify_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.rule_type==0:
            return "rule is {}".format(self.rules_for_computation)
        else:
            return "fields for observation include {}".format(self.fields_for_observation)

    class Meta:
        db_table = 'rules_for_mono'

# class RulesForMulti(models.Model):
#     rule_type = models.CharField(max_length=30)
#     #table_src = models.ForeignKey(TableSets, on_delete=models.DO_NOTHING, default=None)
#     #table_obj = models.ForeignKey(TableSets, on_delete=models.DO_NOTHING, default=None)
#     field_src = models.CharField(max_length=10)
#     field_obj = models.CharField(max_length=10)