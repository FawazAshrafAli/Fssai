from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Enquiry
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_POST

def user_login(request):
    if request.user.is_authenticated:
        return redirect(home)
    else:
        if request.method == "POST":
            username = request.POST["username"]    
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(home)
            else:
                messages.error(request, "Invalid username or password")
                return redirect(user_login)        
    return render(request, "sign-in.html")

def register(request):
    if request.method=="POST":
        name =request.POST.get("name")
        email =request.POST.get("email")
        phoneNumber=request.POST.get("phone")
        location =request.POST.get("location")
        registration =request.POST.get("fssaiindia")
        requirement =request.POST.get("message")

        # creating an enquiry object
        try:
            Enquiry.objects.create(
                name = name,
                email = email,
                phoneNumber = phoneNumber,
                location = location,
                registration = registration,
                requirement = requirement
            )
            messages.success(request, "Enquiry Successfully Submitted.")
            return redirect(register)
        except Exception as e:
            print(e)
            messages.error(request, "Error submitting form.")
            return redirect(register)
    return render(request, 'home.html')

def home(request):
    if request.user.is_authenticated:        
        registrations = Enquiry.objects.all().order_by('-submission_date', '-submission_time')

        # Number of items to display per page
        items_per_page = 50

        # Create a Paginator instance
        paginator = Paginator(registrations, items_per_page)

        # Get the current page number from the request's GET parameters
        page = request.GET.get('page')

        try:
            # Get the specified page
            registrations_page = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver the first page.
            registrations_page = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g., 9999), deliver the last page of results.
            registrations_page = paginator.page(paginator.num_pages)

        context = {
            "registrations": registrations,
            "registrations_page": registrations_page,            
            }
        return render(request, "enquiry_list.html", context)
    else:
        return redirect(user_login)

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect(user_login)
    else:
        return redirect(user_login)

def reset_password(request):        
    if request.user.is_authenticated:
        if request.method == "POST":
            user = request.user
            current_password = request.POST["current_password"]
            new_password = request.POST["new_password"]
            repeat_password = request.POST["repeat_password"]
            if new_password == repeat_password:
                try:
                    user = authenticate(username=user.username, password = current_password)
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Password resetted successfully.")
                    return redirect(user_login)
                except Exception as e:
                    print(e)
                    return redirect(reset_password)
            else:
                messages.error(request, "New passwords are not matching.")
                return redirect(reset_password)
        return render(request, 'reset_password.html')
    else:
        return redirect(user_login)
    
def delete(request, pk):
    if request.user.is_authenticated:
        try:
            enquiry_object = get_object_or_404(Enquiry, pk=pk)
            enquiry_object.delete()
            messages.success(request, "Enquiry deleted successfully.")
            return redirect(home)
        except Http404:
            messages.error(request, "No such Enquiry exists!")
            return redirect(home)
    
@require_POST
def opened(request, pk):
    try:
        enquiry = Enquiry.objects.get(pk=pk)
        enquiry.read = True
        enquiry.save()        
        return JsonResponse({'status': 'success'})
    except Enquiry.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Enquiry not found'})
    
@require_POST
def unread(request, pk):
    try:
        enquiry = Enquiry.objects.get(pk=pk)
        enquiry.read = False
        enquiry.save()                
        return JsonResponse({'unread_status': 'success'})
    except Enquiry.DoesNotExist:
        return JsonResponse({'unread_status': 'error', 'message': 'Enquiry not found'})