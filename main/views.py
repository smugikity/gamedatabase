from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse,HttpResponseNotFound,Http404
from .models import Banner,Category,Brand,Product,ProductAttribute,CartOrder,CartOrderItems,ProductReview,Wishlist,UserAddressBook,Genre,Publisher,Developer,Platform,Game,PersonalList,Rating,Comment
from django.db.models import Max,Min,Count,Avg
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from django.db.models.functions import ExtractMonth
from django.template.loader import render_to_string
from main.forms import SignupForm,ReviewAdd,AddressBookForm,ProfileForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
#paypal
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
import datetime

from main import tools

# Game info - basic info of a game to present in catalog 

# Home Page
def home(request):
	banners=Banner.objects.all().order_by('-id')
	# data=Product.objects.filter(is_featured=True).order_by('-id')
	random_games = tools.get_n_random_games(50)
	return render(request,'index.html',{'data':random_games,'banners':banners})

# Category
def category_list(request):
    data=Category.objects.all().order_by('-id')
    return render(request,'category_list.html',{'data':data})

# Brand
def brand_list(request):
    data=Brand.objects.all().order_by('-id')
    return render(request,'brand_list.html',{'data':data})

# Product List
def product_list(request):
	total_data=Product.objects.count()
	data=Product.objects.all().order_by('-id')[:3]
	min_price=ProductAttribute.objects.aggregate(Min('price'))
	max_price=ProductAttribute.objects.aggregate(Max('price'))
	return render(request,'product_list.html',
		{
			'data':data,
			'total_data':total_data,
			'min_price':min_price,
			'max_price':max_price,
		}
		)

# Product List According to Category
def category_product_list(request,cat_id):
	category=Category.objects.get(id=cat_id)
	data=Product.objects.filter(category=category).order_by('-id')
	return render(request,'category_product_list.html',{
			'data':data,
			})

# Product List According to Brand
def brand_product_list(request,brand_id):
	brand=Brand.objects.get(id=brand_id)
	data=Product.objects.filter(brand=brand).order_by('-id')
	return render(request,'category_product_list.html',{
			'data':data,
			})

# Product Detail
def product_detail(request,slug,id):
	product=Product.objects.get(id=id)
	related_products=Product.objects.filter(category=product.category).exclude(id=id)[:4]
	colors=ProductAttribute.objects.filter(product=product).values('color__id','color__title','color__color_code').distinct()
	sizes=ProductAttribute.objects.filter(product=product).values('size__id','size__title','price','color__id').distinct()
	reviewForm=ReviewAdd()

	# Check
	canAdd=True
	reviewCheck=ProductReview.objects.filter(user=request.user,product=product).count()
	if request.user.is_authenticated:
		if reviewCheck > 0:
			canAdd=False
	# End

	# Fetch reviews
	reviews=ProductReview.objects.filter(product=product)
	# End

	# Fetch avg rating for reviews
	avg_reviews= ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
	# End

	return render(request, 'product_detail.html',{'data':product,'related':related_products,'colors':colors,'sizes':sizes,'reviewForm':reviewForm,'canAdd':canAdd,'reviews':reviews,'avg_reviews':avg_reviews})

# Search
def search(request,custom):
	q=request.GET['q']
	total_count, items=tools.get_search(custom,q)
	return JsonResponse({"total_count":total_count,"items":items})

# Filter Data
def filter_data(request):
	colors=request.GET.getlist('color[]')
	categories=request.GET.getlist('category[]')
	brands=request.GET.getlist('brand[]')
	sizes=request.GET.getlist('size[]')
	minPrice=request.GET['minPrice']
	maxPrice=request.GET['maxPrice']
	allProducts=Product.objects.all().order_by('-id').distinct()
	allProducts=allProducts.filter(productattribute__price__gte=minPrice)
	allProducts=allProducts.filter(productattribute__price__lte=maxPrice)
	if len(colors)>0:
		allProducts=allProducts.filter(productattribute__color__id__in=colors).distinct()
	if len(categories)>0:
		allProducts=allProducts.filter(category__id__in=categories).distinct()
	if len(brands)>0:
		allProducts=allProducts.filter(brand__id__in=brands).distinct()
	if len(sizes)>0:
		allProducts=allProducts.filter(productattribute__size__id__in=sizes).distinct()
	t=render_to_string('ajax/product-list.html',{'data':allProducts})
	return JsonResponse({'data':t})

# Load More
def load_more_data(request):
	offset=int(request.GET['offset'])
	limit=int(request.GET['limit'])
	data=Product.objects.all().order_by('-id')[offset:offset+limit]
	t=render_to_string('ajax/product-list.html',{'data':data})
	return JsonResponse({'data':t}
)

# Add to cart
def add_to_cart(request):
	# del request.session['cartdata']
	cart_p={}
	cart_p[str(request.GET['id'])]={
		'image':request.GET['image'],
		'title':request.GET['title'],
		'qty':request.GET['qty'],
		'price':request.GET['price'],
	}
	if 'cartdata' in request.session:
		if str(request.GET['id']) in request.session['cartdata']:
			cart_data=request.session['cartdata']
			cart_data[str(request.GET['id'])]['qty']=int(cart_p[str(request.GET['id'])]['qty'])
			cart_data.update(cart_data)
			request.session['cartdata']=cart_data
		else:
			cart_data=request.session['cartdata']
			cart_data.update(cart_p)
			request.session['cartdata']=cart_data
	else:
		request.session['cartdata']=cart_p
	return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})

# Cart List Page
def cart_list(request):
	total_amt=0
	if 'cartdata' in request.session:
		for p_id,item in request.session['cartdata'].items():
			total_amt+=int(item['qty'])*float(item['price'])
		return render(request, 'cart.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	else:
		return render(request, 'cart.html',{'cart_data':'','totalitems':0,'total_amt':total_amt})


# Delete Cart Item
def delete_cart_item(request):
	p_id=str(request.GET['id'])
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			del request.session['cartdata'][p_id]
			request.session['cartdata']=cart_data
	total_amt=0
	for p_id,item in request.session['cartdata'].items():
		total_amt+=int(item['qty'])*float(item['price'])
	t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

# Delete Cart Item
def update_cart_item(request):
	p_id=str(request.GET['id'])
	p_qty=request.GET['qty']
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			cart_data[str(request.GET['id'])]['qty']=p_qty
			request.session['cartdata']=cart_data
	total_amt=0
	for p_id,item in request.session['cartdata'].items():
		total_amt+=int(item['qty'])*float(item['price'])
	t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

#Chart
def chart(request):
	colors=request.GET.getlist('color[]')
	categories=request.GET.getlist('category[]')
	brands=request.GET.getlist('brand[]')
	sizes=request.GET.getlist('size[]')
	minRating=request.GET['minRating']
	allProducts=Product.objects.all().order_by('-id').distinct()
	allProducts=allProducts.filter(productattribute__price__gte=minPrice)
	allProducts=allProducts.filter(productattribute__price__lte=maxPrice)
	if len(colors)>0:
		allProducts=allProducts.filter(productattribute__color__id__in=colors).distinct()
	if len(categories)>0:
		allProducts=allProducts.filter(category__id__in=categories).distinct()
	if len(brands)>0:
		allProducts=allProducts.filter(brand__id__in=brands).distinct()
	if len(sizes)>0:
		allProducts=allProducts.filter(productattribute__size__id__in=sizes).distinct()
	t=render_to_string('ajax/product-list.html',{'data':allProducts})
	return JsonResponse({'data':t})

# Signup Form
def signup(request):
	if request.method=='POST':
		form=SignupForm(request.POST)
		if form.is_valid():
			form.save()
			username=form.cleaned_data.get('username')
			pwd=form.cleaned_data.get('password1')
			user=authenticate(username=username,password=pwd)
			login(request, user)
			return redirect('home')
	else:
		form=SignupForm
	return render(request, 'registration/signup.html', {'form':form})


# Checkout
@login_required
def checkout(request):
	total_amt=0
	totalAmt=0
	if 'cartdata' in request.session:
		for p_id,item in request.session['cartdata'].items():
			totalAmt+=int(item['qty'])*float(item['price'])
		# Order
		order=CartOrder.objects.create(
				user=request.user,
				total_amt=totalAmt
			)
		# End
		for p_id,item in request.session['cartdata'].items():
			total_amt+=int(item['qty'])*float(item['price'])
			# OrderItems
			items=CartOrderItems.objects.create(
				order=order,
				invoice_no='INV-'+str(order.id),
				item=item['title'],
				image=item['image'],
				qty=item['qty'],
				price=item['price'],
				total=float(item['qty'])*float(item['price'])
				)
			# End
		# Process Payment
		host = request.get_host()
		paypal_dict = {
		    'business': settings.PAYPAL_RECEIVER_EMAIL,
		    'amount': total_amt,
		    'item_name': 'OrderNo-'+str(order.id),
		    'invoice': 'INV-'+str(order.id),
		    'currency_code': 'USD',
		    'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
		    'return_url': 'http://{}{}'.format(host,reverse('payment_done')),
		    'cancel_return': 'http://{}{}'.format(host,reverse('payment_cancelled')),
		}
		form = PayPalPaymentsForm(initial=paypal_dict)
		address=UserAddressBook.objects.filter(user=request.user,status=True).first()
		return render(request, 'checkout.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt,'form':form,'address':address})

@csrf_exempt
def payment_done(request):
	returnData=request.POST
	return render(request, 'payment-success.html',{'data':returnData})


@csrf_exempt
def payment_canceled(request):
	return render(request, 'payment-fail.html')


# Save Review
def save_review(request,pid):
	product=Product.objects.get(pk=pid)
	user=request.user
	review=ProductReview.objects.create(
		user=user,
		product=product,
		review_text=request.POST['review_text'],
		review_rating=request.POST['review_rating'],
		)
	data={
		'user':user.username,
		'review_text':request.POST['review_text'],
		'review_rating':request.POST['review_rating']
	}

	# Fetch avg rating for reviews
	avg_reviews=ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
	# End

	return JsonResponse({'bool':True,'data':data,'avg_reviews':avg_reviews})

# User Dashboard
import calendar
def my_dashboard(request):
	orders=CartOrder.objects.annotate(month=ExtractMonth('order_dt')).values('month').annotate(count=Count('id')).values('month','count')
	monthNumber=[]
	totalOrders=[]
	for d in orders:
		monthNumber.append(calendar.month_name[d['month']])
		totalOrders.append(d['count'])
	return render(request, 'user/dashboard.html',{'monthNumber':monthNumber,'totalOrders':totalOrders})

# My Orders
def my_orders(request):
	orders=CartOrder.objects.filter(user=request.user).order_by('-id')
	return render(request, 'user/orders.html',{'orders':orders})

# Order Detail
def my_order_items(request,id):
	order=CartOrder.objects.get(pk=id)
	orderitems=CartOrderItems.objects.filter(order=order).order_by('-id')
	return render(request, 'user/order-items.html',{'orderitems':orderitems})

# Wishlist
def add_wishlist(request):
	pid=request.GET['product']
	product=Product.objects.get(pk=pid)
	data={}
	checkw=Wishlist.objects.filter(product=product,user=request.user).count()
	if checkw > 0:
		data={
			'bool':False
		}
	else:
		wishlist=Wishlist.objects.create(
			product=product,
			user=request.user
		)
		data={
			'bool':True
		}
	return JsonResponse(data)

# My Wishlist
def my_wishlist(request):
	wlist=Wishlist.objects.filter(user=request.user).order_by('-id')
	return render(request, 'user/wishlist.html',{'wlist':wlist})

# My Reviews
def my_reviews(request):
	reviews=ProductReview.objects.filter(user=request.user).order_by('-id')
	return render(request, 'user/reviews.html',{'reviews':reviews})

# My AddressBook
def my_addressbook(request):
	addbook=UserAddressBook.objects.filter(user=request.user).order_by('-id')
	return render(request, 'user/addressbook.html',{'addbook':addbook})

# Save addressbook
def save_address(request):
	msg=None
	if request.method=='POST':
		form=AddressBookForm(request.POST)
		if form.is_valid():
			saveForm=form.save(commit=False)
			saveForm.user=request.user
			if 'status' in request.POST:
				UserAddressBook.objects.update(status=False)
			saveForm.save()
			msg='Data has been saved'
	form=AddressBookForm
	return render(request, 'user/add-address.html',{'form':form,'msg':msg})

# Activate address
def activate_address(request):
	a_id=str(request.GET['id'])
	UserAddressBook.objects.update(status=False)
	UserAddressBook.objects.filter(id=a_id).update(status=True)
	return JsonResponse({'bool':True})

# Edit Profile
def edit_profile(request):
	msg=None
	if request.method=='POST':
		form=ProfileForm(request.POST,instance=request.user)
		if form.is_valid():
			form.save()
			msg='Data has been saved'
	form=ProfileForm(instance=request.user)
	return render(request, 'user/edit-profile.html',{'form':form,'msg':msg})

# Update addressbook
def update_address(request,id):
	address=UserAddressBook.objects.get(pk=id)
	msg=None
	if request.method=='POST':
		form=AddressBookForm(request.POST,instance=address)
		if form.is_valid():
			saveForm=form.save(commit=False)
			saveForm.user=request.user
			if 'status' in request.POST:
				UserAddressBook.objects.update(status=False)
			saveForm.save()
			msg='Data has been saved'
	form=AddressBookForm(instance=address)
	return render(request, 'user/update-address.html',{'form':form,'msg':msg})

# Edited

# 404
def handler404(request, exception, template_name='404.html'):
    response = render(request, template_name)
    response.status_code = 404
    return response


SORT_CHOICES = {
    0: "By default",
    1: "By name",
    2: "By popularity",
	3: "By rating"
}
DEFAULT_LIST_PARAS = {
	'sort': 0,
	'n_per': 9,
	'page': 1,
	'startdate': '01/01/1000',
	'enddate': '31/12/9999',
	'date_format_src': '%d/%m/%Y',
	'date_format_dest': '%Y-%m-%d',
}
#default sort=0, n_per=9, page=1
def custom_list(request,custom):
	sort=DEFAULT_LIST_PARAS['sort']
	n_per=DEFAULT_LIST_PARAS['n_per']
	page=DEFAULT_LIST_PARAS['page']
	count,max_page,page,data = tools.get_list(custom,sort,n_per,page)
	p=render_to_string('ajax/list_pages.html',{'count':count,'max_page':max_page,'page':page})
	c=render_to_string('ajax/custom_list_cards.html',{'data':data})
	return render(request, 'list.html',
	{'custom':custom, 'sort_choice': {k: SORT_CHOICES[k] for k in list(SORT_CHOICES.keys())[:3]},'p':p,'c':c})

def src_custom_list(request,custom):
	sort=int(request.GET.get('sort',DEFAULT_LIST_PARAS['sort'])) 
	n_per=int(request.GET.get('n_per',DEFAULT_LIST_PARAS['n_per']))
	page=int(request.GET.get('page',DEFAULT_LIST_PARAS['page']))
	count,max_page,page,data = tools.get_list(custom,sort,n_per,page)
	p=render_to_string('ajax/list_pages.html',{'count':count,'max_page':max_page,'page':page})
	c=render_to_string('ajax/custom_list_cards.html',{'data':data})
	return JsonResponse({'p': p,'c': c})


# Game List
def game_list(request):
	sort=DEFAULT_LIST_PARAS['sort']
	n_per=DEFAULT_LIST_PARAS['n_per']
	page=DEFAULT_LIST_PARAS['page']
	startdate=datetime.datetime.strptime(DEFAULT_LIST_PARAS['startdate'],DEFAULT_LIST_PARAS['date_format_src']).strftime(DEFAULT_LIST_PARAS['date_format_dest']) 
	enddate=datetime.datetime.strptime(DEFAULT_LIST_PARAS['enddate'],DEFAULT_LIST_PARAS['date_format_src']).strftime(DEFAULT_LIST_PARAS['date_format_dest']) 
	genres=[]
	publishers=[]
	platforms=[]
	count,max_page,page,data = tools.get_game_list(sort,n_per,page,startdate,enddate,genres,publishers,platforms)
	p=render_to_string('ajax/list_pages.html',{'count':count,'max_page':max_page,'page':page})
	c=render_to_string('ajax/custom_list_cards.html',{'data':data})
	return render(request, 'game_list.html',{'sort_choice': SORT_CHOICES,'p':p,'c':c})

	#except (TypeError, ValidationError) as error:
	#	raise Http404(error)

# Game List
def src_game_list(request):
	sort=int(request.GET.get('sort',DEFAULT_LIST_PARAS['sort'])) 
	n_per=int(request.GET.get('n_per',DEFAULT_LIST_PARAS['n_per']))
	page=int(request.GET.get('page',DEFAULT_LIST_PARAS['page']))
	startdate=datetime.datetime.strptime(request.GET.get('startdate',DEFAULT_LIST_PARAS['startdate']),DEFAULT_LIST_PARAS['date_format_src']).strftime(DEFAULT_LIST_PARAS['date_format_dest']) 
	enddate=datetime.datetime.strptime(request.GET.get('enddate',DEFAULT_LIST_PARAS['enddate']),DEFAULT_LIST_PARAS['date_format_src']).strftime(DEFAULT_LIST_PARAS['date_format_dest']) 
	genres=request.GET.getlist('genre')
	publishers=request.GET.getlist('publisher')
	platforms=request.GET.getlist('platform')
	count,max_page,page,data = tools.get_game_list(sort,n_per,page,startdate,enddate,genres,publishers,platforms)
	p=render_to_string('ajax/list_pages.html',{'count':count,'max_page':max_page,'page':page})
	c=render_to_string('ajax/custom_list_cards.html',{'data':data})
	return JsonResponse({'p': p,'c': c})

	#except (TypeError, ValidationError) as error:
	#	raise Http404(error)


def view_item(request,custom,id):
	try:
		data = tools.get_custom_item(custom,id)
		return JsonResponse(data)
	except (ObjectDoesNotExist,MultipleObjectsReturned) as error:
		raise Http404(error)

# Game Detail
def game_detail(request,id):
	game=Game.objects.get(id=id)
	genres=game.genre.values_list("id","title")
	developers_query=game.developer
	developers=developers_query.values_list("id","title")
	publishers=developers_query.values_list("publisher__id","publisher_title")
	platforms=game.platform.values_list("id","title")
	# related_game=Game.objects.filter(genre=game.genre).exclude(id=id)[:4]

	reviewForm=ReviewAdd()

	# Check
	# canAdd=True
	# reviewCheck=ProductReview.objects.filter(user=request.user,product=product).count()
	# if request.user.is_authenticated:
	# 	if reviewCheck > 0:
	# 		canAdd=False
	# End

	# Fetch reviews
	reviews=Rating.objects.filter(game=game)
	comments=Comment.objects.filter(game=game)
	# End

	# Fetch avg rating for reviews
	avg_reviews=getattr(game, 'avg_rating')
	avg_star=round(avg_reviews*2)

	return render(request, 'game_detail.html',{'data':game,'genres':genres,'developers':developers,'publishers':publishers,'platforms':platforms,'reviewForm':reviewForm,'reviews':reviews,'comments':comments,'avg_reviews':avg_reviews,'avg_star':avg_star})