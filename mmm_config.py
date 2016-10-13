#CONFIG
TIME_SHORT = '1D' 										#The 'short' period. Options: '1D' to '7D' (n days)
SHORT_STEP = '20min'									#The timestep in the 'short' graph. Options: '10min' to '24H'
LONG_STEP = '2H'										#The timestep in the 'long' graph. Options: '1H' to '365D'
REPEAT = 601											#Monitoring refresh (s). Recommend 601. Website refresh is independent of this value.
LOG_FILE_PATH = "../xmr-proxy-master/log/logfile.log"	#The path to the log file (can be http:// for true remote monitoring)
INIT_WEB_SERVER = True									#You will want this on unless you already have a web server set up.
PORT = 8000												#Web server port