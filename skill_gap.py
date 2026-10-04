def get_skill_gap(best_career):

    missing_skills = best_career["missing_skills"]

    if not missing_skills:
        return [
            "You have all the required skills for this career.",
            "Focus on building real-world projects.",
            "Prepare for technical interviews."
        ]

    recommendations = []

    for skill in missing_skills:
        recommendations.append(
            f"Learn {skill}"
        )

    return recommendations