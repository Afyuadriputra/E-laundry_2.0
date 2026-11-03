<#
.SYNOPSIS
    E-Laundry 2.0 - Automated PostgreSQL Restore Script (PowerShell)
#>

param (
    [Parameter(Mandatory=$true)]
    [string]$BackupFile,
    [string]$ContainerName = "elaundry-db-prod",
    [string]$DbName = $env:POSTGRES_DB,
    [string]$DbUser = $env:POSTGRES_USER
)

if (-not $DbName) { $DbName = "elaundry_db" }
if (-not $DbUser) { $DbUser = "elaundry_user" }

if (-not (Test-Path $BackupFile)) {
    Write-Host "[ERROR] Backup file not found: $BackupFile" -ForegroundColor Red
    exit 1
}

Write-Host "=====================================================================" -ForegroundColor Yellow
Write-Host "WARNING: This operation will restore database '$DbName' from:" -ForegroundColor Yellow
Write-Host "  $BackupFile" -ForegroundColor Yellow
Write-Host "Existing data will be replaced per SQL dump commands." -ForegroundColor Yellow
Write-Host "=====================================================================" -ForegroundColor Yellow

$confirm = Read-Host "Are you sure you want to proceed? (Type 'yes' to proceed)"
if ($confirm -ne "yes") {
    Write-Host "[INFO] Restore aborted." -ForegroundColor Gray
    exit 0
}

Write-Host "[INFO] Decompressing $BackupFile..." -ForegroundColor Cyan
$tempSql = [System.IO.Path]::GetTempFileName() + ".sql"

$sourceFile = [System.IO.File]::OpenRead($BackupFile)
$gzipStream = New-Object System.IO.Compression.GZipStream($sourceFile, [System.IO.Compression.CompressionMode]::Decompress)
$destinationStream = [System.IO.File]::Create($tempSql)
$gzipStream.CopyTo($destinationStream)
$destinationStream.Close()
$gzipStream.Close()
$sourceFile.Close()

$dockerRunning = docker ps --format '{{.Names}}' 2>$null | Select-String "^$ContainerName$"

if ($dockerRunning) {
    Write-Host "[INFO] Restoring into Docker container: $ContainerName..." -ForegroundColor Gray
    Get-Content $tempSql | docker exec -i $ContainerName psql -U $DbUser -d $DbName
} else {
    Write-Host "[INFO] Restoring via host psql..." -ForegroundColor Gray
    Get-Content $tempSql | psql -U $DbUser -d $DbName
}

Remove-Item $tempSql -Force
Write-Host "[SUCCESS] Database '$DbName' successfully restored from $BackupFile." -ForegroundColor Green

