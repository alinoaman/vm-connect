import paramiko
import schedule
import time
from datetime import datetime
import os
import logging
import socket
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# VM configurations
vms = [
    {
        "name": "Windows11",
        "ip": os.getenv('WINDOWS_IP'),
        "username": os.getenv('WINDOWS_USERNAME'),
        "password": os.getenv('WINDOWS_PASSWORD')
    },
    {
        "name": "Ubuntu-server",
        "ip": os.getenv('UBUNTU_IP'),
        "username": os.getenv('UBUNTU_USERNAME'),
        "key_filename": os.getenv('UBUNTU_KEYFILE')
    },
    {
        "name": "AlmaLinux9",
        "ip": os.getenv('ALMALINUX_IP'),
        "username": os.getenv('ALMALINUX_USERNAME'),
        "key_filename": os.getenv('ALMALINUX_KEYFILE')
    }
]

def update_machine(vm, max_retries=2):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    for attempt in range(max_retries):
        try:
            if "password" in vm:
                client.connect(vm["ip"], username=vm["username"], password=vm["password"], timeout=60, banner_timeout=200)
            else:
                client.connect(vm["ip"], username=vm["username"], key_filename=vm["key_filename"], timeout=60, banner_timeout=200)
            
            if vm["name"] == "Windows11":
                stdin, stdout, stderr = client.exec_command('powershell.exe "Get-WindowsUpdate -Install -AcceptAll -AutoReboot"')
            elif vm["name"] == "AlmaLinux9":
                stdin, stdout, stderr = client.exec_command('sudo dnf update -y')
            else:  # Ubuntu
                stdin, stdout, stderr = client.exec_command('sudo DEBIAN_FRONTEND=noninteractive apt-get update && sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade -y')
            
            output = stdout.read().decode()
            error = stderr.read().decode()
            
            result = "Success" if error == "" else "Failure"
            return f"{vm['name']}: {result}\nOutput: {output}\nError: {error}\n"
        
        except (paramiko.AuthenticationException, paramiko.SSHException, socket.error) as e:
            logging.error(f"Connection attempt {attempt + 1} failed for {vm['name']}: {str(e)}. Retrying...")
            time.sleep(2 ** attempt)  
        
        finally:
            client.close()
    
    return f"{vm['name']}: Failure\nError: Max retries reached. Unable to connect.\n"

def update_all_machines():
    report = f"Update Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    for vm in vms:
        report += update_machine(vm) + "\n"
    
    with open("Text_report.txt", "w") as f:
        f.write(report)
    
    logging.info("Update completed. Report saved to Text_report.txt")

# Schedule the task 
schedule.every().thursday.at("20:35").do(update_all_machines)

if __name__ == "__main__":
    logging.info("Scheduler started. Waiting for Thursday at 20:35 AM...")
    while True:
        schedule.run_pending()
        time.sleep(60)
