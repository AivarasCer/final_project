from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .utilities.ocr_reader import ocr_process


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

            result = ocr_process(file_path, selected_language)

            return redirect('success_url')

    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})




