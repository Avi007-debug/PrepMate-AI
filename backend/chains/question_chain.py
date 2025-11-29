# File: backend/chains/question_chain.py
import os
import asyncio
from typing import List, Optional

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from config import settings


class QuestionChain:
    """
    Generate interview questions using LLM.
    Provides:
      - async _generate_question(...)  : core async call
      - generate_questions(role, count): synchronous wrapper returning a list[str]
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
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "question_prompt.txt")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                template = f.read()
        except FileNotFoundError:
            template = (
                "You are an expert interviewer. Generate a {difficulty} level interview question "
                "for a {role} position focusing on {topic}.\n\n"
                "Previous questions asked: {previous_questions}\n\n"
                "Generate a unique question that hasn't been asked before.\n\nQuestion:"
            )

        return PromptTemplate(
            input_variables=["role", "difficulty", "topic", "previous_questions"],
            template=template,
        )

    async def _generate_question(
            self,
            role: str,
            difficulty: str,
            topic: str,
            previous_questions: List[str],
    ) -> str:
        prev = "\n".join(previous_questions) if previous_questions else "None"
        result = await self.chain.arun(
            role=role,
            difficulty=difficulty,
            topic=topic,
            previous_questions=prev,
        )
        return result.strip()

    def generate_questions(
            self,
            role: str,
            count: int = 5,
            topics: Optional[List[str]] = None,
    ) -> List[str]:
        """
        Synchronous wrapper that generates `count` questions for `role`.
        Rotates through difficulties and topics if multiple are needed.
        """
        if topics is None:
            topics = ["system design", "algorithms", "testing", "databases", "behavioral"]

        difficulties = ["Easy", "Medium", "Hard"]
        questions: List[str] = []
        for i in range(count):
            difficulty = difficulties[i % len(difficulties)]
            topic = topics[i % len(topics)]
            # call async generator synchronously
            q = asyncio.run(self._generate_question(role, difficulty, topic, questions))
            questions.append(q)
        return questions
