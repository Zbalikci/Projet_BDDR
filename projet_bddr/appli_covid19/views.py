from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.db import models
from appli_covid19.models import Theme, Sous_Theme, Journal, Affiliation, Articles, Article_Theme, StudyType_Articles, StudyType, Author_Affiliation, Author_Article, Authors
from datetime import datetime
from collections import Counter
from django.db.models.functions import Length
from django.core.paginator import Paginator

def index(request):
    themes = Theme.objects.all()
    template = loader.get_template('acceuil.twig')
    context = {'themes': themes,}
    return HttpResponse(template.render(context, request))

############################ REQUETE 1 Liste d'articles par thématiques et sous-thématique ############################

def sous_themes(request, name_theme):
	themes = Theme.objects.all()
	t = Theme.objects.get(name=str(name_theme))
	sous_themes = Sous_Theme.objects.filter(theme=t).values()
	template = loader.get_template('sous_themes.twig')
	context = {'themes': themes, 'sous_themes': sous_themes, 'theme':name_theme,}
	return HttpResponse(template.render(context, request))

def articles(request, name_sous_theme):
	if name_sous_theme!='NULL':
		themes = Theme.objects.all()
		st = Sous_Theme.objects.get(name=str(name_sous_theme))
		t = st.theme
		articles_sous_themes = Article_Theme.objects.filter(sous_theme=st).values()
		n=len(articles_sous_themes)
		liste_id_articles=[articles_sous_themes[k]['article_id'] for k in range(n)]
		liste_articles=[Articles.objects.get(id_article=i) for i in liste_id_articles]
		template = loader.get_template('articles.twig')
		context = {'themes': themes,'sous_theme' : name_sous_theme, 'theme':t , 'articles_sous_themes': liste_articles,}
		return HttpResponse(template.render(context, request))
	
############################ REQUETE 2 Histogramme d'articles publiés par date, semaine, et mois. ############################

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

############################ REQUETE 4 Nombre de publications par labo/institution. ############################

def affiliations2(request):
	themes = Theme.objects.all()
	liste_affiliations= Affiliation.objects.raw('''
	SELECT appli_covid19_affiliation.id, appli_covid19_affiliation.name, COUNT(DISTINCT appli_covid19_author_article.article_id) as nb_articles
	FROM appli_covid19_affiliation
	INNER JOIN appli_covid19_author_affiliation ON appli_covid19_affiliation.id=appli_covid19_author_affiliation.affiliation_id
	INNER JOIN appli_covid19_author_article ON appli_covid19_author_article.author_id=appli_covid19_author_affiliation.author_id
	GROUP BY appli_covid19_affiliation.id
	ORDER BY nb_articles DESC
	''')
	paginator = Paginator(liste_affiliations, 25)
	page = request.GET.get('page')
	liste_affiliations2 = paginator.get_page(page)
	template = loader.get_template('affiliations2.twig')
	context = {'themes': themes,'liste_affiliations': liste_affiliations2,}
	return HttpResponse(template.render(context, request))

############################ REQUETE 5 Liste de journaux par nombre et type de publications ############################

def journaux2(request):
	themes = Theme.objects.all()
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
	context = {'themes': themes, 'dict_study_type': inv_dict_study_type , }
	return HttpResponse(template.render(context, request))

#################################### REQUETE 6 Liste d'articles/jounaux/affiliations/types de publications ####################################

def des_articles(request):
	themes = Theme.objects.all()
	nb_articles=Articles.objects.count()
	liste_articles = Articles.objects.all().order_by('id_article')
	paginator = Paginator(liste_articles, 25)
	page = request.GET.get('page')
	liste_articles2 = paginator.get_page(page)
	template = loader.get_template('des_articles.twig')
	context = {'themes': themes, 'liste_articles': liste_articles2, 'nb_articles': nb_articles,}
	return HttpResponse(template.render(context, request))

def affiliations(request):
	themes = Theme.objects.all()
	liste_affiliations=Affiliation.objects.all().order_by('id')
	paginator = Paginator(liste_affiliations, 25) 
	page = request.GET.get('page')
	liste_affiliations2 = paginator.get_page(page)
	nb_total_affiliations=Affiliation.objects.count()
	template = loader.get_template('affiliations.twig')
	context = {'themes': themes, 'liste_affiliations': liste_affiliations2, 'nb_total_affiliations':nb_total_affiliations,}
	return HttpResponse(template.render(context, request))

def journaux(request):
	themes = Theme.objects.all()
	journaux = Journal.objects.all().order_by('id_journal')
	paginator = Paginator(journaux, 25)
	page = request.GET.get('page')
	journaux2 = paginator.get_page(page)
	nb_total_journaux=Journal.objects.count()
	template = loader.get_template('journaux.twig')
	context = {'themes': themes, 'journaux': journaux2 , 'nb_total_journaux':nb_total_journaux,}
	return HttpResponse(template.render(context, request))

def studytypes(request):
	themes = Theme.objects.all()
	liste = StudyType.objects.exclude(name='NULL').order_by('id')
	nb_articles=StudyType_Articles.objects.filter(studytype__in=liste).distinct('article').count()
	paginator = Paginator(liste, 25)
	page = request.GET.get('page')
	liste2 = paginator.get_page(page)
	template = loader.get_template('studytypes.twig')
	context = {'themes': themes, 'liste': liste2, 'nb_articles': nb_articles,}
	return HttpResponse(template.render(context, request))

def auteurs(request):
	themes = Theme.objects.all()
	liste = Authors.objects.all().order_by('id')
	paginator = Paginator(liste, 25)
	page = request.GET.get('page')
	liste2 = paginator.get_page(page)
	nb_auteurs=Authors.objects.all().count()
	template = loader.get_template('auteurs.twig')
	context = {'themes': themes, 'liste': liste2, 'nb_auteurs' : nb_auteurs,}
	return HttpResponse(template.render(context, request))

#################################### REQUETE 7 Recherche par nom article/jounal/affiliation ####################################

def des_articles2(request):
	themes = Theme.objects.all()
	if request.method=="POST":
		username=request.POST.get("username")
		u=username.upper()
		liste_articles=Articles.objects.filter(title__icontains=u).values().order_by('id_article')
	else:
		username=None
		liste_articles = Articles.objects.all()
	template = loader.get_template('des_articles2.twig')
	context = {'themes': themes,'liste_articles': liste_articles, 'username': username, }
	return HttpResponse(template.render(context, request))

def affiliations3(request):
	themes = Theme.objects.all()
	if request.method=="POST":
		username=request.POST.get("username")
		u=username.upper()
		liste_affiliations=Affiliation.objects.filter(name__icontains=u).values().order_by('id')
	else:
		username=None
		liste_affiliations = Affiliation.objects.all()
	template = loader.get_template('affiliations3.twig')
	context = {'themes': themes,'liste_affiliations': liste_affiliations, 'username':username}
	return HttpResponse(template.render(context, request))

def journaux3(request):
	themes = Theme.objects.all()
	if request.method=="POST":
		username=request.POST.get("username")
		u=username.upper()
		journaux=Journal.objects.filter(name__icontains=u).values().order_by('id_journal')
	else:
		username=None
		journaux = Journal.objects.all()
	template = loader.get_template('journaux3.twig')
	context = {'themes': themes,'journaux': journaux, 'username':username,}
	return HttpResponse(template.render(context, request))

#################################### REQUETE 8 Données sur un article/jounal/affiliation ####################################

def un_article(request, name_article):
	themes = Theme.objects.all()
	le_article=Articles.objects.get(id_article=name_article)
	l=Author_Article.objects.filter(article=le_article)
	liste_auteurs=Author_Article.objects.filter(article=le_article).values('author')
	liste_affiliation=Author_Affiliation.objects.filter(author__in=liste_auteurs).distinct('affiliation')
	sous_theme=Article_Theme.objects.filter(article=le_article)
	study_types=StudyType_Articles.objects.filter(article=le_article)
	template = loader.get_template('un_article.twig')
	context = {'themes': themes ,'sous_theme' : sous_theme, 'study_types':study_types , 'le_article': le_article, 'liste_auteurs':l, 'liste_affiliation':liste_affiliation,}
	return HttpResponse(template.render(context, request))

def affiliation(request,name_affiliation):
	themes = Theme.objects.all()
	un_affiliation=Affiliation.objects.get(name=name_affiliation)
	le_type=un_affiliation.type
	le_country=un_affiliation.country
	l=Author_Affiliation.objects.filter(affiliation=un_affiliation).values('author')
	nb_articles=Author_Article.objects.filter(author__in=l).distinct('article').count()
	liste_articles=Author_Article.objects.filter(author__in=l).distinct('article').order_by('article_id')
	paginator = Paginator(liste_articles, 25)
	page = request.GET.get('page')
	liste_articles2 = paginator.get_page(page)
	template = loader.get_template('affiliation.twig')
	context = {
		'name_affiliation': name_affiliation, 'le_type': le_type, 'le_country':le_country,
		'liste_articles' : liste_articles2, 'nb_articles':nb_articles, 'themes': themes,
		}
	return HttpResponse(template.render(context, request))

def journal(request,name_journal):
	themes = Theme.objects.all()
	un_journal=Journal.objects.get(name=name_journal)
	nb_articles=Articles.objects.filter(journal_id=un_journal.id_journal).count()
	liste_articles=Articles.objects.filter(journal_id=un_journal.id_journal).order_by('id_article')
	paginator = Paginator(liste_articles, 25)
	page = request.GET.get('page')
	liste_articles2 = paginator.get_page(page)
	template = loader.get_template('journal.twig')
	context = {'themes': themes, 'nb_articles': nb_articles, 'liste_articles':liste_articles2, 'name_journal':name_journal, }
	return HttpResponse(template.render(context, request))

def studytype(request,name_study):
	themes = Theme.objects.all()
	un_study=StudyType.objects.get(name=name_study)
	nb_articles=StudyType_Articles.objects.filter(study=un_study).count()
	liste_articles=StudyType_Articles.objects.filter(study=un_study)
	template = loader.get_template('studytype.twig')
	context = {'themes': themes, 'nb_articles': nb_articles, 'liste_articles':liste_articles, 'name_study':name_study, }
	return HttpResponse(template.render(context, request))
