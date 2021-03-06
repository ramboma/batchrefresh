import os
import shutil
import util
import majorcollege2dict
import logging

'''
学院和专业数据文件拷贝
1、如果是学院报告，需要上传16、17届各学院文件夹下对应学院的主数据源excel(一共2个),
18届各学院文件夹下对应学院里的所有excel(大概是10-11个）
2、如果是专业报告，需要上传16、17届各专业文件夹下对应专业的主数据源excel（一共2个),
18届各专业文件夹下对应专业里的所有excel(大概是10-11个),除此之外还需要上传本专业对应的学院数据，及情况1中的数据源。
'''


logger=util.create_logger(logging.INFO,'fileexport')

def print_and_info(msg):
    logger.info(msg)
    print(msg)
# 检查学院路径是否存在,不存在就在alias列表中查找，有则替换,没有则返回'空学院'
def check_college_has_null_or_alias(college_name, college_path, college_alias):
    print_and_info(college_name)
    path = college_path.format(college_name)
    if os.path.exists(path) == True:  # 存在则返回
        return path
    # 在alias列表中查找
    result = ''
    if college_name in college_alias:
        print_and_info('{}->学院在路径上{}存在别名'.format(college_name, college_path))
        aliaslist = college_alias[college_name]
        for alias in aliaslist:
            aliaspath = college_path.format(alias)
            if os.path.exists(aliaspath) == True:
                result = aliaspath
                break
    if result == '':  # 不在别名列表中,返回'空学院'
        print_and_info("{}下学院名称不存在,将替换为空学院数据".format(path))
        result = college_path.format('空学院')
    return result

# 学院导出


def college_filecopy(college_name, college_config, college_alias):
    # 如果学院名称对应的路径不存在,就把学院名称替换为别名学院或"空学院"
    for copyopt in college_config['exportlist']:
        sourcepath = check_college_has_null_or_alias(
            college_name, copyopt['from'], college_alias)
        if copyopt['type'] == 'file':
            shutil.copy(sourcepath, copyopt['to'])
        else:
            util.xcopy(sourcepath, copyopt['to'])
        print('{}导出至--->{}!'.format(sourcepath, copyopt['to']))
    print_and_info('{}导出完毕!'.format(college_name))


# 检查专业路径是否存在，存在则返回，不存在则返回空专业
def check_major_has_null_or_alias(major_name, major_path):
    print(major_name)
    path = major_path.format(major_name)
    if os.path.exists(path) == True:  # 存在则返回
        return path
    return major_path.format('空专业')

# 专业导出

def major_filecopy(major_name, majorconfig):
    print("专业{}开始导出...".format(major_name))
    for copyopt in majorconfig['exportlist']:
        sourcepath=check_major_has_null_or_alias(major_name,copyopt['from'])
        if copyopt['type'] == 'file':
            shutil.copy(sourcepath, copyopt['to'])
        else:
            util.xcopy(sourcepath, copyopt['to'])
        print('{}导出至--->{}!'.format(sourcepath, copyopt['to']))
    # 本专业对应的学院
    #college_name = majorcollege2dict.major_college_mapping(majorconfig['college_major_mapping_file'])[major_name]
    #print("专业{}对应的学院名称为{}".format(major_name, college_name))
    print_and_info("专业{}导出完毕!".format(major_name))
    # 再导出相应学院
    # college_filecopy(college_name)


def test_college_filecopy():
    # college_filecopy()
    print('test complete')


if __name__ == "__main__":
    # test_college_filecopy()
    major_config = {
        "exportlist": [
            {
                'from': r'e:\newjincin\projects\ros\doc\16届数据\分专业\{}\主数据源.xlsx',
                'to': r'c:\zycopy\test1',
                'type': 'file'
            },
            {
                'from': r'e:\newjincin\projects\ros\doc\17届数据\分专业\{}\主数据源.xlsx',
                'to': r'c:\zycopy\test2',
                'type': 'file'
            },
            {
                'from': r'E:\newjincin\projects\ros\doc\18届数据\分专业\{}',
                'to': r'c:\zycopy\test3',
                'type': 'directory'
            }
        ],
    }
    major_filecopy('naxx', major_config)
