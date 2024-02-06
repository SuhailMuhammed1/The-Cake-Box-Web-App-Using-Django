from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from .models import *
import random
import string
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os
from .forms import ContactForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout


# Create your views here.
#########################################################################################################################
categoryquery=category_tb.objects.all()
db=admin_login_tb.objects.all()

def admin_page(request):
	if request.session.has_key('myid'):
		return render(request,'admin/index.html', {'db':db})
	else:
		return render(request,'admin/login.html', {'db':db})


def index(request):
	return render(request,'front/index.html',{'category':categoryquery})

def about(request):
	return render(request,'front/about.html',{'category':categoryquery})

def gallery(request):
	return render(request,'front/gallery.html',{'category':categoryquery})

def shop(request):
	return render(request,'front/shop.html',{'category':categoryquery})

def order(request):
	pid=request.GET.get('id')
	print(pid,"******************************************")
	p=product_tb.objects.all().filter(id=pid)
	
	return render(request,'front/order.html',{'category':categoryquery,'query':p})

def cart(request):
	return render(request,'front/cart.html',{'category':categoryquery})	

def checkout(request):
	return render(request,'front/checkout.html',{'category':categoryquery})

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            # Send the email
            subject = "Contact Form Submission"
            message = f"Name: {name}\nEmail: {email}\nMessage: {message}"
            from_email = email
            recipient_list = [ settings.EMAIL_HOST_USER ]  # Replace with the email where you want to receive the form submissions
            send_mail(subject, message, from_email, recipient_list)
            return HttpResponseRedirect('/')
            # Redirect to a success page
    else:
        form = ContactForm()
        return render(request,"front/index.html",{"form": form, 'category':categoryquery})
	
def custom_404_view(request, exception):
    return render(request, 'front/404.html', {'category':categoryquery}, status=404)

										

#####################################################################################################################





#####################################################################################################################
###################################################### ADMIN ########################################################
#####################################################################################################################

def admin_login(request):
	if request.method=="POST":
		username=request.POST['email']
		password=request.POST['password']
		b =admin_login_tb.objects.all().filter(email=username,password=password)
		if b.exists():
			for x in b:
				request.session["myid"]=x.id
				return render(request,'admin/index.html',{'message':'Successfully login', 'db':db})

		else:
				return render(request,'admin/login.html',{'message':'Invalid credentials', 'db':db})
	else:
		 return render(request,'admin/login.html')

def admin_logout(request):
	if request.session.has_key('myid'):
		del request.session['myid']
		logout(request)
	return HttpResponseRedirect('/admin_login/')


#####################################################################################################################

def add_category(request):
	if request.session.has_key("myid"):
		if request.method=="POST":
			category=request.POST['category']
			print(category)
			check=category_tb.objects.all().filter(category=category)
			if check:
				return render(request,'admin/add_category.html',{'category':categoryquery,'db':db})
			else:
				add=category_tb(category=category)
				add.save()
				return render(request,'admin/index.html')
		else:
			return render(request,'admin/add_category.html',{'category':categoryquery,'db':db})
	else:
		return render(request,'admin/login.html')



def view_category(request):
	if request.session.has_key("myid"):
		cat=category_tb.objects.all()
		if cat.exists():
			return render(request,"admin/view_category.html",{'cat':cat, 'db':db})
		else:
			return render(request,'admin/view_category.html',{'db':db})
	else:
		return render(request,'admin/login.html')




def delete_category(request):         
	if request.session.has_key("myid"):
		cid=request.GET['id']
		category_tb.objects.all().filter(id=cid).delete()
		cat=category_tb.objects.all()
		return render(request,'admin/view_category.html',{'cat':cat, 'db':db})
	else:
		return render(request,'admin/login.html')


################################################################################################################################

def add_product(request):
	if request.session.has_key('myid'):
		if request.method=='POST':
			category=request.POST['cid']
			print(category,'////////////')
			c=category_tb.objects.get(id=category)	
			print(c,'***************')
		
			image=request.FILES['image']
			image1=request.FILES['image1']
			image2=request.FILES['image2']
			name=request.POST['name']
			price1=request.POST['price1']
			price2=request.POST['price2']
			price3=request.POST['price3']
			price4=request.POST['price4']
			price5=request.POST['price5']

			
			s=product_tb(cid=c,image=image,image1=image1,image2=image2,name=name,price1=price1,price2=price2,price3=price3,price4=price4,price5=price5)
			s.save()
			
			query=category_tb.objects.all()

			return render(request,'admin/add_product.html',{'query':query, 'db':db})
			
		else:	
			query=category_tb.objects.all()
			return render(request,'admin/add_product.html',{'query':query, 'db':db})

	else:
		return render(request,'admin/login.html')



def view_product(request):
	if request.session.has_key("myid"):
		pro=product_tb.objects.all()
		if pro.exists():
			return render(request,"admin/view_product.html",{'pro':pro, 'db':db})
		else:
			return render(request,'admin/view_product.html',{'db':db})
	else:
		return render(request,'admin/login.html')



def delete_product(request):
	if request.session.has_key("myid"):
		pid=request.GET['id']
		product_tb.objects.all().filter(id=pid).delete()
		pro=product_tb.objects.all()
		return render(request,'admin/view_product.html',{'pro':pro, 'db':db})
	else:
		return render(request,'admin/login.html')


def update_product(request):
	if request.session.has_key("myid"):
		print('inside getData')
		if request.method=='GET':
			id2=request.GET['id']
			p=product_tb.objects.all().filter(id=id2)
			print(p)
		if p.exists():
			print('get record')
			return render(request,'admin/update_product.html',{'p':p,'category':categoryquery, 'db':db})
		else:
			print("failed")
			return render(request,"admin/update_product.html",{'db':db})
	else:
		return render(request,'admin/login.html')		



def update_view_product(request):
	if request.session.has_key("myid"):
		if request.method=="POST":
			print("----------update inside post-----------")
		
			category=request.POST['cid']
			print(category,'////////////')
			c=category_tb.objects.get(id=category)	
			print(c,'***************')
			up=request.GET['id']
			name=request.POST['name']
			price1=request.POST['price1']
			price2=request.POST['price2']
			price3=request.POST['price3']
			price4=request.POST['price4']
			price5=request.POST['price5']

		
		
		
			imgup=request.POST['imgupdate1']
			if imgup=='Yes':
				image=request.FILES['image']
				oldrec=product_tb.objects.all().filter(id=up)
				updrec=product_tb.objects.get(id=up)
				for x in oldrec:
					imgurl=x.image.url
					pathtoimage=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+imgurl
					if os.path.exists(pathtoimage):
						os.remove(pathtoimage)
						print('Successfully deleted')
				updrec.image=image
				updrec.save()

			imgup=request.POST['imgupdate2']
			if imgup=='Yes':
				image1=request.FILES['image1']
				oldrec=product_tb.objects.all().filter(id=up)
				updrec=product_tb.objects.get(id=up)
				for x in oldrec:
					imgurl=x.image1.url
					pathtoimage=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+imgurl
					if os.path.exists(pathtoimage):
						os.remove(pathtoimage)
						print('Successfully deleted')
				updrec.image1=image1
				updrec.save()

			imgup=request.POST['imgupdate3']
			if imgup=='Yes':
				image2=request.FILES['image2']
				oldrec=product_tb.objects.all().filter(id=up)
				updrec=product_tb.objects.get(id=up)
				for x in oldrec:
					imgurl=x.image2.url
					pathtoimage=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+imgurl
					if os.path.exists(pathtoimage):
						os.remove(pathtoimage)
						print('Successfully deleted')
				updrec.image2=image2
				updrec.save()

		
		
			product_tb.objects.filter(id=up).update(cid=c,name=name,price1=price1,price2=price2,price3=price3,price4=price4,price5=price5)
			up=product_tb.objects.all().filter()
			query=category_tb.objects.all()
			print("-----------------render page--------------")
			return render(request,'admin/view_product.html',{'pro':up,'query':query, 'db':db})
		elif request.method=="GET":
			print("-----------------get update------------")
			id1=request.GET['id']
			up=product_tb.objects.all().filter(id=up)
			query=category_tb.objects.all()
			print("-----------------render page--------------")
			return render(request,'admin/view_product.html',{'pro':up,'query':query, 'db':db})
	else:
		return render(request,'admin/login.html')

###################################################################################################################
	
def view_order(request):
	if request.session.has_key("myid"):
		odr=order_tb.objects.all()
		if odr.exists():
			return render(request,"admin/view_order.html",{'odr':odr,'db':db})
		else:
			return render(request,'admin/view_order.html',{'db':db})
	else:
		return render(request,'admin/login.html')


def view_bill(request):
	if request.session.has_key("myid"):
		ii=request.GET['id']
		bil=bill_tb.objects.all().filter(oid=ii)
		if bil.exists():
			return render(request,"admin/view_bill.html",{'bil':bil,'db':db})
		else:
			return render(request,'admin/view_bill.html',{'db':db})		
	else:
		return render(request,'admin/login.html')
					


##################################################################################################################
###################################################### Front #####################################################
##################################################################################################################

def touch(request):
	if request.method=="POST":
		name=request.POST['name']
		email=request.POST['email']
		check=touch_tb.objects.all().filter(name=name,email=email)

		if check:
			return render(request,'front/index.html',{'category':categoryquery})
		else:
			sv=touch_tb(name=name,email=email)
			sv.save()
			
			return render(request,'front/index.html',{'category':categoryquery})
	else:
		print('****************')
		return render(request,'front/index.html')
			

def productlist(request):
    categoryid = request.GET.get('id')
    products = product_tb.objects.all().filter(cid=categoryid)
    total_items = products.count()
    categorysingle = category_tb.objects.all().filter(id=categoryid)

    # Pagination
    page = request.GET.get('page', 1)  # Get the current page number
    paginator = Paginator(products, 8)  # Show 8 products per page

    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        p = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page.
        p = paginator.page(paginator.num_pages)

    if p:
        return render(request, 'front/productlist.html', {
            'query': p,
            'single': categorysingle,
            'categoryid': categoryid,
			'category':categoryquery,
            'total_items': total_items
        })
    else:
        return render(request, 'front/index.html')


#################################################################################################################################

def billing(request):
	print("========================")
	if request.method=='POST':
		print("+++++++++++++++++++++++++++++")

		# ii=request.POST['oid']
		# print(ii,'////////////')
		

		first=request.POST['first']
		last=request.POST['last']
		address=request.POST['address']
		city=request.POST['city']
		pin=request.POST['pin']
		email=request.POST['email']
		phone=request.POST['phone']
		amount=request.POST['amount']
		# o=order_tb.objects.get(id=ii)	
		# print(o,'***************')
		ii=order_tb.objects.all().latest('id')


	
		check=bill_tb.objects.all().filter(oid=ii,first=first,last=last,address=address,city=city,pin=pin,email=email,phone=phone,amount=amount)
		if check:
			return render(request,'front/index.html',{'category':categoryquery})
		else:
			sv=bill_tb(oid=ii,first=first,last=last,address=address,city=city,pin=pin,email=email,phone=phone,amount=amount)
			sv.save()
			

			x = ''.join(random.choices(first + string.digits, k=8))
			y = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
			My_subject = 'Welcome to The Cake Box'
			# message = f'Hi {first} {last} , Thank you for ordering in The Cake Box .  Address = {address} , {city} Phone = {phone} . Your order will be delivered soon . For more Info contact us https://Wa.me/+919633045864.'
			email_from = settings.EMAIL_HOST_USER  
			recipient_list = [email, ] 

			sid=request.GET.get('id')
			p=product_tb.objects.all().filter(id=sid)
			cid=request.GET.get('id')
			o=order_tb.objects.all().filter(id=cid)
			iii=order_tb.objects.all().latest('id')
			c=bill_tb.objects.all().filter(oid=ii)
			html_message = render_to_string("front/email.html",{'c':c,'query':p,'o':o,'iii':iii})
			plain_message = strip_tags(html_message)

			message = EmailMultiAlternatives(
				subject=My_subject,
				body=plain_message,
				from_email=email_from,
				to=recipient_list
			)

			message.attach_alternative(html_message,"text/html")
			message.send()

			# email_from = settings.EMAIL_HOST_USER  
			# recipient_list = [email, ] 
			# send_mail( subject, message,  email_from, recipient_list )

			
			
			return render(request,'front/thanks.html',{'category':categoryquery})
			# return render(request,'front/email.html',{'category':categoryquery,'c':c,'query':p,'o':o,'iii':iii})
	else:
		print('****************')
		return render(request,'front/index.html',{'category':categoryquery})


#######################################################################################################################################################3

def single_order(request):
	if request.method=="POST":
		
		
		
		weight=request.POST['weight']
		print(weight,'/////////////////////////')
		message=request.POST['message']
		print(message,'/////////////////////////')
		quantity=request.POST['quantity']
		print(quantity,'/////////////////////////')
		name=request.POST['pid']
		print(name,'////////////')
		n=product_tb.objects.get(id=name)	
		print(n,'***************')
		price=request.POST['pp']
		print(price,'/////////////////////////')
		total=request.POST['total']

		print(quantity,'uuuuuuuuuuuu')
		print(price,'mmmmmmmmmmmmmmmmmmm')
		
		total=int(quantity)*int(price)
		
		
		add=order_tb(pid=n,weight=weight,message=message,price=price,quantity=quantity,total=total)
		add.save()
		ii=order_tb.objects.all().latest('id')
		print(ii,"**************************")
		# iii=order_tb.objects.get(id=ii)
		# print(iii)
		query1=product_tb.objects.all()
		sid=request.GET.get('id')
		p=product_tb.objects.all().filter(id=sid)
		o=order_tb.objects.all()
		

		return render(request,'front/checkout.html',{'query1':query1,'total':total,'category':categoryquery,'ii':ii,'q':p,'oi':o})
		
	else:
		query1=product_tb.objects.all()
		return render(request,'front/order.html',{'query1':query1})		


##############################################################################################################################

# def view_customer_order(request):
	
# 	ii=request.GET['id']
# 	bil=bill_tb.objects.all().filter(id=ii)
# 	for x in bil:
# 		oid=x.oid
# 		query=order_tb.objects.all().filter(id=oid)
# 	if bil.exists():
# 		return render(request,"front/view_customer_order.html",{'bil':bil})
# 	else:
# 		return render(request,'front/view_customer_order.html')	









############### AJAX ############################### 
def view(request):                   
	print("hello")
	a=request.GET.get('p')
	b=product_tb.objects.all().filter(id=a)
	for x in b:
		price1=x.price1

	dat={"price1":price1}
	print(dat)
	return JsonResponse(dat)

def view1(request):                   
	print("hello")
	a=request.GET.get('p')
	b=product_tb.objects.all().filter(id=a)
	for x in b:
		price2=x.price2
		
	dat={"price2":price2}
	print(dat)
	return JsonResponse(dat)

def view2(request):                   
	print("hello")
	a=request.GET.get('p')
	b=product_tb.objects.all().filter(id=a)
	for x in b:
		price3=x.price3
		
	dat={"price3":price3}
	print(dat)
	return JsonResponse(dat)

def view3(request):                   
	print("hello")
	a=request.GET.get('p')
	b=product_tb.objects.all().filter(id=a)
	for x in b:
		price4=x.price4
		
	dat={"price4":price4}
	print(dat)
	return JsonResponse(dat)

def view4(request):                   
	print("hello")
	a=request.GET.get('p')
	b=product_tb.objects.all().filter(id=a)
	for x in b:
		price5=x.price5
		
	dat={"price5":price5}
	print(dat)
	return JsonResponse(dat)

						

##########################################################


####################################################### END ###############################################################################																
######################################################################################################################################																
