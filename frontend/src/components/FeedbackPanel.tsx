import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Feedback } from "@/hooks/useInterviewState";
import { CheckCircle2, AlertTriangle, XCircle, TrendingUp, AlertCircle, Lightbulb } from "lucide-react";
import { cn } from "@/lib/utils";

interface FeedbackPanelProps {
  feedback: Feedback;
}

export function FeedbackPanel({ feedback }: FeedbackPanelProps) {
  const getVerdictConfig = () => {
    switch (feedback.verdict) {
      case "correct":
        return {
          icon: CheckCircle2,
          label: "Excellent Answer!",
          bgClass: "bg-success-light",
          borderClass: "border-success",
          textClass: "text-success",
          iconBg: "bg-success/10",
        };
      case "partial":
        return {
          icon: AlertTriangle,
          label: "Good Effort",
          bgClass: "bg-warning-light",
          borderClass: "border-warning",
          textClass: "text-warning",
          iconBg: "bg-warning/10",
        };
      case "needs-improvement":
        return {
          icon: XCircle,
          label: "Needs Improvement",
          bgClass: "bg-destructive-light",
          borderClass: "border-destructive",
          textClass: "text-destructive",
          iconBg: "bg-destructive/10",
        };
    }
  };

  const config = getVerdictConfig();
  const Icon = config.icon;

  return (
    <Card className={cn("border-2 shadow-lg animate-in fade-in-50 duration-500", config.borderClass)}>
      <CardHeader className={cn("border-b", config.bgClass)}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className={cn("flex h-12 w-12 items-center justify-center rounded-xl", config.iconBg)}>
              <Icon className={cn("h-6 w-6", config.textClass)} />
            </div>
            <div>
              <CardTitle className={cn("text-xl", config.textClass)}>
                {config.label}
              </CardTitle>
              <p className="text-sm text-muted-foreground mt-1">
                AI Evaluation Complete
              </p>
            </div>
          </div>
          <Badge variant="outline" className="text-lg px-4 py-2">
            {feedback.score}/10
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-6 pt-6">
        {/* Strengths */}
        {feedback.strengths.length > 0 && (
          <div>
            <div className="mb-3 flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-success/10">
                <TrendingUp className="h-4 w-4 text-success" />
              </div>
              <h4 className="font-semibold text-foreground">Strengths</h4>
            </div>
            <ul className="space-y-2 ml-10">
              {feedback.strengths.map((strength, index) => (
                <li key={index} className="flex items-start gap-2 text-sm text-foreground">
                  <CheckCircle2 className="h-4 w-4 text-success mt-0.5 flex-shrink-0" />
                  <span>{strength}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Weaknesses */}
        {feedback.weaknesses.length > 0 && (
          <div>
            <div className="mb-3 flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-warning/10">
                <AlertCircle className="h-4 w-4 text-warning" />
              </div>
              <h4 className="font-semibold text-foreground">Areas to Improve</h4>
            </div>
            <ul className="space-y-2 ml-10">
              {feedback.weaknesses.map((weakness, index) => (
                <li key={index} className="flex items-start gap-2 text-sm text-foreground">
                  <AlertTriangle className="h-4 w-4 text-warning mt-0.5 flex-shrink-0" />
                  <span>{weakness}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Suggestions */}
        {feedback.suggestions.length > 0 && (
          <div>
            <div className="mb-3 flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
                <Lightbulb className="h-4 w-4 text-primary" />
              </div>
              <h4 className="font-semibold text-foreground">Suggestions</h4>
            </div>
            <ul className="space-y-2 ml-10">
              {feedback.suggestions.map((suggestion, index) => (
                <li key={index} className="flex items-start gap-2 text-sm text-muted-foreground">
                  <span className="text-primary mt-0.5">→</span>
                  <span>{suggestion}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
