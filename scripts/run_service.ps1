# PowerShell script to run the NER service on Windows

Write-Host "Starting NER Service (PowerShell)..."

# Prefer py -3.10 if available
$py = "python"
try {
    & py -3.10 -c "import sys" 2>$null
    $py = "py -3.10"
} catch {
    # fallback to python
}

if (-not (Test-Path venv)) {
    Write-Host "Creating virtual environment with $py..."
    & $py -m venv venv
}

# Activate venv for the current session
$activate = Join-Path -Path (Get-Location) -ChildPath "venv\Scripts\Activate.ps1"
if (Test-Path $activate) {
    Write-Host "Activating virtual environment..."
    . $activate
} else {
    Write-Warning "Could not find Activate.ps1; you may need to run: venv\Scripts\Activate.ps1"
}

Write-Host "Upgrading pip, setuptools, wheel..."
& $py -m pip install --upgrade pip setuptools wheel

Write-Host "Installing requirements..."
& $py -m pip install -r requirements.txt

Write-Host "Installing spaCy English model (en_core_web_sm)..."
try {
    & $py -m spacy download en_core_web_sm
} catch {
    Write-Warning "spacy download failed; installing wheel directly"
    & $py -m pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.0/en_core_web_sm-3.7.0-py3-none-any.whl
}

Write-Host "Starting API server on http://localhost:8000"
& $py -m uvicorn src.ner_service.main:app --host 0.0.0.0 --port 8000 --reload
