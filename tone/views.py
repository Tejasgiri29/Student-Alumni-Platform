from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student, Alumni, Faculty, Skill, Interest
from django.contrib.auth import get_user_model, authenticate, login, logout
from .forms import StudentRegistrationForm, AlumniRegistrationForm, FacultyRegistrationForm
from django.db.models import Q
from .initial_data import create_initial_interests, create_initial_skills


def home(request):
    return render(request, 'index.html')


User = get_user_model()

def student_registration(request):
    # Create initial interests if they don't exist
    create_initial_interests()
    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            if 'profile_picture' in request.FILES:
                user.profile_picture = request.FILES['profile_picture']
            user.phone_number = form.cleaned_data['phone_number']
            user.date_of_birth = form.cleaned_data['date_of_birth']
            user.gender = form.cleaned_data['gender']
            user.is_active = True
            user.save()
            
            student_profile = Student.objects.create(
                user=user,
                student_id=form.cleaned_data['student_id'],
                current_year=form.cleaned_data['current_year'],
                branch=form.cleaned_data['branch'],
                expected_graduation_year=form.cleaned_data['expected_graduation_year'],
                cgpa=form.cleaned_data['cgpa'],
                linkedin_profile=form.cleaned_data['linkedin_profile'],
                github_profile=form.cleaned_data['github_profile'],
                resume_drive_link=form.cleaned_data['resume_drive_link']
            )
            if form.cleaned_data['interested_areas']:
                student_profile.interested_areas.set(form.cleaned_data['interested_areas'])
            
            # Log the user in after registration
            login(request, user)
            messages.success(request, 'Student registration successful!')
            return redirect('success')
    else:
        form = StudentRegistrationForm()
    return render(request, 'tone/student_registration.html', {'form': form})


def alumni_registration(request):
    # Create initial skills if they don't exist
    create_initial_skills()
    
    if request.method == 'POST':
        form = AlumniRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Save user first
            user = form.save(commit=False)
            if 'profile_picture' in request.FILES:
                user.profile_picture = request.FILES['profile_picture']
            user.phone_number = form.cleaned_data['phone_number']
            user.date_of_birth = form.cleaned_data['date_of_birth']
            user.gender = form.cleaned_data['gender']
            user.is_active = True
            user.save()  # Save the user to the database
            
            # Create alumni profile
            alumni_profile = Alumni.objects.create(
                user=user,
                university_id=form.cleaned_data['university_id'],
                passing_year=form.cleaned_data['passing_year'],
                branch=form.cleaned_data['branch'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                employment_status=form.cleaned_data['employment_status'],
                company=form.cleaned_data.get('company', ''),
                job_title=form.cleaned_data.get('job_title', ''),
                years_of_experience=form.cleaned_data.get('years_of_experience'),
                business_name=form.cleaned_data.get('business_name', ''),
                portfolio_url=form.cleaned_data.get('portfolio_url', ''),
                business_website=form.cleaned_data.get('business_website', ''),
                description_of_activity=form.cleaned_data.get('description_of_activity', ''),
                linkedin_profile=form.cleaned_data.get('linkedin_profile', '')
            )
            
            # Set many-to-many fields
            if form.cleaned_data.get('skills'):
                alumni_profile.skills.set(form.cleaned_data['skills'])
            if form.cleaned_data.get('field_of_work'):
                alumni_profile.field_of_work.set(form.cleaned_data['field_of_work'])
            
            # Log the user in
            login(request, user)
            messages.success(request, 'Alumni registration successful!')
            return redirect('success')
    else:
        form = AlumniRegistrationForm()
    
    return render(request, 'tone/alumni_registration.html', {'form': form})


def faculty_registration(request):
    if request.method == 'POST':
        form = FacultyRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            if 'profile_picture' in request.FILES:
                user.profile_picture = request.FILES['profile_picture']
            user.phone_number = form.cleaned_data['phone_number']
            user.date_of_birth = form.cleaned_data['date_of_birth']
            user.gender = form.cleaned_data['gender']
            user.is_active = True
            user.save()
            
            faculty_profile = Faculty.objects.create(
                user=user,
                faculty_id=form.cleaned_data['faculty_id'],
                department=form.cleaned_data['department'],
                designation=form.cleaned_data['designation'],
                years_of_experience=form.cleaned_data['years_of_experience'],
                research_interests=form.cleaned_data['research_interests'],
                publications=form.cleaned_data['publications'],
                linkedin_profile=form.cleaned_data['linkedin_profile']
            )
            faculty_profile.subjects_taught.set(form.cleaned_data['subjects_taught'])
            messages.success(request, 'Faculty registration successful!')
            return redirect('success')
    else:
        form = FacultyRegistrationForm()
    return render(request, 'tone/faculty_registration.html', {'form': form})


def success(request):
    return render(request, 'tone/success.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'tone/login.html')

@login_required
def dashboard(request):
    user_type = None
    if hasattr(request.user, 'student_profile'):
        user_type = 'student'
    elif hasattr(request.user, 'alumni_profile'):
        user_type = 'alumni'
    elif hasattr(request.user, 'faculty_profile'):
        user_type = 'faculty'

    # Handle search
    query = request.GET.get('query', '')
    filter_type = request.GET.get('filter_type', 'all')
    
    results = []
    if query:
        if filter_type == 'all' or filter_type == 'student':
            students = Student.objects.filter(
                Q(user__username__icontains=query) |
                Q(branch__icontains=query) |
                Q(expected_graduation_year__icontains=query) |
                Q(current_year__icontains=query)  # Assuming current year is relevant
            ).distinct()
            results.extend(('student', student) for student in students)
            
        if filter_type == 'all' or filter_type == 'alumni':
            alumni = Alumni.objects.filter(
                Q(user__username__icontains=query) |
                Q(branch__icontains=query) |
                Q(passing_year__icontains=query) |
                Q(city__icontains=query) |
                Q(state__icontains=query)  # Assuming state is still relevant
            ).distinct()
            results.extend(('alumni', alum) for alum in alumni)
            
        if filter_type == 'all' or filter_type == 'faculty':
            faculty = Faculty.objects.filter(
                Q(user__username__icontains=query) |
                Q(department__icontains=query) |
                Q(designation__icontains=query)
            ).distinct()
            results.extend(('faculty', fac) for fac in faculty)

    context = {
        'user_type': user_type,
        'results': results,
        'query': query,
        'filter_type': filter_type
    }
    return render(request, 'tone/dashboard.html', context)

@login_required
def edit_profile(request):
    if hasattr(request.user, 'student_profile'):
        profile = request.user.student_profile
        form_class = StudentRegistrationForm
    elif hasattr(request.user, 'alumni_profile'):
        profile = request.user.alumni_profile
        form_class = AlumniRegistrationForm
    elif hasattr(request.user, 'faculty_profile'):
        profile = request.user.faculty_profile
        form_class = FacultyRegistrationForm
    else:
        messages.error(request, 'No profile found for this user.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            if 'profile_picture' in request.FILES:
                user.profile_picture = request.FILES['profile_picture']
            user.save()

            # Update profile fields based on user type
            if hasattr(request.user, 'student_profile'):
                profile.student_id = form.cleaned_data['student_id']
                profile.current_year = form.cleaned_data['current_year']
                profile.branch = form.cleaned_data['branch']
                profile.expected_graduation_year = form.cleaned_data['expected_graduation_year']
                profile.cgpa = form.cleaned_data['cgpa']
                profile.linkedin_profile = form.cleaned_data['linkedin_profile']
                profile.github_profile = form.cleaned_data['github_profile']
                profile.resume_drive_link = form.cleaned_data['resume_drive_link']
                profile.interested_areas.set(form.cleaned_data['interested_areas'])
                profile.save()
            elif hasattr(request.user, 'alumni_profile'):
                profile.university_id = form.cleaned_data['university_id']
                profile.passing_year = form.cleaned_data['passing_year']
                profile.branch = form.cleaned_data['branch']
                profile.city = form.cleaned_data['city']
                profile.state = form.cleaned_data['state']
                profile.employment_status = form.cleaned_data['employment_status']
                profile.company = form.cleaned_data.get('company', '')
                profile.job_title = form.cleaned_data.get('job_title', '')
                profile.years_of_experience = form.cleaned_data.get('years_of_experience')
                profile.business_name = form.cleaned_data.get('business_name', '')
                profile.portfolio_url = form.cleaned_data.get('portfolio_url', '')
                profile.business_website = form.cleaned_data.get('business_website', '')
                profile.description_of_activity = form.cleaned_data.get('description_of_activity', '')
                profile.linkedin_profile = form.cleaned_data.get('linkedin_profile', '')
                profile.skills.set(form.cleaned_data['skills'])
                profile.field_of_work.set(form.cleaned_data['field_of_work'])
                profile.save()
            elif hasattr(request.user, 'faculty_profile'):
                profile.faculty_id = form.cleaned_data['faculty_id']
                profile.department = form.cleaned_data['department']
                profile.designation = form.cleaned_data['designation']
                profile.years_of_experience = form.cleaned_data['years_of_experience']
                profile.research_interests = form.cleaned_data['research_interests']
                profile.publications = form.cleaned_data['publications']
                profile.linkedin_profile = form.cleaned_data['linkedin_profile']
                profile.subjects_taught.set(form.cleaned_data['subjects_taught'])
                profile.save()

            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')
    else:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'phone_number': request.user.phone_number,
            'date_of_birth': request.user.date_of_birth,
            'gender': request.user.gender,
        }

        if hasattr(request.user, 'student_profile'):
            initial_data.update({
                'student_id': profile.student_id,
                'current_year': profile.current_year,
                'branch': profile.branch,
                'expected_graduation_year': profile.expected_graduation_year,
                'cgpa': profile.cgpa,
                'linkedin_profile': profile.linkedin_profile,
                'github_profile': profile.github_profile,
                'resume_drive_link': profile.resume_drive_link,
                'interested_areas': profile.interested_areas.all(),
            })
        elif hasattr(request.user, 'alumni_profile'):
            initial_data.update({
                'university_id': profile.university_id,
                'passing_year': profile.passing_year,
                'branch': profile.branch,
                'city': profile.city,
                'state': profile.state,
                'employment_status': profile.employment_status,
                'company': profile.company,
                'job_title': profile.job_title,
                'years_of_experience': profile.years_of_experience,
                'business_name': profile.business_name,
                'portfolio_url': profile.portfolio_url,
                'business_website': profile.business_website,
                'description_of_activity': profile.description_of_activity,
                'linkedin_profile': profile.linkedin_profile,
                'skills': profile.skills.all(),
                'field_of_work': profile.field_of_work.all(),
            })
        elif hasattr(request.user, 'faculty_profile'):
            initial_data.update({
                'faculty_id': profile.faculty_id,
                'department': profile.department,
                'designation': profile.designation,
                'years_of_experience': profile.years_of_experience,
                'research_interests': profile.research_interests,
                'publications': profile.publications,
                'linkedin_profile': profile.linkedin_profile,
                'subjects_taught': profile.subjects_taught.all(),
            })

        form = form_class(initial=initial_data)

    return render(request, 'tone/edit_profile.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

def donate(request):
    return render(request, 'tone/donate.html')
