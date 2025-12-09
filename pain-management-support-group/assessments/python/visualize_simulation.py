#!/usr/bin/env python3
"""
Comprehensive Analysis and Visualization of Pain Management Program Simulation
Analyzes the simulated 8-week program outcomes for 25 diverse patients
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from datetime import datetime
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# Create output directory
os.makedirs('simulation_plots', exist_ok=True)

print("="*60)
print("PAIN MANAGEMENT PROGRAM SIMULATION ANALYSIS")
print("="*60)
print()

# ============================================================================
# 1. LOAD DATA
# ============================================================================

print("Loading simulation data...")

with open('program_simulation_pain_logs.json', 'r') as f:
    pain_logs = json.load(f)

with open('program_simulation_assessments.json', 'r') as f:
    assessments = json.load(f)

with open('program_outcomes_report.json', 'r') as f:
    outcomes = json.load(f)

with open('cohort_profiles.json', 'r') as f:
    profiles = json.load(f)

# ============================================================================
# 2. PROCESS PAIN LOGS
# ============================================================================

print("Processing pain log data...")

# Convert pain logs to DataFrame
# The JSON is already in list format
pain_df = pd.DataFrame(pain_logs)
pain_df['log_date'] = pd.to_datetime(pain_df['log_date'])
pain_df = pain_df.rename(columns={'user_id': 'patient_id'})

# Add week number
pain_df['day_number'] = pain_df.groupby('patient_id')['log_date'].rank()
pain_df['week_number'] = np.ceil(pain_df['day_number'] / 7).astype(int)

# Calculate weekly averages
weekly_avg = pain_df.groupby(['patient_id', 'week_number']).agg({
    'pain_level': 'mean',
    'sleep_quality': 'mean',
    'fatigue_level': 'mean',
    'anxiety_level': 'mean',
    'function_level': 'mean'
}).reset_index()

weekly_avg.columns = ['patient_id', 'week_number', 'avg_pain', 'avg_sleep',
                      'avg_fatigue', 'avg_anxiety', 'avg_function']

# ============================================================================
# 3. STATISTICAL ANALYSIS
# ============================================================================

print("\n" + "="*60)
print("STATISTICAL ANALYSIS")
print("="*60)
print()

# Get Week 1 and Week 8 data
week1 = weekly_avg[weekly_avg['week_number'] == 1].set_index('patient_id')
week8 = weekly_avg[weekly_avg['week_number'] == 8].set_index('patient_id')

# Merge for paired analysis
paired_data = week1.join(week8, how='inner', lsuffix='_w1', rsuffix='_w8')

# Perform paired t-tests
metrics = ['pain', 'sleep', 'fatigue', 'anxiety', 'function']
ttest_results = {}

for metric in metrics:
    w1_col = f'avg_{metric}_w1'
    w8_col = f'avg_{metric}_w8'

    if w1_col in paired_data.columns and w8_col in paired_data.columns:
        w1_vals = paired_data[w1_col].dropna()
        w8_vals = paired_data[w8_col].dropna()

        # Ensure same indices
        common_idx = w1_vals.index.intersection(w8_vals.index)
        w1_vals = w1_vals.loc[common_idx]
        w8_vals = w8_vals.loc[common_idx]

        if len(w1_vals) > 1:
            # Paired t-test
            t_stat, p_value = stats.ttest_rel(w8_vals, w1_vals)

            # Calculate effect size (Cohen's d for paired samples)
            diff = w8_vals - w1_vals
            cohens_d = diff.mean() / diff.std()

            # Confidence interval
            ci = stats.t.interval(0.95, len(diff)-1,
                                 loc=diff.mean(),
                                 scale=stats.sem(diff))

            ttest_results[metric] = {
                'mean_w1': w1_vals.mean(),
                'mean_w8': w8_vals.mean(),
                'mean_change': diff.mean(),
                'sd_change': diff.std(),
                't_statistic': t_stat,
                'p_value': p_value,
                'ci_lower': ci[0],
                'ci_upper': ci[1],
                'cohens_d': cohens_d,
                'n': len(w1_vals)
            }

            # Effect size interpretation
            if abs(cohens_d) < 0.2:
                effect_interp = "negligible"
            elif abs(cohens_d) < 0.5:
                effect_interp = "small"
            elif abs(cohens_d) < 0.8:
                effect_interp = "medium"
            else:
                effect_interp = "large"

            print(f"{metric.upper()}:")
            print(f"  Week 1 Mean: {w1_vals.mean():.2f}")
            print(f"  Week 8 Mean: {w8_vals.mean():.2f}")
            print(f"  Mean Change: {diff.mean():.2f} (SD = {diff.std():.2f})")
            print(f"  t-statistic: {t_stat:.3f}")
            print(f"  p-value: {p_value:.4f} {'**' if p_value < 0.05 else ''}")
            print(f"  95% CI: [{ci[0]:.2f}, {ci[1]:.2f}]")
            print(f"  Cohen's d: {cohens_d:.3f} ({effect_interp})")
            print()

# ============================================================================
# 4. KNOWLEDGE ASSESSMENT ANALYSIS
# ============================================================================

print("="*60)
print("KNOWLEDGE ASSESSMENT RESULTS")
print("="*60)
print()

# Convert assessments to DataFrame
# Structure is {patient_id: {week: {pre_score: X, post_score: Y}}}
assessment_data = []
for patient_id, weeks in assessments.items():
    for week, scores in weeks.items():
        assessment_data.append({
            'patient_id': int(patient_id),
            'week': int(week),
            'assessment_type': 'pre',
            'score': scores.get('pre_score', 0),
            'percentage': scores.get('pre_score', 0)  # Already a percentage
        })
        assessment_data.append({
            'patient_id': int(patient_id),
            'week': int(week),
            'assessment_type': 'post',
            'score': scores.get('post_score', 0),
            'percentage': scores.get('post_score', 0)  # Already a percentage
        })

assessment_df = pd.DataFrame(assessment_data)

# Calculate knowledge gains
knowledge_gains = assessment_df.pivot_table(
    index=['patient_id', 'week'],
    columns='assessment_type',
    values='percentage'
).reset_index()

knowledge_gains['knowledge_gain'] = knowledge_gains['post'] - knowledge_gains['pre']

print(f"Average Knowledge Gain per Week: {knowledge_gains['knowledge_gain'].mean():.2f}%")
print(f"SD: {knowledge_gains['knowledge_gain'].std():.2f}%")
print(f"Range: {knowledge_gains['knowledge_gain'].min():.2f}% to {knowledge_gains['knowledge_gain'].max():.2f}%")
print()

# Overall knowledge gain
first_pre = assessment_df[assessment_df['assessment_type'] == 'pre'].groupby('patient_id').first()
last_post = assessment_df[assessment_df['assessment_type'] == 'post'].groupby('patient_id').last()

overall_gain = pd.DataFrame({
    'pre_score': first_pre['percentage'],
    'post_score': last_post['percentage']
})
overall_gain['overall_gain'] = overall_gain['post_score'] - overall_gain['pre_score']

print("Overall Program Knowledge Gain (Week 1 Pre to Week 8 Post):")
print(f"  Mean: {overall_gain['overall_gain'].mean():.2f}%")
print(f"  Median: {overall_gain['overall_gain'].median():.2f}%")
print(f"  SD: {overall_gain['overall_gain'].std():.2f}%")
print()

# ============================================================================
# 5. VISUALIZATIONS
# ============================================================================

print("Generating visualizations...")

# Plot 1: Individual Pain Trajectories
fig, ax = plt.subplots(figsize=(12, 7))

for patient_id in weekly_avg['patient_id'].unique():
    patient_data = weekly_avg[weekly_avg['patient_id'] == patient_id]
    ax.plot(patient_data['week_number'], patient_data['avg_pain'],
           alpha=0.3, color='steelblue', linewidth=1)

# Add average trend
avg_trend = weekly_avg.groupby('week_number')['avg_pain'].mean()
ax.plot(avg_trend.index, avg_trend.values,
       color='red', linewidth=3, label='Average Trend', zorder=10)

# Add confidence interval
sem = weekly_avg.groupby('week_number')['avg_pain'].sem()
ax.fill_between(avg_trend.index,
               avg_trend - 1.96*sem,
               avg_trend + 1.96*sem,
               color='red', alpha=0.2)

ax.set_xlabel('Week Number', fontsize=12, fontweight='bold')
ax.set_ylabel('Average Pain Level (0-10)', fontsize=12, fontweight='bold')
ax.set_title('Individual Pain Trajectories Over 8 Weeks\nRed line shows average trend with 95% CI',
            fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('simulation_plots/01_pain_trajectories.png', dpi=300, bbox_inches='tight')
plt.close()

# Plot 2: Week 1 vs Week 8 Pain Comparison
fig, ax = plt.subplots(figsize=(10, 7))

comparison_data = pd.DataFrame({
    'Week 1': paired_data['avg_pain_w1'],
    'Week 8': paired_data['avg_pain_w8']
})

positions = [1, 2]
bp = ax.boxplot([comparison_data['Week 1'], comparison_data['Week 8']],
               positions=positions,
               widths=0.6,
               patch_artist=True,
               boxprops=dict(facecolor='lightblue', alpha=0.7),
               medianprops=dict(color='red', linewidth=2))

# Color boxes differently
bp['boxes'][0].set_facecolor('lightcoral')
bp['boxes'][1].set_facecolor('lightgreen')

# Add individual patient lines
for idx in comparison_data.index:
    ax.plot([1, 2], [comparison_data.loc[idx, 'Week 1'],
                    comparison_data.loc[idx, 'Week 8']],
           'o-', alpha=0.2, color='gray')

ax.set_xticks(positions)
ax.set_xticklabels(['Week 1', 'Week 8'], fontsize=12, fontweight='bold')
ax.set_ylabel('Pain Level (0-10)', fontsize=12, fontweight='bold')
ax.set_title('Pain Levels: Week 1 vs Week 8\nLines connect individual patients',
            fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('simulation_plots/02_pain_comparison_boxplot.png', dpi=300, bbox_inches='tight')
plt.close()

# Plot 3: Multi-metric Dashboard
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

metrics_info = [
    ('avg_pain', 'Pain', 'Reds_r'),
    ('avg_fatigue', 'Fatigue', 'Oranges_r'),
    ('avg_anxiety', 'Anxiety', 'Purples_r'),
    ('avg_sleep', 'Sleep Quality', 'Greens'),
    ('avg_function', 'Function', 'Blues'),
]

for idx, (metric, label, cmap) in enumerate(metrics_info):
    ax = axes[idx]

    # Scatter plot with all data points
    for patient_id in weekly_avg['patient_id'].unique():
        patient_data = weekly_avg[weekly_avg['patient_id'] == patient_id]
        ax.scatter(patient_data['week_number'], patient_data[metric],
                  alpha=0.2, color='gray', s=20)

    # Average trend
    avg_trend = weekly_avg.groupby('week_number')[metric].mean()
    sem = weekly_avg.groupby('week_number')[metric].sem()

    ax.plot(avg_trend.index, avg_trend.values,
           color='darkblue', linewidth=2.5, marker='o')
    ax.fill_between(avg_trend.index,
                    avg_trend - 1.96*sem,
                    avg_trend + 1.96*sem,
                    alpha=0.3, color='lightblue')

    ax.set_xlabel('Week Number', fontweight='bold')
    ax.set_ylabel('Score (0-10)', fontweight='bold')
    ax.set_title(label, fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)

# Remove the 6th subplot
axes[5].remove()

plt.suptitle('All Outcome Metrics Over 8 Weeks\nTrends show population averages with 95% confidence intervals',
            fontsize=14, fontweight='bold', y=1.00)
plt.tight_layout()
plt.savefig('simulation_plots/03_all_metrics_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()

# Plot 4: Knowledge Assessment Progress
fig, ax = plt.subplots(figsize=(12, 7))

knowledge_gains_clean = knowledge_gains.dropna(subset=['knowledge_gain'])
weeks = sorted(knowledge_gains_clean['week'].unique())

bp = ax.boxplot([knowledge_gains_clean[knowledge_gains_clean['week'] == w]['knowledge_gain']
                 for w in weeks],
               positions=weeks,
               widths=0.6,
               patch_artist=True,
               boxprops=dict(facecolor='lightblue', alpha=0.7),
               medianprops=dict(color='red', linewidth=2))

# Add jittered points
for w in weeks:
    week_data = knowledge_gains_clean[knowledge_gains_clean['week'] == w]['knowledge_gain']
    x = np.random.normal(w, 0.04, size=len(week_data))
    ax.scatter(x, week_data, alpha=0.3, color='darkblue', s=30)

ax.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.5)
ax.set_xlabel('Week Number', fontsize=12, fontweight='bold')
ax.set_ylabel('Knowledge Gain (%)', fontsize=12, fontweight='bold')
ax.set_title('Knowledge Gain by Week (Post-test minus Pre-test)',
            fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('simulation_plots/04_knowledge_gains.png', dpi=300, bbox_inches='tight')
plt.close()

# Plot 5: Responder Analysis
paired_data['pain_change'] = paired_data['avg_pain_w8'] - paired_data['avg_pain_w1']

def classify_responder(change):
    if change <= -2:
        return 'Strong Responder\n(≥2 pt decrease)'
    elif change < 0:
        return 'Modest Responder\n(decreased)'
    elif change == 0:
        return 'No Change'
    else:
        return 'Non-Responder\n(increased)'

paired_data['responder_status'] = paired_data['pain_change'].apply(classify_responder)

responder_counts = paired_data['responder_status'].value_counts()
responder_pct = (responder_counts / len(paired_data) * 100).round(1)

fig, ax = plt.subplots(figsize=(12, 7))

colors = {
    'Strong Responder\n(≥2 pt decrease)': 'darkgreen',
    'Modest Responder\n(decreased)': 'lightgreen',
    'No Change': 'gray',
    'Non-Responder\n(increased)': 'lightcoral'
}

bars = ax.bar(range(len(responder_counts)), responder_counts.values,
             color=[colors.get(cat, 'gray') for cat in responder_counts.index],
             alpha=0.8)

# Add count and percentage labels
for i, (count, pct) in enumerate(zip(responder_counts.values, responder_pct.values)):
    ax.text(i, count + 0.3, f'n={count}\n({pct}%)',
           ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_xticks(range(len(responder_counts)))
ax.set_xticklabels(responder_counts.index, fontsize=10)
ax.set_ylabel('Number of Patients', fontsize=12, fontweight='bold')
ax.set_title('Patient Response Classification\nBased on pain level change from Week 1 to Week 8',
            fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('simulation_plots/05_responder_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# Plot 6: Baseline vs Improvement Correlation
fig, ax = plt.subplots(figsize=(10, 7))

baseline_pain = paired_data['avg_pain_w1']
pain_reduction = -paired_data['pain_change']  # Negative so improvement is positive

ax.scatter(baseline_pain, pain_reduction, s=100, alpha=0.6, color='steelblue')

# Add regression line
z = np.polyfit(baseline_pain, pain_reduction, 1)
p = np.poly1d(z)
x_line = np.linspace(baseline_pain.min(), baseline_pain.max(), 100)
ax.plot(x_line, p(x_line), "r--", linewidth=2, alpha=0.8)

# Calculate correlation
corr, p_val = stats.pearsonr(baseline_pain, pain_reduction)
ax.text(0.05, 0.95, f'r = {corr:.3f}, p = {p_val:.4f}',
       transform=ax.transAxes, fontsize=12,
       verticalalignment='top',
       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

ax.set_xlabel('Baseline Pain Level (Week 1)', fontsize=12, fontweight='bold')
ax.set_ylabel('Pain Reduction (points)', fontsize=12, fontweight='bold')
ax.set_title('Baseline Pain vs Pain Reduction\nHigher baseline pain associated with greater improvement potential',
            fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('simulation_plots/06_baseline_vs_improvement.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 6. EXPORT SUMMARY REPORT
# ============================================================================

# Responder analysis
responder_analysis = {
    'strong_responders': int((paired_data['pain_change'] <= -2).sum()),
    'modest_responders': int(((paired_data['pain_change'] < 0) & (paired_data['pain_change'] > -2)).sum()),
    'no_change': int((paired_data['pain_change'] == 0).sum()),
    'non_responders': int((paired_data['pain_change'] > 0).sum()),
    'improvement_rate': float((paired_data['pain_change'] < 0).sum() / len(paired_data) * 100)
}

summary_report = {
    'simulation_info': {
        'n_patients': len(paired_data),
        'simulation_date': datetime.now().isoformat(),
        'analysis_version': '1.0'
    },
    'pain_outcomes': ttest_results.get('pain', {}),
    'other_outcomes': {k: v for k, v in ttest_results.items() if k != 'pain'},
    'knowledge_outcomes': {
        'mean_weekly_gain': float(knowledge_gains['knowledge_gain'].mean()),
        'overall_mean_gain': float(overall_gain['overall_gain'].mean()),
        'overall_median_gain': float(overall_gain['overall_gain'].median())
    },
    'responder_analysis': responder_analysis
}

with open('simulation_statistical_summary.json', 'w') as f:
    json.dump(summary_report, f, indent=2)

print("\n" + "="*60)
print("ANALYSIS COMPLETE")
print("="*60)
print()
print("Generated 6 visualization plots in simulation_plots/")
print("Exported statistical summary to simulation_statistical_summary.json")
print()
print("Key Findings:")
print(f"- {len(paired_data)} patients completed simulation")
if 'pain' in ttest_results:
    print(f"- Mean pain reduction: {ttest_results['pain']['mean_change']:.2f} points (p = {ttest_results['pain']['p_value']:.4f})")
    print(f"- Effect size (Cohen's d): {ttest_results['pain']['cohens_d']:.3f}")
print(f"- Improvement rate: {responder_analysis['improvement_rate']:.1f}%")
print(f"- Mean knowledge gain: {summary_report['knowledge_outcomes']['overall_mean_gain']:.2f}%")
print("\nAll results saved successfully.")
