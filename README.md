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

*See troubleshooting for additional custom configurations* 

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

## Troubleshooting
1. Some systems have a different Python path. Run ```which python``` or ```which python3``` to find the path and update the ```ExecStart=``` section in the unit file.
2. While there is a roadmap item for a more automated installation, use ```systemctl status list-units``` and ```journalctl -xe``` if there are any issues starting the service.
3. Nextcloud will generally want "www-data:www-data" as the owner:group of the files.  Find this by running ```cat /etc/passwd``` and update config.yml with the numbers *(the owner and group are generally the same number)*

## Limitations
1. Due to the narrowed scope for the initial development cycle, the program will only handle a single top-level folder to update.  A roadmap item has been created to add multi-folder, multi-permission support options.
2. By default, the service does run as root.  For increased security, a dedicated service could be created and the unit file updated.  Advanced users can take this on and submit a procedure to be included in a future version.

## Roadmap
[ ] Guided installation procedure for setting up as a Systemd service

[ ] Add multi-folder/non-nested folder support.

[ ] Add multi-permission/owner:group support following multi-folder support release