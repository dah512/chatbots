#!/usr/bin/env python3
"""
Demonstration of the Assessment Generator System
Shows how the weekly pre/post tests are created and scored
"""

from assessment_generator import AssessmentGenerator
from dataclasses import asdict
import json

print("="*70)
print("PAIN MANAGEMENT SUPPORT GROUP - ASSESSMENT SYSTEM DEMONSTRATION")
print("="*70)
print()

# Initialize the generator
gen = AssessmentGenerator()

# Generate a Week 1 Pre-Test
print("📝 GENERATING WEEK 1 PRE-TEST...")
print()

assessment = gen.generate_assessment(
    week_number=1,
    assessment_type='pre',
    num_questions=10
)

print(f"Title: {assessment.title}")
print(f"Description: {assessment.description}")
print(f"Total Questions: {len(assessment.questions)}")
print(f"Total Points: {assessment.total_points}")
print(f"Passing Score: {assessment.passing_score}%")
print(f"Time Limit: {assessment.time_limit_minutes} minutes")
print()

# Show first 3 sample questions
print("="*70)
print("SAMPLE QUESTIONS:")
print("="*70)
print()

for i, q in enumerate(assessment.questions[:3], 1):
    print(f"Question {i} [{q.difficulty.value.upper()}] - {q.topic}")
    print(f"{q.text}")
    print()
    for option in q.options:
        print(f"  {option}")
    print()
    print(f"✓ Correct Answer: {q.correct_answer}")
    print(f"💡 Explanation: {q.explanation}")
    print()
    print("-"*70)
    print()

# Simulate taking the test
print("="*70)
print("SCORING DEMONSTRATION")
print("="*70)
print()

# Create some sample user answers (simulating a student)
user_answers = {}
for i, q in enumerate(assessment.questions):
    # Randomly get 70% correct for demonstration
    if i < 7:  # Get first 7 correct
        user_answers[q.id] = q.correct_answer
    else:  # Get last 3 wrong
        # Pick a wrong answer
        wrong_options = [opt[0] for opt in q.options if opt[0] != q.correct_answer]
        user_answers[q.id] = wrong_options[0] if wrong_options else 'A'

print("Student submitted answers...")
print()

# Score the assessment
scoring_result = gen.score_assessment(assessment, user_answers)

print(f"📊 SCORING RESULTS:")
print(f"  Correct Answers: {scoring_result['correct_count']} / {scoring_result['total_questions']}")
print(f"  Points Earned: {scoring_result['points_earned']} / {scoring_result['total_points']}")
print(f"  Percentage: {scoring_result['percentage']:.1f}%")
print(f"  Status: {'✅ PASSED' if scoring_result['passed'] else '❌ FAILED'}")
print(f"  Passing Threshold: {assessment.passing_score}%")
print()

# Show question-by-question breakdown
print("="*70)
print("DETAILED BREAKDOWN:")
print("="*70)
print()

for i, q in enumerate(assessment.questions, 1):
    user_ans = user_answers.get(q.id, "No answer")
    correct = user_ans == q.correct_answer
    status = "✓ Correct" if correct else "✗ Incorrect"

    print(f"{i}. {q.text[:60]}...")
    print(f"   Your Answer: {user_ans} | Correct: {q.correct_answer} | {status}")
    if not correct:
        print(f"   💡 {q.explanation}")
    print()

# Export to JSON
print("="*70)
print("EXPORTING ASSESSMENT DATA")
print("="*70)
print()

# Convert to dict for JSON export
assessment_dict = {
    'week_number': assessment.week_number,
    'assessment_type': assessment.assessment_type,
    'title': assessment.title,
    'description': assessment.description,
    'total_points': assessment.total_points,
    'passing_score': assessment.passing_score,
    'time_limit_minutes': assessment.time_limit_minutes,
    'questions': [
        {
            'id': q.id,
            'text': q.text,
            'type': q.type.value,
            'options': q.options,
            'correct_answer': q.correct_answer,
            'explanation': q.explanation,
            'topic': q.topic,
            'difficulty': q.difficulty.value,
            'points': q.points
        } for q in assessment.questions
    ]
}

with open('sample_week1_assessment.json', 'w') as f:
    json.dump(assessment_dict, f, indent=2)

print("✓ Assessment exported to: sample_week1_assessment.json")
print()

# Generate assessments for all weeks
print("="*70)
print("GENERATING ALL 8 WEEKS OF ASSESSMENTS")
print("="*70)
print()

all_assessments = {}
for week in range(1, 9):
    pre_test = gen.generate_assessment(week, 'pre', num_questions=15)
    post_test = gen.generate_assessment(week, 'post', num_questions=15)

    all_assessments[f'week_{week}'] = {
        'pre_test': {
            'title': pre_test.title,
            'questions': len(pre_test.questions),
            'points': pre_test.total_points
        },
        'post_test': {
            'title': post_test.title,
            'questions': len(post_test.questions),
            'points': post_test.total_points
        }
    }

    print(f"Week {week}: {pre_test.title}")
    print(f"  ✓ Pre-test: {len(pre_test.questions)} questions, {pre_test.total_points} points")
    print(f"  ✓ Post-test: {len(post_test.questions)} questions, {post_test.total_points} points")
    print()

print("="*70)
print("DEMONSTRATION COMPLETE!")
print("="*70)
print()
print("The assessment system can:")
print("  • Generate customized tests for each week")
print("  • Mix difficulty levels (easy, medium, hard)")
print("  • Automatically score responses")
print("  • Provide explanations for learning")
print("  • Track progress over time")
print("  • Export data for analysis")
