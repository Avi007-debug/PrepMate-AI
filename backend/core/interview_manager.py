"""
Interview session management
"""
from typing import Dict, List, Optional
import uuid
from chains.question_chain import QuestionChain
from chains.feedback_chain import FeedbackChain
from core.utils import generate_session_id
from config import settings


class InterviewSession:
    """Represents an active interview session"""
    
    def __init__(self, session_id: str, role: str, difficulty: str, topics: List[str]):
        self.session_id = session_id
        self.role = role
        self.difficulty = difficulty
        self.topics = topics
        self.questions: List[Dict] = []
        self.answers: List[Dict] = []
        self.current_question_id = 0
        self.scores: List[float] = []
    
    def add_question(self, question: str) -> int:
        """Add a question to the session"""
        question_id = self.current_question_id
        self.questions.append({
            "id": question_id,
            "question": question,
            "topic": self.topics[question_id % len(self.topics)]
        })
        self.current_question_id += 1
        return question_id
    
    def add_answer(self, question_id: int, answer: str, feedback: str, score: float):
        """Record an answer with feedback"""
        self.answers.append({
            "question_id": question_id,
            "answer": answer,
            "feedback": feedback,
            "score": score
        })
        self.scores.append(score)
    
    def get_average_score(self) -> float:
        """Calculate average score"""
        if not self.scores:
            return 0.0
        return sum(self.scores) / len(self.scores)
    
    def is_complete(self) -> bool:
        """Check if interview is complete"""
        return len(self.answers) >= settings.MAX_QUESTIONS


class InterviewManager:
    """Manages interview sessions and coordinates chains"""
    
    def __init__(self):
        self.sessions: Dict[str, InterviewSession] = {}
        self.question_chain = QuestionChain()
        self.feedback_chain = FeedbackChain()
    
    async def start_interview(self, role: str, difficulty: str, topics: List[str]) -> dict:
        """Start a new interview session"""
        session_id = generate_session_id()
        session = InterviewSession(session_id, role, difficulty, topics)
        self.sessions[session_id] = session
        
        # Generate first question
        first_topic = topics[0] if topics else "general"
        question = await self.question_chain.generate_question(
            role=role,
            difficulty=difficulty,
            topic=first_topic,
            previous_questions=[]
        )
        
        question_id = session.add_question(question)
        
        return {
            "session_id": session_id,
            "question": question,
            "question_id": question_id
        }
    
    async def process_answer(self, session_id: str, question_id: int, answer: str) -> dict:
        """Process an answer and generate feedback"""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        
        # Get the question
        question_data = next(
            (q for q in session.questions if q["id"] == question_id), 
            None
        )
        if not question_data:
            raise ValueError(f"Question {question_id} not found")
        
        # Generate feedback
        feedback_result = await self.feedback_chain.generate_feedback(
            question=question_data["question"],
            answer=answer
        )
        
        # Record the answer
        session.add_answer(
            question_id=question_id,
            answer=answer,
            feedback=feedback_result["feedback"],
            score=feedback_result["score"]
        )
        
        # Check if interview is complete
        is_complete = session.is_complete()
        
        result = {
            "feedback": feedback_result["feedback"],
            "score": feedback_result["score"],
            "is_complete": is_complete
        }
        
        # Generate next question if not complete
        if not is_complete:
            next_topic = session.topics[len(session.answers) % len(session.topics)]
            previous_questions = [q["question"] for q in session.questions]
            
            next_question = await self.question_chain.generate_question(
                role=session.role,
                difficulty=session.difficulty,
                topic=next_topic,
                previous_questions=previous_questions
            )
            
            next_question_id = session.add_question(next_question)
            result["next_question"] = next_question
            result["next_question_id"] = next_question_id
        
        return result
    
    async def get_summary(self, session_id: str) -> dict:
        """Get interview summary"""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        
        return {
            "session_id": session_id,
            "role": session.role,
            "difficulty": session.difficulty,
            "topics": session.topics,
            "total_questions": len(session.questions),
            "total_answers": len(session.answers),
            "average_score": session.get_average_score(),
            "questions_and_answers": [
                {
                    "question": session.questions[i]["question"],
                    "answer": session.answers[i]["answer"] if i < len(session.answers) else None,
                    "feedback": session.answers[i]["feedback"] if i < len(session.answers) else None,
                    "score": session.answers[i]["score"] if i < len(session.answers) else None,
                }
                for i in range(len(session.questions))
            ]
        }
