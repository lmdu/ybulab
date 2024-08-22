from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.
class Profile(models.Model):
	TITLES = (
		(0, "无"),
		(1, "教授"),
		(2, "研究员"),
		(3, "副教授"),
		(4, "副研究员"),
		(5, "讲师"),
		(6, "助理研究员")
	)

	DEGREES = (
		(0, "无"),
		(1, "博士"),
		(2, "硕士"),
		(3, "学士")
	)

	POSITIONS = (
		(0, "无"),
		(1, "教职工"),
		(2, "博士后"),
		(2, "学生"),
	)

	STATUS = (
		(0, "无"),
		(1, "在职"),
		(2, "离职"),
		(3, "在读"),
		(4, "毕业"),
		(5, "退学"),
	)

	GROUPS = (
		(0, "未激活"),
		(1, "访客"),
		(2, "编辑"),
		(3, "管理员"),
	)

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	major = models.CharField(max_length=150, blank=True, null=True)
	resume = models.TextField(blank=True, null=True)
	title = models.SmallIntegerField(choices=TITLES, default=0)
	degree = models.SmallIntegerField(choices=DEGREES, default=0)
	position = models.SmallIntegerField(choices=POSITIONS, default=0)
	status = models.SmallIntegerField(choices=STATUS, default=0)
	group = models.SmallIntegerField(choices=GROUPS, default=0)
	created = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

class Resource(models.Model):
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	file = models.FileField(upload_to='uploads/%Y/%m/%d/')
	ftype = models.SmallIntegerField()

class Species(models.Model):
	species_en = models.CharField(max_length=100)
	species_cn = models.CharField(max_length=100, blank=True)
	kingdom_en = models.CharField(max_length=30, blank=True)
	kingdom_cn = models.CharField(max_length=30, blank=True)
	phylum_en = models.CharField(max_length=30, blank=True)
	phylum_cn = models.CharField(max_length=30, blank=True)
	class_en = models.CharField(max_length=30, blank=True)
	class_cn = models.CharField(max_length=30, blank=True)
	oder_en = models.CharField(max_length=50, blank=True)
	oder_cn = models.CharField(max_length=50, blank=True)
	family_en = models.CharField(max_length=50, blank=True)
	family_cn = models.CharField(max_length=50, blank=True)
	genus_en = models.CharField(max_length=50, blank=True)
	genus_cn = models.CharField(max_length=50, blank=True)

class Project(models.Model):
	name = models.CharField(max_length=200)
	details = models.TextField(blank=True)
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

class Specimen(models.Model):
	GENDERS = (
		(0, "无"),
		(1, "雄性"),
		(2, "雌性")
	)
	species = ForeignKey(Species, on_delete=models.CASCADE)
	code = models.CharField(max_length=30, blank=True)
	name = models.CharField(max_length=100, blank=True)
	gender = models.SmallIntegerField(choices=GENDERS, default=0)
	bottle = models.CharField(max_length=30, blank=True)
	details = models.TextField(blank=True)
	comment = models.TextField(blank=True)
	creator = ForeignKey(User, on_delete=models.CASCADE)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)


class Sample(models.Model):
	species = ForeignKey(Species, on_delete=models.CASCADE)
	code = models.CharField(max_length=30, blank=True)
	name = models.CharField(max_length=50, blank=True)
	tissue = models.CharField(max_length=30, blank=True)
	collect_location = models.CharField(max_length=200, blank=True)
	collect_longitude = models.CharField(max_length=20, blank=True)
	collect_latitude = models.CharField(max_length=20, blank=True)
	collect_time = models.DateField(blank=True)
	store_place = models.CharField(max_length=100)
	store_method = models.CharField(max_length=100)
	comment = models.TextField(blank=True)
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	photos = GenericRelation(Resource)
	files = GenericRelation(Resource)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

class SampleMeta(models.Model):
	sample = models.OneToOneField(Sample, on_delete=models.CASCADE)
	project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True)
	specimen = models.ForeignKey(Specimen, on_delete=models.CASCADE, blank=True)

