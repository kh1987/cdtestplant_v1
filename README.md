# cdtestplant_v1
后端django-ninja-extra改造，但主要还是ninja内容

## 问题1：部分生成文档字段判断字典值使用硬编码

### 1.create_adequancy_effectiveness

```python
# 在create_adequacy_effectiveness函数
# 获取每个测试项测试类型
test_type = get_list_dict('testType', testDemand.testType)[0].get('ident_version')
# 如果字典没有该key，则创建并value=1
if not test_type in type_dict:
    type_dict[test_type] = 1
else:
    type_dict[test_type] += 1
```

### 2.create_requirement

```python
# 1.被测件类型
dut_qs = round1.rdField.filter(Q(type='XQ') | Q(type='XY') | Q(type='SJ'))

# 2.安全等级
security_boolean = True if int(project_qs.security_level) <= 2 else False
```



### 3.create_information

```python
first_round_SO = project_round.rdField.filter(type='SO').first()
```



### 4.create_performance

```python
design_qs = project_qs.psField.filter(demandType=2)
```



### 5.create_funcList

```python
if designDemand.demandType == '1':
    func['func_name'] = designDemand.name
```

