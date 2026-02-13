# Test Engine Code Runner
# Runs trading_engine.py scripts for all models and reports results
# Date: February 9, 2026

Write-Host "Trading Engine Test Runner"
Write-Host "=========================="
Write-Host ""

$models = Get-ChildItem -Path "C:\development\ai\ollama-model-tests\models" -Directory
$requirementsPath = "C:\development\ai\ollama-model-tests\requirements\historical.csv"
$referenceOutputPath = "C:\development\ai\ollama-model-tests\requirements\engine-output.csv"
$successCount = 0
$failureCount = 0
$comparisonResults = @()

# Function to compare two CSV files
function Compare-TradingResults {
    param(
        [string]$referencePath,
        [string]$modelOutputPath,
        [string]$modelName
    )
    
    if (!(Test-Path $modelOutputPath)) {
        return @{
            Model = $modelName
            Status = "No Output"
            Notes = "output.csv file not found"
            TradesExecuted = 0
            TotalProfitMatch = "N/A"
            AccuracyScore = "0%"
        }
    }
    
    try {
        # Read both CSV files
        $reference = Import-Csv $referencePath
        $modelOutput = Import-Csv $modelOutputPath
        
        # Basic validation
        if ($reference.Count -ne $modelOutput.Count) {
            return @{
                Model = $modelName
                Status = "Row Count Mismatch"
                Notes = "Reference has $($reference.Count) rows, model output has $($modelOutput.Count) rows"
                TradesExecuted = 0
                TotalProfitMatch = "N/A"
                AccuracyScore = "0%"
            }
        }
        
        # Count trading activity
        $refTrades = ($reference | Where-Object { [int]$_.Shares -ne 0 }).Count
        $modelTrades = ($modelOutput | Where-Object { [int]$_.Shares -ne 0 }).Count
        
        # Check final total profit
        $refFinalProfit = [decimal]($reference[-1].TotalProfit)
        $modelFinalProfit = [decimal]($modelOutput[-1].TotalProfit)
        
        $profitMatch = if ([Math]::Abs($refFinalProfit - $modelFinalProfit) -lt 0.01) { "✓ Match" } 
                      else { "✗ Mismatch (Ref: $refFinalProfit, Model: $modelFinalProfit)" }
        
        # Calculate accuracy based on trading decisions and profit
        $accuracyScore = 0
        if ($refTrades -eq $modelTrades -and $refTrades -gt 0) { $accuracyScore += 40 }
        if ([Math]::Abs($refFinalProfit - $modelFinalProfit) -lt 0.01) { $accuracyScore += 60 }
        elseif ([Math]::Abs($refFinalProfit - $modelFinalProfit) -lt ($refFinalProfit * 0.1)) { $accuracyScore += 30 }
        
        # Determine status
        $status = if ($accuracyScore -ge 90) { "Excellent" }
                 elseif ($accuracyScore -ge 70) { "Good" }
                 elseif ($accuracyScore -ge 40) { "Fair" }
                 elseif ($modelTrades -eq 0) { "No Trading" }
                 else { "Poor" }
        
        $notes = "Ref trades: $refTrades, Model trades: $modelTrades"
        if ($modelTrades -eq 0 -and $refTrades -gt 0) {
            $notes += " - Model did not execute any trades"
        }
        
        return @{
            Model = $modelName
            Status = $status
            Notes = $notes
            TradesExecuted = $modelTrades
            TotalProfitMatch = $profitMatch
            AccuracyScore = "$accuracyScore%"
        }
    }
    catch {
        return @{
            Model = $modelName
            Status = "Comparison Error"
            Notes = "Error comparing files: $($_.Exception.Message)"
            TradesExecuted = 0
            TotalProfitMatch = "N/A"
            AccuracyScore = "0%"
        }
    }
}

foreach ($model in $models) {
    $enginePath = Join-Path $model.FullName "results\engine"
    Write-Host "Processing model: $($model.Name)"
    
    if (Test-Path $enginePath) {
        Push-Location $enginePath
        
        # Check if historical.csv exists, copy if not
        if (!(Test-Path "historical.csv")) {
            Write-Host "  Copying historical.csv from requirements"
            Copy-Item $requirementsPath . -Force
        }
        
        # Remove output.csv if it exists
        if (Test-Path "output.csv") {
            Write-Host "  Removing existing output.csv"
            Remove-Item "output.csv" -Force
        }
        
        # Check if trading_engine.py exists
        if (Test-Path "trading_engine.py") {
            Write-Host "  Running trading_engine.py"
            
            # Try running with no arguments first (standard pattern)
            $result = python trading_engine.py 2>&1
            $exitCode = $LASTEXITCODE
            
            # If it fails and shows usage pattern, try with arguments
            if ($exitCode -ne 0 -and $result -like "*Usage:*") {
                Write-Host "  Script requires arguments, trying with historical.csv output.csv"
                python trading_engine.py historical.csv output.csv
                $exitCode = $LASTEXITCODE
            }
            
            if ($exitCode -eq 0 -and (Test-Path "output.csv")) {
                Write-Host "  ✓ output.csv generated successfully"
                $successCount++
                
                # Compare with reference output
                Write-Host "  Comparing with reference output..."
                $comparison = Compare-TradingResults -referencePath $referenceOutputPath -modelOutputPath "output.csv" -modelName $model.Name
                $comparisonResults += $comparison
                Write-Host "  Status: $($comparison.Status) - $($comparison.AccuracyScore)"
                
            } else {
                Write-Host "  ✗ output.csv was not generated"
                Write-Host "  Error: $result"
                $failureCount++
                
                # Add failed comparison result
                $comparisonResults += @{
                    Model = $model.Name
                    Status = "Execution Failed"
                    Notes = "Script execution failed"
                    TradesExecuted = 0
                    TotalProfitMatch = "N/A"
                    AccuracyScore = "0%"
                }
            }
        } else {
            Write-Host "  ✗ trading_engine.py not found"
            $failureCount++
            
            # Add failed comparison result
            $comparisonResults += @{
                Model = $model.Name
                Status = "No Script"
                Notes = "trading_engine.py not found"
                TradesExecuted = 0
                TotalProfitMatch = "N/A"
                AccuracyScore = "0%"
            }
        }
        
        Pop-Location
    } else {
        Write-Host "  ✗ Engine folder not found: $enginePath"
        $failureCount++
        
        # Add failed comparison result
        $comparisonResults += @{
            Model = $model.Name
            Status = "No Folder"
            Notes = "Engine folder not found"
            TradesExecuted = 0
            TotalProfitMatch = "N/A"
            AccuracyScore = "0%"
        }
    }
    Write-Host ""
}

Write-Host "==============================================="
Write-Host "Final Results:"
Write-Host "✓ Successful: $successCount models"
Write-Host "✗ Failed: $failureCount models"
Write-Host "Total: $($successCount + $failureCount) models processed"
Write-Host "==============================================="
Write-Host ""

# Display comparison table
Write-Host "TRADING ENGINE ACCURACY COMPARISON"
Write-Host "=================================="
Write-Host ""

# Create a formatted table
$tableFormat = "{0,-35} {1,-15} {2,-12} {3,-15} {4,-10} {5,-60}"
Write-Host ($tableFormat -f "Model", "Status", "Accuracy", "Trades", "Profit", "Notes")
Write-Host ($tableFormat -f "-----", "------", "--------", "------", "------", "-----")

foreach ($result in $comparisonResults | Sort-Object { 
    # Sort by accuracy score (extract number)
    if ($_.AccuracyScore -match '(\d+)%') { [int]$matches[1] } else { 0 }
} -Descending) {
    $profitStatus = if ($result.TotalProfitMatch -like "*Match*") { "✓" } 
                   elseif ($result.TotalProfitMatch -eq "N/A") { "N/A" }
                   else { "✗" }
    
    Write-Host ($tableFormat -f 
        $result.Model,
        $result.Status,
        $result.AccuracyScore,
        $result.TradesExecuted,
        $profitStatus,
        $result.Notes
    )
}

Write-Host ""
Write-Host "Legend:"
Write-Host "Excellent (90%+): Model performs very close to reference"
Write-Host "Good (70-89%): Model performs well with minor differences"
Write-Host "Fair (40-69%): Model has some trading activity but significant differences"
Write-Host "No Trading: Model generated output but no trades were executed"
Write-Host "Poor (<40%): Model performs poorly compared to reference"
Write-Host ""

# Generate report file
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$reportPath = "C:\development\ai\ollama-model-tests\reports\trading_engine_test_$timestamp.md"

# Load reference data for report
$reference = Import-Csv $referenceOutputPath
$expectedTrades = ($reference | Where-Object { [int]$_.Shares -ne 0 }).Count
$expectedProfit = [decimal]($reference[-1].TotalProfit)

$reportContent = @"
# Trading Engine Test Report
Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

## Summary
- **Total Models Tested**: $($successCount + $failureCount)
- **Successful Runs**: $successCount
- **Failed Runs**: $failureCount

## Accuracy Comparison

| Model | Status | Accuracy | Trades Executed | Profit Match | Notes |
|-------|--------|----------|-----------------|--------------|-------|
"@

foreach ($result in $comparisonResults | Sort-Object { 
    if ($_.AccuracyScore -match '(\d+)%') { [int]$matches[1] } else { 0 }
} -Descending) {
    $profitStatus = if ($result.TotalProfitMatch -like "*Match*") { "✓" } 
                   elseif ($result.TotalProfitMatch -eq "N/A") { "N/A" }
                   else { "✗" }
    
    $reportContent += "`n| $($result.Model) | $($result.Status) | $($result.AccuracyScore) | $($result.TradesExecuted) | $profitStatus | $($result.Notes) |"
}

$reportContent += @"

## Scoring Criteria
- **Excellent (90%+)**: Model performs very close to reference implementation
- **Good (70-89%)**: Model performs well with minor differences in execution
- **Fair (40-69%)**: Model has some trading activity but significant differences
- **No Trading**: Model generated output but no trades were executed
- **Poor (<40%)**: Model performs poorly compared to reference

## Reference Data
- Reference file: requirements/engine-output.csv
- Expected trades: $expectedTrades
- Expected final profit: $expectedProfit
"@

# Ensure reports directory exists
if (!(Test-Path "C:\development\ai\ollama-model-tests\reports")) {
    New-Item -ItemType Directory -Path "C:\development\ai\ollama-model-tests\reports" -Force | Out-Null
}

# Save report
$reportContent | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host "Detailed report saved to: $reportPath"