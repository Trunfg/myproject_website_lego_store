from pyexpat.errors import messages
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import  redirect, render
from rest_framework.views import APIView
from .serializers import UserSerializer, ProductSerializer, CartSerializer, HistorySerializer, FeedbackSerializer
from .models import User, Product, Cart, History, Feedback
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import bcrypt  # Đảm bảo bạn đã cài đặt thư viện bcrypt
from rest_framework_simplejwt.tokens import AccessToken
from .utils import CustomPayload


# trang chủ
class HomeView(APIView):
    def get(self, request, format=None):
        token = request.session.get('jwt_token')
        products = Product.objects.all()
        user = None
        count = 0
        if token:
            try:
                decoded_token = AccessToken(token)
                id_user = decoded_token.payload['id_user']
                user = User.objects.get(id_user=id_user)
                count = Cart.objects.filter(id_user=id_user).count()
                # if datetime.fromtimestamp(decoded_token['exp']) < datetime.now():
                #     user = None
                #     return render(request, 'home.html', {'products': products, 'user': user, 'count':count})
            except (User.DoesNotExist, TokenError):
                user = None
                items_per_page = 8
                paginator = Paginator(products, items_per_page)
                page_number = request.GET.get('page')
                try:
                    products = paginator.page(page_number)
                except PageNotAnInteger:
                    products = paginator.page(1)
                except EmptyPage:
                    products = paginator.page(paginator.num_pages)
                return render(request, 'home.html', {'products': products, 'user': user, 'count':count})
        items_per_page = 8
        paginator = Paginator(products, items_per_page)

        page_number = request.GET.get('page')
        try:
            products = paginator.page(page_number)
        except PageNotAnInteger:
            # Nếu `page` không phải là một số nguyên, trả về trang đầu tiên
            products = paginator.page(1)
        except EmptyPage:
            # Nếu `page` vượt quá phạm vi, trả về trang cuối cùng
            products = paginator.page(paginator.num_pages)

        return render(request, 'home.html', {'products': products, 'user': user, 'count':count})

# chi tiết sản phẩm
class Product_detailView(APIView):
    def get(self, request, pk):
        token = request.session.get('jwt_token')
        user = None
        count = 0
        product = Product.objects.get(id_product=pk)
        if token:
            try:
                decoded_token = AccessToken(token)
                id_user = decoded_token.payload['id_user']
                user = User.objects.get(id_user=id_user)
                count = Cart.objects.filter(id_user=id_user).count()
            except (User.DoesNotExist, TokenError):
                user = None
                return render(request, 'product_detail.html', {'user': user, 'count': count, 'product': product})
        return render(request, 'product_detail.html', {'user': user, 'count': count, 'product': product})
    def post(self, request, pk):
        data = {
            'id_user': request.POST.get('id_user'),
            'id_product': pk,
            'number_of_product': int(request.POST.get('number_of_product')),
        }
        product = Product.objects.get(id_product=data['id_product'])
        if product.quantity > data['number_of_product']:
            serializer = CartSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                messages.success(request, 'Add to cart successfully.')
                return redirect('home')
            else:
                messages.success(request, 'Invalid information.')
                return redirect('product_detail', pk=data['id_product'])
        else:
            messages.success(request, 'Product quantity is not enough.')
            return redirect('product_detail', pk=data['id_product'])

# hiển thị sản phẩm để quản lý
class ProductView(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        token = request.session.get('jwt_token')
        user = None
        count = 0
        if token:
            try:
                decoded_token = AccessToken(token)
                id_user = decoded_token.payload['id_user']
                user = User.objects.get(id_user=id_user)
                count = Cart.objects.filter(id_user=id_user).count()
            except (User.DoesNotExist, TokenError):
                user = None
                items_per_page = 8
                paginator = Paginator(products, items_per_page)
                page_number = request.GET.get('page')
                try:
                    products = paginator.page(page_number)
                except PageNotAnInteger:
                    products = paginator.page(1)
                except EmptyPage:
                    products = paginator.page(paginator.num_pages)
                return render(request, 'product.html', {'products': products, 'user': user, 'count':count})
        
        # Số lượng sản phẩm trên mỗi trang
        items_per_page = 8
        paginator = Paginator(products, items_per_page)

        page_number = request.GET.get('page')
        try:
            products = paginator.page(page_number)
        except PageNotAnInteger:
            # Nếu `page` không phải là một số nguyên, trả về trang đầu tiên
            products = paginator.page(1)
        except EmptyPage:
            # Nếu `page` vượt quá phạm vi, trả về trang cuối cùng
            products = paginator.page(paginator.num_pages)

        return render(request, 'product.html', {'products': products, 'user': user, 'count':count})
# truy vấn và xử lý sản phẩm
class ProductmanageView(APIView):
    def get(self, request, pk):
        products = Product.objects.get(id_product=pk)
        token = request.session.get('jwt_token')
        user = None
        count = 0
        if token:
            try:
                decoded_token = AccessToken(token)
                id_user = decoded_token.payload['id_user']
                user = User.objects.get(id_user=id_user)
                count = Cart.objects.filter(id_user=id_user).count()
            except (User.DoesNotExist, TokenError):
                user = None
                return render(request, 'edit_product.html', {'products': products, 'user': user, 'count':count})
        return render(request, 'edit_product.html', {'products': products, 'user': user, 'count':count})
    def post(self, request, pk, *args, **kwargs):
        products = Product.objects.get(id_product=pk)
        products.name_product = request.POST.get('name_product')
        products.description = request.POST.get('description')
        products.price = request.POST.get('price')
        products.quantity = request.POST.get('quantity')
        img = request.FILES.get('img_product')
        if not (products.name_product and products.description and products.price and products.quantity):
            messages.error(request, 'All fields are required.')
            return redirect('product_edit', pk=pk)
        if img:
            products.img_product = img
        if int(products.quantity) <= 0:
            messages.error(request, 'Invalid quantity.')
            return redirect('product_edit', pk=pk)
        products.save()
        messages.success(request, 'Update product successfully.')
        return redirect('product')

class ProductdeleteView(APIView):
    def post(self, request, pk, *args, **kwargs):
        product = Product.objects.get(id_product=pk)
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('product')

# thêm sản phẩm
class AddView(APIView):
    def get(self, request, format=None):
        token = request.session.get('jwt_token')
        user = None
        count = 0
        if token:
            try:
                decoded_token = AccessToken(token)
                id_user = decoded_token.payload['id_user']
                user = User.objects.get(id_user=id_user)
                count = Cart.objects.filter(id_user=id_user).count()
            except (User.DoesNotExist, TokenError):
                user = None
                return render(request, 'addproduct.html', {'user': user, 'count':count})
        return render(request, 'addproduct.html', {'user': user, 'count':count})
    def post(self, request, *args, **kwargs):
        data = {
            'name_product': request.POST.get('name_product'),
            'img_product': request.FILES.get('img_product'),
            'description': request.POST.get('description'),
            'price': request.POST.get('price'),
            'quantity': request.POST.get('quantity'),
        }
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Add product successfully.')
            return redirect('add_product')
        else:
            messages.success(request, 'Invalid information.')
            return redirect('add_product')

# Thông tin về shop
class InforView(APIView):
    def get(self, request, format=None):
        token = request.session.get('jwt_token')
        user = None
        count = 0
        if token:
            try:
                decoded_token = AccessToken(token)
                id_user = decoded_token.payload['id_user']
                user = User.objects.get(id_user=id_user)
                count = Cart.objects.filter(id_user=id_user).count()
            except (User.DoesNotExist, TokenError):
                user = None
                return render(request, 'information_store.html', {'user': user, 'count':count})
        return render(request, 'information_store.html', {'user': user, 'count':count})

# Liên hệ shop
class ContactView(APIView):
    def get(self, request, format=None):
        token = request.session.get('jwt_token')
        user = None
        count = 0
        if token:
            try:
                decoded_token = AccessToken(token)
                id_user = decoded_token.payload['id_user']
                user = User.objects.get(id_user=id_user)
                count = Cart.objects.filter(id_user=id_user).count()
            except (User.DoesNotExist, TokenError):
                user = None
                return render(request, 'contact.html', {'user': user, 'count':count})
        return render(request, 'contact.html', {'user': user, 'count':count})
    def post(self, request, *args, **kwargs):
        data = {
            'name_customer': request.POST.get('name_customer'),
            'email': request.POST.get('email'),
            'comment': request.POST.get('comment'),
        }
        serializer = FeedbackSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, ' Feedback sent successfully.')
            return redirect('contact')
        else:
            messages.success(request, 'Invalid information.')
            return redirect('contact')
# đăng nhập
class LoginView(APIView):
    def get(self, request, format=None):
        return render(request, 'login.html')
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email).first()
        if user:
            hashed_password = user.password.encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                access_token = CustomPayload.for_user(user)
                request.session['jwt_token'] = str(access_token)
                messages.success(request, 'Log in successfully.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid password')
                return redirect('login')
        else:
            messages.error(request, 'User not found')
            return redirect('login')


# đăng ký
class SignupView(APIView):
    def get(self, request, format=None):
        return render(request, 'signup.html')
    def post(self, request, *args, **kwargs):
        data = {
            'name_user': request.POST.get('name_user'),
            'email': request.POST.get('email'),
            'date_of_birth': request.POST.get('date_of_birth'),
            'phone_number': request.POST.get('phone_number'),
        }
        
        # Kiểm tra xem email đã tồn tại trong cơ sở dữ liệu chưa
        user = User.objects.filter(email=data['email']).first()
        if user:
            messages.success(request, 'Email already exists.')
            return redirect('signup')
        else:
            # Nếu email không tồn tại, kiểm tra ngày sinh
            dob = datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
            current_year = datetime.now().year
            if dob.year > current_year:
                # Nếu ngày sinh lớn hơn năm hiện tại, hiển thị thông báo lỗi
                messages.success(request, 'Invalid date of birth.')
                return redirect('signup')
            # Tiếp tục xử lý nếu ngày sinh hợp lệ
            raw_password = request.POST.get('password')
            hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
            data['password'] = hashed_password.decode('utf-8')  # Chuyển bytes thành chuỗi để lưu vào cơ sở dữ liệu
            
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return HttpResponseRedirect(reverse('login'))
            else:
                messages.success(request, 'Please enter complete information.')
                return redirect('signup')

# giỏ hàng
class CartView(APIView):
    def get(self, request, format=None):
        token = request.session.get('jwt_token')
        carts = None
        user = None
        products = []
        count = 0
        if token:
            try:
                decoded_token = AccessToken(token)
                id_user = decoded_token.payload['id_user']
                user = User.objects.get(id_user=id_user)
                carts = Cart.objects.filter(id_user=id_user)
            except (User.DoesNotExist, TokenError):
                return redirect('login')
        for cart in carts:
            product = cart.id_product
            price = int(product.price)*int(cart.number_of_product)
            # product = Product.objects.get(id_product=id)
            products.append({
                'id_product': product.id_product,
                'totalprice': price,
                'price': product.price,
                'description': product.description,
                'img_product': product.img_product,
                'number_of_product': cart.number_of_product,
            })
        count = carts.count()
        return render(request, 'cart.html', {'carts': carts, 'user': user, 'products':products, 'count':count})
    def post(self, request, pk, *args, **kwargs):
        token = request.session.get('jwt_token')
        decoded_token = AccessToken(token)
        id_user = decoded_token.payload['id_user']
        cart = Cart.objects.filter(id_product=pk, id_user=id_user).first()
        cart.delete()
        messages.success(request, 'Cart deleted successfully.')
        return redirect('cart')

class CartupdateView(APIView):
    def post(self, request, pk, *args, **kwargs):
        token = request.session.get('jwt_token')
        decoded_token = AccessToken(token)
        id_user = decoded_token.payload['id_user']
        cart = Cart.objects.filter(id_product=pk, id_user=id_user).first()
        cart.number_of_product = request.POST.get('number_of_product')
        cart.save();
        messages.success(request, 'Update cart successfully.')
        return redirect('cart')

class buyView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.session.get('jwt_token')
        id_user = 0
        if token:
            try:
                decoded_token = AccessToken(token)
                id_user = decoded_token.payload['id_user']
            except (User.DoesNotExist, TokenError):
                return redirect('login')
        selected_product_ids = request.POST.get('selected_products').split(',')
        if selected_product_ids==['']:
            messages.success(request, 'You have not selected any products yet.')
            return redirect('cart')
        selected_products = Cart.objects.filter(id_product__in=selected_product_ids, id_user=id_user)
        current_date = datetime.now().date()
        for history in selected_products:
            pro = history.id_product
            data = {
                'id_user': id_user,
                'id_product': pro.id_product,
                'purchase_date': current_date,
                'number_of_product': int(history.number_of_product),
            }
            serializer = HistorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            product = Product.objects.get(id_product=pro.id_product)
            product.quantity = product.quantity - history.number_of_product
            product.save()
            cart = Cart.objects.filter(id_product=pro.id_product, id_user=id_user).first()
            cart.delete()
        messages.success(request, 'Payment success.')
        return redirect('home')

# đăng xuất
class LogoutView(APIView):
    def get(self, request):
        # Lấy token từ session
        token = request.session.get('jwt_token')
        if token:
            try:
                decoded_token = AccessToken(token)
                decoded_token.payload['exp'] = datetime.now()
                del request.session['jwt_token']
            except (User.DoesNotExist, TokenError):
                return redirect('login')
        return redirect('login')
    
# thông tin cá nhân
class Personal_infotmationView(APIView):
    def get(self, request, format=None):
        token = request.session.get('jwt_token')
        user = None
        count = 0
        if token:
            try:
                decoded_token = AccessToken(token)
                id_user = decoded_token.payload['id_user']
                user = User.objects.get(id_user=id_user)
                count = Cart.objects.filter(id_user=id_user).count()
            except (User.DoesNotExist, TokenError):
                return redirect('login')
        date = user.date_of_birth.strftime('%Y-%m-%d') if user.date_of_birth else ''
        return render(request, 'personal_information.html', {'user': user, 'count':count, 'date':date})

    def post(self, request, *args, **kwargs):
        token = request.session.get('jwt_token')
        decoded_token = AccessToken(token)
        id_user = decoded_token.payload['id_user']
        user = User.objects.get(id_user=id_user)
        data = request.data
        dob = datetime.strptime(data.get('date_of_birth'), '%Y-%m-%d')
        current_year = datetime.now().year
        if dob.year > current_year:
            messages.error(request, 'Invalid date of birth.')
            return redirect('Personal_infor')
        user.name_user = data.get('name_user')
        user.email = data.get('email')
        user.date_of_birth = data.get('date_of_birth')
        user.phone_number = data.get('phone_number')
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('Personal_infor')

# Lịch sử giao dịch
class HistoryView(APIView):
    def get(self, request, format=None):
        token = request.session.get('jwt_token')
        carts = None
        user = None
        historys = None
        products = []
        count = 0
        if token:
            try:
                decoded_token = AccessToken(token)
                id_user = decoded_token.payload['id_user']
                user = User.objects.get(id_user=id_user)
                carts = Cart.objects.filter(id_user=id_user)
                historys = History.objects.filter(id_user=id_user)
            except (User.DoesNotExist, TokenError):
                return redirect('login')
        for history in historys:
            product = history.id_product
            price = int(product.price)*int(history.number_of_product)
            # product = Product.objects.get(id_product=id)
            products.append({
                'id_product': product.id_product,
                'totalprice': price,
                'img_product': product.img_product,
                'number_of_product': history.number_of_product,
                'purchase_date': history.purchase_date,
            })
        count = carts.count()
        return render(request, 'history.html', {'historys': historys, 'user': user, 'products':products, 'count':count})
    def post(self, request, pk, *args, **kwargs):
        token = request.session.get('jwt_token')
        decoded_token = AccessToken(token)
        id_user = decoded_token.payload['id_user']
        history = History.objects.filter(id_product=pk, id_user=id_user).first()
        history.delete()
        messages.success(request, 'History purchase deleted successfully.')
        return redirect('history')

# Đổi mật khẩu
class ChangePasswordView(APIView):
    def get(self, request, format=None):
        token = request.session.get('jwt_token')
        user = None
        carts = None
        if token:
            try:
                decoded_token = AccessToken(token)
                id_user = decoded_token.payload['id_user']
                user = User.objects.get(id_user=id_user)
                carts = Cart.objects.filter(id_user=id_user)
            except (User.DoesNotExist, TokenError):
                return redirect('login')
        count = 0
        count = carts.count()
        return render(request, 'change_password.html', {'user': user, 'count':count})
    def post(self, request, *args, **kwargs):
        token = request.session.get('jwt_token')
        decoded_token = AccessToken(token)
        id_user = decoded_token.payload['id_user']
        user = User.objects.get(id_user=id_user)
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # So sánh mật khẩu cũ nhập từ người dùng với mật khẩu đã được mã hóa trong cơ sở dữ liệu
        if bcrypt.checkpw(current_password.encode('utf-8'), user.password.encode('utf-8')):
            if new_password == confirm_password:
                # Mã hóa mật khẩu mới và cập nhật vào cơ sở dữ liệu
                hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                user.password = hashed_new_password.decode('utf-8')
                user.save()
                messages.success(request, 'Change password successfully.')
                return redirect('Personal_infor')
            else:
                messages.error(request, 'Re-entered password is incorrect.')
        else:
            messages.error(request, 'Current password is incorrect.')

        return redirect('change_password')

# Quên mật khẩu
class ForgotPasswordView(APIView):
    def get(self, request, format=None):
        return render(request, 'forgot_password.html')
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        # So sánh mật khẩu cũ nhập từ người dùng với mật khẩu đã được mã hóa trong cơ sở dữ liệu
        if email and phone_number and new_password and confirm_password:
            user = User.objects.filter(email=email, phone_number=phone_number).first()
            if user:
                if new_password==confirm_password:
                    hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                    user.password = hashed_new_password.decode('utf-8')
                    user.save()
                    messages.success(request, 'New password has been updated.')
                    return redirect('login')
                messages.success(request, 'Re-entered password is incorrect.')
                return redirect('forgot_password')
            messages.success(request, 'Invalid email or phone number.')
            return redirect('forgot_password')
        messages.success(request, 'Enter complete information.')
        return redirect('forgot_password')

# quản lý user
class manageUserView(APIView):
    def get(self, request, format=None):
        token = request.session.get('jwt_token')
        alluser = None
        # alluser = User.objects.exclude(id_user=id_user).filter(position='khach_hang')
        user = None
        count = 0
        if token:
            try:
                decoded_token = AccessToken(token)
                id_user = decoded_token.payload['id_user']
                user = User.objects.get(id_user=id_user)
                alluser = User.objects.exclude(id_user=id_user)
                carts = Cart.objects.filter(id_user=id_user)
                count = carts.count()
            except (User.DoesNotExist, TokenError):
                return redirect('login')
        return render(request, 'management_user.html', {'allusers': alluser, 'user': user, 'count':count})
    def post(self, request, pk, *args, **kwargs):
        user = User.objects.get(id_user=pk)
        user.position = "admin"
        user.save()
        messages.success(request, 'Set admin successfully.')
        return redirect('management_user')
    
class manageUserCustomerView(APIView):
    def post(self, request, pk, *args, **kwargs):
        user = User.objects.get(id_user=pk)
        user.position = "khach_hang"
        user.save()
        messages.success(request, 'Set customer successfully.')
        return redirect('management_user')
class deleteUserView(APIView):
    def post(self, request, pk, *args, **kwargs):
        user = User.objects.get(id_user=pk)
        user.delete()
        messages.success(request, 'Delete user successfully.')
        return redirect('management_user')