from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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

	pid = models.BigAutoField(primary_key=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	real = models.CharField(max_length=150)
	major = models.CharField(max_length=150, blank=True)
	resume = models.TextField(blank=True)
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

