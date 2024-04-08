from django.urls import path
from .views import HomeView, Product_detailView, AddView, InforView, ContactView, LoginView, SignupView, CartView, LogoutView, ProductView, Personal_infotmationView, ProductmanageView, ProductdeleteView, CartupdateView, buyView

urlpatterns = [
    # trang chủ
    path('', HomeView.as_view(), name='home'),

    # chi tiết sản phẩm
    path('product_detail/<int:pk>/', Product_detailView.as_view(), name='product_detail'),
    path('product_detail/add/<int:pk>/', Product_detailView.as_view(), name='add_to_cart'),

    # quản lý sản phẩm
    path('product/', ProductView.as_view(), name='product'),
    path('product/edit_product/<int:pk>/', ProductmanageView.as_view(), name='product_edit'),
    path('product/edit_product/update_data_product/<int:pk>/', ProductmanageView.as_view(), name='update_data_product'),
    path('product/delete_product/<int:pk>/', ProductdeleteView.as_view(), name='product_delete'),
    # thêm sản phẩm
    path('add_product/', AddView.as_view(), name='add_product'),
    path('add_product/add/', AddView.as_view(), name='add'),
    

    # thông tin về shop
    path('about_us/', InforView.as_view(), name='about_us'),

    # phản hồi của khách hàng
    path('contact/', ContactView.as_view(), name='contact'),
    # xử lý phản hồi
    path('contact/feedback', ContactView.as_view(), name='feedback'),

    # đăng nhập
    path('login/', LoginView.as_view(), name='login'),
    path('login/login_account', LoginView.as_view(), name='login_event'),

    # đăng ký
    path('signup/', SignupView.as_view(), name='signup'),
    path('signup/register_account', SignupView.as_view(), name='register_event'),

    # giỏ hàng
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/delete/<int:pk>/', CartView.as_view(), name='delete_cart'),
    path('cart/update_quantity/<int:pk>/', CartupdateView.as_view(), name='update_quantity_cart'),
    path('cart/Buy/', buyView.as_view(), name='buy_now'),
    

    path('log_out/', LogoutView.as_view(), name='logout'),

    path('Personal_information/', Personal_infotmationView.as_view(), name='Personal_infor'),
    path('Personal_information/update_data', Personal_infotmationView.as_view(), name='update_data'),
]

