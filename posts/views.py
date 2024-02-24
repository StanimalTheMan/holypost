from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import PostForm
from .utils import perform_moderation, upload_image_to_s3

def handle_photo_submission(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            image_data = request.FILES['image'].read()

            s3_key = upload_image_to_s3(image_data)

            moderation_status = perform_moderation(s3_key)
            if moderation_status == 'approved':
                post = form.save(commit=False)
                post.image_s3_key = s3_key
                post.moderated = True
                post.save()
                return redirect(reverse('photo-submission-success'))
            else:
                return render(request, 'error.html', {'message': 'Inappropriate content detected'})
    else:
        form = PostForm()
    return render(request, 'posts/photo-submission.html', {'form': form})

def submission_success(request):
    return render(request, 'posts/photo-submission_success.html')