"""
Interview session management
"""
from typing import Dict, List, Optional
import uuid
from datetime import datetime
from chains.question_chain import QuestionChain
from chains.feedback_chain import FeedbackChain
from core.utils import generate_session_id, calculate_average_score, format_interview_summary, log_info, log_error
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
        self.current_question_index = 0
        self.scores: List[float] = []
        self.state = "not_started"  # not_started, in_progress, completed
        self.created_at = datetime.now()
        self.completed_at: Optional[datetime] = None
    
    def add_question(self, question: str) -> int:
        """Add a question to the session"""
        question_id = self.current_question_id
        self.questions.append({
            "id": question_id,
            "question": question,
            "topic": self.topics[question_id % len(self.topics)] if self.topics else "general"
        })
        self.current_question_id += 1
        return question_id
    
    def add_answer(self, question_id: int, answer: str, feedback: str, score: float):
        """Record an answer with feedback"""
        self.answers.append({
            "question_id": question_id,
            "answer": answer,
            "feedback": feedback,
            "score": score,
            "timestamp": datetime.now().isoformat()
        })
        self.scores.append(score)
    
    def get_current_question(self) -> Optional[Dict]:
        """Get the current question"""
        if self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None
    
    def move_to_next_question(self):
        """Move to the next question"""
        self.current_question_index += 1
    
    def get_average_score(self) -> float:
        """Calculate average score"""
        return calculate_average_score(self.scores)
    
    def is_complete(self) -> bool:
        """Check if interview is complete"""
        return len(self.answers) >= settings.MAX_QUESTIONS
    
    def mark_complete(self):
        """Mark interview as complete"""
        self.state = "completed"
        self.completed_at = datetime.now()
    
    def get_progress(self) -> Dict:
        """Get interview progress"""
        return {
            "total_questions": settings.MAX_QUESTIONS,
            "answered_questions": len(self.answers),
            "remaining_questions": settings.MAX_QUESTIONS - len(self.answers),
            "current_question_number": len(self.answers) + 1,
            "progress_percentage": (len(self.answers) / settings.MAX_QUESTIONS) * 100
        }


class InterviewManager:
    """Manages interview sessions and coordinates chains"""
    
    def __init__(self):
        self.sessions: Dict[str, InterviewSession] = {}
        self.question_chain = QuestionChain()
        self.feedback_chain = FeedbackChain()
        log_info("InterviewManager initialized")
    
    async def start_interview(self, role: str, difficulty: str, topics: List[str]) -> dict:
        """
        Start a new interview session
        
        Args:
            role: Job role for the interview
            difficulty: Difficulty level (easy, medium, hard)
            topics: List of topics to cover
            
        Returns:
            dict with session_id, first question, and question_id
        """
        try:
            session_id = generate_session_id()
            session = InterviewSession(session_id, role, difficulty, topics)
            self.sessions[session_id] = session
            
            log_info(f"Starting interview session {session_id} for role: {role}")
            
            # Update state to in_progress
            session.state = "in_progress"
            
            # Generate first question
            first_topic = topics[0] if topics else "general"
            question = await self.question_chain.generate_question(
                role=role,
                difficulty=difficulty,
                topic=first_topic,
                previous_questions=[]
            )
            
            question_id = session.add_question(question)
            
            log_info(f"Generated first question for session {session_id}")
            
            return {
                "session_id": session_id,
                "question": question,
                "question_id": question_id,
                "progress": session.get_progress()
            }
        except Exception as e:
            log_error(f"Error starting interview: {str(e)}")
            raise
    
    def get_current_question(self, session_id: str) -> Optional[Dict]:
        """
        Get the current question for a session
        
        Args:
            session_id: Session identifier
            
        Returns:
            Current question dict or None
        """
        if session_id not in self.sessions:
            log_error(f"Session {session_id} not found")
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        return session.get_current_question()
    
    async def submit_answer(self, session_id: str, question_id: int, answer: str) -> dict:
        """
        Submit an answer for the current question
        
        Args:
            session_id: Session identifier
            question_id: Question identifier
            answer: User's answer text
            
        Returns:
            dict with feedback, score, and next question info
        """
        try:
            if session_id not in self.sessions:
                log_error(f"Session {session_id} not found")
                raise ValueError(f"Session {session_id} not found")
            
            session = self.sessions[session_id]
            
            # Get the question
            question_data = next(
                (q for q in session.questions if q["id"] == question_id), 
                None
            )
            if not question_data:
                log_error(f"Question {question_id} not found in session {session_id}")
                raise ValueError(f"Question {question_id} not found")
            
            log_info(f"Processing answer for session {session_id}, question {question_id}")
            
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
            
            log_info(f"Answer recorded with score: {feedback_result['score']}")
            
            # Check if interview is complete
            is_complete = session.is_complete()
            
            result = {
                "feedback": feedback_result["feedback"],
                "score": feedback_result["score"],
                "is_complete": is_complete,
                "progress": session.get_progress()
            }
            
            # Generate next question if not complete
            if not is_complete:
                next_question_data = await self.next_question(session_id)
                result.update(next_question_data)
            else:
                session.mark_complete()
                log_info(f"Interview session {session_id} completed")
            
            return result
        except Exception as e:
            log_error(f"Error submitting answer: {str(e)}")
            raise
    
    async def next_question(self, session_id: str) -> dict:
        """
        Generate and return the next question
        
        Args:
            session_id: Session identifier
            
        Returns:
            dict with next_question and next_question_id
        """
        try:
            if session_id not in self.sessions:
                raise ValueError(f"Session {session_id} not found")
            
            session = self.sessions[session_id]
            
            # Move to next question
            session.move_to_next_question()
            
            # Generate next question
            next_topic_index = len(session.answers) % len(session.topics) if session.topics else 0
            next_topic = session.topics[next_topic_index] if session.topics else "general"
            previous_questions = [q["question"] for q in session.questions]
            
            next_question = await self.question_chain.generate_question(
                role=session.role,
                difficulty=session.difficulty,
                topic=next_topic,
                previous_questions=previous_questions
            )
            
            next_question_id = session.add_question(next_question)
            
            log_info(f"Generated next question for session {session_id}")
            
            return {
                "next_question": next_question,
                "next_question_id": next_question_id,
                "topic": next_topic
            }
        except Exception as e:
            log_error(f"Error generating next question: {str(e)}")
            raise
    
    def is_complete(self, session_id: str) -> bool:
        """
        Check if interview is complete
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if complete, False otherwise
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        return self.sessions[session_id].is_complete()
    
    async def generate_summary(self, session_id: str) -> dict:
        """
        Generate comprehensive interview summary
        
        Args:
            session_id: Session identifier
            
        Returns:
            Complete interview summary with statistics and analysis
        """
        try:
            if session_id not in self.sessions:
                log_error(f"Session {session_id} not found")
                raise ValueError(f"Session {session_id} not found")
            
            session = self.sessions[session_id]
            
            log_info(f"Generating summary for session {session_id}")
            
            # Calculate statistics
            average_score = session.get_average_score()
            total_questions = len(session.questions)
            total_answers = len(session.answers)
            
            # Categorize performance
            if average_score >= 8:
                performance_level = "Excellent"
            elif average_score >= 6:
                performance_level = "Good"
            elif average_score >= 4:
                performance_level = "Fair"
            else:
                performance_level = "Needs Improvement"
            
            # Get strongest and weakest areas
            topic_scores: Dict[str, List[float]] = {}
            for i, answer in enumerate(session.answers):
                if i < len(session.questions):
                    topic = session.questions[i]["topic"]
                    if topic not in topic_scores:
                        topic_scores[topic] = []
                    topic_scores[topic].append(answer["score"])
            
            topic_averages = {
                topic: calculate_average_score(scores) 
                for topic, scores in topic_scores.items()
            }
            
            strongest_topic = max(topic_averages.items(), key=lambda x: x[1]) if topic_averages else ("N/A", 0)
            weakest_topic = min(topic_averages.items(), key=lambda x: x[1]) if topic_averages else ("N/A", 0)
            
            summary = {
                "session_id": session_id,
                "role": session.role,
                "difficulty": session.difficulty,
                "topics": session.topics,
                "state": session.state,
                "created_at": session.created_at.isoformat(),
                "completed_at": session.completed_at.isoformat() if session.completed_at else None,
                "statistics": {
                    "total_questions": total_questions,
                    "total_answers": total_answers,
                    "average_score": round(average_score, 2),
                    "performance_level": performance_level,
                    "completion_rate": round((total_answers / settings.MAX_QUESTIONS) * 100, 2)
                },
                "topic_performance": topic_averages,
                "strongest_topic": strongest_topic[0],
                "strongest_topic_score": round(strongest_topic[1], 2),
                "weakest_topic": weakest_topic[0],
                "weakest_topic_score": round(weakest_topic[1], 2),
                "questions_and_answers": [
                    {
                        "question_number": i + 1,
                        "topic": session.questions[i]["topic"],
                        "question": session.questions[i]["question"],
                        "answer": session.answers[i]["answer"] if i < len(session.answers) else None,
                        "feedback": session.answers[i]["feedback"] if i < len(session.answers) else None,
                        "score": session.answers[i]["score"] if i < len(session.answers) else None,
                        "timestamp": session.answers[i]["timestamp"] if i < len(session.answers) else None
                    }
                    for i in range(len(session.questions))
                ]
            }
            
            log_info(f"Summary generated for session {session_id} with average score: {average_score}")
            
            return format_interview_summary(summary)
        except Exception as e:
            log_error(f"Error generating summary: {str(e)}")
            raise
    
    async def get_summary(self, session_id: str) -> dict:
        """Alias for generate_summary for backward compatibility"""
        return await self.generate_summary(session_id)
    
    def get_session_state(self, session_id: str) -> str:
        """
        Get current state of a session
        
        Args:
            session_id: Session identifier
            
        Returns:
            Current state string
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        return self.sessions[session_id].state
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if deleted, False if not found
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            log_info(f"Deleted session {session_id}")
            return True
        return False
    
    def get_all_sessions(self) -> List[str]:
        """Get list of all active session IDs"""
        return list(self.sessions.keys())
