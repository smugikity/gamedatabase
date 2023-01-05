from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse,HttpResponseNotFound,Http404,HttpResponseBadRequest
from .models import Banner,Genre,Publisher,Developer,Platform,Game,PersonalList,Rating,Comment,Profile
from django.db.models import Max,Min,Count,Avg
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from django.db.models.functions import ExtractMonth
from django.template.loader import render_to_string
from main.forms import SignupForm,ReviewAdd,ProfileForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
import datetime
from main import tools

# Game info - basic info of a game to present in catalog 

# Home Page
def home(request):
	banners=Banner.objects.all().order_by('-id')
	# data=Product.objects.filter(is_featured=True).order_by('-id')
	
	if (request.user.is_authenticated): user=request.user
	else: user=None
	data = tools.get_n_random_games(9,user=user)
	c=render_to_string('ajax/game_list_cards.html',{'data':data,'is_authenticated':request.user.is_authenticated})
	return render(request,'index.html',{'c':c,'banners':banners})



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

# User Dashboard
import calendar
def my_dashboard(request):
	orders = []
	monthNumber=[]
	totalOrders=[]
	for d in orders:
		monthNumber.append(calendar.month_name[d['month']])
		totalOrders.append(d['count'])
	return render(request, 'user/dashboard.html',{'monthNumber':monthNumber,'totalOrders':totalOrders})

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

# Edited

# 404
def handler404(request, exception, template_name='404.html'):
    response = render(request, template_name)
    response.status_code = 404
    return response

@login_required
def profile_self(request):
	if (request.user.is_authenticated):
		return profile(request,request.user.username)
	else: return HttpResponseNotFound()

def profile(request, username):
	displaying_user = User.objects.get(username=username)
	lists = PersonalList.objects.filter(user=displaying_user).values("id","title")
	try: prof = Profile.objects.get(user=displaying_user)
	except (ObjectDoesNotExist,MultipleObjectsReturned) as error:
		prof = Profile(user=displaying_user)
		prof.save()
	finally:
		return render(request,'profile.html',{'displaying_user':displaying_user, 'profile': prof, 'lists': lists})

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
	'enddate': '12/31/9999',
	'date_format_src': '%m/%d/%Y',
	'date_format_dest': '%Y-%m-%d',
	'wishlist_id': 0,
	'rtn_game': 0,
}

#default sort=0, n_per=9, page=1
def custom_list(request,custom):
	index_question = request.get_full_path().find('?')
	if (index_question == -1): init_paras_url = ""
	else: init_paras_url = request.get_full_path()[index_question:]
	return render(request, 'list.html',
	{'custom':custom, 'sort_choice': {k: SORT_CHOICES[k] for k in list(SORT_CHOICES.keys())[:3]},'init_paras_url':init_paras_url})

def src_custom_list(request,custom):
	sort=int(request.GET.get('sort',DEFAULT_LIST_PARAS['sort'])) 
	n_per=int(request.GET.get('n_per',DEFAULT_LIST_PARAS['n_per']))
	page=int(request.GET.get('page',DEFAULT_LIST_PARAS['page']))
	count,max_page,page,data = tools.get_custom_list(custom,sort,n_per,page)
	p=render_to_string('ajax/list_pages.html',{'count':count,'max_page':max_page,'page':page,'searching':0})
	c=render_to_string('ajax/custom_list_cards.html',{'data':data})
	return JsonResponse({'p': p,'c': c})

# Game List
def game_list(request):
	index_question = request.get_full_path().find('?')
	if (index_question == -1): init_paras_url = ""
	else: init_paras_url = request.get_full_path()[index_question:]
	return render(request, 'game_list.html',{'sort_choice': SORT_CHOICES,'init_paras_url':init_paras_url})

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
	if (request.user.is_authenticated): user=request.user
	else: user=None
	list_id=request.GET.get('list_id')
	if list_id:
		count,max_page,page,data = tools.get_game_list(sort,n_per,page,startdate,enddate,genres,publishers,platforms,model_list=PersonalList.objects.get(pk=int(list_id)).game,user=user)
	else: count,max_page,page,data = tools.get_game_list(sort,n_per,page,startdate,enddate,genres,publishers,platforms,user=user)
	p=render_to_string('ajax/list_pages.html',{'count':count,'max_page':max_page,'page':page,'searching':0})
	c=render_to_string('ajax/game_list_cards.html',{'data':data,'is_authenticated':request.user.is_authenticated})
	return JsonResponse({'p': p,'c': c})

	#except (TypeError, ValidationError) as error:
	#	raise Http404(error)

def view_item(request,model_id,id):
	try:
		data = tools.get_custom_item(model_id,id)
		return JsonResponse(data)
	except (ObjectDoesNotExist,MultipleObjectsReturned) as error:
		return HttpResponseNotFound(error)

# Search
def search(request,custom):
	q=request.GET.get('q')
	total_count, items=tools.get_search(custom,q)
	return JsonResponse({"total_count":total_count,"items":items})

def custom_search_list(request,custom):
	sort=int(request.GET.get('sort',DEFAULT_LIST_PARAS['sort'])) 
	n_per=int(request.GET.get('n_per',DEFAULT_LIST_PARAS['n_per']))
	page=int(request.GET.get('page',DEFAULT_LIST_PARAS['page']))
	q=request.GET.get('q')
	count,max_page,page,data = tools.get_custom_search(custom,sort,n_per,page,q)
	p=render_to_string('ajax/list_pages.html',{'count':count,'max_page':max_page,'page':page,'searching':1})
	c=render_to_string('ajax/custom_list_cards.html',{'data':data})
	return JsonResponse({'p': p,'c': c})

def game_search_list(request):
	sort=int(request.GET.get('sort',DEFAULT_LIST_PARAS['sort'])) 
	n_per=int(request.GET.get('n_per',DEFAULT_LIST_PARAS['n_per']))
	page=int(request.GET.get('page',DEFAULT_LIST_PARAS['page']))
	q=request.GET.get('q',"")
	if (request.user.is_authenticated): user=request.user
	else: user=None
	list_id=request.GET.get('list_id')
	if list_id:
		count,max_page,page,data = tools.get_game_search(sort,n_per,page,q,model_list=PersonalList.objects.get(pk=int(list_id)).game,user=user)
	else: count,max_page,page,data = tools.get_game_search(sort,n_per,page,q,user=user)
	p=render_to_string('ajax/list_pages.html',{'count':count,'max_page':max_page,'page':page,'searching':1})
	c=render_to_string('ajax/game_list_cards.html',{'data':data,'is_authenticated':request.user.is_authenticated})
	return JsonResponse({'p': p,'c': c})

# Personal List
def personal_list(request,id):
	# try:
	list = get_list_object_if_wishlist(request,id)
	index_question = request.get_full_path().find('?')
	if (index_question == -1): init_paras_url = ""
	else: init_paras_url = request.get_full_path()[index_question:]
	return render(request, 'personal_list.html',{'sort_choice': SORT_CHOICES,'list_id':list.id,'init_paras_url':init_paras_url,'list_title':list.title,'list_description':list.description,'owned_user':list.user.username})
	# except (ObjectDoesNotExist,MultipleObjectsReturned) as error:
	# 	raise Http404(error)
	
@login_required
def personal_list_add(request,id):
	try:
		list = get_list_object_if_wishlist(request,id)
		game_id = int(request.GET.get('game'))
		if (request.user.is_authenticated) and (request.user.id == list.user.id) and (game_id):
			if Game.objects.filter(pk=game_id).exists(): 
				list.game.add(game_id)
				return HttpResponse()
		else: raise ValueError
	except (ObjectDoesNotExist,MultipleObjectsReturned,ValueError) as error:
		return HttpResponseNotFound(error)

@login_required
def personal_list_remove(request,id):
	try:
		list = get_list_object_if_wishlist(request,id)
		game_id = int(request.GET.get('game'))
		if (request.user.is_authenticated) and (request.user.id == list.user.id) and (game_id):
			if Game.objects.filter(pk=game_id).exists(): 
				list.game.remove(game_id)
				return HttpResponse()
			else: raise ObjectDoesNotExist
		else: raise ValueError
	except (ObjectDoesNotExist,MultipleObjectsReturned,ValueError) as error:
		return HttpResponseNotFound(error)

def get_list_object_if_wishlist(request,id):
	if (id==DEFAULT_LIST_PARAS['wishlist_id']):
		id=PersonalList.objects.filter(user=request.user).first().id
	return PersonalList.objects.get(pk=id)
	
# Wishlist
@login_required
def wishlist(request):
	return personal_list(request,DEFAULT_LIST_PARAS['wishlist_id'])
@login_required
def wishlist_add(request):
	return personal_list_add(request,DEFAULT_LIST_PARAS['wishlist_id'])
@login_required
def wishlist_remove(request):
	return personal_list_remove(request,DEFAULT_LIST_PARAS['wishlist_id'])

# Game Detail
def game_detail(request,id):
	user=None
	pfp=None
	if (request.user.is_authenticated): 
		user=request.user
		pfp=Profile.objects.get(user=user).image
	game,n_ratings,genre_list,dev_list,publisher,plat_list,comments,usr_rating,is_favorited = tools.get_game(id,user)
	return render(request, 'game.html',{'game':game,'n_ratings':n_ratings,'genre_list':genre_list,'dev_list':dev_list,'publisher':publisher,'plat_list':plat_list,'comments':comments,'usr_rating':usr_rating,'is_favorited':is_favorited,'pfp':pfp})

def get_rating(request):
	sort=int(request.GET.get('sort',DEFAULT_LIST_PARAS['sort'])) 
	n_per=int(request.GET.get('n_per',DEFAULT_LIST_PARAS['n_per']))
	page=int(request.GET.get('page',DEFAULT_LIST_PARAS['page']))
	by_user=int(request.GET.get('by_user',0))
	by_game=int(request.GET.get('by_game',0))
	# rtn_game=int(request.GET.get('rtn_game'),DEFAULT_LIST_PARAS['rtn_game'])
	if not User.objects.filter(pk=by_user).exists(): by_user=None
	if not Game.objects.filter(pk=by_game).exists(): by_game=None
	# if (rtn_game is 1): rtn_game=True
	# else: rtn_game=False
	count,max_page,page,data = tools.get_rating(sort,n_per,page,by_user=by_user,by_game=by_game)	
	p=render_to_string('ajax/list_pages.html',{'count':count,'max_page':max_page,'page':page,'searching':1})
	c=render_to_string('ajax/review_cards.html',{'data':data,'is_authenticated':request.user.is_authenticated})
	return JsonResponse({'p': p,'c': c})

@login_required
def comment_add(request):
	try:
		if request.method=='POST':
			content = request.POST.get('content').strip()
			if (content is "") or (not request.user.is_authenticated): raise ValueError
			game_id = int(request.POST.get('game_id'))
			Comment.objects.create(user=request.user,game=Game.objects.get(pk=game_id),content=content)
			return HttpResponse('')
		else: return HttpResponseBadRequest()
	except (ObjectDoesNotExist,MultipleObjectsReturned,ValueError) as error:
		return HttpResponseNotFound(error)

@login_required
def review_add(request):
	try:
		if request.method=='POST':
			rating = int(request.POST.get('rating',0))
			if (not rating) or (not request.user.is_authenticated): raise ValueError
			game_id = int(request.POST.get('game_id',0))
			Rating.objects.update_or_create(game_id=game_id,user=request.user,defaults={'review_rating':rating,'review_title':request.POST.get('title',"").strip(),'review_text':request.POST.get('content',"").strip()})
			return HttpResponse('')
		else: return HttpResponseBadRequest('Please pick the star.')
	except (ObjectDoesNotExist,MultipleObjectsReturned,ValueError) as error:
		return HttpResponseNotFound('Please pick the star.')

@login_required
def review_delete(request):
	try:
		if request.method=='POST':
			if (not request.user.is_authenticated): raise ValueError
			game_id = int(request.POST.get('game_id'))
			Rating.objects.filter(game__id=game_id,user=request.user).delete()
			return HttpResponse('')
		else: return HttpResponseBadRequest()
	except (ObjectDoesNotExist,MultipleObjectsReturned,ValueError) as error:
		return HttpResponseNotFound(error)