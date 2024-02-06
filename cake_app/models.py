from django.db import models

# Create your models here.

class admin_login_tb (models.Model):
	name=models.CharField(max_length=100,default='')
	email=models.CharField( max_length=100, default='')
	password=models.CharField(max_length=300, default='')


class category_tb(models.Model):
	category=models.CharField(max_length=100,default='')


class product_tb(models.Model):
	cid=models.ForeignKey(category_tb,on_delete=models.CASCADE,default="")
	image=models.FileField(upload_to='products')
	image1=models.FileField(upload_to='products')
	image2=models.FileField(upload_to='products')
	name=models.CharField( max_length=100, default='')
	price1=models.CharField(max_length=300, default='')
	price2=models.CharField(max_length=300, default='')
	price3=models.CharField(max_length=300, default='')
	price4=models.CharField(max_length=300, default='')
	price5=models.CharField(max_length=300, default='')


class order_tb(models.Model):
	pid=models.ForeignKey(product_tb,on_delete=models.CASCADE,default="")
	weight=models.CharField(max_length=100,default='')
	message=models.CharField(max_length=100,default='')
	quantity=models.CharField(max_length=100,default='')
	price=models.CharField(max_length=100,default='')
	total=models.CharField(max_length=100,default='')



class bill_tb(models.Model):
	oid=models.ForeignKey(order_tb,on_delete=models.CASCADE,default="",null=True)
	first=models.CharField(max_length=100,default='')
	last=models.CharField(max_length=100,default='')	
	address=models.CharField(max_length=100,default='')	
	city=models.CharField(max_length=100,default='')	
	pin=models.CharField(max_length=100,default='')
	email=models.CharField(max_length=100,default='')	
	phone=models.CharField(max_length=100,default='')
	amount=models.CharField(max_length=100,default='')



class touch_tb(models.Model):
	name=models.CharField(max_length=100,default='')
	email=models.CharField(max_length=100,default='')