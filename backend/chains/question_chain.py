"""
Question generation chain with graceful fallback to a mock implementation
"""
import os
from typing import List
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
    # LangChain or its integration not installed — we'll use a local mock implementation
    USE_REAL_LLM = False


if USE_REAL_LLM:
    class QuestionChain:
        """Generate interview questions using LangChain"""

        def __init__(self):
            self.llm = ChatOpenAI(
                model=settings.LLM_MODEL,
                temperature=settings.LLM_TEMPERATURE,
                openai_api_key=settings.OPENAI_API_KEY,
            )
            self.prompt = self._load_prompt()
            self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

        def _load_prompt(self) -> PromptTemplate:
            """Load question generation prompt"""
            prompt_path = os.path.join(
                os.path.dirname(__file__),
                "prompts",
                "question_prompt.txt",
            )
            try:
                with open(prompt_path, "r") as f:
                    template = f.read()
            except FileNotFoundError:
                template = (
                    "You are an expert interviewer. Generate a {difficulty} level interview question "
                    "for a {role} position focusing on {topic}.\n\nPrevious questions asked: {previous_questions}\n\n"
                    "Generate a unique question that hasn't been asked before.\n\nQuestion:"
                )

            return PromptTemplate(
                input_variables=["role", "difficulty", "topic", "previous_questions"],
                template=template,
            )

        async def generate_question(
            self,
            role: str,
            difficulty: str,
            topic: str,
            previous_questions: List[str],
        ) -> str:
            """Generate a new interview question"""
            result = await self.chain.arun(
                role=role,
                difficulty=difficulty,
                topic=topic,
                previous_questions="\n".join(previous_questions) if previous_questions else "None",
            )
            return result.strip()

else:
    class QuestionChain:
        """Lightweight mock question generator used when LangChain isn't available or mocked."""

        def __init__(self):
            pass

        def _load_prompt(self):
            return None

        async def generate_question(self, role: str, difficulty: str, topic: str, previous_questions: List[str]) -> str:
            # Deterministic mock question
            prev = " | ".join(previous_questions) if previous_questions else "none"
            return f"Mock question ({difficulty}) for {role} on {topic}. Previous: {prev}"
