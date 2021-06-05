# Nextcloud Scanner
Forked project from the permcorrect project [https://github.com/iwt-cmd/permcorrect](https://github.com/iwt-cmd/permcorrect).  Intended to be ran as a systemd service, the program monitors for changes made within a folder and updates all files with the desired owner/permission.  If any files need to be corrected, the program will also run the Nextcloud database sync command.  This effectively allows for Nextcloud to handle incoming files outside of the usual upload methods.  Originally designed to allow for FTP uploads from a network scanner.

## Components
**nextcloud-scanner.py** : main program file to be ran as a service

**config.yml** : configuration paramaters for root folder location, log file location and desired owner/permission settings.  
*Note: nextcloud-scanner.py expects config.yml to be located in **/lib/systemd/system/nextcloud-scanner.d/**. "with open(..." will need to be manually updated if located elsewhere*

**nextcloud-scanner.service** : systemd unit file installed by default into */lib/systemd/system*

## Installation: Systemd Service *(recommended)*
1. Clone repo to local system
2. Create */lib/systemd/system/nextcloud-scanner.d/*
3. Update config.yml with desired paramaters
4. Move config.yml and nextcloud-scanner.py into nextcloud-scanner.d
5. Move nextcloud-scanner.service into */lib/systemd/system/*
6. Run ```sudo systemctl daemon-reload```
7. Run ```sudo systemctl start nextcloud-scanner.service```
8. Enable service auto-start by running ```sudo systemctl enable nextcloud-scanner.service```
9. Place an incorrect file within the monitored folder and confirm it is corrected within the wait period (default 5 seconds) as well as an entry created in configured log file location (default */var/log/nextcloud-scanner.log*)

## Installation: Cronjob
1. Clone repo to local system
2. Modify nextcloud-scanner.py as follows:
    - Remove ```Import systemd.daemon```
    - Remove ```time.sleep(1)``` and ```systemd.daemon.notify('READY=1')```
    - Remove ```While True:``` loop
    - Remove ```time.sleep(5)```
    - Adjust indentation of the FOR loops as necessary
3. Update config.yml with desired paramaters
4. Move config.yml and nextcloud-scanner.py into desired folder
5. Create Cronjob as necessary