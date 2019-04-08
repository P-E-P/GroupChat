# A simple web chat.
A simple web chat using TCP protocol.
# Usage

## Client
Launch `__main__.py` using python in `src/client` if you wish to launch a client.
The address of the server is required, for example if you wish to reach a server locally use this command in the client folder:
```
python3 __main__.py localhost
```
More options are available to specify the port, to change the username... Check them out by using `-h` or `--help` on the client.
## Server
Launch `__main__.py` using python in `src/server` if you wish to launch a server. The default listening port is 12000, if you wish to change it use `-p` or `--port` argument. More arguments are available, check them out using `-h` or `--help`.