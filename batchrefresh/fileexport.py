import os
import shutil
import util

'''
学院和专业数据文件拷贝
1、如果是学院报告，需要上传16、17届各学院文件夹下对应学院的主数据源excel(一共2个),
18届各学院文件夹下对应学院里的所有excel(大概是10-11个）
2、如果是专业报告，需要上传16、17届各专业文件夹下对应专业的主数据源excel（一共2个),
18届各专业文件夹下对应专业里的所有excel(大概是10-11个),除此之外还需要上传本专业对应的学院数据，及情况1中的数据源。
'''

def xy_filecopy():
    copyconfig={
        "exportlist":[
            {
                'from':r'E:\newjincin\projects\ros\doc\16届数据\分院系\材料与化学化工学部\主数据源.xlsx',
                'to':r'c:\testcopy\test1',
                'type':'file'
            },
            {
                'from':r'E:\newjincin\projects\ros\doc\17届数据\分院系\材料与化学化工学部\主数据源.xlsx',
                'to':r'c:\testcopy\test2',
                'type':'file'
            },
            {
                'from':r'E:\newjincin\projects\ros\doc\18届数据\分院系\材料与化学化工学部',
                'to':r'c:\testcopy\test3',
                'type':'directory'
            }
        ]
    }
    for copyopt in copyconfig['exportlist']:
        if copyopt['type']=='file':
            shutil.copy(copyopt['from'],copyopt['to'])
        else:
            util.xcopy(copyopt['from'],copyopt['to'])

    print('学院导出 copy')

def test_xy_filecopy():
    xy_filecopy()
    print('test complete')

if __name__ == "__main__":
    test_xy_filecopy()