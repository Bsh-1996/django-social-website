from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ImageCreateForm
from django.shortcuts import get_object_or_404
from . models import Image
from django.http import JsonResponse
from django.views.decorators.http import require_POST
# Create your views here.


@login_required
def image_create(request):
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            # assign current user to the item
            new_image.user = request.user
            new_image.save()
            messages.success(request, "image added successfully")
            # redirect to new created item detail view
            return redirect(new_image.get_absolute_url())
        else:
            messages.error(request, 'There was an error with your submission. Please correct the issues below.')
        
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)
    return render(request, 'images/image/create.html', {'section': 'images', 'form': form})



def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html', {'section': 'images', 'image': image})



@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')  # Get the image id from the POST data
    action = request.POST.get('action')  # Get the action ('like' or 'unlike') from the POST data
    
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)  # Retrieve the image object
            if action == 'like':
                image.users_like.add(request.user)  # Add user to 'users_like' field
            else:
                image.users_like.remove(request.user)  # Remove user from 'users_like' field
            return JsonResponse({'status': 'ok'})  # Send success response
        except Image.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Image not found'})  # Handle image not found
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})  # Handle missing parameters



