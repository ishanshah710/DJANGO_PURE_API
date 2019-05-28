from django import forms
from updates.models import Update as UpdateModel

class UpdateModelForm(forms.ModelForm):
    class Meta():
        model = UpdateModel
        fields = [
            'user',
            'content',
            'image'
        ]

    def clean(self , *args , **kwargs): # for validation that it must not null at least one of image or content
        data = self.cleaned_data
        content = data.get('content', None) # either content or None
        if content == "":
            content = None
        image = data.get('image' , None) # either image or None
        
        if content is None and image is None:
            raise forms.ValidationError("Atleast one of content or image is required!!")
        return super().clean(*args,**kwargs) # will return default
