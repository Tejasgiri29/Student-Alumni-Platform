from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import datetime, date


from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(default=date(2000, 1, 1))
    gender = models.CharField(
        max_length=10, 
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        default='Other'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Update the groups field
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='tone_user_set',  # Custom related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    
    # Update the user_permissions field
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='tone_user_set',  # Custom related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username


# Auxiliary Models
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# Student Model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    current_year = models.CharField(
        max_length=20, 
        choices=[('First Year', 'First Year'), ('Second Year', 'Second Year'), ('Third Year', 'Third Year'), ('Fourth Year', 'Fourth Year')]
    )
    branch = models.CharField(max_length=100)
    expected_graduation_year = models.IntegerField()
    cgpa = models.DecimalField(
        max_digits=4, decimal_places=2, 
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )
    interested_areas = models.ManyToManyField(Interest, related_name='interested_students')
    linkedin_profile = models.URLField(blank=True, null=True)
    github_profile = models.URLField(blank=True, null=True)
    resume_drive_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Student: {self.user.username}"


# Alumni Model
class Alumni(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='alumni_profile')
    university_id = models.CharField(max_length=20, unique=True)
    passing_year = models.IntegerField()
    branch = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    skills = models.ManyToManyField(Skill, related_name='skilled_alumni')
    linkedin_profile = models.URLField(blank=True, null=True)
    employment_status = models.CharField(
        max_length=20, 
        choices=[('Employed', 'Employed'), ('Unemployed', 'Unemployed'), ('Self-Employed', 'Self-Employed'), ('Business Owner', 'Business Owner'), ('Other', 'Other')]
    )
    company = models.CharField(max_length=100, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    years_of_experience = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    business_name = models.CharField(max_length=100, blank=True, null=True)
    field_of_work = models.ManyToManyField(
        Skill, 
        related_name='business_fields', 
        blank=True,
        verbose_name='Fields of Work/Expertise'
    )
    portfolio_url = models.URLField(blank=True, null=True)
    business_website = models.URLField(blank=True, null=True)
    description_of_activity = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Alumni: {self.user.username}"


# Faculty Model
class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile')
    faculty_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    years_of_experience = models.IntegerField(validators=[MinValueValidator(0)])
    subjects_taught = models.ManyToManyField(Skill, related_name='teaching_faculty')
    research_interests = models.TextField(blank=True, null=True)
    publications = models.TextField(blank=True, null=True)
    linkedin_profile = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Faculty: {self.user.username}"
