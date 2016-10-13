#Description

This is a Monero mining rig remote monitoring suite written in python and jQuery. It requires the use of XMR-proxy by Atrides (https://github.com/Atrides/xmr-proxy). It allows you to fully monitor your rigs via the web or locally.

A small disclaimer: I have never coded anything outside of R, so this has been something of an adventure, however humble it may be. The code is made with the 'men in sheds' methodology (i.e. never having seen something before, keep hitting it until it works), so there are large amounts of the code which I am sure seem at best humorous, and at worst quite baffling to the seasoned developer. It works though :)

#Features

* Detailed statistics per rig
* Share quality monitoring
* Uptime monitoring
* Pool connection monitoring
* Built-in web server, allowing you to monitor your rigs locally or remotely

#Installation
Windows:

- install python 2.7.3
- install all dependencies (pandas and numpy)
- install xmr-proxy (good guide for windows users here: https://bitcointalk.org/index.php?topic=735738.msg8331755#msg8331755)
- change logging to 'INFO' mode, to save space (in xmr-proxy-master/config.py)
- give your miners static IP addresses, if you can. 
- point all your miners to the IP running the xmr-proxy
- copy this repository into the parent directory of xmr-proxy (if not, you will have to edit the logfile path in mmm_config.py)
- open the mmm_windows_start.bat file (or make it run automatically at startup by making a shortcut, running shell:startup and putting it there)
- open your web browser to http://127.0.0.1:8000/mmm_web.html

Linux:

- install python 2.7.3
- clone install xmr-proxy (https://github.com/Atrides/xmr-proxy)
- clone this repository into the parent directory of xmr-proxy (if not, you will have to edit the logfile path in mmm_config.py).
- python mmm_code.py
- open your web browser to http://127.0.0.1:8000/mmm_web.html

#ToDo

* Refactor code with an asynch. server (such as Flask) to stop waste of CPU cycles when monitoring is inactive.
* Refactor everything as to lessen the anger of the coding gods

#Configuration

* Configuration is done via mmm_config.py. Web refresh rates must be adjusted in the mmm_js.js

#Donations 

* XMR:  4BHeoptXyZ4BkqHcyQo6QSA51q7M9uYAKB75bAuCwcbUavsbcjwe6ocJhRDyJCHSTd9Cenq418xq3P2dZK2J1CVHKbkTjTi

#Requirements

Monero Mining Monitor is built in python, tested on 2.7.3. Requirements:

* Python 2.7+
* pandas (https://pypi.python.org/pypi/pandas/0.19.0/#downloads)
* numpy (http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy)
* functioning installation of xmr-proxy

#Contact

* I am available via reddit (u/taushet)

#Credits

* This is a clown suit for xmr-proxy, so big thanks to Atrides.
* Thanks to the Bootstrap people for making css/javascript easy.

#License

* GNU GENERAL PUBLIC LICENSE v3
