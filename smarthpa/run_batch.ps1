<#
Runs several experiment pairs (K8s HPA then Smart HPA, same scenario and run number) back to back with
run_experiment.ps1, following the interleaved order of plan.md section 6.

A pair is only started if it can finish before -Deadline (estimated from -PairMinutes), so the laptop is free by then
and no pair is left half done. A run whose results\<scenario>\<autoscaler>\run<N> folder already exists is skipped.
A failed run (controller error or check_run.py rejecting the data) is retried up to -MaxAttempts times, each attempt
waiting until the cluster answers again; the batch stops only when all attempts of a run failed.

Example:
  .\run_batch.ps1 -Deadline 17:30 -Pairs "5R-50%:2","5R-50%:3","2R-20%:1"
  .\run_batch.ps1 -Pairs "5R-50%:1","5R-50%:2" -Shape spike          # improvement C2, results\5R-50-spike\
#>
param(
    [Parameter(Mandatory = $true)][string[]]$Pairs,          # "<scenario>:<run>"
    [string[]]$Autoscalers = @("k8shpa", "smarthpa"),        # run in this order for each pair; add "prosmarthpa" for 2R-20%
    [string]$Deadline = "",                                  # HH:mm today; empty = no deadline
    [double]$PairMinutes = 0,                                # 0 = 21 min per autoscaler (measured: R01+R02 took 41.5 min with default settings)
    [int]$MaxAttempts = 3,
    [ValidateSet("ramp", "spike")][string]$Shape = "ramp"   # passed to run_experiment.ps1
)

$ErrorActionPreference = "Stop"
# powershell -File passes "a","b" as one string "a,b": split on commas either way
$Pairs = @($Pairs | ForEach-Object { $_ -split ',' } | ForEach-Object { $_.Trim() } | Where-Object { $_ })
$Autoscalers = @($Autoscalers | ForEach-Object { $_ -split ',' } | ForEach-Object { $_.Trim() } | Where-Object { $_ })
if ($PairMinutes -le 0) { $PairMinutes = 21 * $Autoscalers.Count }
$Script = Join-Path $PSScriptRoot "run_experiment.ps1"
$end = if ($Deadline) { [datetime]::ParseExact($Deadline, "HH:mm", $null) } else { [datetime]::MaxValue }

function Log($msg) { Write-Host ("[{0}] [batch] {1}" -f (Get-Date -Format "HH:mm:ss"), $msg) }

# block until kubectl reaches the cluster 3 times in a row (the laptop's link to the VMs drops now and then)
function Wait-Cluster {
    $ErrorActionPreference = "Continue"     # with "Stop", PowerShell 5.1 turns kubectl's stderr into a terminating error
    $ok = 0
    $since = Get-Date
    while ($ok -lt 3) {
        & kubectl get nodes --request-timeout=5s 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) { $ok++ } else { $ok = 0 }
        if ($ok -lt 3) { Start-Sleep -Seconds 10 }
        if (((Get-Date) - $since).TotalMinutes -gt 30) { Log "Cluster unreachable for 30 min, stopping batch"; exit 1 }
    }
}

$suffix = if ($Shape -ne "ramp") { "-$Shape" } else { "" }    # same folder naming as run_experiment.ps1

Log "Pairs: $($Pairs -join ', ') | autoscalers: $($Autoscalers -join ', ') | shape: $Shape | deadline: $(if ($Deadline) { $Deadline } else { 'none' }) | ~$PairMinutes min per pair"
foreach ($p in $Pairs) {
    $scenario, $run = $p -split ':'
    $eta = (Get-Date).AddMinutes($PairMinutes)
    if ($eta -gt $end) {
        Log "Skipping $scenario run $run and the rest: would finish ~$($eta.ToString('HH:mm')), after deadline $Deadline"
        break
    }
    foreach ($a in $Autoscalers) {
        $outDir = Join-Path $PSScriptRoot ("..\results\{0}{1}\{2}\run{3}" -f $scenario.TrimEnd('%'), $suffix, $a, $run)
        if (Test-Path $outDir) { Log "=== $a | $scenario | run $run already done, skipping ==="; continue }
        for ($attempt = 1; $attempt -le $MaxAttempts; $attempt++) {
            Wait-Cluster
            Log "=== $a | $scenario | run $run | attempt $attempt/$MaxAttempts ==="
            & powershell -NoProfile -ExecutionPolicy Bypass -File $Script -Autoscaler $a -Scenario $scenario -Run ([int]$run) -Shape $Shape
            if ($LASTEXITCODE -eq 0) { break }
            Log "Run failed (exit $LASTEXITCODE)"
            if ($attempt -eq $MaxAttempts) { Log "All $MaxAttempts attempts failed, stopping batch"; exit 1 }
        }
    }
}
Log "Batch finished"
