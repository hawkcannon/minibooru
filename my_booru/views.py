# Create your views here.
import os

from my_booru.models import Post, Tag
from my_booru.forms import MakePostForm, SearchByTagForm

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

rating_translate = ("Safe", "Questionable", "Explicit",)

def viewPost(request, post_id):
	result = Post.objects.filter(id=post_id)
	if len(result) == 1:
		taglist = result[0].tags
		rendresult = os.path.basename(result[0].path)
	else:
		taglist = None
		rendresult = None
	return render_to_response('viewPost_template.html', {'rating': rating_translate[result[0].rating], 'taglist': taglist, 'post': rendresult}, context_instance=RequestContext(request))

@csrf_exempt
def searchByTags(request):
	if request.method == 'POST':
		form = SearchByTagForm(request.POST)
		if form.is_valid():
			result = Post.objects.all()
			if request.POST['tags'] != '*':
				for mystr in request.POST['tags'].split(" "):
					result = result.filter(tags__name=mystr)
			if request.POST['rating'] != 'x':
				result = result.filter(rating=int(request.POST['rating']))
			result = map(lambda x: {'postid': x.id, 'post': os.path.basename(x.path)}, result)
			return render_to_response('searchByTags_template.html', {'results': result, 'searched': True, 'form': form})
	else:
		form = SearchByTagForm()
	return render_to_response('searchByTags_template.html', {'results': None, 'searched': False, 'form': form})
	
@csrf_exempt
def makePost(request):
	if request.method == 'POST':
		form = MakePostForm(request.POST, request.FILES)
		if form.is_valid():
			mypost = Post()
			mypost.rating = int(form.cleaned_data['rating'])
			mypost.source = form.cleaned_data['source']
			mypost.save()
			
			for mystr in form.cleaned_data['tags'].split(' '):
				matchingtags = Tag.objects.filter(name=mystr)
				if matchingtags and len(matchingtags) == 1:
					mypost.tags.add(matchingtags[0])
				else:
					mytag = Tag()
					mytag.name = mystr
					mytag.creator = False
					mytag.series = False
					mytag.save()
					mypost.tags.add(mytag)
			
			mypost.save()
			myfile = request.FILES['file']
			mypost.path = (os.getcwd() + "/mybooru/static/" + str(mypost.id) + os.path.splitext(myfile.name)[1]).replace("\\", "/")
			with open(mypost.path, 'wb+') as destination:
				for chunk in myfile.chunks():
					destination.write(chunk)
			
			mypost.save()
			
			return HttpResponseRedirect('../view/' + str(mypost.id))
	else:
		form = MakePostForm()
	return render_to_response('makePost_template.html', {'form': form})