## Mock Arduino Simulator

This repository includes a mock Arduino script that can be used to test the dashboard serial communication flow without the physical hardware.

The mock simulator reproduces the basic Arduino behavior:

1. Receives `START` from the dashboard.
2. Simulates bottle movement.
3. Sends a `CONTROL` request to the Python application.
4. Receives `B`, `R` or `N` as the computer vision result.
5. Simulates product routing.

### Running the mock Arduino

```bash
python tools/mock_arduino.py
```

### Virtual serial ports

To connect the dashboard and the mock Arduino script, a pair of virtual serial ports is required.
On Windows, this project was tested using Virtual Serial Port Kit by creating a paired connection such as:

```bash
COM10 <-> COM11
```

Example setup:

```bash
mock_arduino.py uses COM10
FlexiLine dashboard connects to COM11
```

On Linux, a similar setup can be created using socat:

```bash
socat -d -d pty,raw,echo=0 pty,raw,echo=0
```

This will create two linked virtual ports such as:

```bash
/dev/pts/3 <-> /dev/pts/4
```