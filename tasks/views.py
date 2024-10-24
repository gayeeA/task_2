from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate
from django.shortcuts import HttpResponseRedirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.
# def home(request):
#     return render(request, 'home_page.html')
# def login(request):
#     return render(request, 'login.html')
# def signup(request):
#     return render(request, 'signup.html')

# Create your views here.
def home(request):
    # request is used to navgate the command to our html page
    # for navigation we need to use a keyword called as "render"
    return render(request,'home_page.html')
 
def login(request):
    if(request.user.is_authenticated):
        return redirect('/')
    if(request.method == "POST"):
        un = request.POST['username']
        pw = request.POST['password']
        user = authenticate(request,username=un,password=pw)
        #authenticate() used to check for the valid statements given or not by linking with database automatically.
        #if the values are matched, then it will return the username
        #if the values are not matched, then it will return the 'None'
        if(user is not None):
            return redirect('/profile')
        else:
            msg = 'Error in login. Invalid username/password'
            form = AuthenticationForm()
            # used to create a basic login page with username and password conditions
            return render(request,'login.html',{'form':form,'msg':msg})
    else:
        form = AuthenticationForm()
        # used to create a basic login page with username and password conditions
        return render(request,'login.html',{'form':form})
 
def register(request):
    if(request.user.is_authenticated):
        return redirect('/')
    if(request.method == "POST"):
        form = UserCreationForm(request.POST)
        if(form.is_valid()):
            form.save()
            un = form.cleaned_data.get('username')
            pw = form.cleaned_data.get('password1')
            user = authenticate(username=un,password=pw)
            return redirect('/login')
        else:
            return render(request,'signup.html',{'form':form})
    else:
        form = UserCreationForm()
        return render(request,'signup.html', {'form':form})
 

def profile(request):
    if request.method == 'POST' and request.FILES:
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')

        if image1 and image2:
            # Use FileSystemStorage to save the uploaded images
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename1 = fs.save(image1.name, image1)
            filename2 = fs.save(image2.name, image2)
            uploaded_file_url1 = fs.url(filename1)
            uploaded_file_url2 = fs.url(filename2)

            return render(request, 'profile.html', {
                'uploaded_file_url1': uploaded_file_url1,
                'uploaded_file_url2': uploaded_file_url2
            })

    return render(request, 'profile.html')
