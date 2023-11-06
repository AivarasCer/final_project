import os

from django.contrib import messages
from django.contrib.auth.models import User
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from final_project.settings import BASE_DIR
from .forms import UploadFileForm
from .models import MetaData
from .utilities.ocr_reader import ocr_process


def index(request):
    return render(request, 'index.html')


def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            selected_language = form.cleaned_data['language']

            # Save the uploaded file temporarily and get its path
            file_path = os.path.join('main', 'media', 'temp', uploaded_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Process the uploaded file using OCR
            ocr_output = ocr_process(file_path, selected_language)

            file_name = os.path.basename(file_path)
            file_type = os.path.splitext(file_name)[1][1:]

            metadata = MetaData(
                name=file_name,
                user=request.user,
                upload_at=datetime.now(),
                chars=len(ocr_output),
                file_type=file_type
            )
            metadata.save()

            download_url = reverse('download_file', args=[os.path.basename(ocr_output)])
            context = {
                'download_link': download_url
            }

            return render(request, 'success.html', context)

    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def download_file(request, filename):
    file_path = os.path.join(BASE_DIR, 'main', 'media', 'ocr_outputs', filename)
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)


def help_page(request):
    return render(request, 'help_page.html')


@csrf_protect
def register(request):
    if request.method == "POST":
        # Get values from registration form.
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        # Check if passwords match.
        if password == password2:
            # Check if username exists.
            if User.objects.filter(username=username).exists():
                messages.error(
                    request,
                    message=f"User {username} already exists!",
                )
                return redirect("register")
            else:
                # Check if there is already a user with this email.
                if User.objects.filter(email=email).exists():
                    messages.error(
                        request,
                        message=f"User with email {email} already exists!",
                    )
                    return redirect("register")
                else:
                    # If everything is ok, create new user.
                    User.objects.create_user(
                        username=username, email=email, password=password
                    )
                    messages.info(
                        request,
                        message=f"User {username} successfully registered!",
                    )
                    return redirect("login")
        else:
            messages.error(request, message="Passwords do not match!")
            return redirect("register")
    return render(request, template_name="registration/register.html")


@login_required
def account_info(request):
    user_metadata = MetaData.objects.filter(user=request.user)

    context = {'user_metadata': user_metadata}
    return render(request, 'account_info.html', context)


