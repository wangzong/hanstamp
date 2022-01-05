from django.shortcuts import render, redirect

from .models import Wzz
from .forms import HanziForm

# Create your views here.
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
    hanzis = Wzz.objects.filter(character=char)
    context = {"hanzis":hanzis}
    return render(request,'hs/hanzi.html', context)


def search(request):
    searchinput = request.GET.get('search')
    error_msg = ''

    if not searchinput:
        error_msg = '请输入关键词'
        return render(request, 'hs/index.html', {'error_msg': error_msg})

    hanzis = Wzz.objects.filter(character=searchinput)
    if len(hanzis) == 0:
        error_msg = '未找到此字'
    return render(request, 'hs/index.html', {'hanzis': hanzis,'error_msg':error_msg })

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

