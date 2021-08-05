#-*- coding:utf-8 -*-#
#-------------------------------------------------------------------------
#ProjectName:       replay
#FileName:          yujiao_count.py
#Author:            orange
#Date:              2021/7/13 9:41
#Description:   统计预收现金流
#--------------------------------------------------------------------------
#业务订单--字段说明
#支付渠道：trade_type_tag_name
#收费主体：charge_body
#实收金额：amount
#------------------------------统计业务订单中多种渠道中有多少个户数以及各实付总金额------------------------------------------------
from requests import Session
s=Session()

#得到所有已支付、预收费且创建时间为6月的业务订单数据
def qingqiu(token,app_id,project_id):
    request_url="pass"
    data1 ={"app_id": app_id,
    "method": "pass",
    "format": "json",
    "charset": "utf8",
    "timestamp": "pass",
    "token": token,
    "biz_content": 'pass'
    return_data=s.request(method="POST",url=request_url,data=data1)
    num1=return_data.json()["content"]["count"]
    list1=[]
    for i in range(1, int(num1 / 100 + 1) + 1):
        data2 = {"app_id": app_id,
                "method": "pass",
                "format": "json",
                "charset": "utf8",
                "timestamp": "pass",
                "token": token,
                "biz_content": 'pass'
        return_num1 = s.request(method="post", url=request_url, data=data2)
        list1+=return_num1.json()["content"]["lists"]
    return list1
#通过最基础的数据，获取到每一个业务订单的tnum，获取到每个业务订单的详情数据
def get_tnum(token,app_id,tnum):
    URL="pass"
    data={"app_id":app_id,
        "method": "pass",
        "format": "json",
        "charset": "utf8",
        "timestamp": "pass",
        "token": token,
        # "biz_content": '{"tnum":%s}'%str(tnum)}#检查结果是数字
          "biz_content": '{"tnum":"%s"}'%tnum}  #原因就是因为第二个字典没有按照"%s"格式书写占位符的
    return s.request(method="post",url=URL,data=data).json()
#拼接基础数据和详情数据，并且在这两类数据进行计算，得出总数
#通过判断打开每一个详情，如果每一个trade_type：预收费，那么它就是记录到物业管理费中的预收现金流
#       如果trade_type不等于预收费，那么记录到对应科目即可

#测试代码
# result=qingqiu(token,app_id)
# print(len(result))
# tunm="19373084947094323210037"
# result1=get_tnum(token,app_id,tunm)
# print(result1['content'])

# file_handle=open("zjj_yanzheng.txt",mode="w",encoding="utf-8")
# file_handle.write(str(result))

#获得按月缴费和按现金缴费两类数据,按月缴费的详情数据在count()[0]中,按现金缴费的详情数据在count()[1]中
def dataclassify_count(token,app_id,project_id):
    result=qingqiu(token,app_id,project_id)
    xiangqing_data=[]
    not_xiangqing=[]
    for i in result:
        result1=get_tnum(token,app_id,i["tnum"]) #就是这一步，需要循环访问接口导致很慢
        if result1["content"][0]["trade_type"] != "预收费":
            list1=get_tnum(token,app_id,i["tnum"])
            xiangqing_data+=list1["content"]
        else:
            not_xiangqing.append(get_tnum(token,app_id,i["tnum"]))
    return xiangqing_data,not_xiangqing

#按月统计
def anyueamount_count(token,app_id,project_id):
    data_count=dataclassify_count(token,app_id,project_id)
    trade_type1={}
    num=0
    for i in data_count[0]: #整理出按月统计的所有数据
        num+=1
        trade_type1[(i["trade_type"])+str(num)]=i["total_amount"]
    return trade_type1

# print(qitaamount_count(token,app_id))
# print(len(dataclassify_count(token,app_id)[1]),dataclassify_count(token,app_id)[1])
#物业费用的统计
def wuyeamount_count(token,app_id,project_id):
    data_count=dataclassify_count(token,app_id,project_id)
    amount1=0
    for i in data_count[1]:
        amount1+=i["content"][0]["amount"]
    data_count1=anyueamount_count(token,app_id,project_id)
    for j in data_count1:
        if "物业" in j:
            amount1+=data_count1[j]
    return amount1

#其他费用的统计
def qitaamount_count(token,app_id,project_id,feiyong):
    amount1 = 0
    data_count1 = anyueamount_count(token, app_id,project_id)
    for j in data_count1:
        if feiyong in j:
            amount1 += data_count1[j]
    return amount1

if __name__ == '__main__':
    token = "pass"
    app_id = "pass"
    project_id="pass"
    result=qingqiu(token,app_id,project_id)
    print(len(result))
    print(wuyeamount_count(token,app_id,project_id))


