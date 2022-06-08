goto %1

:cpu
echo CPU temp is high >> C:\zabbix\Aida\warrning.txt
exit

:motherboard
echo Motherbord temp is high >> C:\zabbix\Aida\warrning.txt
exit

:3v
echo Problem with 3.3V line on PSU >> C:\zabbix\Aida\warrning.txt
exit

:5v
echo Problem with 5V line on PSU >> C:\zabbix\Aida\warrning.txt
exit

:12v
echo Problem with 12V line on PSU >> C:\zabbix\Aida\warrning.txt
exit

:drive
echo %2 temperature too high >> C:\zabbix\Aida\warrning.txt
exit