import { Progress } from "@/components/ui/progress";
import { CheckCircle2 } from "lucide-react";

interface ProgressHeaderProps {
  currentQuestion: number;
  totalQuestions: number;
}

export function ProgressHeader({ currentQuestion, totalQuestions }: ProgressHeaderProps) {
  const progress = (currentQuestion / totalQuestions) * 100;

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-foreground">
          Question {currentQuestion} of {totalQuestions}
        </h2>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <CheckCircle2 className="h-4 w-4 text-primary" />
          <span>{Math.round(progress)}% Complete</span>
        </div>
      </div>
      <Progress value={progress} className="h-2" />
    </div>
  );
}
