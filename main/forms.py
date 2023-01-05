from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import UserAddressBook,Rating

class SignupForm(UserCreationForm):
	class Meta:
		model=User
		fields=('first_name','last_name','email','username','password1','password2')

# Review Add Form
class ReviewAdd(forms.ModelForm):
	class Meta:
		model=Rating
		fields=('review_rating','review_title','review_text')

# AddressBook Add Form
class AddressBookForm(forms.ModelForm):
	class Meta:
		model=UserAddressBook
		fields=('address','mobile','status')

# ProfileEdit
class ProfileForm(UserChangeForm):
	class Meta:
		model=User
		fields=('first_name','last_name','email','username')


# SORT_CHOICES =(
#     (0, "By default"),
#     (1, "By name"),
#     (2, "By popularity"),
# )
# # List sort form
# class ListSortForm(forms.Form):
# 	sort = forms.ChoiceField(choices=SORT_CHOICES,widget=forms.Select(attrs={'id': "sort"}))
# 	n_per = forms.IntegerField(min_value=1,required=True,widget=forms.NumberInput(attrs={'id': "pro",'value': "9"}))
# 	page = forms.IntegerField(min_value=1,required=True)
