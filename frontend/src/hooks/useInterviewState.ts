import { useState } from "react";

export interface Question {
  id: string;
  text: string;
  category: string;
}

export interface Answer {
  questionId: string;
  text: string;
  feedback?: Feedback;
}

export interface Feedback {
  verdict: "correct" | "partial" | "needs-improvement";
  score: number;
  strengths: string[];
  weaknesses: string[];
  suggestions: string[];
}

export interface InterviewSummary {
  totalQuestions: number;
  averageScore: number;
  weakestTopics: string[];
  strongestAreas: string[];
}

export const useInterviewState = () => {
  const [role, setRole] = useState<string>("");
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState<number>(0);
  const [answers, setAnswers] = useState<Answer[]>([]);
  const [currentAnswer, setCurrentAnswer] = useState<string>("");
  const [showFeedback, setShowFeedback] = useState<boolean>(false);
  const [interviewCompleted, setInterviewCompleted] = useState<boolean>(false);
  const [summary, setSummary] = useState<InterviewSummary | null>(null);

  // PLACEHOLDER: This will be replaced with actual LangChain/AI backend logic
  const generateQuestions = async (targetRole: string) => {
    // Simulated questions for demo purposes
    const mockQuestions: Question[] = [
      {
        id: "q1",
        text: `Explain the concept of Big O notation and analyze the time complexity of a binary search algorithm.`,
        category: "Algorithms",
      },
      {
        id: "q2",
        text: `Design a scalable system for handling millions of concurrent requests. What components would you use?`,
        category: "System Design",
      },
      {
        id: "q3",
        text: `What is the difference between SQL and NoSQL databases? When would you use each?`,
        category: "Databases",
      },
      {
        id: "q4",
        text: `Describe how you would implement a rate limiter for an API.`,
        category: "System Design",
      },
      {
        id: "q5",
        text: `Explain the concept of closures in JavaScript with an example.`,
        category: "Programming",
      },
    ];
    
    setQuestions(mockQuestions);
    setRole(targetRole);
  };

  // PLACEHOLDER: This will be replaced with actual LangChain/AI evaluation logic
  const evaluateAnswer = async (question: Question, answerText: string): Promise<Feedback> => {
    // Simulated evaluation for demo purposes
    const mockFeedback: Feedback = {
      verdict: Math.random() > 0.3 ? "correct" : Math.random() > 0.5 ? "partial" : "needs-improvement",
      score: Math.floor(Math.random() * 4) + 7, // Random score between 7-10
      strengths: [
        "Good explanation of core concepts",
        "Provided relevant examples",
      ],
      weaknesses: [
        "Could elaborate more on edge cases",
        "Missing discussion of trade-offs",
      ],
      suggestions: [
        "Consider discussing time-space complexity trade-offs",
        "Add concrete examples from real-world scenarios",
      ],
    };
    
    return mockFeedback;
  };

  const submitAnswer = async () => {
    const currentQuestion = questions[currentQuestionIndex];
    const feedback = await evaluateAnswer(currentQuestion, currentAnswer);
    
    const newAnswer: Answer = {
      questionId: currentQuestion.id,
      text: currentAnswer,
      feedback,
    };
    
    setAnswers([...answers, newAnswer]);
    setShowFeedback(true);
  };

  const nextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setCurrentAnswer("");
      setShowFeedback(false);
    } else {
      // Complete interview and generate summary
      completeInterview();
    }
  };

  // PLACEHOLDER: This will be replaced with actual summary generation logic
  const completeInterview = () => {
    const allScores = answers
      .map((a) => a.feedback?.score || 0)
      .filter((score) => score > 0);
    
    const avgScore = allScores.length > 0 
      ? allScores.reduce((a, b) => a + b, 0) / allScores.length 
      : 0;

    const mockSummary: InterviewSummary = {
      totalQuestions: questions.length,
      averageScore: Math.round(avgScore * 10) / 10,
      weakestTopics: ["System Design", "Databases"],
      strongestAreas: ["Algorithms", "Programming"],
    };

    setSummary(mockSummary);
    setInterviewCompleted(true);
  };

  const restartInterview = () => {
    setRole("");
    setQuestions([]);
    setCurrentQuestionIndex(0);
    setAnswers([]);
    setCurrentAnswer("");
    setShowFeedback(false);
    setInterviewCompleted(false);
    setSummary(null);
  };

  return {
    role,
    questions,
    currentQuestionIndex,
    answers,
    currentAnswer,
    showFeedback,
    interviewCompleted,
    summary,
    setRole,
    setCurrentAnswer,
    generateQuestions,
    submitAnswer,
    nextQuestion,
    restartInterview,
  };
};
