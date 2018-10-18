from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models.signals import post_save

class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})
        
# Create your models here.
class User(AbstractUser):
	STUDENT = 'ST'
	TEACHER = 'TE'
	USER_ROLE = (
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
	)

	who_is = models.CharField(max_length=2,choices=USER_ROLE,default=TEACHER)
	objects = CustomUserManager()

	def __str__(self):
		return self.first_name

class Course(models.Model):
	thumb = models.CharField(max_length=255)
	name = models.CharField(max_length=200)
	created_date = models.DateTimeField(auto_now_add=True)
	contents = models.ManyToManyField("Content")
	price = models.DecimalField(decimal_places=2, max_digits=8)
	teacher = models.ForeignKey("Teacher", related_name="lectures", on_delete=models.CASCADE)

	def __str__(self):
		return self.name

class Lecture(models.Model):
	thumb = models.CharField(max_length=255)
	created_date = models.DateTimeField(auto_now_add=True)
	url = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	course = models.ForeignKey("Course", related_name="lectures", on_delete=models.CASCADE)

	def __str__(self):
		return self.name

class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="student")
	name = models.CharField(max_length=255)
	contents = models.ManyToManyField("Content")

	def __str__(self):
		return self.name

	def is_it_my_course(self, course_id):
		course = Course.objects.get(pk=course_id)
		return Subscription.objects.filter(student=self, course=course).exists()

	def buy_course(self, course_id):
		if not self.is_it_my_course(course_id):
			course = Course.objects.get(pk=course_id)
			student = self
			Subscription.objects.create(course=course, student=student, price=course.price)
			return True
		else:
			return False

	def favorite_course(self, course_id):
		course = Course.objects.get(pk=course_id)
		student = self
		
		subscription = Subscription.objects.get(course=course, student=student)
		subscription.is_favorite = not subscription.is_favorite
		subscription.save()

	def rate_course(self, course_id, rating):
		course = Course.objects.get(pk=course_id)
		student = self

		subscription = Subscription.objects.get(course=course, student=student)
		subscription.rating = rating
		subscription.save()

class Teacher(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="teacher")
	name = models.CharField(max_length=255)
	contents = models.ManyToManyField("Content")

	def is_it_my_course(self, course_id):
		course = Course.objects.get(pk=course_id)
		return Subscription.objects.filter(course__teacher=self).exists()

	def set_course_payment(self, course_id):
		if self.is_it_my_course(course_id):
			course = Course.objects.get(pk=course_id)
			teacher = self
			subs = Subscription.objects.get(course__teacher=teacher)
			subs.status = 'PA'
			subs.save()
			return True
		else:
			return False

	def __str__(self):
		return self.name	

class Content(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name

class Subscription(models.Model):
	PAID = 'PA'
	PENDING = 'PE'
	PAYMENT_STATUS = (
        (PAID, 'Paid'),
        (PENDING, 'Pending'),
    )
	status = models.CharField(
        max_length=2,
        choices=PAYMENT_STATUS,
        default=PENDING,
    )
	price = models.DecimalField(decimal_places=2, max_digits=8)
	student = models.ForeignKey("Student", related_name="subscriptions", on_delete=models.CASCADE)
	course = models.ForeignKey("Course", related_name="subscriptions", on_delete=models.CASCADE)
	is_favorite = models.BooleanField(default=False)
	rating = models.DecimalField(default=0, decimal_places=1, max_digits=2)
	
	#def 

class DiscountCoupon(models.Model):
	PER_PRICE = 'PPR'
	PER_PERCENTAGE = 'PPE'
	DISCOUNT_CHOICES = (
        (PER_PRICE, 'Per Price'),
        (PER_PERCENTAGE, 'Per Percentage'),
    )
	discount_type = models.CharField(
		max_length=3,
        choices=DISCOUNT_CHOICES,
        default=PER_PRICE,
	)
	value = models.DecimalField(decimal_places=2, max_digits=8)
	expiration_date = models.DateField()
	course = models.ForeignKey("Course", related_name="discount_coupons", on_delete=models.CASCADE)