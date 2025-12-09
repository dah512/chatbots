"""
Program Simulator - Runs patient cohort through 8-week pain management program
Generates realistic outcomes based on patient characteristics
"""
import random
import json
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict
import statistics

from cohort_generator import CohortGenerator, PatientProfile
from outcome_analytics import OutcomeAnalytics


@dataclass
class PainLogEntry:
    """Daily pain log entry"""
    user_id: int
    log_date: str
    pain_level: int
    pain_locations: str
    sleep_quality: int
    fatigue_level: int
    anxiety_level: int
    function_level: int
    medications_taken: str
    notes: str


@dataclass
class AssessmentScore:
    """Weekly assessment score"""
    user_id: int
    week: int
    assessment_type: str  # pre or post
    score: float
    date: str


class ProgramSimulator:
    """
    Simulate patients going through 8-week pain management program

    Factors affecting outcomes:
    - Baseline severity
    - Motivation/adherence
    - Improvement potential
    - Random variation
    - Program effectiveness
    """

    def __init__(self, cohort: List[PatientProfile], program_start_date: str = None):
        self.cohort = cohort
        self.program_start_date = datetime.fromisoformat(program_start_date) if program_start_date else datetime.now()

        # Store all simulation data
        self.pain_logs: Dict[int, List[PainLogEntry]] = {p.id: [] for p in cohort}
        self.assessment_scores: Dict[int, Dict[int, Dict]] = {p.id: {} for p in cohort}
        self.attendance: Dict[int, List[bool]] = {p.id: [] for p in cohort}

    def run_simulation(self, verbose: bool = True):
        """Run the complete 8-week program simulation"""
        print("\n" + "="*80)
        print("STARTING 8-WEEK PAIN MANAGEMENT PROGRAM SIMULATION")
        print("="*80 + "\n")

        for week in range(1, 9):
            if verbose:
                print(f"\n{'─'*80}")
                print(f"WEEK {week}")
                print(f"{'─'*80}")

            self._simulate_week(week, verbose)

        if verbose:
            print(f"\n{'='*80}")
            print("SIMULATION COMPLETE")
            print(f"{'='*80}\n")

    def _simulate_week(self, week: int, verbose: bool):
        """Simulate one week of the program"""

        week_start = self.program_start_date + timedelta(weeks=week-1)

        for patient in self.cohort:
            # Take pre-test (week 1 and subsequent weeks)
            pretest_score = self._generate_assessment_score(patient, week, "pre", week_start)
            self.assessment_scores[patient.id][week] = {"pre_score": pretest_score}

            # Simulate daily logs for the week
            for day in range(7):
                log_date = week_start + timedelta(days=day)

                # Check if patient attends this day (based on adherence)
                attends = random.random() < patient.adherence_probability

                if attends:
                    pain_entry = self._generate_pain_log(patient, week, day, log_date)
                    self.pain_logs[patient.id].append(pain_entry)

            # Take post-test at end of week
            week_end = week_start + timedelta(days=6)
            posttest_score = self._generate_assessment_score(patient, week, "post", week_end)
            self.assessment_scores[patient.id][week]["post_score"] = posttest_score

        if verbose:
            self._print_week_summary(week)

    def _generate_pain_log(self, patient: PatientProfile, week: int, day: int, log_date: datetime) -> PainLogEntry:
        """Generate a realistic pain log entry"""

        # Calculate expected improvement trajectory
        # Week 1-2: Minimal change
        # Week 3-4: Starting to improve
        # Week 5-6: More improvement
        # Week 7-8: Plateau or continued improvement

        improvement_rate = self._get_improvement_rate(patient)

        # Base metrics
        base_pain = patient.baseline_pain
        base_sleep = patient.baseline_sleep
        base_fatigue = patient.baseline_fatigue
        base_anxiety = patient.baseline_anxiety
        base_function = patient.baseline_function

        # Calculate improvement at this week
        weeks_progress = week + (day / 7.0)
        pain_improvement = improvement_rate * weeks_progress * 0.3  # Max 30% improvement by week 8

        # Add weekly variation
        weekly_variation = random.gauss(0, 0.5)  # Random fluctuation

        # Calculate current metrics
        pain_level = max(0, min(10, int(base_pain - pain_improvement + weekly_variation)))
        sleep_quality = max(0, min(10, int(base_sleep + (pain_improvement * 0.8) + weekly_variation)))
        fatigue_level = max(0, min(10, int(base_fatigue - (pain_improvement * 0.7) + weekly_variation)))
        anxiety_level = max(0, min(10, int(base_anxiety - (pain_improvement * 0.6) + weekly_variation)))
        function_level = max(0, min(10, int(base_function + (pain_improvement * 1.0) + weekly_variation)))

        # Good days and bad days (random variation)
        if random.random() < 0.15:  # 15% chance of bad day
            pain_level = min(10, pain_level + random.randint(1, 2))
            sleep_quality = max(0, sleep_quality - random.randint(1, 2))
        elif random.random() < 0.10:  # 10% chance of really good day
            pain_level = max(0, pain_level - random.randint(1, 2))
            sleep_quality = min(10, sleep_quality + random.randint(1, 2))

        # Generate notes
        notes = self._generate_notes(patient, week, pain_level, base_pain)

        return PainLogEntry(
            user_id=patient.id,
            log_date=log_date.strftime("%Y-%m-%d"),
            pain_level=pain_level,
            pain_locations=json.dumps(patient.pain_locations),
            sleep_quality=sleep_quality,
            fatigue_level=fatigue_level,
            anxiety_level=anxiety_level,
            function_level=function_level,
            medications_taken=json.dumps(patient.current_medications),
            notes=notes
        )

    def _generate_assessment_score(self, patient: PatientProfile, week: int, test_type: str, date: datetime) -> float:
        """Generate assessment score (0-100)"""

        # Baseline knowledge (40-70% depending on education)
        education_bonus = {
            "High school diploma": 0,
            "Some college": 5,
            "Associate degree": 8,
            "Bachelor's degree": 12,
            "Graduate degree": 15
        }

        base_score = random.randint(40, 60) + education_bonus.get(patient.education_level, 0)

        if test_type == "pre":
            # Pre-test: just baseline knowledge with some variation
            score = base_score + random.randint(-5, 5)
        else:
            # Post-test: improvement based on motivation and week
            motivation_bonus = {
                "low": 5,
                "medium": 15,
                "high": 25
            }

            improvement = motivation_bonus.get(patient.motivation_level, 15)

            # Cumulative learning effect
            improvement += week * 2  # Learn more as weeks go on

            # Random variation
            improvement += random.randint(-3, 3)

            score = base_score + improvement

        return min(100, max(0, score))

    def _get_improvement_rate(self, patient: PatientProfile) -> float:
        """Calculate patient's improvement rate (0.0 to 1.0)"""

        # Base rate by improvement potential
        potential_rates = {
            "excellent": 0.9,
            "good": 0.7,
            "fair": 0.5,
            "poor": 0.3
        }

        base_rate = potential_rates.get(patient.improvement_potential, 0.5)

        # Adjust for adherence
        adherence_factor = patient.adherence_probability  # 0.3 to 0.95

        # Adjust for motivation
        motivation_factor = {
            "high": 1.2,
            "medium": 1.0,
            "low": 0.8
        }

        final_rate = base_rate * adherence_factor * motivation_factor.get(patient.motivation_level, 1.0)

        return min(1.0, final_rate)

    def _generate_notes(self, patient: PatientProfile, week: int, current_pain: int, baseline_pain: int) -> str:
        """Generate realistic notes for pain log"""

        notes_options = {
            "improved": [
                "Feeling better today, practiced Tai Chi",
                "Pain less severe after movement exercises",
                "Good sleep last night helped",
                "Noticed improvement after adjusting diet",
                "Medication adjustment helping"
            ],
            "same": [
                "About the same as usual",
                "Moderate day, manageable",
                "Fluctuating throughout day",
                "Applied techniques from class"
            ],
            "worse": [
                "Rough day, pain flare",
                "Didn't sleep well, more pain",
                "Overdid activities yesterday",
                "Weather change affecting pain",
                "Stressful day increased pain"
            ]
        }

        if current_pain < baseline_pain - 1:
            category = "improved"
        elif current_pain > baseline_pain + 1:
            category = "worse"
        else:
            category = "same"

        return random.choice(notes_options[category])

    def _print_week_summary(self, week: int):
        """Print summary of week's outcomes"""

        # Calculate average scores
        all_pre_scores = [self.assessment_scores[p.id][week]["pre_score"] for p in self.cohort]
        all_post_scores = [self.assessment_scores[p.id][week]["post_score"] for p in self.cohort]

        avg_pre = statistics.mean(all_pre_scores)
        avg_post = statistics.mean(all_post_scores)
        avg_improvement = avg_post - avg_pre

        print(f"\nWeek {week} Assessment Results:")
        print(f"  Pre-test average:  {avg_pre:.1f}%")
        print(f"  Post-test average: {avg_post:.1f}%")
        print(f"  Average gain:      {avg_improvement:.1f} points")

        # Calculate pain levels for this week
        week_pain_levels = []
        for patient in self.cohort:
            patient_logs = [log for log in self.pain_logs[patient.id] if log.log_date.startswith(f"202")]
            if patient_logs:
                # Get logs from this week
                week_start = (self.program_start_date + timedelta(weeks=week-1)).date()
                week_end = week_start + timedelta(days=6)
                week_logs = [log for log in patient_logs
                            if week_start <= datetime.fromisoformat(log.log_date).date() <= week_end]
                if week_logs:
                    avg_pain = statistics.mean([log.pain_level for log in week_logs])
                    week_pain_levels.append(avg_pain)

        if week_pain_levels:
            print(f"  Average pain level: {statistics.mean(week_pain_levels):.1f}/10")

    def generate_final_report(self) -> Dict:
        """Generate comprehensive final report of program outcomes"""

        print("\n" + "="*80)
        print("FINAL PROGRAM OUTCOMES REPORT")
        print("="*80 + "\n")

        outcomes = {
            "program_info": {
                "cohort_size": len(self.cohort),
                "start_date": self.program_start_date.strftime("%Y-%m-%d"),
                "duration_weeks": 8
            },
            "patients": []
        }

        # Use outcome analytics for each patient
        analytics = OutcomeAnalytics()

        for patient in self.cohort:
            # Get baseline and endpoint metrics
            patient_logs = self.pain_logs[patient.id]

            if not patient_logs:
                continue

            # Convert to format expected by analytics
            logs_dict = [asdict(log) for log in patient_logs]

            # Get baseline (week 1) and endpoint (week 8)
            week1_logs = [log for log in patient_logs if log.log_date < (self.program_start_date + timedelta(weeks=1)).strftime("%Y-%m-%d")]
            week8_logs = [log for log in patient_logs if log.log_date >= (self.program_start_date + timedelta(weeks=7)).strftime("%Y-%m-%d")]

            if week1_logs and week8_logs:
                baseline_pain = statistics.mean([log.pain_level for log in week1_logs])
                endpoint_pain = statistics.mean([log.pain_level for log in week8_logs])
                pain_change = endpoint_pain - baseline_pain
                percent_change = (pain_change / baseline_pain * 100) if baseline_pain > 0 else 0

                # Clinical significance (≥2 point reduction)
                clinically_significant = pain_change <= -2

                # Assessment knowledge gain
                knowledge_gain = 0
                if patient.id in self.assessment_scores:
                    week1_gain = self.assessment_scores[patient.id][1]["post_score"] - self.assessment_scores[patient.id][1]["pre_score"]
                    week8_gain = self.assessment_scores[patient.id][8]["post_score"] - self.assessment_scores[patient.id][8]["pre_score"]
                    knowledge_gain = (week1_gain + week8_gain) / 2

                patient_outcome = {
                    "id": patient.id,
                    "name": f"{patient.first_name} {patient.last_name}",
                    "age": patient.age,
                    "gender": patient.gender,
                    "condition": patient.primary_condition,
                    "motivation": patient.motivation_level,
                    "improvement_potential": patient.improvement_potential,
                    "baseline_pain": round(baseline_pain, 1),
                    "endpoint_pain": round(endpoint_pain, 1),
                    "pain_change": round(pain_change, 1),
                    "percent_change": round(percent_change, 1),
                    "clinically_significant": clinically_significant,
                    "knowledge_gain": round(knowledge_gain, 1),
                    "adherence_rate": round(len(patient_logs) / 56 * 100, 1)  # 56 possible log days (8 weeks × 7 days)
                }

                outcomes["patients"].append(patient_outcome)

        # Calculate aggregate statistics
        if outcomes["patients"]:
            outcomes["aggregate"] = self._calculate_aggregate_stats(outcomes["patients"])

        # Print summary
        self._print_final_summary(outcomes)

        return outcomes

    def _calculate_aggregate_stats(self, patients: List[Dict]) -> Dict:
        """Calculate aggregate statistics across all patients"""

        pain_changes = [p["pain_change"] for p in patients]
        percent_changes = [p["percent_change"] for p in patients]
        clinically_significant_count = sum(1 for p in patients if p["clinically_significant"])
        knowledge_gains = [p["knowledge_gain"] for p in patients]

        return {
            "mean_pain_reduction": round(statistics.mean(pain_changes), 2),
            "median_pain_reduction": round(statistics.median(pain_changes), 2),
            "mean_percent_change": round(statistics.mean(percent_changes), 1),
            "clinically_significant_n": clinically_significant_count,
            "clinically_significant_percent": round(clinically_significant_count / len(patients) * 100, 1),
            "mean_knowledge_gain": round(statistics.mean(knowledge_gains), 1),
            "patients_improved": sum(1 for p in patients if p["pain_change"] < 0),
            "patients_worse": sum(1 for p in patients if p["pain_change"] > 0),
            "patients_unchanged": sum(1 for p in patients if p["pain_change"] == 0)
        }

    def _print_final_summary(self, outcomes: Dict):
        """Print human-readable final summary"""

        agg = outcomes["aggregate"]

        print("AGGREGATE OUTCOMES:\n")
        print(f"Total Patients: {len(outcomes['patients'])}")
        print(f"\nPain Reduction:")
        print(f"  Mean reduction: {abs(agg['mean_pain_reduction']):.2f} points")
        print(f"  Median reduction: {abs(agg['median_pain_reduction']):.2f} points")
        print(f"  Mean percent change: {agg['mean_percent_change']:.1f}%")
        print(f"\nClinical Significance:")
        print(f"  Patients with ≥2 point reduction: {agg['clinically_significant_n']} ({agg['clinically_significant_percent']:.1f}%)")
        print(f"\nKnowledge Gain:")
        print(f"  Mean assessment improvement: {agg['mean_knowledge_gain']:.1f} points")
        print(f"\nOutcome Distribution:")
        print(f"  Improved: {agg['patients_improved']} ({agg['patients_improved']/len(outcomes['patients'])*100:.1f}%)")
        print(f"  Worse: {agg['patients_worse']} ({agg['patients_worse']/len(outcomes['patients'])*100:.1f}%)")
        print(f"  Unchanged: {agg['patients_unchanged']} ({agg['patients_unchanged']/len(outcomes['patients'])*100:.1f}%)")

        print(f"\n{'─'*80}\n")
        print("TOP 5 RESPONDERS (Largest Pain Reduction):\n")

        sorted_patients = sorted(outcomes['patients'], key=lambda x: x['pain_change'])
        for i, patient in enumerate(sorted_patients[:5], 1):
            print(f"{i}. {patient['name']} (ID: {patient['id']})")
            print(f"   Condition: {patient['condition']}")
            print(f"   Pain: {patient['baseline_pain']:.1f} → {patient['endpoint_pain']:.1f} (Δ {patient['pain_change']:.1f})")
            print(f"   Motivation: {patient['motivation']} | Potential: {patient['improvement_potential']}")
            print()

        print(f"{'─'*80}\n")
        print("BOTTOM 5 RESPONDERS (Least Improvement or Worse):\n")

        for i, patient in enumerate(sorted_patients[-5:], 1):
            print(f"{i}. {patient['name']} (ID: {patient['id']})")
            print(f"   Condition: {patient['condition']}")
            print(f"   Pain: {patient['baseline_pain']:.1f} → {patient['endpoint_pain']:.1f} (Δ {patient['pain_change']:.1f})")
            print(f"   Motivation: {patient['motivation']} | Potential: {patient['improvement_potential']}")
            print()

        print("="*80 + "\n")

    def export_simulation_data(self, output_prefix: str = "simulation"):
        """Export all simulation data to files"""

        # Export pain logs
        all_logs = []
        for patient_id, logs in self.pain_logs.items():
            all_logs.extend([asdict(log) for log in logs])

        with open(f"{output_prefix}_pain_logs.json", "w") as f:
            json.dump(all_logs, f, indent=2)

        # Export assessment scores
        with open(f"{output_prefix}_assessments.json", "w") as f:
            json.dump(self.assessment_scores, f, indent=2)

        print(f"Exported simulation data to {output_prefix}_*.json files")


# Main execution
if __name__ == "__main__":
    print("\n" + "="*80)
    print("PAIN MANAGEMENT PROGRAM SIMULATION")
    print("="*80)

    # Generate cohort
    print("\nStep 1: Generating patient cohort...")
    generator = CohortGenerator()
    cohort = generator.generate_cohort(size=25, seed=42)
    generator.print_cohort_summary(cohort)

    # Export cohort
    generator.export_cohort_to_json(cohort, "cohort_profiles.json")

    # Run simulation
    print("\nStep 2: Running 8-week program simulation...")
    simulator = ProgramSimulator(cohort, program_start_date="2024-01-15")
    simulator.run_simulation(verbose=True)

    # Generate final report
    print("\nStep 3: Generating outcomes report...")
    outcomes = simulator.generate_final_report()

    # Export simulation data
    simulator.export_simulation_data("program_simulation")

    # Export outcomes report
    with open("program_outcomes_report.json", "w") as f:
        json.dump(outcomes, f, indent=2)

    print("\n✅ SIMULATION COMPLETE!")
    print("📊 Check the exported files for detailed results:")
    print("   - cohort_profiles.json")
    print("   - program_simulation_pain_logs.json")
    print("   - program_simulation_assessments.json")
    print("   - program_outcomes_report.json")
    print()
