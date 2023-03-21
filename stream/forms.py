from django import  forms 
from .models import TestPost 



class PostForm(forms.ModelForm):
    
    class Meta:
        model = TestPost
        fields = ('title', 'content', 'image', 'visibility', 'date_published')
        visibilityChoices = [('Public', 'Public'), ('Private', 'Private')]

        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'visibility': forms.Select(choices=visibilityChoices, attrs={'class': 'form-control'}),          
        }
