# File: backend/chains/question_chain.py

import os
from typing import List

try:
    from langchain_groq import ChatGroq
    GROQ_AVAILABLE = True
except ImportError:
    from langchain_openai import ChatOpenAI
    GROQ_AVAILABLE = False

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

from config import settings


class QuestionChain:
    """
    Generate interview questions using LLM (GROQ or OpenAI).
    Uses LCEL RunnableSequence instead of deprecated LLMChain.
    """

    def __init__(self):
        # Select LLM provider dynamically
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

        # Load prompt
        self.prompt = self._load_prompt()

        # LCEL replaces LLMChain
        self.chain = RunnableSequence(self.prompt | self.llm)

    def _load_prompt(self) -> PromptTemplate:
        """Loads prompt template from file."""
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "question_prompt.txt")

        if not os.path.exists(prompt_path):
            template = (
                "You are an expert interviewer. Generate a {difficulty} level interview question "
                "for a {role} position focusing on {topic}.\n\n"
                "Previously asked questions:\n{previous_questions}\n\n"
                "Generate a unique question not asked before.\n\n"
                "Question:"
            )
        else:
            with open(prompt_path, "r", encoding="utf-8") as f:
                template = f.read()

        return PromptTemplate(
            template=template,
            input_variables=["role", "difficulty", "topic", "previous_questions"],
        )

    async def generate_question(
        self,
        role: str,
        difficulty: str,
        topic: str,
        previous_questions: List[str],
    ) -> str:
        """Generate a single question asynchronously."""
        prev_txt = "\n".join(previous_questions) if previous_questions else "None"

        result = await self.chain.ainvoke({
            "role": role,
            "difficulty": difficulty,
            "topic": topic,
            "previous_questions": prev_txt,
        })

        return result.content.strip()
