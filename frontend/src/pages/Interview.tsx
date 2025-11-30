import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useInterview } from "@/contexts/InterviewContext";
import { ProgressHeader } from "@/components/ProgressHeader";
import { QuestionCard } from "@/components/QuestionCard";
import { FeedbackPanel } from "@/components/FeedbackPanel";
import { ArrowRight, Send } from "lucide-react";

const Interview = () => {
  const navigate = useNavigate();
  const {
    questions,
    currentQuestionIndex,
    currentQuestion,
    currentAnswer,
    showFeedback,
    answers,
    interviewCompleted,
    loading,
    error,
    setCurrentAnswer,
    submitAnswer,
    nextQuestion,
  } = useInterview();

  // Redirect if no questions loaded
  useEffect(() => {
    if (questions.length === 0) {
      navigate("/");
    }
  }, [questions, navigate]);

  // Redirect to summary if interview completed
  useEffect(() => {
    if (interviewCompleted) {
      navigate("/summary");
    }
  }, [interviewCompleted, navigate]);

  if (questions.length === 0 || !currentQuestion) {
    return null;
  }

  const currentFeedback = answers.find((a) => a.questionId === currentQuestion.id)?.feedback;
  const charCount = currentAnswer.length;

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        <div className="mx-auto max-w-4xl space-y-8">
          {/* Progress Header */}
          <ProgressHeader
            currentQuestion={currentQuestionIndex + 1}
            totalQuestions={questions.length}
          />

          {/* Question Card */}
          <QuestionCard question={currentQuestion} questionNumber={currentQuestionIndex + 1} />

          {/* Answer Input Area */}
          {!showFeedback && (
            <div className="space-y-4 animate-in fade-in-50 duration-500">
              <div className="space-y-2">
                <label htmlFor="answer" className="text-sm font-medium text-foreground">
                  Your Answer
                </label>
                <Textarea
                  id="answer"
                  placeholder="Type your answer here... Be as detailed as possible to get the best feedback."
                  value={currentAnswer}
                  onChange={(e) => setCurrentAnswer(e.target.value)}
                  className="min-h-[200px] resize-none text-base"
                />
                <div className="flex justify-between text-sm text-muted-foreground">
                  <span>Write a comprehensive answer to receive detailed feedback</span>
                  <span>{charCount} characters</span>
                </div>
              </div>

              {error && (
                <div className="text-red-500 text-sm">
                  {error}
                </div>
              )}
              <Button
                onClick={submitAnswer}
                disabled={currentAnswer.trim().length < 10 || loading}
                className="w-full h-12 text-base font-semibold shadow-md hover:shadow-lg transition-all"
                size="lg"
              >
                <Send className="mr-2 h-5 w-5" />
                {loading ? "Submitting..." : "Submit Answer"}
              </Button>
            </div>
          )}

          {/* Feedback Panel */}
          {showFeedback && currentFeedback && (
            <div className="space-y-4">
              <FeedbackPanel feedback={currentFeedback} />
              
              <Button
                onClick={nextQuestion}
                disabled={loading}
                className="w-full h-12 text-base font-semibold shadow-md hover:shadow-lg transition-all"
                size="lg"
              >
                {interviewCompleted ? "View Summary Report" : "Next Question"}
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Interview;
