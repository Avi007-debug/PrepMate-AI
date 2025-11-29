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
        result = await interview_manager.submit_answer(
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
        summary = await interview_manager.generate_summary(session_id)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/current/{session_id}")
async def get_current_question(session_id: str):
    """Get current question for a session"""
    try:
        question = interview_manager.get_current_question(session_id)
        if question is None:
            raise HTTPException(status_code=404, detail="No current question found")
        return question
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{session_id}")
async def get_session_status(session_id: str):
    """Get session status and progress"""
    try:
        state = interview_manager.get_session_state(session_id)
        is_complete = interview_manager.is_complete(session_id)
        return {
            "session_id": session_id,
            "state": state,
            "is_complete": is_complete
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a session"""
    try:
        deleted = interview_manager.delete_session(session_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Session not found")
        return {"message": "Session deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Additional public endpoints (requested) ---


@router.post("/interview/start", response_model=InterviewStartResponse)
async def public_start_interview(request: InterviewStartRequest):
    """Public POST /interview/start - start a new interview session"""
    try:
        result = await interview_manager.start_interview(
            role=request.role,
            difficulty=request.difficulty,
            topics=request.topics,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/interview/question")
async def public_get_current_question(session_id: str):
    """Public GET /interview/question?session_id=... - get the current question"""
    try:
        question = interview_manager.get_current_question(session_id)
        if question is None:
            raise HTTPException(status_code=404, detail="No current question found")
        return question
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/interview/answer", response_model=FeedbackResponse)
async def public_submit_answer(request: AnswerRequest):
    """Public POST /interview/answer - submit an answer and receive feedback"""
    try:
        result = await interview_manager.submit_answer(
            session_id=request.session_id,
            question_id=request.question_id,
            answer=request.answer,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/interview/next")
async def public_next_question(session_id: str):
    """Public GET /interview/next?session_id=... - generate and return the next question"""
    try:
        next_q = await interview_manager.next_question(session_id)
        return next_q
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/interview/summary")
async def public_get_summary(session_id: str):
    """Public GET /interview/summary?session_id=... - get the interview summary"""
    try:
        summary = await interview_manager.generate_summary(session_id)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
