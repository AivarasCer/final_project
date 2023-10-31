import os
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render, redirect
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

            # Ensure that temp directory exists
            temp_dir = os.path.join('main', 'media', 'temp')
            os.makedirs(temp_dir, exist_ok=True)

            # Save the uploaded file temporarily and get irs path
            file_path = os.path.join('main', 'media', 'temp', uploaded_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Process the uploaded file using OCR
            ocr_output = ocr_process(file_path, selected_language)

            # Ensure the OCR outputs directory exists
            ocr_output_dir = os.path.join('main', 'media', 'ocr_outputs')
            os.makedirs(ocr_output_dir, exist_ok=True)

            # Combine the OCR output with a template
            # doc_template_path = os.path.join(settings.BASE_DIR, 'static', 'doc_templates', 'template.docx')
            # output_dir = os.path.join(settings.MEDIA_ROOT, 'ocr_outputs')
            # combined_path = template_composer(doc_template_path, ocr_output, output_dir)

            download_url = reverse('download_file', args=[os.path.basename(ocr_output)])
            context = {
                'download_link': download_url
            }

            return render(request, 'success.html', context)

    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


# Download file
def download_file(request, filename):
    file_path = os.path.join(BASE_DIR, 'main', 'media', 'ocr_outputs', filename)
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)


