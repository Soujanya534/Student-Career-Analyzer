from career_data import careers


def analyze_careers(student_skills):
    results = []

    for career, required_skills in careers.items():

        matched_skills = []

        for skill in required_skills:
            if skill in student_skills:
                matched_skills.append(skill)

        score = (len(matched_skills) / len(required_skills)) * 100

        missing_skills = [
            skill for skill in required_skills
            if skill not in student_skills
        ]

        results.append({
            "career": career,
            "score": round(score, 2),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results