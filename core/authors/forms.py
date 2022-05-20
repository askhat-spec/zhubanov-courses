from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.core.validators import FileExtensionValidator

from courses.models import Course, Lecture


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', required=True)
    password1 = forms.CharField(
        label=("Құпиясөз"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label=("Құпиясөз құптамасы"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=("Құпиясөздер бірдей болуы міндетті!"),
    )

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CourseCreateForm(forms.ModelForm):
    image = forms.ImageField(label='Курс суреті', required=False)

    class Meta:
        model = Course
        fields = ['title', 'code', 'degree', 'description', 'department', 'syllabus', 'readings', 'image']
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class LectureCreateForm(forms.ModelForm):
    video = forms.FileField(label='Лекция видеосы', validators=[FileExtensionValidator(allowed_extensions=['mp4'])], required=False)
    
    class Meta:
        model = Lecture
        fields = ['title', 'description', 'transcript', 'video']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'