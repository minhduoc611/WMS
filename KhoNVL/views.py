from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from .forms import *
from django.forms import formset_factory
import pandas as pd
from django.shortcuts import render
from .forms import UploadExcelForm
from django.contrib import messages
from django.db import transaction
from django.forms import inlineformset_factory
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.db import transaction
from django.http import JsonResponse

from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, render


def index(request):
    return render(request, 'index.html')
from django.shortcuts import render
from .models import NCCVai

def ncc_list(request):
    ten_ncc = request.GET.get('search', '') 
    queryset = NCCVai.objects.all()
    if ten_ncc:
        queryset = queryset.filter(ten_ncc__icontains=ten_ncc)

    return render(request, 'KhoNVL/NCC_list.html', {
        'danh_sach_ncc': queryset,
        'ten_ncc': ten_ncc
    })
def ncc_delete(request, id):
    ncc = get_object_or_404(NCCVai, id=id)
    ncc.delete()
    return redirect('ncc-list')

def ncc_edit(request, id):
    ncc = get_object_or_404(NCCVai, id=id)
    if request.method == 'POST':
        # Lấy thông tin từ form và cập nhật
        ncc.ten_ncc = request.POST.get('ten_ncc')
        ncc.so_dien_thoai = request.POST.get('so_dien_thoai')
        ncc.facebook = request.POST.get('facebook')
        ncc.website = request.POST.get('website')
        ncc.dia_chi = request.POST.get('dia_chi')
        ncc.save()
        return redirect('ncc_list')
    return redirect('ncc_list')



@csrf_exempt
def add_ncc(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ten_ncc = data.get('ten_ncc')
            so_dien_thoai = data.get('so_dien_thoai')
            facebook = data.get('facebook')
            website = data.get('website')
            dia_chi = data.get('dia_chi')

            ncc = NCCVai.objects.create(
                ten_ncc=ten_ncc,
                so_dien_thoai=so_dien_thoai,
                facebook=facebook,
                website=website,
                dia_chi=dia_chi
            )
            return JsonResponse({
                'success': True,
                'message': 'Nhà cung cấp đã được thêm thành công!',
                'ncc': {
                    'id_ncc': ncc.id_ncc,
                    'ten_ncc': ncc.ten_ncc,
                    'so_dien_thoai': ncc.so_dien_thoai,
                    'facebook': ncc.facebook,
                    'website': ncc.website,
                    'dia_chi': ncc.dia_chi,
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Chỉ hỗ trợ phương thức POST'})

def upload_excel_NCC_view(request):
    if request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file, engine='openpyxl')

            required_columns = ['ID NCC Vải', 'Tên NCC Vải']
            if not all(column in df.columns for column in required_columns):
                return JsonResponse({'success': False, 'message': 'File Excel thiếu thông tin cần thiết!'})

      
            df = df.fillna('')

            for index, row in df.iterrows():
                NCCVai.objects.update_or_create(
                    id_ncc=row['ID NCC Vải'],
                    defaults={
                        'ten_ncc': row['Tên NCC Vải'],
                        'so_dien_thoai': row['SĐT'], 
                        'facebook': row['Facebook'], 
                        'website': row['Website'],  
                        'dia_chi': row['Địa chỉ']
                    }
                )
                
            return JsonResponse({'success': True, 'message': 'Upload file thành công!'})

    return JsonResponse({'success': False, 'message': 'Đã có lỗi xảy ra khi upload!'})

# NGUYÊN VẬT LIỆU
def nvl_list(request):

    ten_vai = request.GET.get('ten_vai', '')
    nha_cung_cap = request.GET.get('nha_cung_cap', '')
    mau_sac = request.GET.get('mau_sac', '')

    # Áp dụng bộ lọc
    queryset = NVL.objects.all()

    if ten_vai:
        queryset = queryset.filter(ten_vai__icontains=ten_vai)
    if nha_cung_cap:
        queryset = queryset.filter(nha_cung_cap__id=nha_cung_cap)
    if mau_sac:
        queryset = queryset.filter(mau_sac__icontains=mau_sac)

    context = {
        'danh_sach_nvl': queryset,
        'danh_sach_ncc': NCCVai.objects.all(),
        'ten_vai': ten_vai,
        'nha_cung_cap': nha_cung_cap,
        'mau_sac': mau_sac,
    }
    return render(request, 'KhoNVL/NVL_list.html', context)

@csrf_exempt
def add_nvl(request):
    if request.method == 'POST':
        form = NVLForm(request.POST, request.FILES)
        if form.is_valid():
            nvl = form.save(commit=False)
            ncc_id = request.POST.get('nha_cung_cap')
            try:
                ncc = NCCVai.objects.get(id=ncc_id)
                nvl.nha_cung_cap = ncc 
                nvl.save()
                return JsonResponse({
                    'success': True,
                    'nvl': {
                        'id_vai': nvl.id_vai,
                        'ten_vai': nvl.ten_vai,
                        'mau_sac': nvl.mau_sac,
                        'nha_cung_cap': str(nvl.nha_cung_cap.ten_ncc),
                        'so_luong_ton': nvl.so_luong_ton,
                        'don_vi_tinh': nvl.don_vi_tinh,
                        'gia': nvl.gia,
                        'hinh_anh': nvl.hinh_anh.url if nvl.hinh_anh else None,
                    }
                })
            except NCCVai.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Nhà cung cấp không tồn tại'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
        
def upload_excel_nvl(request):
    if request.method == 'POST' and request.FILES.get('file_excel'):
        try:
            file = request.FILES['file_excel']
            df = pd.read_excel(file)

            df = df.fillna({'Đơn giá': 0})

            nvls = []
            for index, row in df.iterrows():
                try:
                    ncc, _ = NCCVai.objects.get_or_create(ten_ncc=row['Nhà cung cấp'])
                    nvl, created = NVL.objects.get_or_create(
                        id_vai=row['ID Vải'],
                        defaults={
                            'ten_vai': row['Tên Vải'],
                            'nha_cung_cap': ncc,
                            'gia': row['Đơn giá'],
                            'so_luong_ton': row['Số lượng'],
                            'don_vi_tinh': row['ĐVT'],
                            'mau_sac': row['Màu sắc']
                        }
                    )

                    if not created:
                        nvl.ten_vai = row['Tên Vải']
                        nvl.nha_cung_cap = ncc
                        nvl.gia = row['Đơn giá']
                        nvl.so_luong_ton = row['Số lượng']
                        nvl.don_vi_tinh = row['ĐVT']
                        nvl.mau_sac = row['Màu sắc']
                        nvl.save()

                    nvls.append({
                        'id_vai': nvl.id_vai,
                        'ten_vai': nvl.ten_vai,
                        'mau_sac': nvl.mau_sac,
                        'nha_cung_cap': nvl.nha_cung_cap.ten_ncc,
                        'so_luong': nvl.so_luong_ton,
                        'don_vi_tinh': nvl.don_vi_tinh,
                        'gia': nvl.gia
                    })
                except Exception as e:
                    return JsonResponse({'success': False, 'message': f'Lỗi tại hàng {index + 1}: {str(e)}'})

            print(nvls)  # In dữ liệu JSON trả về để kiểm tra
            return JsonResponse({'success': True, 'nvls': nvls})

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})

    return JsonResponse({'success': False, 'message': 'File không hợp lệ'})


# ĐẶT NVL
def tao_don_hang(request):
    if request.method == 'POST':
        order = Order.objects.create()  # Tạo đơn hàng chỉ với ngày đặt hàng
        order_item_formset = OrderItemFormSet(request.POST, prefix='items')

        if order_item_formset.is_valid():
            for form in order_item_formset:
                order_item = form.save(commit=False)
                order_item.order = order
                order_item.save()

                # Cập nhật số lượng tồn kho
                nvl = order_item.nvl
                nvl.so_luong_ton += order_item.so_luong
                nvl.save()

            return JsonResponse({'status': 'success'})
        else:
            order_item_formset_errors = [
                form.errors.as_json() for form in order_item_formset if form.errors
            ]

            return JsonResponse({
                'status': 'error',
                'message': 'Dữ liệu không hợp lệ',
                'formset_errors': order_item_formset_errors
            })

    else:
        order_item_formset = OrderItemFormSet(prefix='items')
        san_pham_list = NVL.objects.all()

        return render(request, 'KhoNVL/tao_don_hang.html', {
            'order_item_formset': order_item_formset,
            'san_pham_list': san_pham_list
        })

def danh_sach_don_nhap_kho(request):
    # Lấy tất cả các đơn nhập kho sắp xếp theo ngày đặt hàng giảm dần
    danh_sach_don_nhap = Order.objects.all().order_by('-ngay_dat_hang')
    return render(request, 'KhoNVL/danh_sach_don_nhap_kho.html', {'danh_sach_don_nhap': danh_sach_don_nhap})


def chi_tiet_don_nhap_kho(request, order_id):
    # Lấy đơn nhập kho dựa trên ID hoặc trả về 404 nếu không tồn tại
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'KhoNVL/chi_tiet_don_nhap_kho.html', {
        'order': order,
        'order_items': order.items.all()  # Lấy tất cả các item trong đơn nhập
    })




# XUẤT KHO NVL
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import DotXuatKho, NVL, XuatKhoItem
import logging

logger = logging.getLogger('custom')

@csrf_exempt
def tao_dot_xuat_kho(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                dot_xuat_kho = DotXuatKho.objects.create(ghi_chu=request.POST.get('ghi_chu', ''))
                nvl_ids = request.POST.getlist('nvl_ids[]')
                so_luong_xuats = request.POST.getlist('so_luong_xuats[]')

                if not nvl_ids or not so_luong_xuats:
                    logger.error("Danh sách nguyên vật liệu hoặc số lượng không hợp lệ.")
                    return JsonResponse({'status': 'error', 'message': 'Danh sách nguyên vật liệu hoặc số lượng không hợp lệ.'})

                processed_ids = set()

                for nvl_id, so_luong_xuat in zip(nvl_ids, so_luong_xuats):
                    if nvl_id in processed_ids:
                        logger.warning(f"NVL ID {nvl_id} đã được xử lý, bỏ qua.")
                        continue
                    processed_ids.add(nvl_id)
                    try:
                        nvl = NVL.objects.select_for_update().get(id=nvl_id)
                    except NVL.DoesNotExist:
                        logger.error(f"Nguyên vật liệu với ID {nvl_id} không tồn tại.")
                        return JsonResponse({'status': 'error', 'message': f'Nguyên vật liệu với ID {nvl_id} không tồn tại.'})
                    try:
                        so_luong_xuat = int(so_luong_xuat)
                    except ValueError:
                        logger.error(f"Số lượng xuất không hợp lệ cho NVL ID {nvl_id}.")
                        return JsonResponse({'status': 'error', 'message': f'Số lượng xuất không hợp lệ cho NVL ID {nvl_id}.'})
                    if nvl.so_luong_ton < so_luong_xuat:
                        logger.warning(f"Tồn kho không đủ cho NVL ID {nvl_id}: Tồn {nvl.so_luong_ton}, Yêu cầu {so_luong_xuat}.")
                        return JsonResponse({
                            'status': 'error',
                            'message': f'Số lượng xuất vượt quá tồn kho cho {nvl.ten_vai} (Tồn: {nvl.so_luong_ton}, Xuất: {so_luong_xuat}).'
                        })
                    XuatKhoItem.objects.create(
                        dot_xuat_kho=dot_xuat_kho,
                        nvl=nvl,
                        so_luong_xuat=so_luong_xuat
                    )
                    logger.debug(f"Before update NVL ID: {nvl_id}, Current stock: {nvl.so_luong_ton}, Reduce: {so_luong_xuat}")
                    nvl.so_luong_ton -= so_luong_xuat
                    nvl.save()
                    logger.debug(f"After update NVL ID: {nvl_id}, New stock: {nvl.so_luong_ton}")

                logger.info("Đợt xuất kho đã được tạo thành công.")
                return JsonResponse({'status': 'success', 'message': 'Đợt xuất kho được tạo thành công!'})

        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return JsonResponse({'status': 'error', 'message': f'Đã xảy ra lỗi: {str(e)}'})
    nvl_list = NVL.objects.all()
    return render(request, 'KhoNVL/tao_dot_xuat_kho.html', {'nvl_list': nvl_list})





def danh_sach_dot_xuat_kho(request):
    danh_sach_xuat_kho = DotXuatKho.objects.all().order_by('-id')  
    return render(request, 'KhoNVL/danh_sach_dot_xuat_kho.html', {
        'danh_sach_xuat_kho': danh_sach_xuat_kho,
    })


def chi_tiet_dot_xuat_kho(request, pk):
    dot_xuat_kho = get_object_or_404(DotXuatKho, pk=pk)
    items = dot_xuat_kho.items.select_related('nvl')  
    return render(request, 'KhoNVL/chi_tiet_dot_xuat_kho.html', {
        'dot_xuat_kho': dot_xuat_kho,
        'items': items,
    })


# Kiểm kho
def tao_dot_kiem_kho(request):
    KiemKhoItemFormSet = modelformset_factory(KiemKhoItem, fields=('nvl', 'so_luong_thuc_te'), extra=0)

    if request.method == 'POST':
        dot_kiem_kho = DotKiemKho.objects.create(ghi_chu=request.POST.get('ghi_chu', ''))
        
        formset = KiemKhoItemFormSet(request.POST, queryset=KiemKhoItem.objects.none())

        if formset.is_valid():
            for form in formset:
                kiem_kho_item = form.save(commit=False)
                kiem_kho_item.dot_kiem_kho = dot_kiem_kho
                kiem_kho_item.so_luong_ly_thuyet = kiem_kho_item.nvl.so_luong_ton 
                kiem_kho_item.save()
            
            return redirect('chi_tiet_dot_kiem_kho')

    else:
        danh_sach_nvl = NVL.objects.all()
        initial_data = [{'nvl': nvl, 'so_luong_thuc_te': nvl.so_luong_ton} for nvl in danh_sach_nvl]
        formset = KiemKhoItemFormSet(queryset=KiemKhoItem.objects.none(), initial=initial_data)

    return render(request, 'KhoNVL/tao_dot_kiem_kho.html', {
        'formset': formset,
        'danh_sach_nvl': danh_sach_nvl,
    })

def chi_tiet_dot_kiem_kho(request, pk):
    dot_kiem_kho = get_object_or_404(DotKiemKho, pk=pk)
    items = dot_kiem_kho.items.select_related('nvl')

    return render(request, 'KhoNVL/chi_tiet_dot_kiem_kho.html', {
        'dot_kiem_kho': dot_kiem_kho,
        'items': items,
    })


def luu_dot_kiem_kho(request):
    if request.method == 'POST':
        dot_kiem_kho = DotKiemKho.objects.create()
        for key, value in request.POST.items():
            if key.startswith('so_luong_thuc_te_'):
                nvl_id = key.split('_')[-1]
                nvl = NVL.objects.get(id=nvl_id)
                so_luong_thuc_te = int(value)
                so_luong_ly_thuyet = nvl.so_luong_ton

                kiem_kho_item = KiemKhoItem.objects.create(
                    dot_kiem_kho=dot_kiem_kho,
                    nvl=nvl,
                    so_luong_thuc_te=so_luong_thuc_te,
                    so_luong_ly_thuyet=so_luong_ly_thuyet,
                )

                nvl.so_luong_ton = so_luong_thuc_te
                nvl.save()
        
        return redirect('chi_tiet_dot_kiem_kho', pk=dot_kiem_kho.id)

    return render(request, 'KhoNVL/tao_dot_kiem_kho.html')

def danh_sach_dot_kiem_kho(request):
    danh_sach_dots = DotKiemKho.objects.prefetch_related('items').annotate(total_items=models.Count('items')).order_by('-id')

    return render(request, 'KhoNVL/danh_sach_dot_kiem_kho.html', {
        'danh_sach_dots': danh_sach_dots,
    })



from django.http import JsonResponse
from .models import OrderItem, XuatKhoItem, KiemKhoItem
from django.db.models import Sum

def tableau_dashboard(request):
    return render(request, 'dashboard.html')

