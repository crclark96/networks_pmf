# Networks Performace Measurement System

## Ryan Hebling, Collin Clark

## CPEG 419

### Usage:

All scripts are marked as executable. Run them using either `./receiver.py` or `python3 receiver.py` in the background or separate terminal windows.

`sender.py` and `receiver.py` should be launched first, either in the background using `./sender.py & ./receiver.py &` or in separate windows on the same machine, or on different machines. Be sure to change the corresponding IP address variables in the headers of the scripts if they are being used on different machines. The default IP is the local loopback address (127.0.0.1).

`controller.py` should be launched after both other scripts are running. Launch it with one of the following arguments: `--udp` or `--tcp`. They will initiate the udp and tcp measurement systems, respectively.

Once one protocol is run, all scripts will exit. They must all be relaunched to test another protocol. 