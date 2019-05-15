import hashlib
import os
import uuid
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from Python1807AXF import settings
from app.models import Wheel, Nav, Mustbuy, Shop, Foodtypes, Goods, User, Cart, Order,OrderGoods


# 首页
def home(request):

    wheels = Wheel.objects.all()


    navs = Nav.objects.all()

    mustbuys = Mustbuy.objects.all()


    shops = Shop.objects.all()


    data = {
        'title': '首页',
        'wheels':wheels,
        'navs':navs,
        'mustbuys':mustbuys,
        'shops':shops,
    }

    return render(request, 'home/home.html', context=data)

def market(request, categoryid, childid, sortid):
    # 分类数据
    foodtypes = Foodtypes.objects.all()

    # 获取点击 历史 [typeIndex]
    # 有typeIndex
    # 无typeIndex，默认0
    typeIndex = int(request.COOKIES.get('typeIndex',0))
    print(foodtypes[typeIndex])
    categoryid = foodtypes[typeIndex].typeid


    # 子类
    childtypenames = foodtypes.get(typeid=categoryid).childtypenames # 对应分类下 子类字符串
    childlist = []
    for item in childtypenames.split('#'):
        arr = item.split(':')
        obj = {'childname':arr[0], 'childid':arr[1]}
        childlist.append(obj)


    # goodslist = Goods.objects.all()[1:10]


    if childid == '0':  # 全部分类
        goodslist = Goods.objects.filter(categoryid=categoryid).order_by('-id')
    else:   # 对应分类
        goodslist = Goods.objects.filter(categoryid=categoryid, childcid=childid).order_by('-id')

    # 排序处理
    if sortid == '1':   # 销量排序
        goodslist= goodslist.order_by('id')




    token = request.session.get('token')
    carts = []
    if token:
        user = User.objects.get(token=token)
        carts = Cart.objects.filter(user=user).exclude(number=0)

    data = {
        'title': '社区',
        'foodtypes':foodtypes,
        'goodslist':goodslist,
        'childlist':childlist,
        'categoryid':categoryid,
        'childid':childid,
        'carts': carts,
        'token':token,
    }

    return render(request, 'market/market.html', context=data)


def cart(request):
    token = request.session.get('token')
    carts = []
    if token:   # 已登录
        # 根据token获取对应用户
        user = User.objects.get(token=token)
        # 根据用户，获取对应购物车 数据
        carts = Cart.objects.filter(user=user).exclude(number=0)

    # 一个班级 对应 多个学生
    # 班级主表
    # 学生从表 【声明关系】

    responseDatra = {
        'title': '购物车',
        'carts': carts
    }


    return render(request, 'cart/cart.html', context=responseDatra)

# 我的中心
def mine(request):
    token = request.session.get('token')

    responseData = {
        'title': '我的中心',
        'payed': 0,
        'wait_pay': 0
    }

    if token:   # 登录
        user = User.objects.get(token=token)
        responseData['name'] = user.name
        responseData['rank'] = user.rank
        responseData['img'] = '/static/uploads/' + user.img
        responseData['islogin'] = True

        # 获取husti信息
        orders = Order.objects.filter(user=user)
        payed = 0
        wait_pay = 0
        for order in orders:
            if order.status == 1:
                wait_pay += 1
            elif order.status == 2:
                payed += 1

        responseData['payed'] = payed
        responseData['wait_pay'] = wait_pay


    else:       # 未登录
        responseData['name'] = '未登录'
        responseData['rank'] = '无等级(未登录)'
        responseData['img'] = '/static/uploads/axf.png'
        responseData['islogin'] = False

    return render(request, 'mine/mine.html', context=responseData)

# 注册
def register(request):
    if request.method == 'POST':
        user = User()
        user.account = request.POST.get('account')
        user.password = generate_password(request.POST.get('password'))
        user.name = request.POST.get('name')
        user.tel = request.POST.get('tel')
        user.address = request.POST.get('address')
        user.sex = request.POST.get('sex')
        user.age = request.POST.get('age')
        user.birthday = request.POST.get('birthday')
        user.xuexing = request.POST.get('xuexing')
        user.xingzuo = request.POST.get('xingzuo')
        istea = request.POST.get('istea')
        if istea == '学生':
            user.istea = 0
        else:
            user.istea = 1


        # 头像
        imgName = user.account + '.png'
        imgPath = os.path.join(settings.MEDIA_ROOT, imgName)
        print(imgPath)
        file = request.FILES.get('file')
        print(file)
        with open(imgPath, 'wb') as fp:
            for data in file.chunks():
                fp.write(data)
        user.img = imgName

        # token
        user.token = str(uuid.uuid5(uuid.uuid4(), 'register'))

        # 保存到数据库
        user.save()

        # 状态保持
        request.session['token'] = user.token

        # 重定向
        return redirect('axf:mine')

    elif request.method == 'GET':
        return render(request, 'mine/register.html')


# 密码
def generate_password(password):
    sha = hashlib.sha512()
    sha.update(password.encode('utf-8'))
    return sha.hexdigest()

# 退出登录
def quit(request):
    # request.session.flush()
    logout(request)
    return redirect('axf:mine')

# 登录
def login(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')

        try:
            user = User.objects.get(account=account)
            if user.password != generate_password(password):    # 密码错误
                return render(request, 'mine/login.html', context={'error': '密码错误!'})
            else:   # 登录成功
                # 更新token
                user.token = str(uuid.uuid5(uuid.uuid4(), 'login'))
                user.save()
                # 状态保持
                request.session['token'] = user.token
                return redirect('axf:mine')
        except:
            return render(request, 'mine/login.html', context={'error':'用户名有误，请检查后输入!'})

    elif request.method == 'GET':
        return render(request, 'mine/login.html')

# 用户验证
def checkuser(request):
    account = request.GET.get('account')
    try:
        user = User.objects.get(account=account)
        return JsonResponse({'msg':'用户名存在!', 'status':'-1'})
    except:
        return JsonResponse({'msg':'用户名可用!', 'status':'1'})


def addtocart(request):
    # goodsid
    goodsid = request.GET.get('goodsid')
    token = request.session.get('token')

    responseData = {
        'msg':'',
        'status':''
    }

    if token:   # 登录
        user = User.objects.get(token=token)
        goods = Goods.objects.get(pk=goodsid)

        carts = Cart.objects.filter(goods=goods).filter(user=user)
        if carts.exists():  # 存在
            cart = carts.first()
            cart.number = cart.number + 1
            if 0 < cart.number:
                cart.number = 1
            cart.save()
            responseData['msg'] = '添加购物车成功'
            responseData['status'] = 1
            responseData['number'] = cart.number
            return JsonResponse(responseData)
        else:           # 不在
            cart = Cart()
            cart.user = user
            cart.goods = goods
            cart.number = 1
            cart.save()

            responseData['msg'] = '添加购物车成功'
            responseData['status'] = 1
            responseData['number'] = cart.number
            return JsonResponse(responseData)
    else:       # 未登录
        # ajax请求操作，是重定向不了的！
        # return redirect('axf:login')

        responseData['msg'] = '请登录后操作'
        responseData['status'] = '-1'

        return JsonResponse(responseData)


def subtocart(request):
    token = request.session.get('token')
    user = User.objects.get(token=token)
    goodsid = request.GET.get('goodsid')
    goods = Goods.objects.get(pk=goodsid)


    carts = Cart.objects.filter(user=user).filter(goods=goods)
    cart = carts.first()
    cart.number = cart.number - 1
    cart.save()

    responseData = {
        'msg': '删减成功',
        'status': '1',
        'number': cart.number
    }

    return JsonResponse(responseData)

# 修改选中状态
def changecartstatus(request):
    cartid = request.GET.get('cartid')
    cart = Cart.objects.get(pk=cartid)
    cart.isselect = not cart.isselect
    cart.save()

    responseData = {
        'msg':'修改状态成功',
        'status':'1',
        'isselect': cart.isselect
    }

    return JsonResponse(responseData)

# 全选/取消全选
def changecartselect(request):
    isall = request.GET.get('isall')
    if isall == 'true':
        isall = True
    else:
        isall = False

    token = request.session.get('token')
    user = User.objects.get(token=token)
    carts = Cart.objects.filter(user=user)
    for cart in carts:
        cart.isselect = isall
        cart.save()

    responseData = {
        'status': '1',
        'msg':'全选/取消全选 操作成功'
    }

    return JsonResponse(responseData)


def generateorder(request):
    token = request.session.get('token')
    if token:
        user = User.objects.get(token=token)
        #
        order = Order()
        order.user = user
        order.number = str(uuid.uuid5(uuid.uuid4(), 'order'))
        order.save()

        carts = Cart.objects.filter(user=user).filter(isselect=True)
        for cart in carts:
            #
            orderGoods = OrderGoods()
            orderGoods.order = order
            orderGoods.goods = cart.goods
            orderGoods.number = cart.number
            orderGoods.save()

            # 移除
            cart.delete()

        responseData = {
            'status': '1',
            'msg': '',
            'orderid': order.id
         }

        return JsonResponse(responseData)

    else:
        return  JsonResponse({'msg':'用户登录后再操作'})

# 订单详情
def orderinfo(request):
    orderid = request.GET.get('orderid')
    order = Order.objects.get(pk=orderid)

    data = {
        'title':'详情',
        'order': order,
    }

    return render(request,'order/orderinfo.html', context=data)

# 订单处理
def changeorderstatusm(request):
    orderid = request.GET.get('orderid')
    status = request.GET.get('status')

    order = Order.objects.get(pk=orderid)
    order.status = status
    order.save()

    responseData = {
        'msg':'成功',
        'status':1
    }

    return JsonResponse(responseData)


def shortshow(request):
    return render(request,'home/shortshow.html')


def honor(request):
    return render(request, 'home/honor.html')


def activaty(request):
    return render(request, 'home/activaty.html')


def member(request,a,num):
    alluser = User.objects.all().filter(istea=int(num))
    users = User.objects.all().filter(istea=int(num)).filter(account=a)
    print('***********************')
    print(users[0].name)
    data  = {
        'users':users,
        'alluser':alluser,
        'num':num
    }

    return render(request,'home/member.html',context=data)




def XYshortshow(request):
    return render(request, 'home/XYshortshow.html')


def announcement(request):
    return render(request, 'home/announcement.html')


def XXshortshow(request):
    return render(request, 'home/XXshortshow.html')


def book(request):
    return render(request, 'home/book.html')


def xc(request):
    return render(request, 'home/xc.html')


def sosiology(request):
    return render(request, 'home/sosiology.html')


def picture(request):
    return render(request, '001/../static/001/index.html')

import time
def bianji(request):
    if request.method == 'POST':
        goods = Goods()
        str1 = str(time.time())
        time1 = str1.split('.')[0]


        goods.childcid = request.POST.get('childcid')

        goods.productname = request.POST.get('productname')
        goods.productlongname = request.POST.get('productlongname')
        goods.categoryid = request.POST.get('categoryid')
        goods.childcidname ='x'
        print()
        # 头像
        imgName = time1+'.png'
        imgPath = os.path.join(settings.IMG_ROOT, imgName)
        print(imgPath)
        file = request.FILES.get('file')
        print(file)


        if file == None:
            imgName = 'axf.png'
        else:
            with open(imgPath, 'wb') as fp:
                for data in file.chunks():
                    fp.write(data)
        goods.productimg = 'http://127.0.0.1:8000/static/market/img/'+imgName
        goods.save()
        # 重定向
        return redirect('axf:home')

    elif request.method == 'GET':
        return render(request, 'market/bianji.html')