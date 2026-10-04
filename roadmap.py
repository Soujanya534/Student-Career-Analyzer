roadmaps = {
    "Python Developer": [
        "Python Basics",
        "Object-Oriented Programming",
        "SQL",
        "Git & GitHub",
        "REST APIs",
        "Flask or Django",
        "Build Python Projects"
    ],

    "Data Analyst": [
        "Python Basics",
        "NumPy",
        "Pandas",
        "SQL",
        "Statistics",
        "Data Visualization",
        "Excel",
        "Power BI",
        "Build Data Analysis Projects"
    ],

    "Web Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "Git & GitHub",
        "React",
        "REST APIs",
        "Build Web Projects"
    ],

    "AI/ML Engineer": [
        "Python",
        "NumPy",
        "Pandas",
        "Statistics",
        "Machine Learning",
        "Scikit-learn",
        "Deep Learning",
        "Build AI/ML Projects"
    ],

    "Software Developer": [
        "Programming Fundamentals",
        "OOP",
        "DSA",
        "SQL",
        "Git & GitHub",
        "Problem Solving",
        "Software Development Projects"
    ]
}


def get_roadmap(career):
    return roadmaps.get(career, [])