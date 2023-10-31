import os
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .utilities.ocr_reader import ocr_process, create_docx
from .utilities.template_creator import template_composer


def index(request):
    return render(request, 'index.html')


def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            selected_language = form.cleaned_data['language']

            temp_dir = os.path.join('media', 'temp')
            os.makedirs(temp_dir, exist_ok=True)

            # Save the uploaded file temporarily and get irs path
            file_path = os.path.join('media', 'temp', uploaded_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Process the uploaded file using OCR
            ocr_output = ocr_process(file_path, selected_language)

            # Ensure the OCR outputs directory exists
            ocr_output_dir = os.path.join('media', 'ocr_outputs')
            os.makedirs(ocr_output_dir, exist_ok=True)

            # Create a DOCX file from OCR output
            ocr_output_path = os.path.join('media', 'ocr_outputs', 'ocr_output.docx')
            create_docx(ocr_output, ocr_output_path)

            # Combine the OCR output with a template
            doc_template_path = os.path.join(settings.BASE_DIR, 'static', 'doc_templates', 'template.docx')
            output_dir = os.path.join(settings.MEDIA_ROOT, 'ocr_outputs')
            combined_path = template_composer(doc_template_path, ocr_output, output_dir)

            context = {
                'download_link': combined_path
            }

            return render(request, 'success.html', context)

    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


