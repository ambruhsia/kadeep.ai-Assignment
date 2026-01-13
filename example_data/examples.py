"""
Example data for InternHub testing
"""
from student_profile import StudentProfile
from internship_job import InternshipJob


def get_example_student() -> StudentProfile:
    """Get an example student profile"""
    return StudentProfile(
        name="Rajesh Kumar",
        email="rajesh.kumar@email.com",
        skills=[
            "Python",
            "JavaScript",
            "React",
            "Flask",
            "REST APIs",
            "SQL",
            "Git"
        ],
        interests=[
            "Web Development",
            "Backend Development",
            "APIs"
        ],
        experience="Built 3 full-stack web projects in college, familiar with DevOps basics",
        cgpa=3.6
    )


def get_example_job() -> InternshipJob:
    """Get an example internship job"""
    return InternshipJob(
        title="Full Stack Web Developer Intern",
        company="TechCorp India",
        description="""
        We are looking for a talented Full Stack Web Developer Intern to join our team.
        You will work on building scalable web applications using modern technologies.
        This is a great opportunity to learn and grow in a fast-paced environment.
        """,
        required_skills=[
            "Python",
            "JavaScript",
            "React",
            "REST APIs",
            "Database Design"
        ],
        preferred_skills=[
            "Docker",
            "AWS",
            "PostgreSQL",
            "Agile/Scrum"
        ],
        responsibilities=[
            "Develop frontend features using React",
            "Build backend APIs using Python/Flask",
            "Write unit tests and maintain code quality",
            "Collaborate with team in daily standups",
            "Debug and optimize application performance"
        ],
        duration_months=3,
        location="Remote",
        compensation="INR 15,000/month"
    )


def get_example_student_2() -> StudentProfile:
    """Get another example student (less experienced)"""
    return StudentProfile(
        name="Priya Sharma",
        email="priya.sharma@email.com",
        skills=[
            "Python",
            "HTML",
            "CSS",
            "Basic JavaScript"
        ],
        interests=[
            "Web Development",
            "Data Science"
        ],
        experience="Completed Python bootcamp, working on personal projects",
        cgpa=3.2
    )


def get_example_job_2() -> InternshipJob:
    """Get another example job (backend focused)"""
    return InternshipJob(
        title="Backend Engineer Intern",
        company="CloudSync Solutions",
        description="""
        Join our backend team to build scalable microservices.
        Work with Python, Docker, Kubernetes, and cloud technologies.
        """,
        required_skills=[
            "Python",
            "System Design",
            "Docker",
            "AWS",
            "Microservices"
        ],
        preferred_skills=[
            "Kubernetes",
            "MongoDB",
            "GraphQL",
            "CI/CD"
        ],
        responsibilities=[
            "Design and implement backend services",
            "Containerize applications using Docker",
            "Deploy services to AWS",
            "Write technical documentation",
            "Conduct code reviews"
        ],
        duration_months=4,
        location="Bangalore, India",
        compensation="INR 20,000/month"
    )
