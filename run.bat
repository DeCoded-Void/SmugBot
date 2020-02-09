@echo off
color 0e
Title SmugBot by DeCoded_Void
echo.

echo 000000000   00000000  000000000000
echo 000000000     000000   00000000000
echo 000 00000       0000    0000000000
echo 0    0000          0      00000000
echo         0                  0000000
echo    ######               #######000
echo  ##     ###           ###      ## 
echo            #         #            
echo ##########             ###########
echo #  #@@@@@####        ####@@@@@#  #
echo  # #@@@@@@@#           #@@@@@@# #
echo    ##@@@@@@#           #@@@@@##   
echo    ##@@@@@##           #@@@@@##   
echo     #@@@@##             #@@@@#    
echo      #####               ####     
echo              #     #             0
echo 0             #####             00
echo 00                            0000
echo 000000                      000000
echo 0000  00                  00  0000
echo 00000   000000000000000000   00000
echo.
echo Booting up...
echo.

:loop
python "bot.py"
echo.
echo Bot Crashed/Shutdown on %date% at %time%

if exist shutdown.txt (
	del shutdown.txt
	exit
) else (
  :: Restarts and puts a 25 second timer so it doesn't spam
	echo Attempting to restart...
	echo.
	timeout 25 > NUL
	goto loop
)
