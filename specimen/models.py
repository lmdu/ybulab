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
		(4, "超级管理员"),
	)

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	major = models.CharField(max_length=150, blank=True, null=True)
	resume = models.TextField(blank=True, null=True)
	phone = models.CharField(max_length=20, blank=True, null=True)
	title = models.SmallIntegerField(choices=TITLES, blank=True, default=0)
	degree = models.SmallIntegerField(choices=DEGREES, blank=True, default=0)
	position = models.SmallIntegerField(choices=POSITIONS, blank=True, default=0)
	status = models.SmallIntegerField(choices=STATUS, blank=True, default=0)
	identity = models.SmallIntegerField(choices=GROUPS, blank=True, default=0)
	created = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

class Resource(models.Model):
	upfile = models.FileField(upload_to='uploads/%Y/%m/%d/')
	uptype = models.SmallIntegerField()
	uptime = models.DateTimeField(auto_now_add=True)

class Species(models.Model):
	species_en = models.CharField(max_length=100)
	species_cn = models.CharField(max_length=100, blank=True)
	kingdom_en = models.CharField(max_length=30, blank=True)
	kingdom_cn = models.CharField(max_length=30, blank=True)
	phylum_en = models.CharField(max_length=30, blank=True)
	phylum_cn = models.CharField(max_length=30, blank=True)
	class_en = models.CharField(max_length=30, blank=True)
	class_cn = models.CharField(max_length=30, blank=True)
	order_en = models.CharField(max_length=50, blank=True)
	order_cn = models.CharField(max_length=50, blank=True)
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
		(0, "未知"),
		(1, "雄性"),
		(2, "雌性")
	)

	STATUS = (
		(0, "无"),
		(1, "在库"),
		(2, "在用"),
		(3, "用完")
	)

	specimen_code = models.CharField(max_length=30, blank=True)
	specimen_name = models.CharField(max_length=100, blank=True)
	specimen_gender = models.SmallIntegerField(choices=GENDERS, default=0)
	collect_location = models.CharField(max_length=200, blank=True)
	collect_longitude = models.CharField(max_length=30, blank=True)
	collect_latitude = models.CharField(max_length=30, blank=True)
	collect_altitude = models.CharField(max_length=20, blank=True)
	collect_people = models.CharField(max_length=100, blank=True)
	collect_date = models.DateField(blank=True, null=True)
	store_place = models.CharField(max_length=200, blank=True)
	store_method = models.CharField(max_length=100, blank=True)
	bottle = models.CharField(max_length=30, blank=True)
	comment = models.TextField(blank=True)
	photos = models.JSONField(blank=True, default=[])
	attachments = models.JSONField(blank=True, default=[])
	status = models.SmallIntegerField(choices=STATUS, blank=True, default=0)
	species = models.ForeignKey(Species, on_delete=models.CASCADE)
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)


class Sample(models.Model):
	STATUS = (
		(0, "无"),
		(1, "在库"),
		(2, "在用"),
		(3, "用完")
	)

	sample_code = models.CharField(max_length=30, blank=True)
	sample_name = models.CharField(max_length=50, blank=True)
	sample_type = models.CharField(max_length=30, blank=True)
	sample_tissue = models.CharField(max_length=30, blank=True)
	collect_location = models.CharField(max_length=200, blank=True)
	collect_longitude = models.CharField(max_length=30, blank=True)
	collect_latitude = models.CharField(max_length=30, blank=True)
	collect_altitude = models.CharField(max_length=20, blank=True)
	collect_people = models.CharField(max_length=100, blank=True)
	collect_date = models.DateField(blank=True, null=True)
	store_place = models.CharField(max_length=200, blank=True)
	store_method = models.CharField(max_length=100, blank=True)
	comment = models.TextField(blank=True)
	photos = models.JSONField(blank=True, default=[])
	attachments = models.JSONField(blank=True, default=[])
	status = models.SmallIntegerField(choices=STATUS, blank=True, default=0)
	species = models.ForeignKey(Species, on_delete=models.CASCADE)
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

class SampleMeta(models.Model):
	sample = models.OneToOneField(Sample, on_delete=models.CASCADE)
	project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True)
	specimen = models.ForeignKey(Specimen, on_delete=models.CASCADE, blank=True)

