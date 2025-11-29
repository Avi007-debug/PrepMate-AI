# File: backend/chains/feedback_chain.py

import os
import json
from typing import Dict

try:
    from langchain_groq import ChatGroq
    GROQ_AVAILABLE = True
except ImportError:
    from langchain_openai import ChatOpenAI
    GROQ_AVAILABLE = False

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

from config import settings


class FeedbackChain:
    """
    Evaluate candidate answers using modern LangChain LCEL.
    Uses RunnableSequence instead of the removed LLMChain.
    """

    def __init__(self):
        # Choose LLM provider
        if GROQ_AVAILABLE and settings.GROQ_API_KEY:
            self.llm = ChatGroq(
                model=settings.LLM_MODEL,
                groq_api_key=settings.GROQ_API_KEY,
                temperature=settings.LLM_TEMPERATURE,
            )
        else:
            self.llm = ChatOpenAI(
                model=settings.LLM_MODEL,
                api_key=settings.OPENAI_API_KEY,
                temperature=settings.LLM_TEMPERATURE,
            )

        self.prompt = self._load_prompt()

        # LCEL chain
        self.chain = RunnableSequence(self.prompt | self.llm)

    def _load_prompt(self) -> PromptTemplate:
        """Load evaluation prompt."""
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "feedback_prompt.txt")

        if not os.path.exists(prompt_path):
            template = (
                "You are an expert interviewer. Given the `question` and a candidate `answer`, "
                "evaluate the answer and return a JSON object with exactly two fields:\n"
                "  - score: number from 0 to 10\n"
                "  - feedback: detailed constructive explanation\n\n"
                "Return ONLY valid JSON.\n\n"
                "Question: {question}\n"
                "Answer: {answer}\n\n"
                "JSON:"
            )
        else:
            with open(prompt_path, "r", encoding="utf-8") as f:
                template = f.read()

        return PromptTemplate(
            template=template,
            input_variables=["question", "answer"],
        )

    async def generate_feedback(self, question: str, answer: str) -> Dict[str, float]:
        """
        Generates feedback score + explanation.
        Returns:
            { "score": float, "feedback": str }
        """
        raw = await self.chain.ainvoke({"question": question, "answer": answer})
        raw_text = raw.content.strip()

        # Remove markdown code blocks
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1].strip()
            raw_text = raw_text.replace("json", "").strip()

        # Try JSON parsing
        try:
            data = json.loads(raw_text)

            score = None
            feedback = None

            # score extraction patterns
            if "score" in data:
                score = float(data["score"])
            elif "scores" in data and isinstance(data["scores"], dict):
                score = float(data["scores"].get("overall", 5.0))

            # feedback extraction
            if "feedback" in data:
                feedback = str(data["feedback"])
            elif "detailed_feedback" in data:
                feedback = str(data["detailed_feedback"])

            return {
                "score": score if score is not None else 5.0,
                "feedback": feedback if feedback else raw_text,
            }

        except Exception:
            pass

        # Fallback if JSON is malformed
        return {
            "score": 5.0,
            "feedback": raw_text,
        }
