if (-not (Test-NetConnection 127.0.0.1 -Port 11434 -InformationLevel Quiet)) {
    $ollama = (Get-Command ollama -ErrorAction SilentlyContinue).Source

    if (-not $ollama) {
        $default = "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"

        if (Test-Path $default) {
            $ollama = $default
        }
    }

    if ($ollama) {
        $p = Start-Process $ollama -WindowStyle Hidden -PassThru
        Start-Sleep -Milliseconds 800
        Stop-Process -Id $p.Id -Force
    }
    else {
        Write-Host "Ollama nicht gefunden - überspringe Ollama-Start."
    }
}
else {
    Write-Host "Ollama läuft bereits."
}