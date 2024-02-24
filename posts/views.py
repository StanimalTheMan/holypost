from django.shortcuts import render, redirect
from .forms import PostForm
import boto3
from django.conf import settings

def handle_photo_submission(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            image_data = request.FILES['image'].read()
            moderation_status = perform_moderation(image_data)
            if moderation_status == 'approved':
                post = form.save(commit=False)
                post.moderated = True
                post.save()
                return redirect('submission_success')
            else:
                return render(request, 'error.html', {'message': 'Inappropriate content detected'})
    else:
        form = PostForm()
    return render(request, 'posts/photo-submission.html', {'form': form})

def perform_moderation(image_data):
    try:
        client = boto3.client('rekognition', region_name=settings.AWS_REGION)
        moderation_response = client.detect_moderation_labels(Image={'Bytes': image_data})
        moderation_labels = moderation_response.get('ModerationLabels', [])
        if moderation_labels:
            print("MODERATION  lABELS", moderation_labels)
            return 'rejected'
        else:
            return 'approved'
    except Exception as e:
        print("Error during moderation:", e)
        return 'error'

def submission_success(request):
    return render(request, 'posts/photo-submission_success.html')