Import-Module ActiveDirectory
Get-ADUser -Filter * -SearchBase "OU=group,DC=domain,DC=name" |
  Set-ADUser -PasswordNeverExpires:$True
