Installieren Sie Windows Linux Subsystem + Ubuntu 22.04 auf Ihrem Windows PC:

1. Öffne Powershell.exe > gib ".\install_wsl-step1.ps1" ein.
2. Wahrscheinlich musst du deinen PC nach Schritt 1 neu starten, fahre danach mit der Datei aus Schritt 3 fort.
3. Öffne Powershell.exe > gib ".\install_wsl-step2.ps1" ein.


////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////


Installiere alles, was du für die Ubuntu-Installation benötigst:

1. chmod +x install.sh
2. ./install.sh
3. python3 linux.py 


////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////


Installiere alles, was auf Windows benötigt wird:

1. Öffne Powershell.exe > ".\windows-setup.ps1"
2. PC restarten
3. cmd.exe öffnen
4. cd "C:\Users\XXX\Desktop\paperMC"
5. python windows.py
6. Der Rest sollte sich von selber erklären.

(Bei Schritt 4 muss der Ordner mit dem Server natürlich auf dem Desktop liegen.)
(Bei Schritt 5 "python3 windows.py" versuchen, falls der normale Python command nicht geht)