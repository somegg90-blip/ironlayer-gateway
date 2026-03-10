# test_suite.ps1
# This script runs 3 tests to verify the proxy is secure.

Write-Host "--- starting CleanPipe Security Tests ---" -ForegroundColor Cyan

# TEST 1: Standard PII (Email & Phone)
Write-Host "`n[Test 1] Sending PII (Email & Phone)..." -ForegroundColor Yellow
 $body1 = @{
    model = "arcee-ai/trinity-large-preview:free"
    messages = @(
        @{
            role = "user"
            content = "My email is agent@secret.com and my phone is 555-0199."
        }
    )
} | ConvertTo-Json -Depth 3

 $result1 = Invoke-RestMethod -Uri "http://127.0.0.1:8000/chat/completions" -Method Post -Headers @{"Content-Type"="application/json"} -Body $body1
Write-Host "Result 1: " -NoNewline
Write-Host $result1.choices[0].message.content -ForegroundColor Green

# TEST 2: Custom IP Protection (Secret Project Name)
Write-Host "`n[Test 2] Sending Custom Secret (ProjectStarlight)..." -ForegroundColor Yellow
 $body2 = @{
    model = "arcee-ai/trinity-large-preview:free"
    messages = @(
        @{
            role = "user"
            content = "I need the budget for ProjectStarlight immediately."
        }
    )
} | ConvertTo-Json -Depth 3

 $result2 = Invoke-RestMethod -Uri "http://127.0.0.1:8000/chat/completions" -Method Post -Headers @{"Content-Type"="application/json"} -Body $body2
Write-Host "Result 2: " -NoNewline
Write-Host $result2.choices[0].message.content -ForegroundColor Green

# TEST 3: The "Combo" Attack (PII + Secret)
Write-Host "`n[Test 3] Sending Mixed Attack (Secret + Credit Card)..." -ForegroundColor Yellow
 $body3 = @{
    model = "arcee-ai/trinity-large-preview:free"
    messages = @(
        @{
            role = "user"
            content = "The recipe for CocaColaFormula is linked to card 4111-1111-1111-1111."
        }
    )
} | ConvertTo-Json -Depth 3

 $result3 = Invoke-RestMethod -Uri "http://127.0.0.1:8000/chat/completions" -Method Post -Headers @{"Content-Type"="application/json"} -Body $body3
Write-Host "Result 3: " -NoNewline
Write-Host $result3.choices[0].message.content -ForegroundColor Green

Write-Host "`n--- Tests Complete. Check your Uvicorn Terminal to verify what the AI SAW vs what YOU see. ---" -ForegroundColor Cyan