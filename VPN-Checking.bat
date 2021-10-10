:check_internet
ping ya.ru 
if %errorlevel% EQU 0 (cls & echo Internet OK!) else ( cls & echo No enternet connection & timeout 60 & goto check_internet )

:check_vpn
ping %vpn_gateway%
echo off
if %errorlevel% EQU 0 (echo VPN connection OK! & timeout 60 & cls & goto check_vpn) else ( echo Can't reach VPN Gateway. Trying to connect. & goto connect_vpn)

:connect_vpn
rasdial.exe %vpn_name% %vpn_login% %vpn_pass% & echo %errorlevel%
if %errorlevel% EQU 0 ( cls & echo VPN connected & goto check_vpn ) else ( goto check_internet )
