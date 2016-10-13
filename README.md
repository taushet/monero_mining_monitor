#Description

This is a Monero mining rig remote monitoring suite written in python and jQuery. It requires the use of XMR-proxy by Atrides (https://github.com/Atrides/xmr-proxy). I have never coded anything outside of R, so this has been something of an adventure, however humble it may be. 

The code is made with the 'men in sheds' methodology (i.e. never having seen something before, keep hitting it until it works), so there are large amounts of the code which I am sure seem at best humorous, and at worst quite baffling to the seasoned developer. 

#Features

* Detailed statistics per rig.
* Share quality monitoring
* Uptime monitoring
* Built-in web server, allowing you to monitor your rigs locally or remotely.

#How to use

* Windows: 
- install python 2.7.3
- install all dependencies (pandas and numpy)
- install xmr-proxy (good guide for windows users here: https://bitcointalk.org/index.php?topic=735738.msg8331755#msg8331755)
- change logging to 'INFO' mode, to save space (in xmr-proxy-master/config.py)
- give your miners static IP addresses, if you can. 
- point all your miners to the IP running the xmr-proxy
- copy this repository into the parent directory of xmr-proxy (if not, you will have to edit the logfile path in MMM.py)
- open the MMM.bat file (or make it run automatically at startup by making a shortcut, running shell:startup and putting it there)
- watch your rigs.

#ToDo

* Refactor code with an asynch. server (such as Flask) to stop waste of CPU cycles when monitoring is inactive.
* Refactor everything as to lessen the anger of the coding gods

#Configuration

* Configuration is done both in the javascript file (monitor_js.js) and the main python file (MMM.py)

#Donations 

* XMR:  4BHeoptXyZ4BkqHcyQo6QSA51q7M9uYAKB75bAuCwcbUavsbcjwe6ocJhRDyJCHSTd9Cenq418xq3P2dZK2J1CVHKbkTjTi

#Requirements

Monero Mining Monitor is built in python, tested on 2.7.3. Requirements:

* Python 2.7+
* pandas (python add-on)
* numpy (python add-on, http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy)
* functioning installation of xmr-proxy

#Installation

* just copy and start xmr-proxy.py

#Contact

* I am available via reddit (u/taushet)

#Credits

* This is a clown suit for the logfile of xmr-proxy, so big thanks to Atrides.
* Thanks to the Bootstrap people for making css/javascript easy.

#License

* GNU GENERAL PUBLIC LICENSE v3