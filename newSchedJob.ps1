$jobname = "Set AD passwords to Never Expire"
$script =  "C:\Users\admin\pwdNeverExpire.ps1 -Server your-Server-Hostname"
$repeat = (New-TimeSpan -Days 7)

# Script will run as user specified and will run every week as specified in $repeat.
$scriptblock = [scriptblock]::Create($script)
$trigger = New-JobTrigger -Once -At (Get-Date).Date -RepeatIndefinitely -RepetitionInterval $repeat
$msg = "Enter the username and password that will run the task";
$credential = $Host.UI.PromptForCredential("Task username and password",$msg,"$env:userdomain\$env:username",$env:userdomain)

$options = New-ScheduledJobOption -RunElevated -ContinueIfGoingOnBattery -StartIfOnBattery
Register-ScheduledJob -Name $jobname -ScriptBlock $scriptblock -Trigger $trigger -ScheduledJobOption $options -Credential $credential
