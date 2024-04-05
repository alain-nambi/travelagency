'''
Created on 8 Sep 2022

'''
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from AmadeusDecoder.models.user.Users import User
from AmadeusDecoder.models.user.Users import Role
from AmadeusDecoder.forms import UserForm
from django.db.models import Q

@login_required(login_url='index')
def users(request):
    context = {}
    context['users'] = User.objects.all()
    context['roles'] = Role.objects.all()
    
    object_list = context['users']
    row_num = request.GET.get('paginate_by', 25) or 25
    page_num = request.GET.get('page', 1)
    paginator = Paginator(object_list, row_num)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger: 
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context['page_obj'] = page_obj
    context['row_num'] = row_num
    return render(request,'manage_users.html', context)


@login_required(login_url='index')
def register(request):
    context = {}
    form = UserForm()

    if request.POST:
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
        context['form'] = form
        return redirect('users')
    else:
        context['form'] = form

    context['users'] = User.objects.all()
    
    return render(request,'add-user.html', context)

@login_required(login_url='index')
def user_details(request,user_id):
    context={}
    user = User.objects.get(pk=user_id)
    roles = Role.objects.all()

    context['user'] = user
    context['roles'] = roles
    return render(request,'user-details.html',context)

@login_required(login_url='index')
def archive_user(request):
    context = {}
    if request.method == 'POST':

        user_id = request.POST.get('user')

        connected_user_id = request.POST.get('connected_user')

        password = request.POST.get('password')

        connected_user = User.objects.get(pk= connected_user_id)

        # Checking the password
        connected_user_authenticated = authenticate(request, username=connected_user.email, password=password)
        
        # Change is_active to false
        if connected_user_authenticated is not None:
            user = User.objects.get(pk=user_id)

            if not user.is_active:
                context['message'] = "Utilisateur déjà archivé"
                context['status'] = 20
            
            else:
                user.is_active = False
                user.save()

                context['message'] = "Utilisateur archivée avec succès"
                context['status'] = 200
        else:
            context['message'] = "Mot de passe incorrect"
            context['status'] = 10

    return JsonResponse(context)

@login_required(login_url='index')
def reactive_user(request):
    context = {}
    if request.method == 'POST':

        user_id = request.POST.get('user')

        connected_user_id = request.POST.get('connected_user')

        password = request.POST.get('password')

        connected_user = User.objects.get(pk= connected_user_id)

        # Checking the password
        connected_user_authenticated = authenticate(request, username=connected_user.email, password=password)
        
        # Change is_active to false
        if connected_user_authenticated is not None:
            user = User.objects.get(pk=user_id)

            if user.is_active:
                context['message'] = "Utilisateur déjà activé"
                context['status'] = 20
            
            else:
                user.is_active = True
                user.save()

                context['message'] = "Utilisateur réactivé avec succès"
                context['status'] = 200
        else:
            context['message'] = "Mot de passe incorrect"
            context['status'] = 10

    return JsonResponse(context)

@login_required(login_url='index')
def update_password(request):
    context={}
    if request.method == 'POST':
        current_password = request.POST.get('currentPassword')
        new_password = request.POST.get('newPassword')
        user_id = request.POST.get('user_id')

        user = User.objects.get(pk=user_id)

        # Check the current password
        user_authenticated = authenticate(request,username=user.email, password=current_password)
        if user_authenticated is not None:
            # update password
            user.set_password(new_password)
            user.save()
            context['message'] = "Mot de passe modifié"
            context['status'] = 200

        else:
            context['message'] = "Mot de passe actuel incorrect"
            context['status'] = 10

    return JsonResponse(context)

login_required(login_url='index')
def update_info(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        first_name = request.POST.get('first_name')

        email = request.POST.get('email')

        role = request.POST.get('role')

        user_id = request.POST.get('user')

        connected_user_id = request.POST.get('connected_user')

        password = request.POST.get('password')


        # Check connected user
        connected_user = User.objects.get(pk=connected_user_id)
        connected_user_authenticated = authenticate(request, username=connected_user.email, password=password)

        if connected_user_authenticated is not None:
            # update info
            user = User.objects.get(pk=user_id)
            user.name = name
            user.first_name = first_name
            user.email = email
            user.role = Role.objects.get(pk=role)
            user.save()
            context['message'] = "Informations modifiées"
            context['status'] = 200

        else:
            context['message'] = "Mot de passe incorrect"
            context['status'] = 10

    return JsonResponse(context)

@login_required(login_url="index")
def user_research(request):
    context = {}
    
    if request.method == 'POST' and request.POST.get('user_research'):
        search_results = []
        
        user_research = request.POST.get('user_research')
        user_results = User.objects.all().filter(Q(name__icontains=user_research) | Q(first_name__icontains=user_research)| Q(email__icontains=user_research) | Q(username__icontains=user_research))
        
        if user_results.exists():
            for user in user_results :
                search_results.append(user)
        print(search_results)

        results = []
        for user in search_results:
            
            values = {}
            values['id'] = user.id
            values['name'] = user.name
            values['first_name'] = user.first_name
            values['username'] = user.username
            values['email'] = user.email
            values['role'] = user.role.name

           
            results.append(values)
        pnr_count = len(results)
        
        context = {'results' : results, 'pnr_count' :  pnr_count}
    return JsonResponse(context)
       
@login_required(login_url="index")
def user_filter(request):
    context = {}
    if request.method == 'POST' and request.POST.get('role_id'):
        search_results = []
        
        role_id = request.POST.get('role_id')
        user_results = User.objects.all().filter(role_id=role_id)
        if user_results.exists():
            for user in user_results :
                search_results.append(user)
        print(search_results)

        results = []
        for user in search_results:
            
            values = {}
            values['id'] = user.id
            values['name'] = user.name
            values['first_name'] = user.first_name
            values['username'] = user.username
            values['email'] = user.email
            values['role'] = user.role.name

           
            results.append(values)
        pnr_count = len(results)
        
        context = {'results' : results, 'pnr_count' :  pnr_count}
    return JsonResponse(context)
       