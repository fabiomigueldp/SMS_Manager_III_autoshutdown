
# autoshtdwn.py

This project contains a Python script named `autoshtdwn.py`, designed to monitor the battery level of a UPS connected via a serial port (`/dev/ttyUSB0`). If the battery level falls below a specified threshold, the script will automatically shut down the computer to prevent data loss.

## Prerequisites

- Python 3.x
- `pyserial` library: Install with `pip install pyserial`
- Access to the serial device `/dev/ttyUSB0`

## Script Overview

The script performs the following actions:

1. Opens a serial connection to the UPS.
2. Sends a command to the UPS to retrieve the battery status.
3. Parses the response and checks the battery level.
4. If the battery level is below the defined threshold (default: 15%), it triggers a system shutdown.

## Installation and Setup

### 1. Save the Script

Save the `autoshtdwn.py` script in the desired directory, for example, `/path/to/your/script/`.

### 2. Create a Systemd Service

To run the script automatically at startup and restart it in case of failure, create a systemd service:

1. Create the service file:

```bash
sudo nano /etc/systemd/system/autoshtdwn.service
```

2. Add the following content, replacing placeholders with appropriate values:

```ini
[Unit]
Description=Script to monitor UPS battery level and shutdown the computer if necessary
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/your/script/autoshtdwn.py
WorkingDirectory=/path/to/your/script/
Restart=always
User=your_user
Group=your_group
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=ups_monitor
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

3. Enable and start the service:

```bash
sudo systemctl enable autoshtdwn.service
sudo systemctl start autoshtdwn.service
```

### 3. Adjust Permissions

To allow the script to access the serial port (`/dev/ttyUSB0`), ensure your user is part of the `dialout` group:

```bash
sudo usermod -aG dialout your_user
```

You may need to log out and log back in for the group change to take effect.

### 4. Check the Service Status

To verify that the service is running correctly:

```bash
sudo systemctl status autoshtdwn.service
```

### 5. Logging

The script logs its activities in two places:

- **Console Output:** Displays real-time battery status.
- **Log File (`ups_monitor.log`):** Stores error and status messages for later review.

## Customization

- **Battery Threshold:** The default shutdown threshold is 15%. You can change this by modifying the `UPS_BATERY_LEVEL` variable in the script.
- **Serial Port:** If your UPS is connected to a different port, change the `SERIAL_PORT` variable.
- **Shutdown Command:** The shutdown command is set for Unix/Linux/Mac systems. Modify it if you're using a different operating system.

## License

This project is licensed under the MIT License.
