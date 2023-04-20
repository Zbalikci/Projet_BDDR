from django.db import models

class Theme(models.Model):
	name=models.CharField(max_length=50,unique=True)
	def __str__(self):
		return self.name
	def __repr__(self):
		return self.name
		
class Sous_Theme(models.Model):
	name=models.CharField(max_length=100,unique=True)
	theme=models.ForeignKey(Theme, on_delete=models.CASCADE)
	def __str__(self):
		return self.name
	def __repr__(self):
		return self.name

class Journal(models.Model):
	name=models.CharField(max_length=600, unique=True)
	def __str__(self):
		return self.name
	def __repr__(self):
		return self.name
	@classmethod
	def nb_articles(self):
		return Articles.objects.filter(journal=self).count()
	nb = property(nb_articles)

class StudyType(models.Model):
	name=models.CharField(max_length=100, unique=True)
	def __str__(self):
		return self.name
	def __repr__(self):
		return self.name

class Affiliation(models.Model):
	name=models.TextField(unique=True,null=True)
	type=models.CharField(max_length=50)
	country=models.CharField(max_length=360,null=True)
	def __str__(self):
		return self.name
	def __repr__(self):
		return self.name

class Authors(models.Model):
	name=models.CharField(max_length=100,unique=True)
	email=models.CharField(max_length=100,null=True)
	def __str__(self):
		return self.name
	def __repr__(self):
		return self.name
		
class Articles(models.Model):
	id = models.BigIntegerField(primary_key=True)
	title=models.TextField(null=True)
	publish_time=models.CharField(max_length=15,null=True)
	abstract=models.TextField(null=True)
	studylink=models.URLField(max_length=400,null=True)
	journal=models.ForeignKey(Journal, on_delete=models.CASCADE)
	def __str__(self):
		return self.title
	def __repr__(self):
		return self.title
	
class Author_Article(models.Model):
	author=models.ForeignKey(Authors, on_delete=models.CASCADE)
	article=models.ForeignKey(Articles, on_delete=models.CASCADE)

class Article_Theme(models.Model):
	sous_theme=models.ForeignKey(Sous_Theme, on_delete=models.CASCADE)
	article=models.ForeignKey(Articles, on_delete=models.CASCADE)

class Author_Affiliation(models.Model):
	author=models.ForeignKey(Authors, on_delete=models.CASCADE)
	affiliation=models.ForeignKey(Affiliation, on_delete=models.CASCADE)
	
class StudyType_Articles(models.Model):
	studytype=models.ForeignKey(StudyType, on_delete=models.CASCADE)
	article=models.ForeignKey(Articles, on_delete=models.CASCADE)

