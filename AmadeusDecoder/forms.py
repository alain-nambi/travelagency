
from django.forms import *
from django.contrib.auth.forms import *
from AmadeusDecoder.models.user.Users import User

class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'username', 'name', 'first_name', 'role', 'office', 'password1', 'password2', 'gds_id')
        widgets = {
            'email' : EmailInput(attrs={'class': 'form-control'}),
            'username' : TextInput(attrs={'class': 'form-control'}),
            'name' : TextInput(attrs={'class': 'form-control'}),
            'first_name' : TextInput(attrs={'class': 'form-control'}),
            'role' : Select(attrs={'class':'form-control', 'style':'width: 100%'}),
            'office' : Select(attrs={'class':'form-control', 'style':'width: 100%'}),
            'gds_id' : TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'required':True, 'class':'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'required':True, 'class':'form-control'})
        
        
class UploadFileForm(forms.Form):
    file_upload = forms.FileField()
    
    def clean_file_upload(self):
        file = self.cleaned_data.get('file_upload')
        if file:
            if not file.name.endswith('.csv'):
                raise forms.ValidationError("Only CSV files are allowed.")
        return file