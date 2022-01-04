from django.shortcuts import render, redirect

from .models import Wzz
from .forms import HanziForm

# Create your views here.
def index(request):
    """定义主页"""
    # 此函数是由urls.py中调用的
    hanzis = Wzz.objects.all()
    context = {"hanzis":hanzis}
    return render(request,'hs/index.html', context)
    # return render(request, 'hs/index.html')

def hanzi(request):
    """显示所有汉字"""
    hanzi = Wzz.objects.get(character="神")
    context = {"hanzi":hanzi}
    return render(request,'hs/hanzi.html', context)

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

