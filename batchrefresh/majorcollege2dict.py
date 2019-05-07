import openpyxl

def major_college_mapping(mappingpath):
    data = openpyxl.load_workbook(mappingpath)
    sheet1 = data['sheet1']
    if sheet1.max_row<2:
        print("学院专业映射文件行数少于2,文件路径为:{}".format(mappingpath))
        raise Exception("学院专业映射文件行数少于2,文件路径为:{}".format(mappingpath))
    if sheet1.max_column<2:
        print("学院专业映射文件列数少于2,文件路径为:{}".format(mappingpath))
        raise Exception("学院专业映射文件列数少于2,文件路径为:{}".format(mappingpath))
    major_college_mapper={}
    for i in range(2,sheet1.max_row):
        major=sheet1.cell(row=i,column=2).value
        college=sheet1.cell(row=i,column=1).value
        major_college_mapper[major]=college
    #print(major_college_mapper)
    return major_college_mapper

def test_major_college_mapping():
    path=r'e:\newjincin\projects\ros\doc\18届数据\院系-专业对照表.xlsx'
    major_college_mapping(path)
if __name__ == "__main__":
    test_major_college_mapping()
        
    
        
    