from ..models import *
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator

def ProductSearch(request):
    if request.GET:
        # search = Products.objects.filter(name='product1')
        # return HttpResponse('You search ' + request.GET['product'])
        menus = Navigation.objects.filter(parent_page_id=0).order_by('position')
        all_product = Products.objects.filter(name__icontains=request.GET['product'])
        product = Paginator(all_product, 16)
        # return HttpResponse(all_product)
        page_number = request.GET.get('page')
        product = product.get_page(page_number)
        c_id = request.COOKIES['c_id']
        global_data = GlobalSettings.objects.first()
        data = {'menus':menus,'global_data':global_data,'product':product,'c_id':c_id,'search':'Search'}
        return render(request,'main/sale.html',data)
