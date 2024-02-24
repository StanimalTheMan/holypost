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

# def upload_image_to_s3(image_data):
#     try:
#         s3_client = boto3.client('s3', region_name=settings.AWS_REGION)
#         s3_bucket_name = settings.AWS_STORAGE_BUCKET_NAME
#         s3_key = 'images/' + str(uuid.uuid4())
#         s3_client.put_object(Bucket=s3_bucket_name, Key=s3_key, Body=image_data)
#         return s3_key
#     except Exception as e:
#         print("Error uploading image to S3:", e)
#         return None

# def perform_moderation(s3_key):
#     try:
#         client = boto3.client('rekognition', region_name=settings.AWS_REGION)
#         moderation_response = client.detect_moderation_labels(Image={'S3Object': {'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Name': s3_key}})
#         moderation_labels = moderation_response.get('ModerationLabels', [])
#         if moderation_labels:
#             print("MODERATION  lABELS", moderation_labels)
#             return 'rejected'
#         else:
#             return 'approved'
#     except Exception as e:
#         print("Error during moderation:", e)
#         return 'error'

def submission_success(request):
    return render(request, 'posts/photo-submission_success.html')