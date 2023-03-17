from django.db import models

# Create your models here.

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
	name=models.CharField(max_length=300, unique=True)
	def __str__(self):
		return self.name
	def __repr__(self):
		return self.name

class StudyType(models.Model):
	name=models.CharField(max_length=100, unique=True)
	def __str__(self):
		return self.name
	def __repr__(self):
		return self.name

class Affiliation(models.Model):
	name=models.CharField(max_length=200, unique=True,null=True)
	type=models.CharField(max_length=50)
	location=models.CharField(max_length=200,null=True)
	def __str__(self):
		return self.name
	def __repr__(self):
		return self.name

class Authors(models.Model):
	name=models.CharField(max_length=100, unique=True)
	email=models.CharField(max_length=100, unique=True,null=True)
	affliation=models.ForeignKey(Affiliation, on_delete=models.CASCADE)
	def __str__(self):
		return self.name
	def __repr__(self):
		return self.name
		
class Articles(models.Model):
	title=models.CharField(max_length=200)
	publication_date=models.DateTimeField(null=True)
	abstract=models.TextField()
	stulink=models.URLField(null=True)
	studytype=models.ForeignKey(StudyType, on_delete=models.CASCADE)
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
