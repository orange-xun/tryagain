# 计算截至到昨天晚上23:59:59，未缴费的欠费数据

#-*- coding:utf-8 -*-#
#-------------------------------------------------------------------------
#ProjectName:       replay
#FileName:          rework427.py
#Author:            orange
#Date:              2021/7/16 17:14
#Description:       计算昨天所在月所有的未缴费的欠费房屋
#--------------------------------------------------------------------------
from requests import Session
import datetime

#获取昨天时间和当前月月初时间
def get_data():
    #获取当天
    today=datetime.datetime.today()
    #获取昨天
    yesterday=str(today - datetime.timedelta(days=1))[:10]
    # 获取当前月月份第一天
    start_date = str(str(yesterday)[:9] + "1")
    return start_date,yesterday

#传入对应租户-项目-欠费列表的请求地址和token即可获取基础数据
def get_basedata(url,app_id,token):
    s = Session()
    request_url = url
    data = {"app_id": app_id,
            "method": "pass",
            "format": "json",
            "charset": "utf8",
            "timestamp": "pass",
            "biz_content":"pass"
    return_num = s.request(method="post", url=request_url, data=data).json()["content"]["total"]
    print(return_num)
    list1 = []
    for i in range(1, int(return_num / 100 + 1) + 1):
        data = {"app_id": app_id,
                "method": "pass",
                "format": "json",
                "charset": "utf8",
                "timestamp": "pass",
                "token": token,
                "biz_content": "pass"
        return_num1 = s.request(method="post", url=request_url, data=data)
        list1 += return_num1.json()["content"]["lists"]
    # print(list1[0]["arrears_begin_time"], len(list1), type(list1[0]["arrears_begin_time"]))
    return list1

#欠费列表字段说明：
#       pass

#先计算一下每栋房屋的欠费总额(因为每一栋房屋只有一条欠费数据，所以直接算就是了)
def get_amount(request_url,app_id,token):
    amount_sum={}
    for i in get_basedata(request_url,app_id,token):
        amount_sum[i["space_name_full"]]=((float(i["total_amount"]))*100+(float(i["penalty_money"]))*100)/100
    return amount_sum

#获取欠费列表中的详情数据
#只有在欠费列表中的欠费详情中才可以看到欠费具体的欠费月份以及欠费金额，后期如果要用到欠费费用类型还可以从此处获取
def get_xiangqingdata(request_url, app_id, token):
    basedata = get_basedata(request_url, app_id, token)
    list3=[]
    for i in range(len(basedata)):
        for j in range(len(basedata[i]['sub_arrears_detail']['lists'])):
            list2 = {}
            list2.update(basedata[i]['sub_arrears_detail']['lists'][j])
            list2["space_name_full"]=basedata[i]['space_name_full']
            list3.append(list2)
    # print(len(list3),list3)
    return list3    #list3已经获取到本月截至到前一天的所有欠费详情数据

#对所有欠费房屋的数据做一轮封装
#最终得到的结果是：{'1栋-2单元-1层-107室': ['2021-06', '2021-05', '2021-04', '2021-03'],'3栋-2单元-1层-101室': [].... }
#并且最终结果中的房屋是不会有重复的欠费月份
def get_house(request_url, app_id, token):
    list3=get_xiangqingdata(request_url, app_id, token)
    jihe1=[]
    for i in list3:
        jihe1.append(i["space_name_full"])
    jihe1=list(set(jihe1)) #对所有欠费详情数据再做一轮筛选，以便获取到所有欠费的房屋

    #根据上述获取的欠费房屋，使其所有数据变为字典格式；欠费房屋为key，欠费月数为value   (当然value可能存在重复欠费月份)
    dict2={}
    for j in jihe1:
        dict2[j]=[]
    for i in jihe1:
        for j in list3:
            if i == j["space_name_full"]:
                dict2[i].append(j["arrears_sub_month"])
    #因为上述dict2中得到的数据是会有重复月份的,所以通过一个新的循环对欠费月份使用集合的方法去重
    dict3 = {}
    for i in dict2:
        dict3[i] = list(set(dict2[i]))
    return dict3

# 对每一个value计算一下长度，就能知道欠费几个月了
def change_house(request_url, app_id, token):
    dict3 = get_house(request_url, app_id, token)
    dict4 = {}
    for i in dict3:
        dict4[i] = len(dict3[i])  # 通过计算对应月份的列表长度,获取欠费几个月
    return dict4

#一、当欠费月数偏多时，怎么自动构造，不需要去重复写if条件语句
#二、怎么去过滤数据
#如果我声明两个字典，然后把里头所有的key和value类型都为数值，最后设定一个条件，当value为零时则不打印
def get_finaldata(request_url, app_id, token):
    dict4 = change_house(request_url, app_id, token)
    amount_sum = get_amount(request_url, app_id, token)
    zidian1={} #计算有多少户(欠费一个月的有多少户,欠费两个月的有多少户...)
    zidian2={} #计算有多少金额
        #上面这两个字典的key，表示欠费月数
    for i in dict4:
        if dict4[i] in zidian1.keys():
            zidian1[dict4[i]]=zidian1[dict4[i]]+1
            zidian2[dict4[i]]=zidian2[dict4[i]]+amount_sum[i]
        else:
            zidian1[dict4[i]]=1
            zidian2[dict4[i]]=amount_sum[i]
    #  最终的结果是:zidian1中以欠费月数为key,欠费该月数对应有多少户为value
    #           zidian2中以欠费月数为key,欠费该月数对应的欠费金额为value
    return zidian1,zidian2

#前面所有部分属于后端操作逻辑,而接下来这一步就是前端数据展示要做的
#   把整理出来的数据按"欠费XX个月有XX户,总欠费金额为：XX元"的格式展示出来
def show_data(request_url, app_id, token):
    finaldata=get_finaldata(request_url, app_id, token)
    zidian1=finaldata[0]
    zidian2=finaldata[1]
    qianfei_amout=0
    # print(sorted(list(zidian1.keys()))) #[1, 2, 3, 4, 5, 6]
    for i in sorted(list(zidian1.keys())):
        print("欠费{0}个月有{1}户,总欠费金额为：{2}元".format(i,zidian1[i],round(zidian2[i],2)))
        qianfei_amout+=round(zidian2[i],2)
    print("总欠费金额为：%d元"%qianfei_amout) #为啥这里只有整数呢？为啥计算不出小数部分呢？

#如果需要把欠费多少个月的数据给读到xs.txt文件中怎么做
def get_adddata(num,request_url, app_id, token):
    if type(num)==int:
        dict4 = change_house(request_url, app_id, token)
        dict5={}
        for i in dict4:
            if dict4[i]==num:
                dict5[i]=1
        #把数据写入到txt文件当中
        file_handle=open("zjj_yanzheng.txt",mode="w",encoding="utf-8")
        file_handle.write(str(dict5))
    else:
        return "num必须为正整数!"

if __name__ == '__main__':
    url="pass"
    token="pass"
    app_id="pass"
    #调用可计算本月1号到当天前一天的欠费数据
    show_data(url,app_id,token)
