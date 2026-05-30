
#!/bin/bash

# build packages
python3 ./build_linux.py

# build standalone binary
./build_linux_standalone.sh
