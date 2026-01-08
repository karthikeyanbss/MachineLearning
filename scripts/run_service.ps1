# PowerShell script to run the NER service on Windows

Write-Host "Starting NER Service (PowerShell)..."

if (-not (Test-Path venv)) {
    Write-Host "Creating virtual environment..."
    # Use system 'python' to create venv; user can recreate with a specific interpreter if needed
    & python -m venv venv
}

# Activate venv for the current session
$activate = Join-Path -Path (Get-Location) -ChildPath "venv\Scripts\Activate.ps1"
if (Test-Path $activate) {
    Write-Host "Activating virtual environment..."
    . $activate
} else {
    Write-Warning "Could not find Activate.ps1; you may need to run: venv\Scripts\Activate.ps1"
}

# Prefer the venv python executable after activation
$venvPython = Join-Path -Path (Get-Location) -ChildPath "venv\Scripts\python.exe"
if (Test-Path $venvPython) {
    $pythonExe = $venvPython
} else {
    # Fallback to system python or py.exe
    if (Get-Command python -ErrorAction SilentlyContinue) { $pythonExe = "python" }
    elseif (Get-Command py -ErrorAction SilentlyContinue) { $pythonExe = "py" }
    else { throw "No Python interpreter found. Install Python and retry." }
}

Write-Host "Using Python: $pythonExe"

Write-Host "Upgrading pip, setuptools, wheel..."
& $pythonExe -m pip install --upgrade pip setuptools wheel

Write-Host "Installing requirements..."
& $pythonExe -m pip install -r requirements.txt

Write-Host "Installing spaCy English model (en_core_web_sm) via matching wheel..."
# Use model wheel version that matches spaCy 3.7.x installed in requirements
$modelVer = "3.7.0"
$wheelUrl = "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-$modelVer/en_core_web_sm-$modelVer-py3-none-any.whl"
Write-Host "Installing model wheel: $wheelUrl"
& $pythonExe -m pip install $wheelUrl

Write-Host "Starting API server on http://localhost:8000"
& $pythonExe -m uvicorn src.ner_service.main:app --host 0.0.0.0 --port 8000 --reload
