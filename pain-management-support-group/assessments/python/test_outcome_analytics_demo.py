#!/usr/bin/env python3
"""
Demonstration of the Outcome Analytics System
Shows how patient progress is analyzed and reported
"""

import json
from datetime import datetime, timedelta
from outcome_analytics import OutcomeAnalytics

print("="*70)
print("PAIN MANAGEMENT SUPPORT GROUP - OUTCOME ANALYTICS DEMONSTRATION")
print("="*70)
print()

# Load our simulation data
print("📊 Loading simulation data...")
print()

with open('program_simulation_pain_logs.json', 'r') as f:
    pain_logs = json.load(f)

with open('program_simulation_assessments.json', 'r') as f:
    assessments = json.load(f)

with open('program_outcomes_report.json', 'r') as f:
    outcomes = json.load(f)

print(f"✓ Loaded {len(pain_logs)} pain log entries")
print(f"✓ Loaded assessment data for {len(assessments)} patients")
print(f"✓ Loaded outcomes for {len(outcomes['patients'])} patients")
print()

# Initialize analytics engine
analytics = OutcomeAnalytics()

# Analyze a specific patient
print("="*70)
print("INDIVIDUAL PATIENT ANALYSIS")
print("="*70)
print()

# Get patient 1's data
patient_id = 1
patient_logs = [log for log in pain_logs if log['user_id'] == patient_id]
patient_assessments = assessments.get(str(patient_id), {})

print(f"Patient ID: {patient_id}")
print(f"Total Pain Logs: {len(patient_logs)}")
print()

# Show pain trajectory
print("📈 PAIN TRAJECTORY:")
print("-"*70)

# Group by week
from collections import defaultdict
weekly_pain = defaultdict(list)

for log in patient_logs:
    log_date = datetime.fromisoformat(log['log_date'])
    # Calculate week number (assuming first log is week 1)
    first_date = min([datetime.fromisoformat(l['log_date']) for l in patient_logs])
    week = ((log_date - first_date).days // 7) + 1
    weekly_pain[week].append(log['pain_level'])

for week in sorted(weekly_pain.keys()):
    avg_pain = sum(weekly_pain[week]) / len(weekly_pain[week])
    print(f"  Week {week}: {avg_pain:.1f} (n={len(weekly_pain[week])} logs)")

print()

# Show knowledge progress
if patient_assessments:
    print("📚 KNOWLEDGE ASSESSMENT PROGRESS:")
    print("-"*70)
    for week in sorted([int(w) for w in patient_assessments.keys()]):
        scores = patient_assessments[str(week)]
        gain = scores['post_score'] - scores['pre_score']
        print(f"  Week {week}: Pre={scores['pre_score']}% → Post={scores['post_score']}% (Gain: +{gain}%)")
    print()

# Calculate overall improvement
first_week_pain = weekly_pain[1]
last_week_pain = weekly_pain[max(weekly_pain.keys())]

baseline_pain = sum(first_week_pain) / len(first_week_pain)
endpoint_pain = sum(last_week_pain) / len(last_week_pain)
pain_change = endpoint_pain - baseline_pain
percent_change = (pain_change / baseline_pain) * 100

print("="*70)
print("OUTCOME SUMMARY:")
print("="*70)
print(f"  Baseline Pain Level: {baseline_pain:.1f}")
print(f"  Endpoint Pain Level: {endpoint_pain:.1f}")
print(f"  Absolute Change: {pain_change:+.1f} points")
print(f"  Percent Change: {percent_change:+.1f}%")
print(f"  Clinical Status: {'✅ IMPROVED' if pain_change < 0 else '⚠️ NO IMPROVEMENT'}")
print(f"  Clinically Significant: {'✅ YES' if pain_change <= -2 else '❌ NO'} (≥2 point reduction)")
print()

# Aggregate cohort analysis
print("="*70)
print("COHORT-LEVEL ANALYSIS")
print("="*70)
print()

print("📊 COHORT DEMOGRAPHICS:")
print("-"*70)

cohort_outcomes = outcomes['patients']
print(f"  Total Patients: {len(cohort_outcomes)}")

improved_count = sum(1 for p in cohort_outcomes if p['pain_change'] < 0)
print(f"  Patients Improved: {improved_count} ({improved_count/len(cohort_outcomes)*100:.1f}%)")

clinically_sig = sum(1 for p in cohort_outcomes if p['pain_change'] <= -2)
print(f"  Clinically Significant: {clinically_sig} ({clinically_sig/len(cohort_outcomes)*100:.1f}%)")

print()

# Pain reduction statistics
pain_changes = [p['pain_change'] for p in cohort_outcomes]
import numpy as np

print("📉 PAIN REDUCTION STATISTICS:")
print("-"*70)
print(f"  Mean Change: {np.mean(pain_changes):.2f} points")
print(f"  Median Change: {np.median(pain_changes):.2f} points")
print(f"  Std Dev: {np.std(pain_changes):.2f}")
print(f"  Min Change: {min(pain_changes):.2f} points (best improvement)")
print(f"  Max Change: {max(pain_changes):.2f} points (worst outcome)")
print()

# Note: Secondary outcomes (sleep, function, etc.) would be calculated from raw pain logs
# For this demo, focusing on pain and knowledge outcomes
print("📊 KNOWLEDGE OUTCOMES:")
print("-"*70)
knowledge_gains = [p['knowledge_gain'] for p in cohort_outcomes]
print(f"  Mean Knowledge Gain: {np.mean(knowledge_gains):+.2f}%")
print(f"  Median Knowledge Gain: {np.median(knowledge_gains):+.2f}%")
print(f"  Range: {min(knowledge_gains):.2f}% to {max(knowledge_gains):.2f}%")
print()

# Top performers
print("="*70)
print("TOP 5 RESPONDERS (Greatest Pain Reduction)")
print("="*70)
print()

sorted_patients = sorted(cohort_outcomes, key=lambda x: x['pain_change'])

for i, data in enumerate(sorted_patients[:5], 1):
    print(f"{i}. {data['name']} (ID: {data['id']}):")
    print(f"   Condition: {data['condition']}")
    print(f"   Pain: {data['baseline_pain']:.1f} → {data['endpoint_pain']:.1f} ({data['pain_change']:+.1f})")
    print(f"   Knowledge Gain: +{data['knowledge_gain']:.1f}%")
    print()

# Bottom performers (non-responders)
print("="*70)
print("NON-RESPONDERS (Pain Increased or No Change)")
print("="*70)
print()

non_responders = [p for p in cohort_outcomes if p['pain_change'] >= 0]

if non_responders:
    for i, data in enumerate(sorted(non_responders,
                                   key=lambda x: -x['pain_change']), 1):
        print(f"{i}. {data['name']} (ID: {data['id']}):")
        print(f"   Condition: {data['condition']}")
        print(f"   Pain: {data['baseline_pain']:.1f} → {data['endpoint_pain']:.1f} ({data['pain_change']:+.1f})")
        print()
else:
    print("  No non-responders - all patients improved!")
    print()

# Generate report card
print("="*70)
print("PROGRAM REPORT CARD")
print("="*70)
print()

total_patients = len(cohort_outcomes)
improved = sum(1 for p in cohort_outcomes if p['pain_change'] < 0)
clinically_sig = sum(1 for p in cohort_outcomes if p['pain_change'] <= -2)
mean_reduction = abs(np.mean([p['pain_change'] for p in cohort_outcomes if p['pain_change'] < 0]))

# Grade the program
improvement_rate = (improved / total_patients) * 100

if improvement_rate >= 90:
    grade = "A+"
elif improvement_rate >= 80:
    grade = "A"
elif improvement_rate >= 70:
    grade = "B"
elif improvement_rate >= 60:
    grade = "C"
else:
    grade = "D"

print(f"  Overall Grade: {grade}")
print(f"  Improvement Rate: {improvement_rate:.1f}%")
print(f"  Mean Pain Reduction (responders): {mean_reduction:.2f} points")
print(f"  Clinically Significant Rate: {clinically_sig/total_patients*100:.1f}%")
print()

print("✓ Meets Minimal Clinically Important Difference (MCID):",
      "✅ YES" if mean_reduction >= 0.5 else "❌ NO")
print("✓ Acceptable Improvement Rate (≥70%):",
      "✅ YES" if improvement_rate >= 70 else "❌ NO")
print()

print("="*70)
print("DEMONSTRATION COMPLETE!")
print("="*70)
print()
print("The outcome analytics system can:")
print("  • Track individual patient progress over time")
print("  • Calculate baseline vs endpoint comparisons")
print("  • Determine clinical significance of changes")
print("  • Aggregate cohort-level statistics")
print("  • Identify top responders and non-responders")
print("  • Generate comprehensive program report cards")
print("  • Export data for further statistical analysis")
