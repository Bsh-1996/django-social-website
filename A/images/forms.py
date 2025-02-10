import requests
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django import forms
from . models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        widgets = {
            'url': forms.HiddenInput,
        }
    
    def clean_url(self):
        url = self.cleaned_data["url"]
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extensions.')
        return url
    


    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False)  # Step 1: Create the instance but don't save it yet
    
        image_url = self.cleaned_data['url']  # Step 2: Retrieve the URL from the form data
        name = slugify(image.title)  # Step 3: Convert the title into a slug (clean, URL-friendly string)
    
        extension = image_url.rsplit('.', 1)[1].lower()  # Step 3: Extract the file extension (e.g., jpg, png)
        image_name = f'{name}.{extension}'  # Step 3: Create a filename using the slug and extension
    
        # Step 4: Download the image from the URL
        response = requests.get(image_url)

        # Step 5: Save the image content to the model's image field
        image.image.save(
            image_name,  # Name of the image file
            ContentFile(response.content),  # Content of the image (downloaded from the URL)
            save=False  # Don't save the model yet
        )

        # Step 6: If commit=True, save the image to the database
        if commit:
            image.save()

        return image

    




