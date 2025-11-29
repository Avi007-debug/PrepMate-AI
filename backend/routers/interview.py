"""
Interview API endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from core.interview_manager import InterviewManager

router = APIRouter(prefix="/api/interview", tags=["interview"])
interview_manager = InterviewManager()


class InterviewStartRequest(BaseModel):
    role: str
    difficulty: str
    topics: List[str]


class AnswerRequest(BaseModel):
    session_id: str
    question_id: int
    answer: str


class InterviewStartResponse(BaseModel):
    session_id: str
    question: str
    question_id: int


class FeedbackResponse(BaseModel):
    feedback: str
    score: float
    next_question: Optional[str] = None
    next_question_id: Optional[int] = None
    is_complete: bool = False


@router.post("/start", response_model=InterviewStartResponse)
async def start_interview(request: InterviewStartRequest):
    """Start a new interview session"""
    try:
        result = await interview_manager.start_interview(
            role=request.role,
            difficulty=request.difficulty,
            topics=request.topics
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/answer", response_model=FeedbackResponse)
async def submit_answer(request: AnswerRequest):
    """Submit an answer and get feedback"""
    try:
        result = await interview_manager.process_answer(
            session_id=request.session_id,
            question_id=request.question_id,
            answer=request.answer
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary/{session_id}")
async def get_summary(session_id: str):
    """Get interview summary"""
    try:
        summary = await interview_manager.get_summary(session_id)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
