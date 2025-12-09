"""
Cohort Generator for Pain Management Program Simulation
Creates realistic patient profiles with diverse demographics and conditions
"""
import random
import json
from datetime import datetime, timedelta
from typing import List, Dict
from dataclasses import dataclass, asdict


@dataclass
class PatientProfile:
    """Patient profile with demographics and baseline characteristics"""
    id: int
    first_name: str
    last_name: str
    age: int
    gender: str
    primary_condition: str
    pain_locations: List[str]
    baseline_pain: int  # 0-10
    baseline_sleep: int  # 0-10
    baseline_fatigue: int  # 0-10
    baseline_anxiety: int  # 0-10
    baseline_function: int  # 0-10
    current_medications: List[str]
    comorbidities: List[str]
    employment_status: str
    education_level: str
    motivation_level: str  # low, medium, high
    adherence_probability: float  # 0.0-1.0
    improvement_potential: str  # poor, fair, good, excellent


class CohortGenerator:
    """Generate diverse patient cohort for simulation"""

    # Demographics
    FIRST_NAMES_MALE = [
        "James", "John", "Robert", "Michael", "William", "David", "Richard",
        "Joseph", "Thomas", "Christopher", "Daniel", "Matthew", "Anthony", "Donald"
    ]

    FIRST_NAMES_FEMALE = [
        "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan",
        "Jessica", "Sarah", "Karen", "Nancy", "Lisa", "Margaret", "Betty", "Sandra"
    ]

    LAST_NAMES = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
        "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
        "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"
    ]

    # Medical conditions
    CONDITIONS = {
        "Chronic Low Back Pain": {
            "locations": ["lower_back"],
            "typical_age": (35, 65),
            "baseline_pain_range": (5, 8),
            "gender_ratio": 0.5  # 50% male/female
        },
        "Osteoarthritis (Knees)": {
            "locations": ["knee_left", "knee_right"],
            "typical_age": (50, 75),
            "baseline_pain_range": (4, 7),
            "gender_ratio": 0.4  # 40% male, 60% female
        },
        "Rheumatoid Arthritis": {
            "locations": ["hand_left", "hand_right", "wrist_left", "wrist_right"],
            "typical_age": (40, 70),
            "baseline_pain_range": (5, 9),
            "gender_ratio": 0.25  # 25% male, 75% female
        },
        "Fibromyalgia": {
            "locations": ["whole_body"],
            "typical_age": (35, 60),
            "baseline_pain_range": (6, 9),
            "gender_ratio": 0.1  # 10% male, 90% female
        },
        "Cervical Spine Disorder": {
            "locations": ["neck", "shoulder_left", "shoulder_right"],
            "typical_age": (40, 65),
            "baseline_pain_range": (5, 8),
            "gender_ratio": 0.5
        },
        "Lupus (SLE)": {
            "locations": ["hand_left", "hand_right", "knee_left", "knee_right"],
            "typical_age": (25, 55),
            "baseline_pain_range": (5, 8),
            "gender_ratio": 0.1  # 10% male, 90% female
        },
        "Hip Osteoarthritis": {
            "locations": ["hip_left", "hip_right"],
            "typical_age": (50, 75),
            "baseline_pain_range": (4, 7),
            "gender_ratio": 0.45
        },
        "Post-Surgical Pain": {
            "locations": ["lower_back", "shoulder_right"],  # Varies
            "typical_age": (35, 70),
            "baseline_pain_range": (6, 9),
            "gender_ratio": 0.5
        },
        "Scleroderma": {
            "locations": ["hand_left", "hand_right"],
            "typical_age": (40, 65),
            "baseline_pain_range": (4, 7),
            "gender_ratio": 0.2  # 20% male, 80% female
        },
        "Shoulder Rotator Cuff Injury": {
            "locations": ["shoulder_right"],  # or left
            "typical_age": (45, 70),
            "baseline_pain_range": (5, 8),
            "gender_ratio": 0.6  # 60% male, 40% female
        }
    }

    MEDICATIONS = [
        "Ibuprofen 400mg",
        "Naproxen 500mg",
        "Acetaminophen 500mg",
        "Tramadol 50mg",
        "Hydrocodone/APAP 5/325mg",
        "Oxycodone 5mg",
        "Gabapentin 300mg",
        "Pregabalin 75mg",
        "Duloxetine 60mg",
        "Amitriptyline 25mg",
        "Meloxicam 15mg",
        "Cyclobenzaprine 10mg"
    ]

    COMORBIDITIES = [
        "Hypertension",
        "Diabetes Type 2",
        "Depression",
        "Anxiety Disorder",
        "Obesity (BMI > 30)",
        "Sleep Apnea",
        "GERD",
        "Hypothyroidism"
    ]

    EMPLOYMENT = [
        "Full-time employed",
        "Part-time employed",
        "Unemployed due to disability",
        "Retired",
        "Self-employed",
        "On medical leave"
    ]

    EDUCATION = [
        "High school diploma",
        "Some college",
        "Associate degree",
        "Bachelor's degree",
        "Graduate degree"
    ]

    def generate_cohort(self, size: int = 25, seed: int = None) -> List[PatientProfile]:
        """
        Generate a cohort of diverse patients

        Args:
            size: Number of patients to generate
            seed: Random seed for reproducibility

        Returns:
            List of PatientProfile objects
        """
        if seed:
            random.seed(seed)

        cohort = []

        # Ensure diversity in conditions
        conditions_list = list(self.CONDITIONS.keys())
        condition_distribution = []

        # Distribute conditions
        for i in range(size):
            condition = conditions_list[i % len(conditions_list)]
            condition_distribution.append(condition)

        random.shuffle(condition_distribution)

        for i in range(size):
            condition = condition_distribution[i]
            patient = self._generate_patient(i + 1, condition)
            cohort.append(patient)

        return cohort

    def _generate_patient(self, patient_id: int, condition: str) -> PatientProfile:
        """Generate a single patient profile"""

        condition_info = self.CONDITIONS[condition]

        # Gender based on condition typical distribution
        is_male = random.random() < condition_info["gender_ratio"]
        gender = "Male" if is_male else "Female"

        # Name
        if is_male:
            first_name = random.choice(self.FIRST_NAMES_MALE)
        else:
            first_name = random.choice(self.FIRST_NAMES_FEMALE)

        last_name = random.choice(self.LAST_NAMES)

        # Age
        age_min, age_max = condition_info["typical_age"]
        age = random.randint(age_min, age_max)

        # Baseline pain (condition specific)
        pain_min, pain_max = condition_info["baseline_pain_range"]
        baseline_pain = random.randint(pain_min, pain_max)

        # Other baselines (correlated with pain)
        # Worse pain = worse sleep, more fatigue, more anxiety, lower function
        pain_severity = baseline_pain / 10.0

        baseline_sleep = max(1, int(10 - (pain_severity * 8) + random.randint(-1, 1)))
        baseline_fatigue = min(10, int(2 + (pain_severity * 7) + random.randint(-1, 1)))
        baseline_anxiety = min(10, int(1 + (pain_severity * 6) + random.randint(-1, 1)))
        baseline_function = max(1, int(10 - (pain_severity * 7) + random.randint(-1, 1)))

        # Medications (1-3 medications)
        num_meds = random.randint(1, 3)
        current_medications = random.sample(self.MEDICATIONS, num_meds)

        # Comorbidities (0-3)
        num_comorbidities = random.choices([0, 1, 2, 3], weights=[0.2, 0.4, 0.3, 0.1])[0]
        comorbidities = random.sample(self.COMORBIDITIES, num_comorbidities) if num_comorbidities > 0 else []

        # Employment
        if age >= 65:
            employment_status = "Retired"
        elif baseline_pain >= 7:
            employment_status = random.choice(["Unemployed due to disability", "On medical leave", "Part-time employed"])
        else:
            employment_status = random.choice(["Full-time employed", "Part-time employed", "Self-employed"])

        # Education
        education_level = random.choice(self.EDUCATION)

        # Motivation (inversely correlated with depression/anxiety, but not perfectly)
        has_depression = "Depression" in comorbidities or "Anxiety Disorder" in comorbidities

        if has_depression:
            motivation_level = random.choices(["low", "medium", "high"], weights=[0.5, 0.4, 0.1])[0]
        else:
            motivation_level = random.choices(["low", "medium", "high"], weights=[0.1, 0.4, 0.5])[0]

        # Adherence probability (based on motivation and other factors)
        base_adherence = 0.7
        if motivation_level == "high":
            adherence_probability = base_adherence + 0.2
        elif motivation_level == "low":
            adherence_probability = base_adherence - 0.2
        else:
            adherence_probability = base_adherence

        # Adjust for comorbidities
        adherence_probability -= len(comorbidities) * 0.05
        adherence_probability = max(0.3, min(0.95, adherence_probability))

        # Improvement potential (based on multiple factors)
        potential_score = 0

        # Lower baseline pain = better improvement potential
        if baseline_pain <= 5:
            potential_score += 2
        elif baseline_pain >= 8:
            potential_score -= 1

        # Higher motivation = better potential
        if motivation_level == "high":
            potential_score += 2
        elif motivation_level == "low":
            potential_score -= 1

        # Fewer comorbidities = better potential
        potential_score -= len(comorbidities)

        # Younger age = slightly better potential
        if age < 50:
            potential_score += 1

        # Map score to category
        if potential_score >= 3:
            improvement_potential = "excellent"
        elif potential_score >= 1:
            improvement_potential = "good"
        elif potential_score >= -1:
            improvement_potential = "fair"
        else:
            improvement_potential = "poor"

        return PatientProfile(
            id=patient_id,
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender,
            primary_condition=condition,
            pain_locations=condition_info["locations"],
            baseline_pain=baseline_pain,
            baseline_sleep=baseline_sleep,
            baseline_fatigue=baseline_fatigue,
            baseline_anxiety=baseline_anxiety,
            baseline_function=baseline_function,
            current_medications=current_medications,
            comorbidities=comorbidities,
            employment_status=employment_status,
            education_level=education_level,
            motivation_level=motivation_level,
            adherence_probability=adherence_probability,
            improvement_potential=improvement_potential
        )

    def export_cohort_to_json(self, cohort: List[PatientProfile], filepath: str):
        """Export cohort to JSON file"""
        cohort_data = [asdict(patient) for patient in cohort]
        with open(filepath, 'w') as f:
            json.dump(cohort_data, f, indent=2)

    def print_cohort_summary(self, cohort: List[PatientProfile]):
        """Print summary statistics of cohort"""
        print(f"\n{'='*80}")
        print(f"COHORT SUMMARY (N={len(cohort)})")
        print(f"{'='*80}\n")

        # Demographics
        males = sum(1 for p in cohort if p.gender == "Male")
        females = len(cohort) - males
        avg_age = sum(p.age for p in cohort) / len(cohort)

        print(f"DEMOGRAPHICS:")
        print(f"  Gender: {males} Male ({males/len(cohort)*100:.1f}%), {females} Female ({females/len(cohort)*100:.1f}%)")
        print(f"  Age: {avg_age:.1f} years (range: {min(p.age for p in cohort)}-{max(p.age for p in cohort)})")

        # Conditions
        print(f"\nPRIMARY CONDITIONS:")
        condition_counts = {}
        for patient in cohort:
            condition_counts[patient.primary_condition] = condition_counts.get(patient.primary_condition, 0) + 1

        for condition, count in sorted(condition_counts.items(), key=lambda x: -x[1]):
            print(f"  {condition}: {count} ({count/len(cohort)*100:.1f}%)")

        # Baseline metrics
        print(f"\nBASELINE METRICS (mean ± std):")
        import statistics
        metrics = ['baseline_pain', 'baseline_sleep', 'baseline_fatigue', 'baseline_anxiety', 'baseline_function']
        metric_names = ['Pain Level', 'Sleep Quality', 'Fatigue Level', 'Anxiety Level', 'Function Level']

        for metric, name in zip(metrics, metric_names):
            values = [getattr(p, metric) for p in cohort]
            mean = statistics.mean(values)
            stdev = statistics.stdev(values) if len(values) > 1 else 0
            print(f"  {name}: {mean:.2f} ± {stdev:.2f}")

        # Medications
        all_meds = [med for p in cohort for med in p.current_medications]
        avg_meds = len(all_meds) / len(cohort)
        print(f"\nMEDICATIONS:")
        print(f"  Average per patient: {avg_meds:.2f}")

        # Motivation
        motivation_counts = {}
        for patient in cohort:
            motivation_counts[patient.motivation_level] = motivation_counts.get(patient.motivation_level, 0) + 1

        print(f"\nMOTIVATION LEVELS:")
        for level in ["high", "medium", "low"]:
            count = motivation_counts.get(level, 0)
            print(f"  {level.capitalize()}: {count} ({count/len(cohort)*100:.1f}%)")

        # Improvement potential
        potential_counts = {}
        for patient in cohort:
            potential_counts[patient.improvement_potential] = potential_counts.get(patient.improvement_potential, 0) + 1

        print(f"\nIMPROVEMENT POTENTIAL:")
        for level in ["excellent", "good", "fair", "poor"]:
            count = potential_counts.get(level, 0)
            print(f"  {level.capitalize()}: {count} ({count/len(cohort)*100:.1f}%)")

        print(f"\n{'='*80}\n")


# Example usage
if __name__ == "__main__":
    generator = CohortGenerator()

    # Generate cohort of 25 patients with seed for reproducibility
    cohort = generator.generate_cohort(size=25, seed=42)

    # Print summary
    generator.print_cohort_summary(cohort)

    # Print individual profiles
    print("\nINDIVIDUAL PATIENT PROFILES:\n")
    for patient in cohort:
        print(f"ID: {patient.id} | {patient.first_name} {patient.last_name}")
        print(f"  Age: {patient.age} | Gender: {patient.gender}")
        print(f"  Condition: {patient.primary_condition}")
        print(f"  Baseline Pain: {patient.baseline_pain}/10")
        print(f"  Medications: {', '.join(patient.current_medications)}")
        print(f"  Motivation: {patient.motivation_level} | Potential: {patient.improvement_potential}")
        print()

    # Export to JSON
    generator.export_cohort_to_json(cohort, "cohort_25patients.json")
    print("Cohort exported to cohort_25patients.json")
