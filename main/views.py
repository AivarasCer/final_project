import os
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .utilities.ocr_reader import ocr_process
from .utilities.template_creator import template_composer


def index(request):
    return render(request, 'index.html')


def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            selected_language = form.cleaned_data['language']

            with open(uploaded_file, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            file_path = destination.name

            ocr_output = ocr_process(file_path, selected_language)

            doc_template_path = os.path.join(settings.STATIC_URL, 'doc_templates', 'template.docx')
            output_dir = os.path.join(settings.MEDIA_ROOT, 'ocr_outputs')
            combined_path = template_composer(doc_template_path, ocr_output, output_dir)

            context = {
                'download_link': combined_path
            }

            return render(request, 'success.html', context)

    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})




