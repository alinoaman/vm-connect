# VM-Connect Project

This project is designed to update Windows, Ubuntu, and AlmaLinux virtual machines (VMs) by connecting to them via SSH and executing the necessary commands. The process is automated using a scheduler that runs at a specified time each week.

## Prerequisites

- Python 3.x installed on your machine
- Virtual machines set up and accessible via SSH
- A `.env` file containing your VM credentials

## Setup Instructions

### 1. Clone the Repository

First, clone the repository to your local machine.

```bash
git clone https://github.com/your-repository/vm-connect.git
cd vm-connect
```

### 2. Create a Virtual Environment

Set up a virtual environment to manage dependencies.

```bash
python -m venv venv
```

Activate the virtual environment:

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Linux/MacOS:**
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

Install the required Python packages using `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4. Set Up the `.env` File

Create a `.env` file in the project root directory and add the following environment variables, replacing the placeholders with your actual VM details:

```plaintext
# .env file

# Windows VM
WINDOWS_IP=your-windows-ip
WINDOWS_USERNAME=your-windows-username
WINDOWS_PASSWORD=your-windows-password

# Ubuntu VM
UBUNTU_IP=your-ubuntu-ip
UBUNTU_USERNAME=your-ubuntu-username
UBUNTU_KEYFILE=path-to-your-ubuntu-keyfile

# AlmaLinux VM
ALMALINUX_IP=your-almalinux-ip
ALMALINUX_USERNAME=your-almalinux-username
ALMALINUX_KEYFILE=path-to-your-almalinux-keyfile
```

### 5. Running the Project

Once your environment is set up, run the script to start the scheduler.

```bash
python index.py
```

The scheduler will wait for the specified time and then automatically connect to each VM, perform the updates, and generate a report.

### 6. Modifying the Schedule

The current schedule is set to run every Thursday at 8:35 PM. To change this, edit the following line in `index.py`:

```python
schedule.every().thursday.at("20:35").do(update_all_machines)
```

You can modify the day and time according to your needs. For example, to run the task every Sunday at 7 PM, you would change it to:

```python
schedule.every().sunday.at("19:00").do(update_all_machines)
```

### 7. Viewing the Report

After the script runs, a report will be generated and saved as `Text_report.txt` in the project directory. The report contains the success or failure status of each VM update.
