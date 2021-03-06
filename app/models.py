from django.db import models

# Create your models here.

# 基础 类
class Base(models.Model):
    img = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    trackid = models.CharField(max_length=20)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


# 轮播图 模型类
class Wheel(Base):
    class Meta:
        db_table = 'axf_wheel'


# 导航 模型类
class Nav(Base):
    class Meta:
        db_table = 'axf_nav'

# 每日必购 模型类
class Mustbuy(Base):
    class Meta:
        db_table = 'axf_mustbuy'

# 商品部分内容
class Shop(Base):
    class Meta:
        db_table = 'axf_shop'


# 商品主体
class MainShow(models.Model):
    trackid = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    img = models.CharField(max_length=200)
    categoryid = models.CharField(max_length=10)
    brandname = models.CharField(max_length=50)

    img1 = models.CharField(max_length=200)
    childcid1 = models.CharField(max_length=10)
    productid1 = models.CharField(max_length=10)
    longname1 = models.CharField(max_length=200)
    price1 = models.FloatField()
    marketprice1 = models.FloatField()

    img2 = models.CharField(max_length=200)
    childcid2 = models.CharField(max_length=10)
    productid2 = models.CharField(max_length=10)
    longname2 = models.CharField(max_length=200)
    price2 = models.FloatField()
    marketprice2 = models.FloatField()

    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=10)
    productid3 = models.CharField(max_length=10)
    longname3 = models.CharField(max_length=200)
    price3 = models.FloatField()
    marketprice3 = models.FloatField()

    class Meta:
        db_table = 'axf_mainshow'

    def __str__(self):
        return self.name


# 商品分类
class Foodtypes(models.Model):
    # 分类id
    typeid = models.CharField(max_length=10)
    # 分类名称
    typename = models.CharField(max_length=100)
    # 子类名称
    childtypenames = models.CharField(max_length=200)
    # 分类排序(显示的先后顺序)
    typesort = models.IntegerField()

    class Meta:
        db_table = 'axf_foodtypes'

    def __str__(self):
        return self.typename


# 商品模型类
class Goods(models.Model):
    # 商品ID
    productid = models.CharField(max_length=10)
    # 商品图片
    productimg = models.CharField(max_length=200)
    # 商品名称
    productname = models.CharField(max_length=100)
    # 商品长名字
    productlongname = models.CharField(max_length=200)
    # 分类ID
    categoryid = models.CharField(max_length=10)
    # 子类ID
    childcid = models.CharField(max_length=10)



    class Meta:
        db_table = 'axf_goods'



# 用户模型类
class User(models.Model):
    # 账号
    account = models.CharField(max_length=20, unique=True)
    # 密码
    password = models.CharField(max_length=256)
    # 名字
    name = models.CharField(max_length=100)
    # 电话
    tel = models.CharField(max_length=20)
    # 地址
    address = models.CharField(max_length=256)
    # 头像
    img = models.CharField(max_length=100)
    # 等级
    rank = models.IntegerField(default=1)

    sex = models.CharField(max_length=50,default='-1')

    age = models.CharField(max_length=50,default='-1')

    birthday = models.CharField(max_length=50,default='-1')

    xuexing = models.CharField(max_length=50,default='-1')

    xingzuo = models.CharField(max_length=50,default='-1')

    istea =  models.BooleanField(default=0)
    # token
    token = models.CharField(max_length=100)

# 购物车 模型类
class Cart(models.Model):
    # 用户
    user = models.ForeignKey(User)
    # 商品
    goods = models.ForeignKey(Goods)
    # 选择数量
    number = models.IntegerField(default=1)
    # 是否选中
    isselect = models.BooleanField(default=True)


# 订单 模型类
# 一个 用户 对应 多个表单
# 主 用户
# 从 订单 【声明关系】
class Order(models.Model):
    # 用户
    user = models.ForeignKey(User)
    # 订单号 (时间+字符串)
    number = models.CharField(max_length=256)
    # 状态
    # 1 未付款
    # 2 已付款，未发货
    # 3 已发货，未收货
    # 4 已收货，未评级
    # 5 已评价
    # 6 退款....
    status = models.IntegerField(default=1)
    # 创建时间
    createtime = models.DateTimeField(auto_now=True)


# 订单 商品
# 一个 订单 对应 多个商品
# 主 订单
# 从 订单商品 【声明关系】
class OrderGoods(models.Model):
    # 订单
    order = models.ForeignKey(Order)
    # 商品
    goods = models.ForeignKey(Goods)
    # 数量
    number = models.IntegerField(default=1)


