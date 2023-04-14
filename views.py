from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from appli_covid19.models import Theme
#from appli_covid19.models import Articles, Journal, StudyType_Articles, StudyType, Sous_Theme, Article_Theme,Theme



def index(request):
    return HttpResponse("Ceci est une vue basique pour l'application de mon projet.\n")
    
    
def themes(request):
    return render(request, 'themes.tmpl', 
        {                                          
            'themes': Theme.objects.all()
        })
    
#def articles(request):
	#return render(request, 'articles.tmpl', 
        #{                                          
        #    'articles': Articles.objects.all()[:50],
        #   'themes': Theme.objects.all(),
        #   'sous_themes': Sous_Theme.objects.all(),
        #    'article_theme':Article_Theme.objects.all()
      
       
        #})
        
def page(request):
	return render(request, 'page.tmpl')
