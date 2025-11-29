import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Question } from "@/hooks/useInterviewState";
import { FileQuestion } from "lucide-react";

interface QuestionCardProps {
  question: Question;
  questionNumber: number;
}

export function QuestionCard({ question, questionNumber }: QuestionCardProps) {
  return (
    <Card className="border-2 shadow-md">
      <CardHeader className="border-b bg-muted/30">
        <div className="flex items-start justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
              <FileQuestion className="h-5 w-5 text-primary" />
            </div>
            <div>
              <h3 className="text-sm font-medium text-muted-foreground">
                Question #{questionNumber}
              </h3>
              <Badge variant="secondary" className="mt-1">
                {question.category}
              </Badge>
            </div>
          </div>
        </div>
      </CardHeader>
      <CardContent className="pt-6">
        <p className="text-lg leading-relaxed text-foreground">
          {question.text}
        </p>
      </CardContent>
    </Card>
  );
}
