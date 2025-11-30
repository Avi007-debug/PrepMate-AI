import { useState } from "react";
import { apiClient } from "@/lib/api";

export interface Question {
  id: number;
  text: string;
  category: string;
  difficulty?: string;
  topic_tags?: string[];
  ideal_answer_brief?: string;
}

export interface Answer {
  questionId: number;
  text: string;
  feedback?: Feedback;
}

export interface Feedback {
  feedback: string;
  score: number;
  verdict?: "correct" | "partial" | "needs-improvement";
  strengths?: string[];
  weaknesses?: string[];
  suggestions?: string[];
}

export interface InterviewSummary {
  totalQuestions: number;
  averageScore: number;
  questionsAndAnswers: Array<{
    question: string;
    answer: string;
    score: number;
    feedback: string;
  }>;
  overallFeedback: string;
}

export const useInterviewState = () => {
  const [role, setRole] = useState<string>("");
  const [sessionId, setSessionId] = useState<string>("");
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState<number>(0);
  const [answers, setAnswers] = useState<Answer[]>([]);
  const [currentAnswer, setCurrentAnswer] = useState<string>("");
  const [showFeedback, setShowFeedback] = useState<boolean>(false);
  const [interviewCompleted, setInterviewCompleted] = useState<boolean>(false);
  const [summary, setSummary] = useState<InterviewSummary | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const startInterview = async (targetRole: string) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiClient.startInterview({
        role: targetRole,
        difficulty: "medium",
        topics: ["algorithms", "system-design", "programming"]
      });
      
      setSessionId(response.session_id);
      
      // Parse the JSON string in the question field
      const questionData = JSON.parse(response.question);
      const allQuestions = questionData.questions.map((q: any, index: number) => ({
        id: index,
        text: q.question,
        category: q.category,
        difficulty: q.difficulty,
        topic_tags: q.topic_tags,
        ideal_answer_brief: q.ideal_answer_brief
      }));
      
      setQuestions(allQuestions);
      setCurrentQuestionIndex(0);
      setRole(targetRole);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to start interview");
    } finally {
      setLoading(false);
    }
  };



  const submitAnswer = async () => {
    const currentQuestion = questions[currentQuestionIndex];
    if (!currentQuestion || !sessionId) return;
    
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiClient.submitAnswer({
        session_id: sessionId,
        question_id: currentQuestion.id,
        answer: currentAnswer
      });
      
      const feedback: Feedback = {
        feedback: response.feedback,
        score: response.score
      };
      
      const newAnswer: Answer = {
        questionId: currentQuestion.id,
        text: currentAnswer,
        feedback,
      };
      
      setAnswers([...answers, newAnswer]);
      setShowFeedback(true);
      
      if (response.is_complete) {
        setInterviewCompleted(true);
      } else if (response.next_question && response.next_question_id) {
        const nextQuestion: Question = {
          id: response.next_question_id,
          text: response.next_question,
          category: "Interview Question"
        };
        setQuestions([...questions, nextQuestion]);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit answer");
    } finally {
      setLoading(false);
    }
  };

  const nextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setCurrentAnswer("");
      setShowFeedback(false);
    }
  };

  const loadSummary = async () => {
    if (!sessionId) return;
    
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiClient.getSummary(sessionId);
      
      const summaryData: InterviewSummary = {
        totalQuestions: response.total_questions,
        averageScore: response.average_score,
        questionsAndAnswers: response.questions_and_answers,
        overallFeedback: response.overall_feedback
      };
      
      setSummary(summaryData);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load summary");
    } finally {
      setLoading(false);
    }
  };

  const restartInterview = () => {
    setRole("");
    setSessionId("");
    setQuestions([]);
    setCurrentQuestionIndex(0);
    setAnswers([]);
    setCurrentAnswer("");
    setShowFeedback(false);
    setInterviewCompleted(false);
    setSummary(null);
    setError(null);
  };

  return {
    role,
    sessionId,
    questions,
    currentQuestionIndex,
    currentQuestion: questions[currentQuestionIndex] || null,
    answers,
    currentAnswer,
    showFeedback,
    interviewCompleted,
    summary,
    loading,
    error,
    setRole,
    setCurrentAnswer,
    startInterview,
    submitAnswer,
    nextQuestion,
    loadSummary,
    restartInterview,
  };
};
