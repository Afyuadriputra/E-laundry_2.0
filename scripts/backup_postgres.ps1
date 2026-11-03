<#
.SYNOPSIS
    E-Laundry 2.0 - Automated PostgreSQL Backup Script (PowerShell)
.DESCRIPTION
    Dumps PostgreSQL database, compresses into .sql.gz, and rotates old backups.
#>

param (
    [string]$BackupDir = ".\backups",
    [string]$ContainerName = "elaundry-db-prod",
    [string]$DbName = $env:POSTGRES_DB,
    [string]$DbUser = $env:POSTGRES_USER,
    [int]$RetentionDays = 14
)

if (-not $DbName) { $DbName = "elaundry_db" }
if (-not $DbUser) { $DbUser = "elaundry_user" }

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
if (-not (Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
}

$rawSqlFile = Join-Path $BackupDir "elaundry_backup_$timestamp.sql"
$gzFile = "$rawSqlFile.gz"

Write-Host "[INFO] Starting PostgreSQL backup for database: $DbName..." -ForegroundColor Cyan

$dockerRunning = docker ps --format '{{.Names}}' 2>$null | Select-String "^$ContainerName$"

if ($dockerRunning) {
    Write-Host "[INFO] Dumping from Docker container: $ContainerName..." -ForegroundColor Gray
    docker exec $ContainerName pg_dump -U $DbUser -d $DbName --clean --if-exists --no-owner > $rawSqlFile
} else {
    Write-Host "[INFO] Dumping via host pg_dump..." -ForegroundColor Gray
    pg_dump -U $DbUser -d $DbName --clean --if-exists --no-owner > $rawSqlFile
}

if ((Test-Path $rawSqlFile) -and ((Get-Item $rawSqlFile).Length -gt 0)) {
    Write-Host "[INFO] Compressing to GZip..." -ForegroundColor Gray
    $sourceBytes = [System.IO.File]::ReadAllBytes($rawSqlFile)
    $destinationFile = [System.IO.File]::Create($gzFile)
    $gzipStream = New-Object System.IO.Compression.GZipStream($destinationFile, [System.IO.Compression.CompressionMode]::Compress)
    $gzipStream.Write($sourceBytes, 0, $sourceBytes.Length)
    $gzipStream.Close()
    $destinationFile.Close()
    Remove-Item $rawSqlFile -Force

    $sizeMb = [math]::Round((Get-Item $gzFile).Length / 1MB, 2)
    Write-Host "[SUCCESS] Backup created: $gzFile ($sizeMb MB)" -ForegroundColor Green
} else {
    Write-Host "[ERROR] pg_dump output empty or failed." -ForegroundColor Red
    exit 1
}

# Cleanup retention
$cutoffDate = (Get-Date).AddDays(-$RetentionDays)
Get-ChildItem -Path $BackupDir -Filter "elaundry_backup_*.sql.gz" | Where-Object { $_.LastWriteTime -lt $cutoffDate } | ForEach-Object {
    Write-Host "[INFO] Removing expired backup: $($_.Name)" -ForegroundColor Yellow
    Remove-Item $_.FullName -Force
}

Write-Host "[SUCCESS] Backup workflow completed." -ForegroundColor Green

