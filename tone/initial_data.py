from .models import Interest, Skill

def create_initial_skills():
    skills = [
        "Python",
        "Java",
        "JavaScript",
        "C++",
        "Web Development",
        "Mobile Development",
        "Data Science",
        "Machine Learning",
        "Cloud Computing",
        "DevOps",
        "Database Management",
        "UI/UX Design",
        "Project Management",
        "Digital Marketing",
        "Business Analytics"
    ]
    
    for skill_name in skills:
        Skill.objects.get_or_create(name=skill_name)

def create_initial_interests():
    interests = [
        "Artificial Intelligence",
        "Machine Learning",
        "Web Development",
        "Mobile App Development",
        "Data Science",
        "Cybersecurity",
        "Cloud Computing",
        "Internet of Things",
        "Blockchain",
        "Robotics",
        "UI/UX Design",
        "Database Management",
        "Network Security",
        "Software Testing",
        "DevOps"
    ]
    
    for interest_name in interests:
        Interest.objects.get_or_create(name=interest_name) 