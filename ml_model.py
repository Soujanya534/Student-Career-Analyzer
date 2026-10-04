from sklearn.ensemble import RandomForestClassifier
from career_data import careers


# Create the complete skill list
all_skills = sorted(
    set(
        skill
        for required_skills in careers.values()
        for skill in required_skills
    )
)


# Create training data
X = []
y = []


for career, required_skills in careers.items():

    skill_vector = []

    for skill in all_skills:

        if skill in required_skills:
            skill_vector.append(1)
        else:
            skill_vector.append(0)

    X.append(skill_vector)
    y.append(career)


# Train the ML model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)


def predict_career(student_skills):

    student_vector = []

    for skill in all_skills:

        if skill in student_skills:
            student_vector.append(1)
        else:
            student_vector.append(0)

    prediction = model.predict(
        [student_vector]
    )

    probabilities = model.predict_proba(
        [student_vector]
    )[0]

    career_probabilities = {}

    for career, probability in zip(
        model.classes_,
        probabilities
    ):

        career_probabilities[career] = round(
            probability * 100,
            2
        )

    return prediction[0], career_probabilities