from django.shortcuts import render, redirect
from django.db.models import Q
import sqlite3
import logging

from .models import Wzz
from .forms import HanziForm

# Create your views here.

picurl = '\\汉印文字征分列图片'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def index(request):
    """定义主页"""
    # 此函数是由urls.py中调用的
    # hanzis = Wzz.objects.all()
    # context = {"hanzis":hanzis}
    return render(request,'hs/index.html')
    # return render(request, 'hs/index.html')

def hanzis(request,char="神"):
    """显示所有汉字"""
    # 可能是多个相同字的记录
    # hanzis = Wzz.objects.get(component_contains=char)
    # hanzis = Wzz.objects.filter(Q(character=char)|Q(component__contains=char))
    context = {"hanzis":hanzis}
    return render(request,'hs/hanzi.html', context)


def search(request):
    searchinput = request.GET.get('search')
    # 这里的search是index.html中的name=search的form
    error_msg = ''

    # 这句可以不要，因为search的form已经是required
    if not searchinput:
        error_msg = '请输入关键词'
        return render(request, 'hs/index.html', {'error_msg': error_msg})

    # hanzis = Wzz.objects.filter(character=searchinput)
    # hanzis = Wzz.objects.filter(Q(component__contains=searchinput)|Q(character=searchinput))

    mydb = sqlite3.connect('db.sqlite3')
    mydb.row_factory = sqlite3.Row
    # cursor = mydb.cursor()
    sql_statement = "SELECT * from wzz where character like '%" + searchinput + "%'" \
                    + "OR component like '%" + searchinput +"%'" \
                    + "OR simplified like '%" + searchinput +"%'"
    values = mydb.execute(sql_statement).fetchall()
    logger.info(values)
    # print(values)
    # result = query.fetchall()

    list_result = []

    if len(values) == 0:
        error_msg = '未找到此字'
    dict_values = []
    for value in values:
        dict_values.append({"character": value['character'],
                            "component": value['component'],
                            "simplified": value['simplified'],
                            "picurl": picurl + '\\'+ value['index_code']+'.jpg'})
    return render(request, 'hs/index.html', {'hanzis': dict_values,'error_msg':error_msg })

# def hanzi(request, char_id):
#     char = WZZ.objects.get(id=char_id)
#     context = {'char':char}
#     return render(request,'hs/index.html',context)


# def hanzis(request):
#     """显示所有汉字"""
#     hanzis = Hanzi.objects.all()
#     # print(hanzis)
#     context = {"hanzis":hanzis}
#     # context = {"hanzis":['王']}
#     return render(request,'hs/index.html', context)

# def new_hanzi(request):
#     """添加汉字"""
#     if request.method != 'POST':
#         # 未提交数据：则创建一个新表单
#         form = HanziForm()
#     else:
#         # POST提交数据：对数据进行处理
#         form = HanziForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('hs:index')
#
#     context = {'form':form}
#     return render(request, 'hs/new_hanzi.html', context)

