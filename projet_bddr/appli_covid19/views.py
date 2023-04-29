from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader
from appli_covid19.models import Theme, Sous_Theme, Journal, Affiliation, Articles, Article_Theme, StudyType_Articles, StudyType, Author_Affiliation, Author_Article
from datetime import datetime
from collections import Counter
from django.db.models.functions import Length
from django.db.models import Count

def index(request):
    return render(request, 'page.tmpl')

def des_articles(request):
	nb_articles=Articles.objects.count()
	liste_articles = Articles.objects.all()
	template = loader.get_template('des_articles.twig')
	context = {'liste_articles': liste_articles, 'nb_articles': nb_articles,}
	return HttpResponse(template.render(context, request))

############################ REQUETE 1 Liste d'articles par thématiques et sous-thématique ############################

def sous_themes(request, name_theme):
	t = Theme.objects.get(name=str(name_theme))
	sous_themes = Sous_Theme.objects.filter(theme=t).values()
	template = loader.get_template('sous_themes.twig')
	context = {'sous_themes': sous_themes, 'theme':name_theme,}
	return HttpResponse(template.render(context, request))

def articles(request, name_sous_theme):
	if name_sous_theme!='NULL':
		st = Sous_Theme.objects.get(name=str(name_sous_theme))
		t = st.theme
		articles_sous_themes = Article_Theme.objects.filter(sous_theme=st).values()
		n=len(articles_sous_themes)
		liste_id_articles=[articles_sous_themes[k]['article_id'] for k in range(n)]
		liste_articles=[Articles.objects.get(id_article=i) for i in liste_id_articles]
		template = loader.get_template('articles.twig')
		context = {'sous_theme' : name_sous_theme, 'theme':t , 'articles_sous_themes': liste_articles,}
		return HttpResponse(template.render(context, request))

############################ REQUETE 3 Liste des thématiques ############################

def themes(request):
	themes = Theme.objects.all()
	template = loader.get_template('themes.twig')
	context = {'themes': themes,}
	return HttpResponse(template.render(context, request))

############################ REQUETE 4 Nombre de publications par labo/institution. ############################

def affiliations(request):
	liste_affiliations=Affiliation.objects.all()
	nb_total_affiliations=Affiliation.objects.count()
	template = loader.get_template('affiliations.twig')
	context = {'liste_affiliations': liste_affiliations, 'nb_total_affiliations':nb_total_affiliations,}
	return HttpResponse(template.render(context, request))

def affiliation(request,name_affiliation):
	un_affiliation=Affiliation.objects.get(name=name_affiliation)
	le_type=un_affiliation.type
	le_country=un_affiliation.country
	l=Author_Affiliation.objects.filter(affiliation=un_affiliation).values('author')
	nb_articles=Author_Article.objects.filter(author__in=l).distinct('article').count()
	liste_articles=Author_Article.objects.filter(author__in=l).distinct('article')
	template = loader.get_template('affiliation.twig')
	context = {
		'name_affiliation': name_affiliation, 'le_type': le_type, 'le_country':le_country,
		'liste_articles' : liste_articles, 'nb_articles':nb_articles, 
		}
	return HttpResponse(template.render(context, request))

def affiliations2(request):
	liste_affiliations= Affiliation.objects.raw('''
	SELECT appli_covid19_affiliation.id, appli_covid19_affiliation.name, COUNT(DISTINCT appli_covid19_author_article.article_id) as nb_articles
	FROM appli_covid19_affiliation
	INNER JOIN appli_covid19_author_affiliation ON appli_covid19_affiliation.id=appli_covid19_author_affiliation.affiliation_id
	INNER JOIN appli_covid19_author_article ON appli_covid19_author_article.author_id=appli_covid19_author_affiliation.author_id
	GROUP BY appli_covid19_affiliation.id
	ORDER BY nb_articles DESC
	''')
	template = loader.get_template('affiliations2.twig')
	context = {'liste_affiliations': liste_affiliations,}
	return HttpResponse(template.render(context, request))

############################ REQUETE 5 Liste de journaux par nombre et type de publications ############################
''' 
Idee 1 : création de dict={ un_journal : nb_articles_de_ce_journal , un_autre_journal : nb_articles_de_ce_journal, ets... }
Conséquence : lonque chargement de la page
Idee 2 : création d'un page par journal avec ses types de publications
Conséquence : non affichage des types de publications car trop de journal avec 0 type de publications connus
Idee 3 : Création d'un page par studytype
'''
def journaux(request):
	journaux = Journal.objects.all()
	nb_total_journaux=Journal.objects.count()
	template = loader.get_template('journaux.twig')
	context = {'journaux': journaux , 'nb_total_journaux':nb_total_journaux,}
	return HttpResponse(template.render(context, request))

def journal(request,name_journal):
	un_journal=Journal.objects.get(name=name_journal)
	nb_articles=Articles.objects.filter(journal_id=un_journal.id_journal).count()
	liste_articles=Articles.objects.filter(journal_id=un_journal.id_journal)
	liste_auteurs=Author_Article.objects.filter(article__in=liste_articles)
	template = loader.get_template('journal.twig')
	context = {'nb_articles': nb_articles, 'liste_articles':liste_articles, 'name_journal':name_journal, 'liste_auteurs':liste_auteurs, }
	return HttpResponse(template.render(context, request))

def journaux2(request):
	keys=StudyType.objects.exclude(name='NULL')
	dict_study_type={k : list(set([s.article.journal for s in StudyType_Articles.objects.filter(studytype=k)])) for k in keys }
	inv_dict_study_type= {}
	for k, v in dict_study_type.items():
		for j in v:
			if j not in inv_dict_study_type:
				inv_dict_study_type[j] = {'liste_study_types' : [k], 'nb_articles': Articles.objects.filter(journal=j).count()}
			else:
				inv_dict_study_type[j]['liste_study_types'].append(k)
	template = loader.get_template('journaux2.twig')
	context = {'dict_study_type': inv_dict_study_type , }
	return HttpResponse(template.render(context, request))

############################ REQUETE 2 Histogramme d'articles publiés par date, semaine, et mois. ############################

def histogram(request):
	return render(request, 'histogram.twig')

def histogram_annee(request):

	liste_annee1=[A.publish_time for A in Articles.objects.annotate(text_len=Length('publish_time')).filter(text_len__lt=5)]
	liste_annee2=[A.publish_time[0:4] for A in Articles.objects.annotate(text_len=Length('publish_time')).filter(text_len__gt=5)]
	liste_annee=dict(Counter(liste_annee1+liste_annee2))
	template = loader.get_template('histogram_annee.twig')
	context = {'liste_annee': liste_annee, }
	return HttpResponse(template.render(context, request))

def histogram_mois(request):

	liste_mois1=[datetime.strptime(A.publish_time,'%Y-%m-%d').month for A in Articles.objects.annotate(text_len=Length('publish_time')).filter(text_len__gt=5)]
	liste_mois=dict(Counter(liste_mois1))
	template = loader.get_template('histogram_mois.twig')
	context = {'liste_mois': liste_mois, }
	return HttpResponse(template.render(context, request))

def histogram_semaine(request):

	liste_semaine1=[datetime.strptime(A.publish_time,'%Y-%m-%d').isocalendar().week for A in Articles.objects.annotate(text_len=Length('publish_time')).filter(text_len__gt=5)]
	liste_semaine=dict(Counter(liste_semaine1))
	template = loader.get_template('histogram_semaine.twig')
	context = {'liste_semaine': liste_semaine, }
	return HttpResponse(template.render(context, request))

def histogram_date(request):

	liste_date1=[A.publish_time for A in Articles.objects.annotate(text_len=Length('publish_time')).filter(text_len__gt=5)]
	liste_date=dict(Counter(liste_date1))
	template = loader.get_template('histogram_date.twig')
	context = {'liste_date': liste_date, }
	return HttpResponse(template.render(context, request))

class ArticleChart(TemplateView):
	template_name = 'chart.twig'
	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context["qs"]= Articles.objects.all()[:10]
		return context