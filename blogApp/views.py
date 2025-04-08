from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, files, CustomUser
from blogApp.forms import PostForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



# Create your views here.
def homeview(request):
    post = Post.objects.all()
    paginator = Paginator(post, 3)
    page_number = request.GET.get('page')
    try:
        post = paginator.page(page_number)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)
    return render(request,'blogApp/index.html',{'post':post})
    
def register_view(request):
    form = CustomUserForm()
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Set password correctly
            user.save()
            return redirect('login')  # Redirect to login page after successful registration
    return render(request, 'blogApp/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/home')  # Redirect to home page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('/home')

@login_required
def my_blog_view(request):
    form=PostForm()
    if request.method == 'Post':
        form = PostForm(request.Post)
        if form.is_valid():
            form.save()

            return render(request,'bloApp/index.html')
    return render(request,'blogApp/myblog.html',{'form':form})

def blogdetail_view(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blogApp/blogdetail.html', {'post': [post]})

def file_detail_view(request, pk):
    file = get_object_or_404(files, pk=pk)
    return render(request, 'blogApp/file_detail.html', {'file': file})

#pagination using class based views
from django.views.generic import ListView
class PostListView(ListView):
    model = Post
    paginate_by = 1
#to send email
from django.core.mail import send_mail
from blogApp.forms import EmailSendForm

def mail_send_view(request,id):
    post = get_object_or_404(Post,id=id,status='published')
    sent = False
    if request.method == 'POST':
        form = EmailSendForm(request.Post)
        if form.is_valid():
            cd = form.cleaned_data
            print("read data and send mail" )
            sent = True
    form = EmailSendForm()
    return render(request,'blogApp/sharebymail.html',{'form':form})