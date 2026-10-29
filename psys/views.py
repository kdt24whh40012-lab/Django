from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Customer, Employee  # Employee を追加


def Login(request):
    """ログイン画面表示・認証処理"""
    error_message = None

    if request.method == 'POST':
        employee_no = request.POST.get('employee_no', '').strip()
        password = request.POST.get('password', '').strip()

        # 入力チェック
        if not employee_no or not password:
            error_message = "従業員番号とパスワードを入力してください。"
        else:
            # DBから従業員情報を照合
            try:
                employee = Employee.objects.get(employee_no=employee_no, password=password)
                # 認証成功：セッションに従業員情報を保存
                request.session['employee_no'] = employee.employee_no
                request.session['employee_name'] = employee.employee_name
                
                # 顧客検索画面へリダイレクト
                return redirect('psys:CustomerSearch')
            except Employee.DoesNotExist:
                error_message = "従業員番号またはパスワードが正しくありません。"

    context = {
        'error_message': error_message,
    }
    return render(request, 'login.html', context)


def CustomerSearch(request):
    """得意先検索画面（ログインチェック付き）"""
    # ログインしていない場合はログイン画面へリダイレクト
    if 'employee_no' not in request.session:
        return redirect('psys:Login')

    # POST処理 (PRGパターン)
    if request.method == 'POST':
        #search_word = request.POST.get('search_word', '').strip()
        request.session['search_name'] = request.POST.get('search_name', '').strip()
        request.session['search_tel'] = request.POST.get('search_tel', '').strip()
        request.session['search_address'] = request.POST.get('search_address', '').strip()
        return redirect('psys:CustomerSearch')

    # GET処理および検索・バリデーション
    #search_word = request.session.pop('search_word', None)
    search_name = request.session.pop('search_name', None)
    search_tel = request.session.pop('search_tel', None)
    search_address = request.session.pop('search_address', None)
    
    customers = None
    error_message = None

    if any(v is not None for v in [search_name, search_tel, search_address]):
        # すべて空文字の場合のバリデーション
        if not search_name and not search_tel and not search_address:
            error_message = "少なくとも1つの検索条件を入力してください。"
        else:
            # 有効顧客(delete_flag=0)をベースに絞り込み
            queryset = Customer.objects.filter(delete_flag=0)

            if search_name:
                queryset = queryset.filter(customer_name__icontains=search_name)
            if search_tel:
                queryset = queryset.filter(customer_telno__icontains=search_tel)
            if search_address:
                queryset = queryset.filter(customer_address__icontains=search_address)

            if queryset.exists():
                customers = queryset
            else:
                error_message = "指定した条件に該当する得意先は見つかりませんでした。"

    context = {
        'search_name': search_name if search_name else '',
        'search_tel': search_tel if search_tel else '',
        'search_address': search_address if search_address else '',
        'customers': customers,
        'error_message': error_message,
        'employee_name': request.session.get('employee_name'),  # ログイン中ユーザー名表示用
    }
    return render(request, 'CustomerSearch.html', context)


def Logout(request):
    """ログアウト処理"""
    request.session.flush()  # セッション消去
    return redirect('psys:Login')