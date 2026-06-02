# KARTRIX / PASZPORTOS node initialization and backup script
# Target: Dell hardware node from SGGW
# Purpose: prepare workspace, verify tooling, and create a local backup snapshot

[CmdletBinding()]
param(
    [string]$RootPath = (Get-Location).Path,
    [string]$NodeName = "Dell-SGGW",
    [string]$BackupRoot = "$env:USERPROFILE\KARTRIX_BACKUPS",
    [switch]$SkipBackup
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    Write-Host "[$timestamp] $Message"
}

function Ensure-Directory {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
    }
}

function Test-Command {
    param([string]$Name)
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

function New-BackupSnapshot {
    param(
        [string]$SourcePath,
        [string]$TargetRoot,
        [string]$NodeLabel
    )

    $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    $snapshotFolder = Join-Path $TargetRoot "$NodeLabel-$stamp"
    Ensure-Directory -Path $snapshotFolder

    $itemsToBackup = @(
        'node_setup',
        'config',
        'docs',
        'scripts'
    )

    foreach ($item in $itemsToBackup) {
        $sourceItem = Join-Path $SourcePath $item
        if (Test-Path -LiteralPath $sourceItem) {
            Copy-Item -Path $sourceItem -Destination $snapshotFolder -Recurse -Force
        }
    }

    $archivePath = "$snapshotFolder.zip"
    if (Test-Path -LiteralPath $archivePath) {
        Remove-Item -LiteralPath $archivePath -Force
    }
    Compress-Archive -Path (Join-Path $snapshotFolder '*') -DestinationPath $archivePath -Force

    Write-Log "Backup created: $archivePath"
    return $archivePath
}

Write-Log "Starting KARTRIX initialization for $NodeName"
Ensure-Directory -Path $RootPath
Ensure-Directory -Path $BackupRoot

$requiredCommands = @('git', 'powershell')
foreach ($command in $requiredCommands) {
    if (-not (Test-Command -Name $command)) {
        Write-Log "Missing command: $command"
    }
}

$nodeSetupPath = Join-Path $RootPath 'node_setup'
Ensure-Directory -Path $nodeSetupPath

$marker = Join-Path $nodeSetupPath '.kartrix-node.json'
$markerData = [ordered]@{
    nodeName = $NodeName
    rootPath = $RootPath
    initializedAt = (Get-Date).ToString('o')
    backupRoot = $BackupRoot
}
$markerData | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $marker -Encoding UTF8

if (-not $SkipBackup) {
    New-BackupSnapshot -SourcePath $RootPath -TargetRoot $BackupRoot -NodeLabel $NodeName | Out-Null
}

Write-Log 'Initialization complete.'
