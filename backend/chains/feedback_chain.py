"""
Feedback generation chain using LangChain
"""
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import settings
import os


class FeedbackChain:
    """Generate feedback for interview answers using LLM"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.prompt = self._load_prompt()
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def _load_prompt(self) -> PromptTemplate:
        """Load feedback generation prompt"""
        prompt_path = os.path.join(
            os.path.dirname(__file__), 
            "prompts", 
            "feedback_prompt.txt"
        )
        try:
            with open(prompt_path, "r") as f:
                template = f.read()
        except FileNotFoundError:
            # Fallback template
            template = """You are an expert interviewer evaluating a candidate's answer.

Question: {question}
Candidate's Answer: {answer}

Provide detailed feedback on:
1. Correctness and completeness
2. Communication clarity
3. Technical depth
4. Areas for improvement

Also provide a score from 0-10.

Format your response as:
FEEDBACK: [detailed feedback]
SCORE: [numerical score]
"""
        
        return PromptTemplate(
            input_variables=["question", "answer"],
            template=template
        )
    
    async def generate_feedback(self, question: str, answer: str) -> dict:
        """Generate feedback for an answer"""
        result = await self.chain.arun(
            question=question,
            answer=answer
        )
        
        # Parse the result
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
        
        return {
            "feedback": feedback,
            "score": score
        }
