import os
from django.http import FileResponse
from django.shortcuts import render
from django.urls import reverse

from final_project.settings import BASE_DIR
from .forms import UploadFileForm
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


