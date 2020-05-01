from django.db import models
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.conf import settings


# class User (User):
# 	class Meta:
# 		verbose_name = "User"

class Tag(models.Model):
	COLOR_CHOICES = (
		("R","Red"),
		("O","Orange"),
		("G","Green"),
	)
	class Meta:
		verbose_name = "Tag"
	name = models.CharField(max_length=100, default="")
	color = models.CharField(max_length=100, choices=COLOR_CHOICES, default="Green")

	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse_lazy('tags')


class Project(models.Model):
	"""
    Déclinaison de produit déterminée par des attributs comme la couleur, etc.
    """

	class Meta:
		verbose_name = "Projet"

	name = models.CharField(max_length=100)
	code = models.PositiveSmallIntegerField("code", null=True, blank=True)
	description = models.TextField(default="")
	security_needs = models.ManyToManyField("SecurityNeedValue", related_name="project_item")
	tags = models.ManyToManyField("Tag", related_name="tags")
	author = models.ForeignKey(User, related_name="author", on_delete=models.DO_NOTHING, default="", null=True, blank=True)
	contributors  = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="contributors")

	def __unicode__(self):
		return u"{0} [{1}]".format(self.product.name, self.code)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse_lazy('portal')


class SecurityNeed(models.Model):
	"""
    Attributs produit
    """

	class Meta:
		verbose_name = "Security Need"

	name = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name
	def __str__(self):
		return self.name


class SecurityNeedValue(models.Model):
	"""
    Valeurs des attributs
    """

	class Meta:
		verbose_name = "Security Need Value"
		ordering = ['position']

	value = models.IntegerField()
	#type = models.CharField(max_length=100, default="None")
	attribute = models.ForeignKey('SecurityNeed', verbose_name="Unité", on_delete=models.CASCADE)
	position = models.PositiveSmallIntegerField("Position", null=True, blank=True)

	def __unicode__(self):
		return u"[{1}] {0}".format(self.attribute, self.value)
	def __str__(self):
		return u"{0} level {1}".format(self.attribute.name, self.value)


class Control(models.Model):
	"""
    Valeurs des attributs
    """

	class Meta:
		verbose_name = "Security Control"
		verbose_name_plural = "Security Controls"


	code = models.CharField(max_length=100)
	#control_attribute = models.ForeignKey('ControlsCatalog', verbose_name="Catalogue de Controles", on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	control_description = models.TextField()
	applicable_securityneedvalue = models.ManyToManyField("SecurityNeedValue")
	applicable_tags = models.ManyToManyField("Tag")

	def __unicode__(self):
		return u"{0}".format(self.title)
	def __str__(self):
		return u"{0}".format(self.code)
	def get_absolute_url(self):
		return reverse_lazy('controls')



class ProjectControl(models.Model):
	APPLICABLE_CHOICES = (
		("A","Applicable"),
		("NA","Not Applicable"),
	)
	STATUS_CHOICES = (
		("D","Done"),
		("NP", "Not Planned"),
		("P", "Planned")
	)
	project = models.ForeignKey('Project', verbose_name="Project", on_delete=models.CASCADE)
	control = models.ForeignKey('Control', verbose_name="Controle", on_delete=models.CASCADE)
	applicable = models.CharField(max_length=100, null=True, choices=APPLICABLE_CHOICES)
	status = models.CharField(max_length=100, choices=STATUS_CHOICES)


	class Meta:
		verbose_name = "Project Control"
		unique_together = ('project','control',)


	def __unicode__(self):
		return u"{0} [{1}]".format(self.project,)

	def __str__(self):
		return u"[{1}] {0}".format(self.project, self.control)

	def get_absolute_url(self):
		return reverse('project', kwargs=dict(id=self.project.pk))