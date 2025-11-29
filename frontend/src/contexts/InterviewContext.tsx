import React, { createContext, useContext, ReactNode } from "react";
import { useInterviewState } from "@/hooks/useInterviewState";

type InterviewContextType = ReturnType<typeof useInterviewState>;

const InterviewContext = createContext<InterviewContextType | undefined>(undefined);

export function InterviewProvider({ children }: { children: ReactNode }) {
  const interviewState = useInterviewState();

  return (
    <InterviewContext.Provider value={interviewState}>
      {children}
    </InterviewContext.Provider>
  );
}

export function useInterview() {
  const context = useContext(InterviewContext);
  if (context === undefined) {
    throw new Error("useInterview must be used within an InterviewProvider");
  }
  return context;
}
