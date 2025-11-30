import { Brain, BarChart3, RotateCcw, Home, Info, Play } from "lucide-react";
import { NavLink } from "@/components/NavLink";
import { useInterview } from "@/contexts/InterviewContext";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarHeader,
  SidebarFooter,
} from "@/components/ui/sidebar";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";

interface AppSidebarProps {
  onRestart?: () => void;
  showSummary?: boolean;
  onShowSummary?: () => void;
}

export function AppSidebar({ onRestart, showSummary, onShowSummary }: AppSidebarProps) {
  const { sessionId, interviewCompleted } = useInterview();
  const navigate = useNavigate();

  const handleInterviewClick = (e: React.MouseEvent) => {
    if (!sessionId) {
      e.preventDefault();
      toast.info("Please start an interview first", {
        description: "Go to Get Started to begin a new interview session",
      });
    }
  };

  const handleSummaryClick = (e: React.MouseEvent) => {
    if (!sessionId) {
      e.preventDefault();
      toast.info("No interview in progress", {
        description: "Complete an interview to view your summary",
      });
    } else if (!interviewCompleted) {
      e.preventDefault();
      toast.info("Interview in progress", {
        description: "Complete all questions to view your summary report",
      });
    }
  };

  return (
    <Sidebar className="border-r">
      <SidebarHeader className="border-b p-6">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-primary">
            <Brain className="h-6 w-6 text-primary-foreground" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-foreground">PrepMate AI</h2>
            <p className="text-xs text-muted-foreground">Powered by LLMs</p>
          </div>
        </div>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Navigation</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <NavLink
                    to="/"
                    end
                    className="hover:bg-accent"
                    activeClassName="bg-accent text-accent-foreground font-medium"
                  >
                    <Home className="h-4 w-4" />
                    <span>Home</span>
                  </NavLink>
                </SidebarMenuButton>
              </SidebarMenuItem>
              
              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <NavLink
                    to="/get-started"
                    className="hover:bg-accent"
                    activeClassName="bg-accent text-accent-foreground font-medium"
                  >
                    <Play className="h-4 w-4" />
                    <span>Start Interview</span>
                  </NavLink>
                </SidebarMenuButton>
              </SidebarMenuItem>

              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <NavLink
                    to="/interview"
                    className="hover:bg-accent"
                    activeClassName="bg-accent text-accent-foreground font-medium"
                    onClick={handleInterviewClick}
                  >
                    <Brain className="h-4 w-4" />
                    <span>Interview</span>
                  </NavLink>
                </SidebarMenuButton>
              </SidebarMenuItem>

              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <NavLink
                    to="/summary"
                    className="hover:bg-accent"
                    activeClassName="bg-accent text-accent-foreground font-medium"
                    onClick={handleSummaryClick}
                  >
                    <BarChart3 className="h-4 w-4" />
                    <span>Summary</span>
                  </NavLink>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        <Separator className="my-4" />

        <SidebarGroup>
          <SidebarGroupLabel>About</SidebarGroupLabel>
          <SidebarGroupContent>
            <div className="px-3 py-2 text-sm text-muted-foreground">
              <p className="mb-3">
                Generate role-specific technical interview questions powered by Large Language Models.
              </p>
              <p className="text-xs">
                Practice with AI-driven feedback to ace your next FAANG interview.
              </p>
            </div>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter className="border-t p-4">
        <div className="space-y-2">
          {onRestart && sessionId && (
            <Button
              onClick={onRestart}
              variant="outline"
              className="w-full justify-start"
              size="sm"
            >
              <RotateCcw className="mr-2 h-4 w-4" />
              Restart Interview
            </Button>
          )}
          
          <Button
            variant="ghost"
            className="w-full justify-start text-muted-foreground hover:text-foreground"
            size="sm"
            asChild
          >
            <a
              href="https://github.com/Avi007-debug/PrepMate-AI"
              target="_blank"
              rel="noopener noreferrer"
            >
              <Info className="mr-2 h-4 w-4" />
              About Project
            </a>
          </Button>
        </div>
      </SidebarFooter>
    </Sidebar>
  );
}
