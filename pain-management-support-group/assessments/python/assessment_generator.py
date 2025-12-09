"""
Assessment Generator for Pre/Post Tests
Generates multiple choice tests based on curriculum content
"""
import json
import random
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class QuestionDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SCALE = "scale"


@dataclass
class Question:
    """Question data structure"""
    id: str
    text: str
    type: QuestionType
    options: List[str]
    correct_answer: str
    explanation: str
    topic: str
    difficulty: QuestionDifficulty
    points: int = 1


@dataclass
class Assessment:
    """Assessment data structure"""
    week_number: int
    assessment_type: str  # 'pre_test' or 'post_test'
    title: str
    description: str
    questions: List[Question]
    total_points: int
    passing_score: float
    time_limit_minutes: Optional[int] = None


class AssessmentGenerator:
    """
    Generate assessments for each week of the program
    """

    def __init__(self):
        self.question_bank = self._load_question_bank()

    def _load_question_bank(self) -> Dict[int, List[Question]]:
        """Load questions organized by week"""
        # This would typically load from a database or file
        # For now, we'll create sample questions
        return self._create_sample_questions()

    def _create_sample_questions(self) -> Dict[int, List[Question]]:
        """Create sample questions for each week"""
        questions_by_week = {}

        # Week 1: Understanding Pain
        questions_by_week[1] = [
            Question(
                id="w1_q1",
                text="What is the primary difference between acute and chronic pain?",
                type=QuestionType.MULTIPLE_CHOICE,
                options=[
                    "A. Acute pain is worse than chronic pain",
                    "B. Acute pain serves a protective function while chronic pain persists beyond healing",
                    "C. Chronic pain only occurs in elderly people",
                    "D. There is no difference"
                ],
                correct_answer="B",
                explanation="Acute pain is a warning signal that protects us from harm, while chronic pain persists beyond the expected healing time and may not serve a protective purpose.",
                topic="Pain Science",
                difficulty=QuestionDifficulty.EASY
            ),
            Question(
                id="w1_q2",
                text="Which nerve fibers are responsible for transmitting sharp, localized pain?",
                type=QuestionType.MULTIPLE_CHOICE,
                options=[
                    "A. C-fibers",
                    "B. A-delta fibers",
                    "C. Motor neurons",
                    "D. Sympathetic fibers"
                ],
                correct_answer="B",
                explanation="A-delta fibers are myelinated and transmit sharp, well-localized pain quickly. C-fibers transmit dull, aching pain more slowly.",
                topic="Nerve Anatomy",
                difficulty=QuestionDifficulty.MEDIUM
            ),
            Question(
                id="w1_q3",
                text="The spinothalamic tract carries pain signals to which structure in the brain?",
                type=QuestionType.MULTIPLE_CHOICE,
                options=[
                    "A. Cerebellum",
                    "B. Thalamus",
                    "C. Hippocampus",
                    "D. Medulla"
                ],
                correct_answer="B",
                explanation="The spinothalamic tract carries pain and temperature information from the spinal cord to the thalamus, which then relays it to the cerebral cortex.",
                topic="Pain Pathways",
                difficulty=QuestionDifficulty.MEDIUM
            ),
            Question(
                id="w1_q4",
                text="Which branch of the autonomic nervous system is activated during the stress response to pain?",
                type=QuestionType.MULTIPLE_CHOICE,
                options=[
                    "A. Parasympathetic",
                    "B. Sympathetic",
                    "C. Somatic",
                    "D. Enteric"
                ],
                correct_answer="B",
                explanation="The sympathetic nervous system is activated during stress and pain, triggering the 'fight or flight' response with increased heart rate and cortisol release.",
                topic="Autonomic Nervous System",
                difficulty=QuestionDifficulty.EASY
            ),
        ]

        # Week 2: Pharmacology
        questions_by_week[2] = [
            Question(
                id="w2_q1",
                text="What is the maximum recommended daily dose of acetaminophen (Tylenol) for most adults?",
                type=QuestionType.MULTIPLE_CHOICE,
                options=[
                    "A. 1000mg",
                    "B. 2000mg",
                    "C. 3000-4000mg",
                    "D. 6000mg"
                ],
                correct_answer="C",
                explanation="The maximum recommended daily dose is 3000-4000mg for adults. Higher doses increase the risk of liver damage (hepatotoxicity).",
                topic="OTC Medications",
                difficulty=QuestionDifficulty.EASY
            ),
            Question(
                id="w2_q2",
                text="Which opioid receptors are primarily responsible for pain relief?",
                type=QuestionType.MULTIPLE_CHOICE,
                options=[
                    "A. Mu (μ) receptors",
                    "B. Alpha receptors",
                    "C. Beta receptors",
                    "D. GABA receptors"
                ],
                correct_answer="A",
                explanation="Mu (μ) opioid receptors are the primary mediators of analgesia (pain relief) when activated by opioids or endogenous endorphins.",
                topic="Opioid Mechanisms",
                difficulty=QuestionDifficulty.MEDIUM
            ),
            Question(
                id="w2_q3",
                text="NSAIDs work by inhibiting which enzyme?",
                type=QuestionType.MULTIPLE_CHOICE,
                options=[
                    "A. Monoamine oxidase",
                    "B. Cyclooxygenase (COX)",
                    "C. Acetylcholinesterase",
                    "D. Protease"
                ],
                correct_answer="B",
                explanation="NSAIDs inhibit cyclooxygenase (COX) enzymes, which reduces prostaglandin production and thereby reduces inflammation and pain.",
                topic="NSAID Mechanisms",
                difficulty=QuestionDifficulty.MEDIUM
            ),
        ]

        # Week 3-8: Add more questions for remaining weeks
        # (Abbreviated for space - would include 15 questions per week)

        return questions_by_week

    def generate_assessment(
        self,
        week_number: int,
        assessment_type: str,
        num_questions: int = 15,
        difficulty_distribution: Optional[Dict[QuestionDifficulty, float]] = None
    ) -> Assessment:
        """
        Generate an assessment for a specific week

        Args:
            week_number: Week number (1-8)
            assessment_type: 'pre_test' or 'post_test'
            num_questions: Number of questions to include
            difficulty_distribution: Optional distribution (easy: 0.4, medium: 0.4, hard: 0.2)

        Returns:
            Assessment object
        """
        if week_number not in self.question_bank:
            raise ValueError(f"No questions available for week {week_number}")

        # Default difficulty distribution
        if difficulty_distribution is None:
            difficulty_distribution = {
                QuestionDifficulty.EASY: 0.4,
                QuestionDifficulty.MEDIUM: 0.4,
                QuestionDifficulty.HARD: 0.2
            }

        # Select questions based on difficulty distribution
        available_questions = self.question_bank[week_number]
        selected_questions = []

        for difficulty, proportion in difficulty_distribution.items():
            num_for_difficulty = int(num_questions * proportion)
            difficulty_questions = [q for q in available_questions if q.difficulty == difficulty]

            if len(difficulty_questions) < num_for_difficulty:
                # If not enough questions, add what we have
                selected_questions.extend(difficulty_questions)
            else:
                selected_questions.extend(random.sample(difficulty_questions, num_for_difficulty))

        # Fill remaining slots if needed
        while len(selected_questions) < num_questions and len(available_questions) > len(selected_questions):
            remaining = [q for q in available_questions if q not in selected_questions]
            if remaining:
                selected_questions.append(random.choice(remaining))
            else:
                break

        # Shuffle questions
        random.shuffle(selected_questions)

        # Calculate total points
        total_points = sum(q.points for q in selected_questions)

        # Create assessment
        assessment = Assessment(
            week_number=week_number,
            assessment_type=assessment_type,
            title=f"Week {week_number} {'Pre-Test' if assessment_type == 'pre_test' else 'Post-Test'}",
            description=f"Assessment covering Week {week_number} material",
            questions=selected_questions,
            total_points=total_points,
            passing_score=70.0,
            time_limit_minutes=30
        )

        return assessment

    def export_to_json(self, assessment: Assessment, filepath: str):
        """Export assessment to JSON file"""
        data = {
            "week_number": assessment.week_number,
            "assessment_type": assessment.assessment_type,
            "title": assessment.title,
            "description": assessment.description,
            "total_points": assessment.total_points,
            "passing_score": assessment.passing_score,
            "time_limit_minutes": assessment.time_limit_minutes,
            "questions": [
                {
                    "id": q.id,
                    "text": q.text,
                    "type": q.type.value,
                    "options": q.options,
                    "correct_answer": q.correct_answer,
                    "explanation": q.explanation,
                    "topic": q.topic,
                    "difficulty": q.difficulty.value,
                    "points": q.points
                }
                for q in assessment.questions
            ]
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def score_assessment(
        self,
        assessment: Assessment,
        user_answers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Score a completed assessment

        Args:
            assessment: The assessment being scored
            user_answers: Dictionary of question_id -> user_answer

        Returns:
            Dict with scoring results
        """
        correct_count = 0
        total_points = 0
        points_earned = 0
        results = []

        for question in assessment.questions:
            user_answer = user_answers.get(question.id)
            is_correct = user_answer == question.correct_answer

            if is_correct:
                correct_count += 1
                points_earned += question.points

            total_points += question.points

            results.append({
                "question_id": question.id,
                "question_text": question.text,
                "user_answer": user_answer,
                "correct_answer": question.correct_answer,
                "is_correct": is_correct,
                "points_earned": question.points if is_correct else 0,
                "explanation": question.explanation
            })

        percentage = (points_earned / total_points * 100) if total_points > 0 else 0
        passed = percentage >= assessment.passing_score

        return {
            "assessment_title": assessment.title,
            "week_number": assessment.week_number,
            "total_questions": len(assessment.questions),
            "correct_count": correct_count,
            "total_points": total_points,
            "points_earned": points_earned,
            "percentage": round(percentage, 2),
            "passed": passed,
            "passing_score": assessment.passing_score,
            "results": results
        }


# Example usage
if __name__ == "__main__":
    generator = AssessmentGenerator()

    # Generate Week 1 pre-test
    week1_pretest = generator.generate_assessment(
        week_number=1,
        assessment_type="pre_test",
        num_questions=15
    )

    # Export to JSON
    generator.export_to_json(
        week1_pretest,
        "week1_pretest.json"
    )

    print(f"Generated: {week1_pretest.title}")
    print(f"Questions: {len(week1_pretest.questions)}")
    print(f"Total Points: {week1_pretest.total_points}")

    # Simulate scoring
    sample_answers = {
        "w1_q1": "B",
        "w1_q2": "B",
        "w1_q3": "B",
        "w1_q4": "B"
    }

    score_result = generator.score_assessment(week1_pretest, sample_answers)
    print(f"\nScore: {score_result['percentage']}%")
    print(f"Passed: {score_result['passed']}")
