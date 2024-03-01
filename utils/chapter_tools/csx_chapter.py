from apps.project.models import Round

def create_csx_chapter_dict(one_round: Round, ):
    """传入轮次对象，返回测试项类型数组and测试项key的字典，以便后续使用"""
    testType_list = []
    last_chapter_items = {}
    if one_round:
        for csx in one_round.rtField.all():
            if csx.testType not in testType_list:
                testType_list.append(csx.testType)
        testType_list.sort(key=lambda x: int(x), reverse=False)
        for test_type in testType_list:
            last_chapter_items[test_type] = []
        for csx in one_round.rtField.all():
            last_chapter_items[csx.testType].append(csx.key)
    return testType_list, last_chapter_items
