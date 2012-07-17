from django import forms

class MakePostForm(forms.Form):
	rating = forms.ChoiceField(choices= (
		('0', 'Safe'),
		('1', 'Questionable'),
		('2', 'Explicit')
	))
	file = forms.FileField()
	source = forms.CharField(max_length=256)
	tags = forms.CharField()
	
class SearchByTagForm(forms.Form):
	tags = forms.CharField()
	rating = forms.ChoiceField(choices= (
		('x', 'All'),
		('0', 'Safe'),
		('1', 'Questionable'),
		('2', 'Explicit'),
	))