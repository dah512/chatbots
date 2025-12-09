"""
Outcome Analytics for Pain Management Program
Analyzes patient progress and outcomes over the 8-week program
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import json


class OutcomeAnalytics:
    """
    Analytics engine for tracking patient outcomes across multiple dimensions:
    - Pain levels
    - Sleep quality
    - Fatigue
    - Anxiety
    - Physical function
    - ADL completion
    - Medication usage
    """

    def __init__(self):
        self.metrics = [
            "pain_level",
            "sleep_quality",
            "fatigue_level",
            "anxiety_level",
            "function_level"
        ]

    def load_pain_logs(self, user_id: int, logs: List[Dict]) -> pd.DataFrame:
        """Load pain logs into pandas DataFrame"""
        df = pd.DataFrame(logs)
        df['log_date'] = pd.to_datetime(df['log_date'])
        df = df.sort_values('log_date')
        return df

    def calculate_baseline_metrics(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate baseline metrics (Week 1 averages)"""
        week1_cutoff = df['log_date'].min() + timedelta(days=7)
        week1_data = df[df['log_date'] <= week1_cutoff]

        baseline = {}
        for metric in self.metrics:
            if metric in week1_data.columns:
                baseline[metric] = week1_data[metric].mean()
            else:
                baseline[metric] = None

        return baseline

    def calculate_endpoint_metrics(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate endpoint metrics (Week 8 averages)"""
        week8_start = df['log_date'].max() - timedelta(days=7)
        week8_data = df[df['log_date'] >= week8_start]

        endpoint = {}
        for metric in self.metrics:
            if metric in week8_data.columns:
                endpoint[metric] = week8_data[metric].mean()
            else:
                endpoint[metric] = None

        return endpoint

    def calculate_change_scores(
        self,
        baseline: Dict[str, float],
        endpoint: Dict[str, float]
    ) -> Dict[str, Dict[str, float]]:
        """Calculate change from baseline to endpoint"""
        changes = {}

        for metric in self.metrics:
            if baseline[metric] is not None and endpoint[metric] is not None:
                absolute_change = endpoint[metric] - baseline[metric]
                percent_change = (absolute_change / baseline[metric] * 100) if baseline[metric] != 0 else 0

                # For pain, fatigue, anxiety: negative change is improvement
                # For sleep, function: positive change is improvement
                improvement_direction = -1 if metric in ['pain_level', 'fatigue_level', 'anxiety_level'] else 1

                changes[metric] = {
                    "baseline": round(baseline[metric], 2),
                    "endpoint": round(endpoint[metric], 2),
                    "absolute_change": round(absolute_change, 2),
                    "percent_change": round(percent_change, 2),
                    "improved": (absolute_change * improvement_direction) > 0
                }

        return changes

    def calculate_weekly_trends(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate weekly averages for trend analysis"""
        df['week'] = ((df['log_date'] - df['log_date'].min()).dt.days // 7) + 1

        weekly_data = df.groupby('week')[self.metrics].mean().reset_index()
        return weekly_data

    def calculate_clinically_significant_improvement(
        self,
        changes: Dict[str, Dict[str, float]]
    ) -> Dict[str, bool]:
        """
        Determine if improvements meet clinically significant thresholds

        Thresholds:
        - Pain: ≥2 point reduction on 0-10 scale (20%)
        - Sleep: ≥1 point improvement
        - Fatigue: ≥1 point reduction
        - Anxiety: ≥2 point reduction
        - Function: ≥1 point improvement
        """
        thresholds = {
            "pain_level": -2.0,  # Negative = reduction
            "sleep_quality": 1.0,
            "fatigue_level": -1.0,
            "anxiety_level": -2.0,
            "function_level": 1.0
        }

        significant = {}
        for metric, threshold in thresholds.items():
            if metric in changes and changes[metric]["absolute_change"] is not None:
                met_threshold = changes[metric]["absolute_change"] <= threshold if threshold < 0 else changes[metric]["absolute_change"] >= threshold
                significant[metric] = met_threshold
            else:
                significant[metric] = False

        return significant

    def generate_patient_report(
        self,
        user_id: int,
        pain_logs: List[Dict],
        assessment_scores: Dict[int, Dict],
        program_completion: bool
    ) -> Dict:
        """
        Generate comprehensive patient outcome report

        Args:
            user_id: Patient ID
            pain_logs: List of pain log entries
            assessment_scores: Dict of week -> {pre_score, post_score}
            program_completion: Whether patient completed program

        Returns:
            Comprehensive report dictionary
        """
        df = self.load_pain_logs(user_id, pain_logs)

        baseline = self.calculate_baseline_metrics(df)
        endpoint = self.calculate_endpoint_metrics(df)
        changes = self.calculate_change_scores(baseline, endpoint)
        weekly_trends = self.calculate_weekly_trends(df)
        significant = self.calculate_clinically_significant_improvement(changes)

        # Calculate knowledge gain from assessments
        knowledge_gain = {}
        for week, scores in assessment_scores.items():
            if 'pre_score' in scores and 'post_score' in scores:
                gain = scores['post_score'] - scores['pre_score']
                knowledge_gain[week] = {
                    "pre_score": scores['pre_score'],
                    "post_score": scores['post_score'],
                    "gain": round(gain, 2)
                }

        avg_knowledge_gain = np.mean([v['gain'] for v in knowledge_gain.values()]) if knowledge_gain else 0

        # Overall program effectiveness
        improvements_count = sum(1 for v in changes.values() if v.get("improved", False))
        significant_count = sum(1 for v in significant.values() if v)

        report = {
            "user_id": user_id,
            "generated_at": datetime.now().isoformat(),
            "program_completed": program_completion,
            "summary": {
                "metrics_improved": improvements_count,
                "total_metrics": len(self.metrics),
                "clinically_significant_improvements": significant_count,
                "average_knowledge_gain": round(avg_knowledge_gain, 2)
            },
            "baseline_metrics": baseline,
            "endpoint_metrics": endpoint,
            "changes": changes,
            "clinically_significant": significant,
            "weekly_trends": weekly_trends.to_dict('records'),
            "knowledge_gain_by_week": knowledge_gain,
            "recommendations": self._generate_recommendations(changes, significant)
        }

        return report

    def _generate_recommendations(
        self,
        changes: Dict[str, Dict],
        significant: Dict[str, bool]
    ) -> List[str]:
        """Generate personalized recommendations based on outcomes"""
        recommendations = []

        # Pain
        if not significant.get("pain_level", False):
            recommendations.append(
                "Continue practicing pain management techniques learned in the program. "
                "Consider discussing additional interventions with your healthcare provider."
            )

        # Sleep
        if not significant.get("sleep_quality", False):
            recommendations.append(
                "Focus on sleep hygiene practices from Week 6. "
                "Consider keeping a sleep diary to identify patterns."
            )

        # Function
        if significant.get("function_level", True):
            recommendations.append(
                "Great improvement in physical function! Continue your exercise routine "
                "to maintain these gains."
            )

        # General
        recommendations.append(
            "Continue daily pain logging to track your progress and identify triggers."
        )

        recommendations.append(
            "Stay connected with the support group community for ongoing encouragement and shared strategies."
        )

        return recommendations

    def export_report_to_json(self, report: Dict, filepath: str):
        """Export report to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)

    def export_report_to_csv(self, report: Dict, filepath: str):
        """Export summary metrics to CSV"""
        # Flatten the report structure for CSV
        rows = []

        for metric, data in report['changes'].items():
            rows.append({
                "metric": metric,
                "baseline": data.get("baseline"),
                "endpoint": data.get("endpoint"),
                "absolute_change": data.get("absolute_change"),
                "percent_change": data.get("percent_change"),
                "improved": data.get("improved"),
                "clinically_significant": report['clinically_significant'].get(metric, False)
            })

        df = pd.DataFrame(rows)
        df.to_csv(filepath, index=False)


# Example usage
if __name__ == "__main__":
    analytics = OutcomeAnalytics()

    # Sample pain logs
    sample_logs = [
        {
            "log_date": "2024-01-01",
            "pain_level": 7,
            "sleep_quality": 4,
            "fatigue_level": 8,
            "anxiety_level": 6,
            "function_level": 4
        },
        {
            "log_date": "2024-01-15",
            "pain_level": 6,
            "sleep_quality": 5,
            "fatigue_level": 7,
            "anxiety_level": 5,
            "function_level": 5
        },
        {
            "log_date": "2024-02-15",
            "pain_level": 5,
            "sleep_quality": 6,
            "fatigue_level": 6,
            "anxiety_level": 4,
            "function_level": 6
        }
    ]

    # Sample assessment scores
    sample_assessments = {
        1: {"pre_score": 60, "post_score": 85},
        2: {"pre_score": 65, "post_score": 90},
    }

    # Generate report
    report = analytics.generate_patient_report(
        user_id=1,
        pain_logs=sample_logs,
        assessment_scores=sample_assessments,
        program_completion=True
    )

    # Export
    analytics.export_report_to_json(report, "patient_outcome_report.json")
    analytics.export_report_to_csv(report, "patient_outcome_summary.csv")

    print("Report generated successfully!")
    print(f"Improvements: {report['summary']['metrics_improved']}/{report['summary']['total_metrics']}")
    print(f"Clinically Significant: {report['summary']['clinically_significant_improvements']}")
