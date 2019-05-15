from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^$', views.home, name='home'),            # 首页

    url(r'^home/$', views.home, name='home'),       # 首页
    url(r'^market/(\d+)/(\d+)/(\d+)/$', views.market, name='market'), # 闪购超市
    url(r'^cart/$', views.cart, name='cart'),       # 购物车

    url(r'^mine/$', views.mine, name='mine'),       # 我的
    url(r'^register/$', views.register, name='register'), # 注册
    url(r'^login/$', views.login, name='login'),    # 登录
    url(r'^logout/$', views.quit, name='logout'),   # 退出登录
    url(r'checkuser/$', views.checkuser, name='checkuser'), # 用户名验证

    url(r'^addtocart/$', views.addtocart, name='addtocart'),    # 添加到购物车
    url(r'^subtocart/$', views.subtocart, name='subtocart'),    # 购物车删减
    url(r'changecartstatus/$', views.changecartstatus, name='changecartstatus'), # 修改选中状态
    url(r'^changecartselect/$', views.changecartselect, name='changecartselect'),   # 全选/取消全选

    url(r'^generateorder/$', views.generateorder, name='generateorder'),    # 下单
    url(r'^orderinfo/$', views.orderinfo, name='orderinfo'),    # 订单详情
    url(r'^changeorderstatus/$', views.changeorderstatusm, name='changeorderstatus'),   # 修改订单状态
    url(r'^shortshow/$',views.shortshow,name='shortshow'),#班级简介
    url(r'^honor/$',views.honor,name='honor'),#班级荣誉
    url(r'^activaty/$',views.activaty,name='activaty'),#班级活动
    url(r'^member/(.+)/(.+)$',views.member,name='member'),#班级成员
    url(r'^teacher/(.+)/(.+)$',views.member,name='teacher'),#班级教师
    url(r'^XYshortshow/$',views.XYshortshow,name='XYshortshow'),#学院简介
    url(r'^announcement/$',views.announcement,name='announcement'),#通告
    url(r'^XXshortshow/$',views.XXshortshow,name='XXshortshow'),#学校简介
    url(r'^book/$',views.book,name='book'),#电子图书
    url(r'^xc/$',views.xc,name='xc'),#课程
    url(r'^sosiology/$', views.sosiology, name='sosiology'),  # 社会
    url(r'^picture/$', views.picture, name='picture'),  # 相册
    url(r'^bianji/$',views.bianji,name='bianji')


]