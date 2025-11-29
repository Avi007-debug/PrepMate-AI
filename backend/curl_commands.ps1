# PrepMate-AI backend API examples (PowerShell)
# Usage: edit the `$BASE` variable if necessary and replace <SESSION_ID> when required.

$BASE = "http://127.0.0.1:8000"

function Start-Interview {
    $body = @{
        role = "Software Engineer"
        difficulty = "medium"
        topics = @("algorithms", "system design")
    }
    $resp = Invoke-RestMethod -Method Post -Uri "$BASE/api/interview/start" -ContentType "application/json" -Body ($body | ConvertTo-Json)
    $resp | ConvertTo-Json -Depth 5
    return $resp
}

function Get-Current {
    param([string]$session_id)
    Invoke-RestMethod -Method Get -Uri "$BASE/api/interview/current/$session_id"
}

function Submit-Answer {
    param(
        [string]$session_id,
        [int]$question_id = 0,
        [string]$answer = "Example answer text"
    )
    $body = @{
        session_id = $session_id
        question_id = $question_id
        answer = $answer
    }
    Invoke-RestMethod -Method Post -Uri "$BASE/api/interview/answer" -ContentType "application/json" -Body ($body | ConvertTo-Json)
}

function Get-Status {
    param([string]$session_id)
    Invoke-RestMethod -Method Get -Uri "$BASE/api/interview/status/$session_id"
}

function Get-Summary {
    param([string]$session_id)
    Invoke-RestMethod -Method Get -Uri "$BASE/api/interview/summary/$session_id"
}

function Delete-Session {
    param([string]$session_id)
    Invoke-RestMethod -Method Delete -Uri "$BASE/api/interview/session/$session_id"
}

# Example quick flow (uncomment to run):
# $start = Start-Interview
# $sessionId = $start.session_id
# Submit-Answer -session_id $sessionId -question_id $start.question_id -answer "This is my answer"
# Get-Summary -session_id $sessionId

Write-Host "Script loaded. Use Start-Interview, Submit-Answer, Get-Current, Get-Status, Get-Summary, Delete-Session." -ForegroundColor Green
