import time
from datetime import datetime
import systemd.daemon
import os
import yaml
import logging
import sys
import signal

def sig_handler(sig, frame):
    sys.exit(0)

if __name__ == '__main__':
    
    time.sleep(1)
    systemd.daemon.notify('READY=1')
    #Config file is expected at /lib/systemd/system/nextcloud-scanner.d/.  Update below as well as Systemd unit file if changed
    try:
        with open("/lib/systemd/system/nextcloud-scanner.d/config.yml", "r") as yfile:
            cfg = yaml.load(yfile, Loader=yaml.FullLoader)
    except:
        logging.warning("Config file not found")
        signal.signal(signal.SIGINT, sig_handler)

    #Set values from config file. Will need to restart service if config.yml updated
    try:    
        root_path = cfg["paths"]["root_path"]
        log_path =  cfg["paths"]["log_path"]
        owner_uid = cfg["params"]["uid"]
        owner_gid = cfg["params"]["gid"]
    except:
        logging.warning("Config file not formatted correctly or missing values")
        signal.signal(signal.SIGINT, sig_handler)
    
    #Main loop.  Change time.sleep(5) if longer or shorter check interval needed
    while True:
        
        for root, dirs, files in os.walk(root_path, topdown=False):
            for name in files:
                path = os.path.join(root, name)
                perm = (oct(os.stat(path).st_mode))[-3:]
                owner = os.stat(path).st_uid
                group = os.stat(path).st_gid
                #Uses octal format, update last 3 digits for desired permission
                if ((perm != "664") or (owner != owner_uid) or (group != owner_gid)):
                    now = datetime.now()
                    now = time.strftime("%H:%M:%S")
                    f = open(log_path, "a")
                    f.write(now)
                    f.write( f"  {perm} {owner} {group} {path} >> ")
                    #If comparision above updated, update os.chmod below to match
                    os.chmod(path, 0o0664)
                    os.chown(path, owner_uid, owner_gid)
                    path = os.path.join(root, name)
                    perm = (oct(os.stat(path).st_mode))[-3:]
                    owner = os.stat(path).st_uid
                    group = os.stat(path).st_gid
                    f.write( f"{perm} {owner} {group} {name}")
                    f.write("\n")
                    f.close()
        time.sleep(5)