while ($true) {
	$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
	$LogMessage = "[$Timestamp] Фоновый мониторинг активности PowerShell в Сессии 0. Статус: OK"

	Add-Content -Path "C:\\ps_service_log.txt" -Value $LogMessage  

	Start-Sleep -Seconds 5
}