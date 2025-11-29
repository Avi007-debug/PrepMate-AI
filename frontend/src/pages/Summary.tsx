import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useInterview } from "@/contexts/InterviewContext";
import { Trophy, TrendingUp, TrendingDown, FileText, RotateCcw, Home } from "lucide-react";
import { Badge } from "@/components/ui/badge";

const Summary = () => {
  const navigate = useNavigate();
  const { summary, answers, questions, restartInterview } = useInterview();

  useEffect(() => {
    if (!summary) {
      navigate("/");
    }
  }, [summary, navigate]);

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

            {/* Strongest Areas */}
            <Card className="border-2 shadow-md">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-lg">
                  <TrendingUp className="h-5 w-5 text-success" />
                  Strongest Areas
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {summary.strongestAreas.map((area, index) => (
                    <Badge key={index} variant="secondary" className="bg-success-light text-success">
                      {area}
                    </Badge>
                  ))}
                </div>
                <p className="mt-3 text-sm text-muted-foreground">
                  Keep up the excellent work in these areas!
                </p>
              </CardContent>
            </Card>

            {/* Weakest Topics */}
            <Card className="border-2 shadow-md">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-lg">
                  <TrendingDown className="h-5 w-5 text-warning" />
                  Areas to Improve
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {summary.weakestTopics.map((topic, index) => (
                    <Badge key={index} variant="secondary" className="bg-warning-light text-warning">
                      {topic}
                    </Badge>
                  ))}
                </div>
                <p className="mt-3 text-sm text-muted-foreground">
                  Focus your study on these topics for better results
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
                {answers.map((answer, index) => {
                  const question = questions.find((q) => q.id === answer.questionId);
                  const score = answer.feedback?.score || 0;
                  return (
                    <div
                      key={answer.questionId}
                      className="flex items-center justify-between rounded-lg border p-4"
                    >
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-sm font-medium text-muted-foreground">
                            Question {index + 1}
                          </span>
                          <Badge variant="outline" className="text-xs">
                            {question?.category}
                          </Badge>
                        </div>
                        <p className="text-sm text-foreground line-clamp-1">
                          {question?.text}
                        </p>
                      </div>
                      <div className="ml-4 flex items-center gap-2">
                        <span className={`text-2xl font-bold ${getScoreColor(score)}`}>
                          {score}
                        </span>
                        <span className="text-sm text-muted-foreground">/10</span>
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
