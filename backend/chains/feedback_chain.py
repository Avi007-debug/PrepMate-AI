# File: backend/chains/feedback_chain.py
import os
import json
import asyncio
from typing import Dict, Any

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from config import settings


class FeedbackChain:
    """
    Evaluate an answer using LLM.
    Exposes:
      - async _evaluate_answer(question, answer): core async call
      - evaluate_answer(question, answer): synchronous wrapper returning a dict with keys 'score' and 'feedback'
    """

    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            openai_api_key=settings.OPENAI_API_KEY,
        )
        self.prompt = self._load_prompt()
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def _load_prompt(self) -> PromptTemplate:
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "feedback_prompt.txt")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                template = f.read()
        except FileNotFoundError:
            # Instruct model to return strict JSON for easy parsing
            template = (
                "You are an expert interviewer. Given the `question` and a candidate `answer`, "
                "evaluate the answer and return a JSON object with exactly two fields:\n"
                "  - score: integer between 1 and 5 (5 = excellent)\n"
                "  - feedback: short constructive feedback (one or two sentences)\n\n"
                "Return only the JSON object.\n\n"
                "Question: {question}\n"
                "Answer: {answer}\n\n"
                "JSON:"
            )

        return PromptTemplate(
            input_variables=["question", "answer"],
            template=template,
        )

    async def _evaluate_answer(self, question: str, answer: str) -> str:
        result = await self.chain.arun(question=question, answer=answer)
        return result.strip()

    def evaluate_answer(self, question: str, answer: str) -> Dict[str, Any]:
        """
        Synchronous wrapper that returns a parsed dict: {'score': int, 'feedback': str, 'raw': str}
        If JSON parsing fails, 'raw' will contain the model output and 'score' may be None.
        """
        raw = asyncio.run(self._evaluate_answer(question, answer))
        parsed = {"score": None, "feedback": "", "raw": raw}
        try:
            # Try to parse JSON directly
            data = json.loads(raw)
            if isinstance(data, dict):
                parsed["score"] = int(data.get("score")) if data.get("score") is not None else None
                parsed["feedback"] = str(data.get("feedback", "")).strip()
                parsed["raw"] = raw
                return parsed
        except Exception:
            pass

        # Fallback: attempt to extract a numeric score like "score: 4" and the rest as feedback
        try:
            lower = raw.lower()
            score = None
            if "score" in lower:
                # simple extraction
                for token in raw.replace("\n", " ").split():
                    if token.strip().rstrip(",.").isdigit():
                        candidate = int(token.strip().rstrip(",."))
                        if 1 <= candidate <= 5:
                            score = candidate
                            break
            parsed["score"] = score
            # use remainder as feedback
            parsed["feedback"] = raw
        except Exception:
            parsed["feedback"] = raw

        return parsed
