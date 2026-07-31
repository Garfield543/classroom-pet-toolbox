# Netlify Zero-Dependency Deployment Script for Windows PowerShell
# Packs the public folder and deploys it to Netlify using the REST API.

$ErrorActionPreference = "Stop"

# 1. Load NETLIFY_AUTH_TOKEN from .env files
$token = $null
$envPaths = @(
    "c:\2026antigravity2\.env",
    "$env:USERPROFILE\.env"
)

foreach ($path in $envPaths) {
    if (Test-Path $path) {
        $lines = Get-Content $path
        foreach ($line in $lines) {
            # Skip comments or empty lines
            if ($line -match "^\s*#") { continue }
            if ($line -match "^NETLIFY_AUTH_TOKEN=(.+)$") {
                $token = $Matches[1].Trim()
                # Remove quotes if present
                $token = $token -replace '^["'']|["'']$'
                break
            }
        }
    }
    if ($token) { break }
}

if (-not $token) {
    Write-Error "Error: NETLIFY_AUTH_TOKEN not found in .env files!"
    Write-Host "Please ensure you have saved your Netlify API token in C:\Users\User\.env"
    exit 1
}

# 2. Package the website files
$publicDir = "c:\2026antigravity2\public"
if (-not (Test-Path $publicDir)) {
    Write-Error "Error: Public directory not found at $publicDir"
    exit 1
}

# Generate a temporary zip file path
$tempZip = Join-Path $env:TEMP "netlify_deploy_$([Guid]::NewGuid().ToString().Substring(0,8)).zip"
if (Test-Path $tempZip) { Remove-Item $tempZip }

Write-Host "Packing website files from $publicDir into a zip archive..." -ForegroundColor Cyan

# Compress the contents of public folder to the zip root
# We use Get-ChildItem to ensure files are at the root level of the zip archive.
Compress-Archive -Path (Join-Path $publicDir "*") -DestinationPath $tempZip

Write-Host "Zip archive created successfully at $tempZip" -ForegroundColor Green

# 3. Deploy to Netlify REST API
Write-Host "Sending deployment to Netlify API..." -ForegroundColor Cyan

$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type"  = "application/zip"
}

try {
    # Read zip file bytes
    $bytes = [System.IO.File]::ReadAllBytes($tempZip)
    
    # POST to /sites endpoint to create a site and deploy instantly
    $response = Invoke-RestMethod -Uri "https://api.netlify.com/api/v1/sites" -Method Post -Headers $headers -Body $bytes
    
    Write-Host "`n==================================================" -ForegroundColor Green
    Write-Host "🚀 Deployment Successful!" -ForegroundColor Green
    Write-Host "==================================================" -ForegroundColor Green
    Write-Host "Site Name : $($response.name)"
    Write-Host "Live URL  : $($response.url)"
    Write-Host "Admin URL : $($response.admin_url)"
    Write-Host "Site ID   : $($response.id)"
    Write-Host "==================================================`n" -ForegroundColor Green
    
} catch {
    Write-Host "`n❌ Deployment Failed!" -ForegroundColor Red
    if ($_.Exception.Response) {
        $streamReader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $errResp = $streamReader.ReadToEnd()
        Write-Host "Error details: $errResp" -ForegroundColor Red
    } else {
        Write-Host "Error message: $($_.Exception.Message)" -ForegroundColor Red
    }
    exit 1
} finally {
    # Clean up the temporary zip file
    if (Test-Path $tempZip) {
        Remove-Item $tempZip
        Write-Host "Temporary files cleaned up." -ForegroundColor Gray
    }
}
