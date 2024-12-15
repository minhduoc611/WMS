# views.py trong app KhoThanhPham
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import *
from KhoNVL.models import ThanhPham
import json
from .forms import *
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

# Nhập kho thành phẩm
def nhap_kho_thanh_pham(request):
    if request.method == 'POST':
        nhap_kho = NhapKhoThanhPham.objects.create()
        formset = ThanhPhamItemFormSet(request.POST, prefix='items')

        if formset.is_valid():
            for form in formset:
                nhap_kho_item = form.save(commit=False)
                nhap_kho_item.nhap_kho = nhap_kho
                nhap_kho_item.save()

                
                thanh_pham = nhap_kho_item.thanh_pham
                thanh_pham.so_luong_ton += nhap_kho_item.so_luong
                thanh_pham.save()

            return JsonResponse({'status': 'success', 'nhap_kho_id': nhap_kho.id})
        else:
            return JsonResponse({'status': 'error', 'message': 'Dữ liệu không hợp lệ'})

    else:
        formset = ThanhPhamItemFormSet(queryset=NhapKhoThanhPhamItem.objects.none(), prefix='items')
        san_pham_list = ThanhPham.objects.all()
        return render(request, 'KhoThanhPham/tao_nhap_kho_thanh_pham.html', {
            'formset': formset,
            'san_pham_list': san_pham_list
        })


def danh_sach_don_nhap_kho(request):
    danh_sach_don = NhapKhoThanhPham.objects.all().order_by('-ngay_nhap')
    return render(request, 'KhoThanhPham/danh_sach_nhap_kho.html', {'danh_sach_don_nhap_kho': danh_sach_don})

def chi_tiet_don_nhap_kho(request, pk):
    don_nhap_kho = get_object_or_404(NhapKhoThanhPham, pk=pk)
    items = don_nhap_kho.items.all()
    
    return render(request, 'KhoThanhPham/chi_tiet_don_nhap_kho.html', {
        'don_nhap_kho': don_nhap_kho,
        'items': items  
    })

# Kho thành phẩm
def danh_sach_thanh_pham(request):

    ten_thanh_pham=request.GET.get('ten_thanh_pham','')
    size=request.GET.get('size','')
    mau_sac=request.GET.get('mau_sac','')

    queryset=ThanhPham.objects.all()
    thanh_pham_list = ThanhPham.objects.all()
    
    if ten_thanh_pham:
        queryset=queryset.filter(ten_thanh_pham__icontains=ten_thanh_pham)
    if size:
        queryset=queryset.filter(size__icontains=size)
    if mau_sac:
        queryset = queryset.filter(mau_sac__icontains=mau_sac)

    context={
        'thanh_pham_list': thanh_pham_list,
        'danh_sach_tp' : queryset,
        'size':size,
        'mau_sac':mau_sac
        


    }

    return render(request, 'KhoThanhPham/danh_sach_thanh_pham.html',context)

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def add_thanh_pham(request):
    if request.method == "POST":
        try:
            # Kiểm tra nội dung của body request
            data = json.loads(request.body)
            print(data)  # Debugging - xem dữ liệu nhận được từ client

            ten_thanh_pham = data.get('ten_thanh_pham')
            mau_sac = data.get('mau_sac')
            size = data.get('size')
            don_gia = data.get('don_gia')
            so_luong_ton = data.get('so_luong_ton')

            thanh_pham = ThanhPham.objects.create(
                ten_thanh_pham=ten_thanh_pham,
                mau_sac=mau_sac,
                size=size,
                don_gia=don_gia,
                so_luong_ton=so_luong_ton
            )

            return JsonResponse({
                'success': True,
                'ten_thanh_pham': thanh_pham.ten_thanh_pham,
                'mau_sac': thanh_pham.mau_sac,
                'size': thanh_pham.size,
                'don_gia': thanh_pham.don_gia,
                'so_luong_ton': thanh_pham.so_luong_ton,
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid method'})

from django.core.exceptions import ValidationError
from django.contrib import messages
def upload_excel(request):
    if request.method == 'POST' and request.FILES.get('file'):
        excel_file = request.FILES['file']
        
        try:

            df = pd.read_excel(excel_file, engine='openpyxl')
            
            required_columns = ['Tên thành phẩm', 'Màu sắc', 'Size', 'Đơn giá (VND)', 'Số lượng tồn kho']
            for col in required_columns:
                if col not in df.columns:
                    raise ValidationError(f"Thiếu cột: {col}")
            
            for _, row in df.iterrows():
                ThanhPham.objects.create(
                    ten_thanh_pham=row['Tên thành phẩm'],
                    mau_sac=row['Màu sắc'],
                    size=row['Size'],
                    don_gia=row['Đơn giá (VND)'],
                    so_luong_ton=row['Số lượng tồn kho']
                )
            
            return JsonResponse({'success': True, 'message': 'File đã được tải lên thành công!'})
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': f"Đã có lỗi xảy ra: {str(e)}"})
    
    return JsonResponse({'success': False, 'message': "Không có file nào được chọn!"})
#Xuất kho
def xuat_kho_thanh_pham(request):
    if request.method == 'POST':
        formset = XuatThanhPhamItemFormSet(request.POST, prefix='items')

        if formset.is_valid():
            xuat_kho = XuatKhoThanhPham.objects.create()
            for form in formset:
                
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    print("Đang xử lý form:", form.cleaned_data)
                    xuat_kho_item = form.save(commit=False)
                    xuat_kho_item.xuat_kho = xuat_kho
                    thanh_pham = xuat_kho_item.thanh_pham

                    
                    if thanh_pham.so_luong_ton >= xuat_kho_item.so_luong:
                        thanh_pham.so_luong_ton -= xuat_kho_item.so_luong
                        thanh_pham.save()
                        xuat_kho_item.save()
                    else:
                        return JsonResponse({'status': 'error', 'message': f"Số lượng tồn kho không đủ cho {thanh_pham.ten_thanh_pham}"})
            return JsonResponse({'status': 'success'})
        else:
            
            for i, form in enumerate(formset):
                if not form.is_valid():
                    print(f"Lỗi form {i}:", form.errors)
            print("Lỗi formset tổng thể:", formset.errors)
            return JsonResponse({'status': 'error', 'message': 'Dữ liệu không hợp lệ'})
    else:
        formset = XuatThanhPhamItemFormSet(queryset=XuatKhoThanhPhamItem.objects.none(), prefix='items')
        san_pham_list = ThanhPham.objects.all()
        return render(request, 'KhoThanhPham/tao_xuat_kho_thanh_pham.html', {
            'formset': formset,
            'san_pham_list': san_pham_list
        })


def danh_sach_xuat_kho_thanh_pham(request):
    danh_sach_don_xuat = XuatKhoThanhPham.objects.all().order_by('-ngay_xuat')
    return render(request, 'KhoThanhPham/danh_sach_xuat_kho_thanh_pham.html', {'danh_sach_don_xuat': danh_sach_don_xuat})


def chi_tiet_don_xuat_kho_thanh_pham(request, pk):
    don_xuat_kho = get_object_or_404(XuatKhoThanhPham, pk=pk)
    return render(request, 'KhoThanhPham/chi_tiet_don_xuat_kho_thanh_pham.html', {'don_xuat_kho': don_xuat_kho})


#Kiểm kho

def tao_dot_kiem_kho_thanh_pham(request):
    KiemKhoThanhPhamItemFormSet = modelformset_factory(
        KiemKhoThanhPhamItem,
        fields=('thanh_pham', 'so_luong_thuc_te'),
        extra=0
    )

    if request.method == 'POST':
        dot_kiem_kho_thanh_pham = KiemKhoThanhPham.objects.create(ghi_chu=request.POST.get('ghi_chu', ''))

        formset = KiemKhoThanhPhamItemFormSet(request.POST, queryset=KiemKhoThanhPhamItem.objects.none())

        if formset.is_valid():
            for form in formset:
                kiem_kho_item = form.save(commit=False)
                kiem_kho_item.kiem_kho = dot_kiem_kho_thanh_pham
                kiem_kho_item.so_luong_ly_thuyet = kiem_kho_item.thanh_pham.so_luong_ton  # Lấy số lượng lý thuyết từ hệ thống
                kiem_kho_item.save()

            return redirect('chi_tiet_dot_kiem_kho_thanh_pham')

    else:
        danh_sach_thanh_pham = ThanhPham.objects.all()
        initial_data = [{'thanh_pham': tp, 'so_luong_thuc_te': tp.so_luong_ton} for tp in danh_sach_thanh_pham]
        formset = KiemKhoThanhPhamItemFormSet(queryset=KiemKhoThanhPhamItem.objects.none(), initial=initial_data)

    return render(request, 'KhoThanhPham/tao_dot_kiem_kho_thanh_pham.html', {
        'formset': formset,
        'danh_sach_thanh_pham': danh_sach_thanh_pham,
    })


def luu_dot_kiem_kho_thanh_pham(request):
    if request.method == 'POST':
        dot_kiem_kho = KiemKhoThanhPham.objects.create()
        for key, value in request.POST.items():
            if key.startswith('so_luong_thuc_te_'):
                tp_id = key.split('_')[-1]
                thanh_pham = ThanhPham.objects.get(id=tp_id)
                so_luong_thuc_te = int(value)
                so_luong_ly_thuyet = thanh_pham.so_luong_ton

                kiem_kho_item = KiemKhoThanhPhamItem.objects.create(
                    kiem_kho=dot_kiem_kho,  
                    thanh_pham=thanh_pham,
                    so_luong_thuc_te=so_luong_thuc_te,
                    so_luong_ly_thuyet=so_luong_ly_thuyet,
                )

                # Cập nhật lại số lượng tồn kho nếu cần
                thanh_pham.so_luong_ton = so_luong_thuc_te
                thanh_pham.save()

        return redirect('KhoThanhPham:chi_tiet_dot_kiem_kho_thanh_pham', pk=dot_kiem_kho.id)

    return render(request, 'KhoThanhPham/tao_dot_kiem_kho_thanh_pham.html')



def chi_tiet_dot_kiem_kho_thanh_pham(request, pk):
    dot_kiem_kho = get_object_or_404(KiemKhoThanhPham, pk=pk)
    kiem_kho_items = dot_kiem_kho.items.all()

    return render(request, 'KhoThanhPham/chi_tiet_dot_kiem_kho_thanh_pham.html', {
        'dot_kiem_kho': dot_kiem_kho,
        'kiem_kho_items': kiem_kho_items,
    })

def danh_sach_dot_kiem_kho_thanh_pham(request):
    danh_sach_dot_kiem_kho = KiemKhoThanhPham.objects.all().order_by('-ngay_kiem')
    return render(request, 'KhoThanhPham/danh_sach_dot_kiem_kho_thanh_pham.html', {
        'danh_sach_dot_kiem_kho': danh_sach_dot_kiem_kho,
    })  