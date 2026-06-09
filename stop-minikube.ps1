$ErrorActionPreference = "Stop"

Write-Host "Stopping kubectl port-forward (if running)..."
Get-CimInstance Win32_Process |
    Where-Object { $_.Name -like "kubectl*" -and $_.CommandLine -like "*port-forward*" } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force }

Write-Host "Deleting Kubernetes deployment..."
kubectl delete -f myapp.yml

Write-Host "Done."
