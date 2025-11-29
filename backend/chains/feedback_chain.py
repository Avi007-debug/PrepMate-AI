"""
Feedback generation chain with graceful fallback to a mock implementation
"""
import os
from typing import Dict
from config import settings


# Try to import LangChain/OpenAI integration; if unavailable, fall back to a lightweight mock
USE_REAL_LLM = False
try:
    if not settings.MOCK_LLM:
        from langchain_openai import ChatOpenAI  # type: ignore
        from langchain.prompts import PromptTemplate  # type: ignore
        from langchain.chains import LLMChain  # type: ignore
        USE_REAL_LLM = True
except Exception:
    USE_REAL_LLM = False


if USE_REAL_LLM:
    class FeedbackChain:
        """Generate feedback for interview answers using LangChain"""

        def __init__(self):
            self.llm = ChatOpenAI(
                model=settings.LLM_MODEL,
                temperature=settings.LLM_TEMPERATURE,
                openai_api_key=settings.OPENAI_API_KEY,
            )
            self.prompt = self._load_prompt()
            self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

        def _load_prompt(self) -> PromptTemplate:
            """Load feedback generation prompt"""
            prompt_path = os.path.join(
                os.path.dirname(__file__),
                "prompts",
                "feedback_prompt.txt",
            )
            try:
                with open(prompt_path, "r") as f:
                    template = f.read()
            except FileNotFoundError:
                template = (
                    "You are an experienced technical interviewer evaluating a candidate's response.\n\n"
                    "Interview Question:\n{question}\n\nCandidate's Answer:\n{answer}\n\nProvide comprehensive feedback...\n\n"
                    "Format your response EXACTLY as:\nFEEDBACK: [Your detailed feedback here]\nSCORE: [numerical score]"
                )

            return PromptTemplate(input_variables=["question", "answer"], template=template)

        async def generate_feedback(self, question: str, answer: str) -> Dict[str, float]:
            result = await self.chain.arun(question=question, answer=answer)

            # Parse output
            lines = result.strip().split("\n")
            feedback = ""
            score = 0.0
            for line in lines:
                if line.startswith("FEEDBACK:"):
                    feedback = line.replace("FEEDBACK:", "").strip()
                elif line.startswith("SCORE:"):
                    try:
                        score = float(line.replace("SCORE:", "").strip())
                    except ValueError:
                        score = 5.0

            if not feedback:
                feedback = result.strip()

            return {"feedback": feedback, "score": score}

else:
    class FeedbackChain:
        """Simple mock feedback generator used when LangChain isn't available or mocked."""

        def __init__(self):
            pass

        def _load_prompt(self):
            return None

        async def generate_feedback(self, question: str, answer: str) -> Dict[str, float]:
            # Deterministic mock feedback
            feedback = f"Mock feedback: Your answer to '{question[:60]}' is concise and covers main points."
            score = 7.0
            return {"feedback": feedback, "score": score}
