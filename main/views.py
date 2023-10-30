from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .utilities.ocr_reader import ocr_process
from .utilities.template_creator import template_composer


def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            selected_language = form.cleaned_data['language']

            with open(uploaded_file, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            file_path = destination.name

            ocr_output_path = ocr_process(file_path, selected_language)

            template_path = ''
            combined_path = template_composer(template_path, ocr_output_path)

            context = {
                'download_link': combined_path
            }

            return redirect('success_url')

    # else:
    #     form = UploadFileForm()
    return render(request, 'index.html')




