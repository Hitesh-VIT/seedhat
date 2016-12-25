from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render,redirect,render_to_response
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from datetime import  datetime,date

from django.http import HttpResponse



def register_user(request):
    if request.method== 'POST' :
        register_form=ProfileForms(request.POST)
        if register_form.is_valid():
            try:
                key_value=Keys.objects.get(key=register_form.cleaned_data['key'])
                key_value.delete()
                register_form.save()
                return HttpResponseRedirect(reverse('homepage'))
            except ObjectDoesNotExist:
                messages.error(request, ('Key is invlaid'))

    else:
        register_form = ProfileForms(request.POST)
    return render(request, 'restro/register.html', {
        'form': register_form
    })

def Restaurant_login_view(request):

    if request.method == 'POST' :
        login_form = LogForm(request.POST)



        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
            else:
                messages.error(request, ('Invalid Crediantials'))
    else:
        login_form = LogForm(request.POST)
    return render(request, 'restro/login.html',{'login_form':login_form})


def user_homepage(request):

    if request.method == 'POST':
        user_key_info=User_infoForm(request.POST)
        if user_key_info.is_valid():
            key=user_key_info.cleaned_data['user_key']
            try:
                profile=Profile.objects.get(pk=key)
                return HttpResponseRedirect(reverse('user info', args=(key,)))
            except :
                return HttpResponseRedirect(reverse('user info', args=(key,)))


    else:
        user_key = User_infoForm()
    return render(request, 'restro/home.html', {'key': user_key})


def user_info(request,pk):
    l=[]
    v=Visits.objects.filter(user_id=pk).values('visit_count','restaurant')
    number_of_restaurants_visited=v.count()
    Total_restuarants=Restaurants.objects.all().count()
    if number_of_restaurants_visited < Total_restuarants:
        list_of_restuarant_visited=[]
        list_of_total=[]
        for i in v:
            list_of_restuarant_visited.append(i['restaurant'])
        for j in Restaurants.objects.all():
            list_of_total.append(j.restraunt_id)
        for i in list_of_total :
            if i not in list_of_restuarant_visited:
                response_dict={}
                response_dict['restarant_id']=i
                response_dict['discount_rate']=Discounts.objects.filter(restarant=i,visit_count=1).first().discount_rate
                l.append(response_dict)



    for i in v:
        d=Discounts.objects.filter(restarant=i['restaurant'],visit_count=i['visit_count']+1).values()
        response_view_dict = {}
        try:
            response_view_dict['restarant_id']=d[0]['restarant_id']
            response_view_dict['discount_rate']=d[0]['discount_rate']
            l.append(response_view_dict)
        except:
            pass

    special_discount_update=Special_discount.objects.filter(date=date.today())
    if special_discount_update is None:
        response_dict={"view":l,"key":pk,"special_true":"False"}
    else:
        l2=[]
        for i in special_discount_update:
            special_dict={}
            special_dict['restarant_id']=i.restaurant_id
            special_dict['discount_rate']=i.discount_rate
            l2.append(special_dict)
        response_dict={"view":l,"key":pk,"special_true":"True","special":l2}
    return render(request, 'restro/user.html', response_dict)



def user_redeem(request,pk,rest_id):

    if request.method=='POST':
        user_form = User_redeemForm(request.POST)
        try:
            user_key = Profile.objects.get(pk=pk)
        except ObjectDoesNotExist:
            messages.error(request, ("User doesn't exist"))
            return render(request, 'restro/user_redeem.html', {'form':user_form })


        if user_form.is_valid():
            restuarant_id=rest_id
            amount=user_form.cleaned_data['amount']
            pin=user_form.cleaned_data['pin']
            restuarantobj=Restaurants.objects.get(pk=restuarant_id)
            flag=1
            if pin==restuarantobj.pin:
                try:
                    visit_count=Visits.objects.get(restaurant=restuarantobj,user_id=user_key)

                    if visit_count.last_visit==date.today():

                        messages.error(request, ("You have reached the limit of usage of card Try again tomorrow"))
                        return render(request, 'restro/user_redeem.html', {'form': user_form})

                    else:
                        visit_count.visit_count = visit_count.visit_count + 1
                        visit_count.last_visit = date.today()
                        visit_count.save()

                except ObjectDoesNotExist:
                    visit_count=Visits.objects.create(restaurant=restuarantobj,user_id=user_key,visit_count=1,last_visit=date.today())

                    discount_obj = Discounts.objects.get(visit_count=visit_count.visit_count, restarant=restuarantobj)
                    discount = discount_obj.discount_rate

                try:
                    discount_obj=Discounts.objects.get(visit_count=visit_count.visit_count,restarant=restuarantobj)
                    discount=discount_obj.discount_rate
                except ObjectDoesNotExist:
                    discount=0.0
                try:
                    special_discount=Special_discount.objects.filter(restaurant=restuarantobj,date=date.today()).first()
                    if special_discount is not None:
                        discount=special_discount.discount_rate
                        messages.error(request, ("Special discount available"))
                except:
                    pass

                if flag ==0:
                    discount=0.0

                new_amount=float(amount)-float(amount)*(float(discount)/100.00)

                messages.error(request, ('New amount is',new_amount))
            else :
                messages.error(request, ('Pin is incorrect'))
        else :
            messages.error(request, ('Enter Correct Data'))
    else:
        user_form=User_redeemForm(request.POST)
    return render(request, 'restro/user_redeem.html',{'form':user_form})







def restaurant_redeem(request):
    user=request.user
    restaurant=Restaurants.objects.get(restraunt_owner=user)

    if request.method =='POST':
        restaurant_form=Restarant_redeemForm(request.POST)
        if restaurant_form.is_valid():
            user_key=restaurant_form.cleaned_data['user_key']
            try:
                user_key=Profile.objects.get(pk=user_key)
            except ObjectDoesNotExist:
                messages.error(request, ("User doesn't exist"))
                return render(request, 'restro/restro_redeem.html', {'form': restaurant_form})


            amount=restaurant_form.cleaned_data['amount']
            try:
                visit_count = Visits.objects.get(restaurant=restaurant, user_id=user_key)

                if visit_count.last_visit == date.today():
                    messages.error(request, ("You have reached the limit of usage of card Try again tomorrow"))
                    return render(request, 'restro/restro_redeem.html', {'form': restaurant_form})

                else:
                    visit_count.visit_count = visit_count.visit_count + 1
                    visit_count.last_visit = date.today()
                    visit_count.save()

            except ObjectDoesNotExist:
                visit_count = Visits.objects.create(restaurant=restaurant, user_id=user_key, visit_count=1,
                                                    last_visit=date.today())

                discount_obj = Discounts.objects.get(visit_count=visit_count.visit_count, restarant=restaurant)
                discount = discount_obj.discount_rate

            try:
                discount_obj = Discounts.objects.get(visit_count=visit_count.visit_count, restarant=restaurant)
                discount = discount_obj.discount_rate
            except ObjectDoesNotExist:
                messages.error(request, ("No more discounts avaliable"))
                return render(request, 'restro/restro_redeem.html', {'form': restaurant_form})
            try:
                special_discount=Special_discount.objects.filter(restaurant=restaurant,date=date.today()).first()
                if special_discount is not None:
                    discount=special_discount.discount_rate
                    messages.error(request, ("Special discount available"))


            except:
                pass



            new_amount = float(amount) - float(amount) * (float(discount) / 100.00)


            messages.error(request, ('New amount is', new_amount))
        else:
            messages.error(request, ('Enter Correct Data'))
    else:
        restaurant_form = Restarant_redeemForm(request.POST)
    return render(request, 'restro/restro_redeem.html', {'form':restaurant_form})







def restaurant_view(request):  #view add discount and specia discount
    user = request.user
    restaurant = Restaurants.objects.get(restraunt_owner=user)
    if request.method == 'POST':
        update_form = Restaurant_discount_Form(request.POST)
        update_discount_form =Restaurant_special_discount_Form(request.POST)
        if update_form.is_valid():
            visit_count = update_form.cleaned_data['visits']
            discount_rate = update_form.cleaned_data['discounts']
            obj, created = Discounts.objects.update_or_create(
                visit_count=visit_count, discount_rate=discount_rate,
                restarant=restaurant
            )

        if update_discount_form.is_valid():
                date = update_discount_form.cleaned_data['date']
                discount_rate = update_discount_form.cleaned_data['discount_rate']
                obj, created = Special_discount.objects.update_or_create(
                    date=date, discount_rate=discount_rate,
                    restaurant=restaurant
                )
                obj.save()



    else:
        update_form=Restaurant_discount_Form(request.POST)
        update_discount_form=Restaurant_special_discount_Form(request.POST)
    return render(request,'restro/login-2.html',{'update_discount_form':update_discount_form,'update_form':update_form})















