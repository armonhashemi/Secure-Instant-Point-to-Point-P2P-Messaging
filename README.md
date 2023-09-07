# ComputerSecurity-Project

## Overview
There are two main ways of using this project. The first is to simulate both the client and the server on one laptop using
two terminal windows, or this project can be used by two laptops or virtual machines communicating with each other over the network.

This can be accomplished by setting the ip_address and port variables in main.py to the server's ip_address and port or if simulating on one laptop you can use
127.0.0.1 as the ip_address. Next, you must set the port. Depending on the network, the port may be busy, thus picking a port may require some experimentation. 

After these variables have been set, both laptops (or terminals) can run the main.py function. From there the user that has chosen to be the server will select "s" in the terminal, then the client should select "c". Next, the UI will appear for both the users. From there, the users can securely send and recieve messages following the protocols listed for this assignments.

## Required Dependencies
It is recommended the you use Python 3.9.16 in order for ensured compatibility. You should also run 'pip install -r requirements.txt' in the cloned root project directory to install all the dependencies needed.
