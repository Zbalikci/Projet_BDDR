from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
from django.http import HttpResponse
from appli_covid19.models import Theme,Articles
#from appli_covid19.models import Articles, Journal, StudyType_Articles, StudyType, Sous_Theme, Article_Theme,Theme



def index(request):
    return render(request, 'page.tmpl')
    
    
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
        
class ArticleChart(TemplateView):
	template_name = 'appli_covid19/chart.html'
	
	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context["qs"]= Articles.objects.all()[:10]
		return context
		
