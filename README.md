# Permission Correction
Python-based service to change files within a folder to the desired owner and permission level.  Originally developed to correct owern/permissions for files uploaded from scanner into Nextcloud over FTP.  

## Components
**permcorrect.py** : main program file to be ran as a service

**config.yml** : configuration paramaters for root folder location, log file location and desired owner/permission settings.  
*Note: permcorrect.py expects config.yml to be located in **/lib/systemd/system/permcorrect.d/**. "with open(..." will need to be manually updated if located elsewhere*

**permcorrect.service** : systemd unit file installed by default into */lib/systemd/system*

## Installation: Systemd Service *(recommended)*
1. Clone repo to local system
2. Create */lib/systemd/system/permcorrect.d/*
3. Update config.yml with desired paramaters
4. Move config.yml and permcorrect.py into permcorrect.d
5. Move permcorrect.service into */lib/systemd/system/*
6. Run ```sudo systemctl daemon-reload```
7. Run ```sudo systemctl start permcorrect.service```
8. Enable service auto-start by running ```sudo systemctl enable permcorrect.service```
9. Place an incorrect file within the monitored folder and confirm it is corrected within the wait period (default 5 seconds) as well as an entry created in configured log file location (default */var/log/permcorrect.log*)

## Installation: Cronjob
1. Clone repo to local system
2. Modify permcorrect.py as follows:
    - Remove ```Import systemd.daemon```
    - Remove ```time.sleep(1)``` and ```systemd.daemon.notify('READY=1')```
    - Remove ```While True:``` loop
    - Remove ```time.sleep(5)```
    - Adjust indentation of the FOR loops as necessary
3. Update config.yml with desired paramaters
4. Move config.yml and permcorrect.py into desired folder
5. Create Cronjob as necessary
