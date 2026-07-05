# Lighter
Sync your smart bulbs to your laptop screen.

## Running Lighter
- Install the system packages using this command
  ```bash
  sudo apt install python3-gi gir1.2-gstreamer-1.0 gstreamer1.0-plugins-good gstreamer1.0-plugins-base gstreamer1.0-pipewire python3-dbus
  ```
- Create a virtualenv with the system packages
  ```bash
  python3 -m venv --system-site-packages .venv
  ```
- Activate the environment
  ```bash
  source .venv/bin/activate
  ```
- Install Python packages
  ```bash
  pip install -r requirements.txt
  ```
- Run Lighter
  ```bash
  python lighter.py
  ```
- You would be asked to give screengrab permission, allow it. Lighter uses it to capture the screen to detect the color to be set.

# References
- [Loop testing](https://www.youtube.com/watch?v=IVdyt2pNxn8)
