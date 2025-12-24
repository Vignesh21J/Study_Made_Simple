from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['email'].label = "Email address"
        self.fields.pop('usable_password', None)
