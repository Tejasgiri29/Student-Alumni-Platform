from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Student, Alumni, Faculty, Skill, Interest

class StudentRegistrationForm(UserCreationForm):
    # User model fields
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    profile_picture = forms.ImageField()
    phone_number = forms.CharField(max_length=15)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])

    # Student model fields
    student_id = forms.CharField(max_length=20)
    current_year = forms.ChoiceField(choices=Student._meta.get_field('current_year').choices)
    branch = forms.CharField(max_length=100)
    expected_graduation_year = forms.IntegerField()
    cgpa = forms.DecimalField(max_digits=4, decimal_places=2)
    interested_areas = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        help_text="Select one or more areas of interest"
    )
    linkedin_profile = forms.URLField(required=False)
    github_profile = forms.URLField(required=False)
    resume_drive_link = forms.URLField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 
                 'profile_picture', 'phone_number', 'date_of_birth', 'gender', 'student_id', 
                 'current_year', 'branch', 'expected_graduation_year', 'cgpa', 'interested_areas', 
                 'linkedin_profile', 'github_profile', 'resume_drive_link']


class AlumniRegistrationForm(UserCreationForm):
    # User model fields
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    profile_picture = forms.ImageField()
    phone_number = forms.CharField(max_length=15)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])

    # Alumni model fields
    university_id = forms.CharField(max_length=20)
    passing_year = forms.IntegerField()
    branch = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True,
        help_text="Select your technical skills"
    )
    employment_status = forms.ChoiceField(choices=Alumni._meta.get_field('employment_status').choices)
    company = forms.CharField(max_length=100, required=False)
    job_title = forms.CharField(max_length=100, required=False)
    years_of_experience = forms.IntegerField(required=False)
    business_name = forms.CharField(max_length=100, required=False)
    field_of_work = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        help_text="Select your fields of work/expertise (optional)"
    )
    portfolio_url = forms.URLField(required=False)
    business_website = forms.URLField(required=False)
    description_of_activity = forms.CharField(widget=forms.Textarea, required=False)
    linkedin_profile = forms.URLField(required=False)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email', 
            'password1', 'password2', 'profile_picture', 
            'phone_number', 'date_of_birth', 'gender',
            'university_id', 'passing_year', 'branch', 'city', 'state',
            'skills', 'employment_status', 'company', 'job_title',
            'years_of_experience', 'business_name', 'field_of_work',
            'portfolio_url', 'business_website', 'description_of_activity',
            'linkedin_profile'
        ]


class FacultyRegistrationForm(UserCreationForm):
    # User model fields
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    profile_picture = forms.ImageField()
    phone_number = forms.CharField(max_length=15)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])

    # Faculty model fields
    faculty_id = forms.CharField(max_length=20)
    department = forms.CharField(max_length=100)
    designation = forms.CharField(max_length=100)
    years_of_experience = forms.IntegerField()
    subjects_taught = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), widget=forms.CheckboxSelectMultiple)
    research_interests = forms.CharField(widget=forms.Textarea, required=False)
    publications = forms.CharField(widget=forms.Textarea, required=False)
    linkedin_profile = forms.URLField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 
                 'profile_picture', 'phone_number', 'date_of_birth', 'gender', 'faculty_id', 
                 'department', 'designation', 'years_of_experience', 'subjects_taught', 
                 'research_interests', 'publications', 'linkedin_profile']
