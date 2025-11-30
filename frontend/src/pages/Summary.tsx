import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useInterview } from "@/contexts/InterviewContext";
import { Trophy, TrendingUp, TrendingDown, FileText, RotateCcw, Home, CheckCircle2, XCircle, AlertCircle } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

const Summary = () => {
  const navigate = useNavigate();
  const { summary, sessionId, loadSummary, restartInterview, loading, error } = useInterview();

  useEffect(() => {
    if (sessionId && !summary) {
      loadSummary();
    } else if (!sessionId && !loading) {
      // No session ID, redirect to home
      navigate("/");
    }
  }, [sessionId, summary, loadSummary, loading, navigate]);

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
    if (score >= 8) return "text-green-600";
    if (score >= 6) return "text-yellow-600";
    return "text-red-600";
  };

  const getScoreBgColor = (score: number) => {
    if (score >= 8) return "bg-green-100";
    if (score >= 6) return "bg-yellow-100";
    return "bg-red-100";
  };

  const getScoreIcon = (score: number) => {
    if (score >= 8) return <CheckCircle2 className="h-5 w-5 text-green-600" />;
    if (score >= 6) return <AlertCircle className="h-5 w-5 text-yellow-600" />;
    return <XCircle className="h-5 w-5 text-red-600" />;
  };

  const getPerformanceLabel = (score: number) => {
    if (score >= 8) return "Excellent";
    if (score >= 6) return "Good";
    if (score >= 4) return "Fair";
    return "Needs Improvement";
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
          <div className="grid gap-6 md:grid-cols-3 animate-in fade-in-50 duration-700 delay-100">
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
                  Questions answered
                </p>
              </CardContent>
            </Card>

            {/* Overall Score */}
            <Card className="border-2 shadow-md">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-lg">
                  <Trophy className="h-5 w-5 text-primary" />
                  Average Score
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-3">
                  <p className={`text-4xl font-bold ${getScoreColor(summary.averageScore)}`}>
                    {summary.averageScore.toFixed(1)}
                  </p>
                  <div className="flex flex-col">
                    <span className="text-sm text-muted-foreground">/10</span>
                    <Badge variant="secondary" className="text-xs">
                      {getPerformanceLabel(summary.averageScore)}
                    </Badge>
                  </div>
                </div>
                <Progress 
                  value={summary.averageScore * 10} 
                  className="mt-3 h-2"
                />
              </CardContent>
            </Card>

            {/* Performance Badge */}
            <Card className="border-2 shadow-md">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-lg">
                  {getScoreIcon(summary.averageScore)}
                  Performance
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className={`inline-flex items-center gap-2 rounded-full px-4 py-2 ${getScoreBgColor(summary.averageScore)}`}>
                  <span className={`text-2xl font-bold ${getScoreColor(summary.averageScore)}`}>
                    {getPerformanceLabel(summary.averageScore)}
                  </span>
                </div>
                <p className="mt-3 text-sm text-muted-foreground">
                  {summary.averageScore >= 8 ? "Outstanding performance!" : 
                   summary.averageScore >= 6 ? "Keep up the good work!" : 
                   "Room for improvement"}
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Overall Feedback */}
          <Card className="border-2 shadow-md animate-in fade-in-50 duration-700 delay-150">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-xl">
                <FileText className="h-6 w-6 text-primary" />
                Overall Performance Assessment
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="prose prose-sm max-w-none">
                <p className="text-foreground whitespace-pre-wrap leading-relaxed">
                  {summary.overallFeedback}
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Individual Question Scores */}
          <Card className="border-2 shadow-md animate-in fade-in-50 duration-700 delay-200">
            <CardHeader>
              <CardTitle className="text-xl">Detailed Question Analysis</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {summary.questionsAndAnswers.map((qa, index) => {
                  const score = qa.score;
                  return (
                    <div
                      key={index}
                      className="rounded-lg border-2 p-5 space-y-4 hover:shadow-md transition-shadow"
                    >
                      {/* Question Header */}
                      <div className="flex items-start justify-between gap-4">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <Badge variant="outline" className="text-xs">
                              Question {index + 1}
                            </Badge>
                            {getScoreIcon(score)}
                          </div>
                          <p className="text-base font-medium text-foreground leading-relaxed">
                            {qa.question}
                          </p>
                        </div>
                        <div className="flex flex-col items-end gap-1 min-w-[80px]">
                          <div className="flex items-baseline gap-1">
                            <span className={`text-3xl font-bold ${getScoreColor(score)}`}>
                              {score}
                            </span>
                            <span className="text-sm text-muted-foreground">/10</span>
                          </div>
                          <Progress value={score * 10} className="h-1.5 w-16" />
                        </div>
                      </div>

                      {/* Your Answer */}
                      <div className="space-y-2">
                        <h4 className="text-sm font-semibold text-foreground flex items-center gap-2">
                          <FileText className="h-4 w-4" />
                          Your Answer
                        </h4>
                        <div className="bg-accent/50 rounded-md p-3">
                          <p className="text-sm text-foreground leading-relaxed">
                            {qa.answer}
                          </p>
                        </div>
                      </div>

                      {/* AI Feedback */}
                      <div className="space-y-2">
                        <h4 className="text-sm font-semibold text-foreground flex items-center gap-2">
                          <TrendingUp className="h-4 w-4 text-primary" />
                          AI Feedback & Analysis
                        </h4>
                        <div className="bg-primary/5 rounded-md p-3 border border-primary/10">
                          <p className="text-sm text-foreground leading-relaxed whitespace-pre-wrap">
                            {qa.feedback}
                          </p>
                        </div>
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
