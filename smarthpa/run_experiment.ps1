<#
Runs ONE experiment run end to end (plan.md, section 6 "Quy trinh mot lan chay"):
  1. Check kubectl targets the k3s lab cluster
  2. Reset: delete HPAs, scale every deployment to 1, wait until clean, cool down
  3. Start the autoscaler under test:
       smarthpa    -> Microservice_Capacity_Analyzer.py (scales the app itself)
       prosmarthpa -> ..\prosmarthpa\prosmart_hpa.py with D:\prosmart-venv (PROPHET models in ..\prosmarthpa\models)
       k8shpa   -> kubectl autoscale for all deployments + k8shpa_observer.py (records only)
  4. Start cluster_recorder.py and Locust at the same time
  5. Stop everything, remove HPAs, copy Knowledge Base + logs to results\<scenario>\<autoscaler>\run<N>\

Example:
  .\run_experiment.ps1 -Autoscaler k8shpa -Scenario 5R-50% -Run 1
  .\run_experiment.ps1 -Autoscaler smarthpa -Scenario 5R-50% -Run 0 -DurationSec 300 -Users 100 -CooldownSec 60   # short trial
#>
param(
    [Parameter(Mandatory = $true)][ValidateSet("smarthpa", "prosmarthpa", "k8shpa")][string]$Autoscaler,
    [Parameter(Mandatory = $true)][ValidatePattern('^\d+R-\d+%$')][string]$Scenario,
    [Parameter(Mandatory = $true)][int]$Run,
    [int]$Users = 200,
    [double]$SpawnRate = 0.67,
    [int]$DurationSec = 900,
    [int]$CooldownSec = 300,
    [string]$TargetHost = "http://192.168.161.10",
    [string]$ExpectedContext = "k3s-lab",
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$Python = "D:\smarthpa-venv\Scripts\python.exe"
$Locust = "D:\smarthpa-venv\Scripts\locust.exe"
$ProSmartPython = "D:\prosmart-venv\Scripts\python.exe"         # prophet needs numpy < 2 / pandas 2.x, kept apart from smarthpa-venv
$CodeDir = $PSScriptRoot
$ScenarioDir = $Scenario.TrimEnd('%')
$RelOut = "..\results\$ScenarioDir\$Autoscaler\run$Run"
$OutDir = Join-Path $CodeDir $RelOut

function Log($msg) { Write-Host ("[{0}] {1}" -f (Get-Date -Format "HH:mm:ss"), $msg) }

function Invoke-Kubectl {
    $out = & kubectl @args
    if ($LASTEXITCODE -ne 0) { throw "kubectl $args failed (exit $LASTEXITCODE)" }
    return $out
}

function Get-DeploymentNames { Invoke-Kubectl get deployments -o "jsonpath={.items[*].metadata.name}" | ForEach-Object { $_ -split ' ' } }

# ---------------------------------------------------------------- 1. Safety checks
$ctx = (Invoke-Kubectl config current-context).Trim()
if ($ctx -ne $ExpectedContext) { throw "kubectl context is '$ctx', expected '$ExpectedContext'. Aborting." }
if ((Test-Path $OutDir) -and -not $Force) { throw "$OutDir already exists. Use -Force to overwrite or pick another -Run." }
if ($Autoscaler -eq "prosmarthpa") {
    $models = @(Get-ChildItem (Join-Path $CodeDir "..\prosmarthpa\models") -Filter *.pkl -ErrorAction SilentlyContinue).Count
    if ($models -ne 22) { throw "Expected 22 PROPHET models in ..\prosmarthpa\models, found $models. Run train_prophet.py first." }
}
$m = [regex]::Match($Scenario, '^(\d+)R-(\d+)%$')
$MaxR = [int]$m.Groups[1].Value
$Threshold = [int]$m.Groups[2].Value
$Deployments = @(Get-DeploymentNames)
Log "Context $ctx | $Autoscaler | $Scenario (maxR=$MaxR, threshold=$Threshold%) | run $Run | $Users users @ $SpawnRate/s | ${DurationSec}s"

$procs = @()
$failed = $false
try {
    # ------------------------------------------------------------ 2. Reset
    Log "Reset: deleting HPAs, scaling all deployments to 1"
    & kubectl delete hpa --all --ignore-not-found | Out-Null
    Invoke-Kubectl scale deployment --all --replicas=1 | Out-Null

    $deadline = (Get-Date).AddSeconds(600)
    while ($true) {
        $deps = (Invoke-Kubectl get deployments -o json | Out-String | ConvertFrom-Json).items
        $pods = (Invoke-Kubectl get pods -o json | Out-String | ConvertFrom-Json).items
        $notReady = @($deps | Where-Object { $_.spec.replicas -ne 1 -or $_.status.readyReplicas -ne 1 }).Count
        $terminating = @($pods | Where-Object { $_.metadata.deletionTimestamp }).Count
        $pending = @($pods | Where-Object { $_.status.phase -eq "Pending" }).Count
        if ($notReady -eq 0 -and $terminating -eq 0 -and $pending -eq 0 -and $pods.Count -eq $deps.Count) { break }
        if ((Get-Date) -gt $deadline) { throw "Cluster did not settle within 600s (notReady=$notReady terminating=$terminating pending=$pending)" }
        Start-Sleep -Seconds 5
    }
    Log "Cluster clean: $($deps.Count) deployments x 1 replica. Cooling down ${CooldownSec}s"
    Start-Sleep -Seconds $CooldownSec

    # ------------------------------------------------------------ 3. Prepare outputs and autoscaler
    if (Test-Path $OutDir) { Remove-Item -Recurse -Force $OutDir }
    New-Item -ItemType Directory -Force $OutDir | Out-Null
    $kb = Join-Path $CodeDir "Knowledge Base"
    if (Test-Path $kb) { Remove-Item -Recurse -Force $kb }
    Copy-Item -Recurse (Join-Path $CodeDir "kb_template") $kb

    $env:SMARTHPA_SCENARIO = $Scenario
    $env:SMARTHPA_DURATION = "$DurationSec"

    if ($Autoscaler -eq "k8shpa") {
        foreach ($d in $Deployments) {
            # kubectl >= 1.33 uses --cpu=<N>% (the % matters: without it the value is read as milliCPU)
            Invoke-Kubectl autoscale deployment $d "--cpu=$Threshold%" --min=1 "--max=$MaxR" | Out-Null
        }
        Log "Created $($Deployments.Count) Kubernetes HPAs (cpu=$Threshold%, max=$MaxR)"
        $controllerScript = "k8shpa_observer.py"
    } elseif ($Autoscaler -eq "prosmarthpa") {
        $controllerScript = "..\prosmarthpa\prosmart_hpa.py"
    } else {
        $controllerScript = "Microservice_Capacity_Analyzer.py"
    }
    $controllerPython = if ($Autoscaler -eq "prosmarthpa") { $ProSmartPython } else { $Python }

    $info = [ordered]@{
        autoscaler = $Autoscaler; scenario = $Scenario; run = $Run; max_replicas = $MaxR; cpu_threshold = $Threshold
        users = $Users; spawn_rate = $SpawnRate; duration_sec = $DurationSec; cooldown_sec = $CooldownSec
        host = $TargetHost; kube_context = $ctx; started_at = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    }

    # ------------------------------------------------------------ 4. Start recorder, Locust and controller together
    Log "Starting $controllerScript, cluster_recorder.py and Locust"
    $procs += Start-Process $Python -ArgumentList "cluster_recorder.py `"$RelOut\cluster_metrics.csv`" $($DurationSec + 30) 15" `
        -WorkingDirectory $CodeDir -NoNewWindow -PassThru -RedirectStandardError "$OutDir\recorder.err.log"
    $procs += Start-Process $Locust -ArgumentList "-f locustfile.py --host $TargetHost --headless -u $Users -r $SpawnRate -t ${DurationSec}s --csv `"$RelOut\locust`" --csv-full-history --only-summary" `
        -WorkingDirectory $CodeDir -NoNewWindow -PassThru -RedirectStandardOutput "$OutDir\locust.out.log" -RedirectStandardError "$OutDir\locust.err.log"
    $controller = Start-Process $controllerPython -ArgumentList $controllerScript `
        -WorkingDirectory $CodeDir -NoNewWindow -PassThru -RedirectStandardOutput "$OutDir\controller.out.log" -RedirectStandardError "$OutDir\controller.err.log"
    $null = $controller.Handle          # PowerShell 5.1 only reports ExitCode if the handle was opened while running
    $procs += $controller

    $t0 = Get-Date
    $monitorErrors = 0
    while (-not $controller.HasExited) {
        Start-Sleep -Seconds 30
        # progress display only: a network blip here must not kill the run (the controller has its own kubectl retry)
        try { $replicas = (Invoke-Kubectl get deployments -o "jsonpath={range .items[*]}{.metadata.name}={.spec.replicas} {end}") }
        catch { $monitorErrors++; $replicas = "WARNING: kubectl unreachable ($monitorErrors so far)" }
        Log ("{0,4:N0}s | {1}" -f ((Get-Date) - $t0).TotalSeconds, $replicas)
    }
    Log "Controller exited with code $($controller.ExitCode)"
    $info.monitor_kubectl_errors = $monitorErrors
    if ($monitorErrors) { Log "WARNING: kubectl was unreachable $monitorErrors time(s) during the run; check locust_failures.csv before using it" }
    foreach ($p in $procs) { if (-not $p.HasExited) { $p.WaitForExit(120000) | Out-Null } }

    $info.finished_at = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    $info.controller_exit_code = $controller.ExitCode
    if ($controller.ExitCode -ne 0) { $failed = $true }
}
catch {
    $failed = $true
    Log "ERROR: $_"
}
finally {
    # ------------------------------------------------------------ 5. Clean up and collect
    # /T also kills the multiprocessing Pool children, which otherwise keep the log files open
    foreach ($p in $procs) { if ($p -and -not $p.HasExited) { Log "Stopping PID $($p.Id)"; & taskkill /T /F /PID $p.Id 2>&1 | Out-Null; $p.WaitForExit(30000) | Out-Null } }
    if ($Autoscaler -eq "k8shpa") {
        & kubectl delete hpa --all --ignore-not-found | Out-Null
        if ($LASTEXITCODE -eq 0) { Log "Deleted Kubernetes HPAs" } else { Log "WARNING: could not delete HPAs, the next run's reset will retry" }
    }
    if (Test-Path $OutDir) {
        $kb = Join-Path $CodeDir "Knowledge Base"
        if (Test-Path $kb) { Copy-Item -Recurse -Force $kb (Join-Path $OutDir "knowledge_base") }
        & kubectl get pods -o wide | Out-File -Encoding utf8 (Join-Path $OutDir "pods_at_end.txt")
        # UTF-8 without BOM so Python's json.load can read it
        if ($info) { [IO.File]::WriteAllText((Join-Path $OutDir "run_info.json"), ($info | ConvertTo-Json), (New-Object Text.UTF8Encoding $false)) }
        if (-not $failed -and (Test-Path (Join-Path $OutDir "locust_stats_history.csv"))) {
            # a run the controller survived can still be damaged by the laptop losing the cluster (no load, failures)
            & $Python (Join-Path $CodeDir "check_run.py") $OutDir | ForEach-Object { Log $_ }
            if ($LASTEXITCODE -ne 0) { $failed = $true }
        }
        if ($failed) {
            # keep the data for diagnosis, but out of the run<N> folders the reports and comparison read
            $failedDir = Join-Path (Split-Path $OutDir) ("_failed_run{0}_{1}" -f $Run, (Get-Date -Format "yyyyMMdd-HHmm"))
            for ($i = 1; $i -le 6; $i++) {
                try { Move-Item $OutDir $failedDir -ErrorAction Stop; break }
                catch { if ($i -eq 6) { throw }; Start-Sleep -Seconds 5 }
            }
            Log "RUN FAILED - data moved to $failedDir (see controller.err.log). Rerun this run number."
        }
        else { Log "Results saved to $OutDir" }
        if (-not $failed -and $info -and (Test-Path (Join-Path $OutDir "locust_stats_history.csv"))) {
            # metrics.csv, summary.md and the three figures for this run
            & $Python (Join-Path $CodeDir "make_run_report.py") $OutDir
            if ($LASTEXITCODE -ne 0) { Log "WARNING: make_run_report.py failed (exit $LASTEXITCODE); data is saved, rerun it by hand" }
            # rebuild the cross-run trend charts of this scenario (results\<scenario>\comparison\)
            $compareArgs = @((Join-Path $CodeDir "make_comparison.py"), (Split-Path (Split-Path $OutDir)))
            if ($Run -eq 0) { $compareArgs += "--include-trials" }
            & $Python @compareArgs
            # user-side metrics of the scenario (latency, SLO, throughput); trial runs are too short for its phases
            & $Python (Join-Path $CodeDir "make_user_metrics.py") (Split-Path (Split-Path $OutDir))
        }
    }
}
if ($failed) { exit 1 }
