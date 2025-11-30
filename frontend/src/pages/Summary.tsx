import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useInterview } from "@/contexts/InterviewContext";
import { Trophy, TrendingUp, TrendingDown, FileText, RotateCcw, Home } from "lucide-react";
import { Badge } from "@/components/ui/badge";

const Summary = () => {
  const navigate = useNavigate();
  const { summary, answers, loadSummary, restartInterview, loading, error } = useInterview();

  useEffect(() => {
    if (!summary) {
      loadSummary();
    }
  }, [summary, loadSummary]);

  useEffect(() => {
    if (!summary && !loading) {
      navigate("/");
    }
  }, [summary, loading, navigate]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-subtle flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-lg text-muted-foreground">Loading summary...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-subtle flex items-center justify-center">
        <div className="text-center">
          <p className="text-lg text-red-500 mb-4">{error}</p>
          <Button onClick={() => navigate("/")}>
            Go to Home
          </Button>
        </div>
      </div>
    );
  }

  if (!summary) {
    return null;
  }

  const handleRestart = () => {
    restartInterview();
    navigate("/");
  };

  const getScoreColor = (score: number) => {
    if (score >= 8) return "text-success";
    if (score >= 6) return "text-warning";
    return "text-destructive";
  };

  // PLACEHOLDER: PDF download functionality to be implemented with backend
  const handleDownloadPDF = () => {
    alert("PDF download functionality will be implemented with backend integration");
  };

  return (
    <div className="min-h-screen bg-gradient-subtle">
      <div className="container mx-auto px-4 py-12">
        <div className="mx-auto max-w-4xl space-y-8">
          {/* Header */}
          <div className="text-center animate-in fade-in-50 duration-700">
            <div className="mb-4 flex justify-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-primary shadow-glow">
                <Trophy className="h-8 w-8 text-primary-foreground" />
              </div>
            </div>
            <h1 className="mb-2 text-4xl font-bold text-foreground">
              Interview Summary Report
            </h1>
            <p className="text-lg text-muted-foreground">
              Here's how you performed across all questions
            </p>
          </div>

          {/* Summary Cards Grid */}
          <div className="grid gap-6 md:grid-cols-2 animate-in fade-in-50 duration-700 delay-100">
            {/* Total Questions */}
            <Card className="border-2 shadow-md">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-lg">
                  <FileText className="h-5 w-5 text-primary" />
                  Total Questions
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-4xl font-bold text-foreground">
                  {summary.totalQuestions}
                </p>
                <p className="mt-2 text-sm text-muted-foreground">
                  Questions completed
                </p>
              </CardContent>
            </Card>

            {/* Overall Score */}
            <Card className="border-2 shadow-md">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-lg">
                  <Trophy className="h-5 w-5 text-primary" />
                  Overall Score
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className={`text-4xl font-bold ${getScoreColor(summary.averageScore)}`}>
                  {summary.averageScore}/10
                </p>
                <p className="mt-2 text-sm text-muted-foreground">
                  Average across all questions
                </p>
              </CardContent>
            </Card>

            {/* Overall Feedback */}
            <Card className="border-2 shadow-md md:col-span-2">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-lg">
                  <FileText className="h-5 w-5 text-primary" />
                  Overall Feedback
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground whitespace-pre-wrap">
                  {summary.overallFeedback}
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Individual Question Scores */}
          <Card className="border-2 shadow-md animate-in fade-in-50 duration-700 delay-200">
            <CardHeader>
              <CardTitle>Question-by-Question Breakdown</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {summary.questionsAndAnswers.map((qa, index) => {
                  const score = qa.score;
                  return (
                    <div
                      key={index}
                      className="rounded-lg border p-4 space-y-3"
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="text-sm font-medium text-muted-foreground">
                              Question {index + 1}
                            </span>
                          </div>
                          <p className="text-sm text-foreground">
                            {qa.question}
                          </p>
                        </div>
                        <div className="ml-4 flex items-center gap-2">
                          <span className={`text-2xl font-bold ${getScoreColor(score)}`}>
                            {score}
                          </span>
                          <span className="text-sm text-muted-foreground">/10</span>
                        </div>
                      </div>
                      <div className="text-xs text-muted-foreground">
                        <strong>Your Answer:</strong> {qa.answer.substring(0, 100)}...
                      </div>
                      <div className="text-xs text-muted-foreground">
                        <strong>Feedback:</strong> {qa.feedback}
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>

          {/* Action Buttons */}
          <div className="flex flex-col gap-4 sm:flex-row animate-in fade-in-50 duration-700 delay-300">
            <Button
              onClick={handleDownloadPDF}
              variant="outline"
              className="flex-1 h-12 text-base font-semibold"
              size="lg"
            >
              <FileText className="mr-2 h-5 w-5" />
              Download PDF Summary
            </Button>
            <Button
              onClick={handleRestart}
              variant="outline"
              className="flex-1 h-12 text-base font-semibold"
              size="lg"
            >
              <RotateCcw className="mr-2 h-5 w-5" />
              Retake Interview
            </Button>
            <Button
              onClick={() => navigate("/")}
              className="flex-1 h-12 text-base font-semibold shadow-md hover:shadow-lg transition-all"
              size="lg"
            >
              <Home className="mr-2 h-5 w-5" />
              Go to Home
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Summary;
