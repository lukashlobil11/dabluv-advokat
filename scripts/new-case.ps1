[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[a-z0-9][a-z0-9-]{1,63}$')]
    [string]$Name
)

$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$casesRoot = Join-Path $repoRoot 'cases'
$template = Join-Path $casesRoot '_template'
$target = Join-Path $casesRoot $Name

if (-not (Test-Path -LiteralPath $template -PathType Container)) {
    throw "Chybí šablona: $template"
}

if (Test-Path -LiteralPath $target) {
    throw "Case již existuje: $target"
}

Copy-Item -LiteralPath $template -Destination $target -Recurse

$directories = @(
    'zadani',
    'dukazy',
    'kontrola-fu',
    'analyza',
    'reserse',
    'argumentace',
    'oponentura',
    'final'
)

foreach ($directory in $directories) {
    New-Item -ItemType Directory -Force -Path (Join-Path $target $directory) | Out-Null
}

$matterPath = Join-Path $target 'matter.yaml'
$matter = [System.IO.File]::ReadAllText($matterPath)
$matter = $matter.Replace('[NAZEV-CASE]', $Name)
[System.IO.File]::WriteAllText($matterPath, $matter, [System.Text.UTF8Encoding]::new($false))

Write-Output "Vytvořen důvěrný case: $target"
Write-Output "Git jej ignoruje; ověřte příkazem: git check-ignore -v cases/$Name/matter.yaml"
