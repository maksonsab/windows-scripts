#RETURN LOCAL ADMINS
function Get-LocalAdministrators {  
    param ($strcomputer)  

    $admins = Get-WmiObject win32_groupuser –computer $strcomputer   
    $admins = $admins |? {$_.groupcomponent –like '*"LOCAL ADMINS GROUP NAME"'}  

    $admins | ForEach-Object {  
    $_.partcomponent –match ".+Domain\=(.+)\,Name\=(.+)$" > $nul  
    $matches[1].trim('"') + "\" + $matches[2].trim('"')  
    }  
}
#RETURN DOMIAN ADMINS
function Get-DomainAdministrators {  
    param ($strcomputer)  

    $admins = Get-WmiObject win32_groupuser –computer $strcomputer   
    $admins = $admins |? {$_.groupcomponent –like '*"DOMAIN ADMINS GROUP NAME"'}  

    $admins | ForEach-Object {  
    $_.partcomponent –match ".+Domain\=(.+)\,Name\=(.+)$" > $nul  
    $matches[1].trim('"') + "\" + $matches[2].trim('"')  
    }  
}

$host_pc = hostname
$admins = Get-LocalAdministrators($host_pc)
$domain_admins = Get-DomainAdministrators($host_pc)
Write-Host($domain_admins)
Write-Host($admins)
$users = @()
$allowed = @() #ALLOWED USERS TO BE ADMIN
$not_allowed = @()

#local
foreach($item in $admins){
    $item, $user = $item -split "\\"
    $users += $user
    $iscontains =$allowed -contains $user
    if (!$iscontains ) {
        Write-Host($user, 'not allowed to be admin')
        $not_allowed += $user
    }
}
#domain
foreach($item in $domain_admins){
    #$item, $user = $item  -split '\s+'
    $users += $item
    $iscontains =$allowed -contains $item
    if (!$iscontains ) {
        Write-Host($item, 'not allowed to be admin')
        $not_allowed += $item
    }
}
$not_allowed > file.txt
