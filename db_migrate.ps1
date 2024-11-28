# Define paths
$migrationsPath = ".\migrations\"
$revisionFile = ".\db_revision.txt"

# Function to get migration files
function Get-Migrations {
    Get-ChildItem -Path $migrationsPath -File | Sort-Object Name | Select-Object -ExpandProperty Name
}

# Ensure fzf is installed
if (-not (Get-Command fzf -ErrorAction SilentlyContinue)) {
    Write-Error "fzf is not installed. Please install it to proceed."
    exit 1
}

# Get all migrations
$migrations = Get-Migrations

# Check if the revision file exists
if (-not (Test-Path $revisionFile)) {
    Write-Host "No revision file found. Listing all migrations..."
    $appliedMigration = $migrations | fzf --prompt "Select the last migration that was already applied: "

    if (-not $appliedMigration) {
        Write-Error "No migration selected. Exiting."
        exit 1
    }

    # Extract numeric index and write to revision file
    $appliedIndex = $appliedMigration -split '_' | Select-Object -First 1
    $appliedIndex | Out-File $revisionFile
    Write-Host "Set current revision to: $appliedIndex"
    exit 0
}

# Read the current revision
$currentRevision = Get-Content $revisionFile -Raw
Write-Host "Current revision: $currentRevision"

# Get migrations to apply
$remainingMigrations = $migrations | Where-Object {
    ($_ -split '_')[0] -as [int] -gt $currentRevision
}

if (-not $remainingMigrations) {
    Write-Host "No migrations to apply. Exiting."
    exit 0
}

if ($remainingMigrations.Count -eq 1) {
    $nextMigration = $remainingMigrations
    Write-Host "Only one migration available: $nextMigration"
} else {
    $nextMigration = $remainingMigrations | fzf --prompt "Select the migration to apply next: "
    if (-not $nextMigration) {
        Write-Error "No migration selected. Exiting."
        exit 1
    }
}

# Apply the selected migration
$nextIndex = $nextMigration -split '_' | Select-Object -First 1
Write-Host "Applying migration: $nextMigration"

# Here you can add the logic to actually apply the migration (e.g., executing SQL scripts)
psql -d mydb -f "migrations/$nextMigration"


# Update the revision file
$nextIndex | Out-File $revisionFile
Write-Host "Updated current revision to: $nextIndex"
