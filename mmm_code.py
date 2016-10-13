import time, datetime, re, csv, os, threading
import pandas as pd
import numpy as np
import mmm_files.texttime as texttime
from datetime import date
from datetime import datetime
import mmm_config as conf

#File Paths
int_path = "mmm_files/data/"
total_file = int_path + "totals.csv"
total_html = int_path + "totals.html"
total_short_file = int_path + "totalsShort.csv"
total_short_html = int_path + "totalsShort.html"
hash_file = int_path + "hashAll.csv"
hash_short_file = int_path + "hashShort.csv"
pool_file = int_path + "pool.csv"
pool_html = int_path + "pool.html"
pool_string_html = int_path + "poolString.html"
server_string_html = int_path + "server_info.html"
log_string_html = int_path + "logging_start.html"
info_html = int_path + "info_s.html"
short_heading_html = int_path + "short_heading.html"
long_heading_html = int_path + "long_heading.html"
scratch_file = int_path + "scratch.txt"

#Group by time periods
def timeGroup (frame, step, file_csv): 
	dfx = frame.set_index(['time'])
	dfx = dfx[dfx.status == 'accepted']
	grouper = dfx.groupby([pd.TimeGrouper(step), 'Miner'])
	dfTimeS = grouper['Miner'].count().unstack('Miner').fillna(0)
	dfTimeS = dfTimeS[:-1] #There are arguments for and against this. The final group is not 'complete', so we will not include it.
	dfTimeS.to_csv(file_csv, encoding='utf-8')
	return dfTimeS

#Summary tables
def totalCount (frame, time_frame, file_csv, file_html):
	#Uptime (called 'A', a percentage of time periods alive)
	uptime = 100 - 100 * (time_frame == 0).mean()
	uptime = uptime.to_frame()
	uptime.columns = ['A']
	uptime[['A']] = uptime[['A']].astype(int) 
	
	#Everything else
	frame['status_bool'] = frame.status.eq('accepted') * 1
	dfTotal = frame.groupby('Miner').agg(
		dict(status=dict(Shares='count'),
			 status_bool=dict(Accepted='sum',
							  Q=lambda x: int(np.sum(x) * 1. / np.size(x)*100)),
			 time=dict(Last='last')
			))
	dfTotal.columns = dfTotal.columns.droplevel(0)
	dfTotal['Rejected'] = dfTotal['Shares'] - dfTotal['Accepted']
	dfTotal['Elapsed'] = datetime.now() - dfTotal['Last']
	dfTotal['Last Seen'] = dfTotal['Elapsed'].apply(lambda x: texttime.stringify(x)) + ' ago'
	dfTotal['Elapsed'] = dfTotal['Elapsed'].astype(pd.Timedelta).apply(lambda l: l.seconds)
	dfTotal = dfTotal.join(uptime)
	dfTotal = dfTotal[['Shares', 'Accepted','Q', 'A', 'Last Seen', 'Last', 'Rejected', 'Elapsed']]
	
	#Health (yes this is wonky af but it works. maybe.)
	dfTotal['HealthX'] = np.nan
	dfTotal = dfTotal.fillna(0)
	dfTotal[['HealthX']] = dfTotal[['HealthX']].astype(int) 
	dfTotal.loc[dfTotal['Elapsed'] > 120, 'HealthX'] += 1
	dfTotal.loc[dfTotal['Elapsed'] > 240, 'HealthX'] += 2
	dfTotal.loc[dfTotal['Q'] < 95, 'HealthX'] += 1
	dfTotal.loc[dfTotal['Q'] < 90, 'HealthX'] += 1
	dfTotal.loc[dfTotal['A'] < 95, 'HealthX'] += 1
	dfTotal.loc[dfTotal['A'] < 90, 'HealthX'] += 1
	dfTotal.loc[dfTotal['HealthX'] == 0, 'Health'] = "<span class='healthy'>OK!</span>"
	dfTotal.loc[dfTotal['HealthX'] == 1, 'Health'] = "<span class='issues'>Sick</span>"
	dfTotal.loc[dfTotal['HealthX'] == 2, 'Health'] = "<span class='sick'>Very Sick</span>"
	dfTotal.loc[dfTotal['HealthX'] >= 3, 'Health'] = "<span class='dead'>Likely Dead</span>"
	dfTotal.to_csv(file_csv, encoding='utf-8')
	dfTotal = dfTotal[['Q', 'A', 'Last Seen','Health']]
	dfTotal.reset_index().to_html(file_html, escape=False)
	
	return dfTotal

#Tools
def writeToFile(str, file):
	t = open(file, "w")
	t.write(str)
	t.close()
def convert_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
def file_size(file_path):
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)

#Workhorse
def increment():
	print "Updating... "+datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	#Import logfile (the '1 2 3... is to ensure the csv parses)
	log = "1 2 3 4 5 6 7 8 9 10\n" + open(conf.LOG_FILE_PATH, "r").read()

	#Pool list
	pl = re.sub(r'(?m)^((?!Connected).)*$', r'', log)
	pl = re.sub(u'(?imu)^\s*\n', u'', pl)
	pl = re.sub(u'(,.*)(at )', u',', pl)
	writeToFile(pl, scratch_file)
	dfPool = pd.read_csv(scratch_file, header=None, delimiter=',')
	dfPool.columns = ['Time', 'Pool']
	dfPool.to_csv(pool_file, encoding='utf-8')
	dfPool.to_html(pool_html)

	#Last pool string
	poolStart = dfPool.tail(1).iloc[0]['Time']
	s1 = datetime.strptime(poolStart, "%Y-%m-%d %H:%M:%S")
	s2 = datetime.now()
	poolStr = "<b>Pool</b>: <i>" + dfPool.tail(1).iloc[0]['Pool'] + "</i> for <span data-toggle='tooltip' title='"+poolStart+"'>" + texttime.stringify(s2-s1) + "</span>"
	writeToFile(poolStr, pool_string_html)

	#Last server info string
	nowStr = "<b>Monitoring updated</b>: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	writeToFile(nowStr, server_string_html)
	
	#Short title string
	sp = conf.TIME_SHORT[:-1]
	sps = ""
	if sp == '1':
		sps = "24 hours"
	else:
		sps = sp + " days"
	sp = conf.SHORT_STEP
	spq = ""
	if sp[-1:] == 'H':
		spq = sp[:-1] + " hours"
	else:
		spq = sp[:-3] + " minutes"
	shTit = "<h3 data-toggle='tooltip' title='Graph timestep is "+ spq +"'>Last "+ sps + "</h3>"
	writeToFile(shTit, short_heading_html)
	
	#Long title string
	sp = conf.LONG_STEP
	spq = ""
	if sp[-1:] == 'D':
		spq = sp[:-1] + " days"
	elif int(sp[:-1]) == 1:
		spq = sp[:-1] + " hour"
	else :
		spq = sp[:-1] + " hours"
	shTit = "<h3 data-toggle='tooltip' title='Graph timestep is "+ spq + "'>All Time</h3>"
	writeToFile(shTit, long_heading_html)

	#Series Start
	logStart = dfPool.iloc[0]['Time']
	s1 = datetime.strptime(logStart, "%Y-%m-%d %H:%M:%S")
	s2 = datetime.now()
	str_t = "<b>Logging began</b>: <span data-toggle='tooltip' title='"+logStart+"'>"+texttime.stringify(s2-s1)+" ago</span>"
	writeToFile(str_t, log_string_html)

	#Share list
	f = re.sub(r'(?m)^((?!Share).)*$', r'', log)
	f = re.sub(u'(?imu)^\s*\n', u'', f)
	f = re.sub(r'(REJECTED.*\n)', 'REJECTED\n', f)
	f = re.sub(r'(Share from )', '', f)
	f = f.replace(" ", ",")
	f = re.sub(r'(:..)(,.*\])', r'\1', f)
	f = re.sub(r'(-..)(,)', r'\1 ', f)
	f = f.replace("'", "")
	writeToFile(f, scratch_file)
	df = pd.read_csv(int_path + "scratch.txt", header=None, delimiter=',')
	df.columns = ['time', 'Miner', 'status']
	df['status_bool'] = df.status.eq('accepted') * 1
	df['time'] = pd.to_datetime(df['time'])

	#Mask Short Period (Last X time)
	start =  df.tail(1).iloc[0]['time']
	mask = (df['time'] > start - pd.Timedelta(conf.TIME_SHORT)) & (df['time'] <= start)
	dfTemp = df.loc[mask].copy()

	#Group by Time
	dfTimeAll = timeGroup(df, conf.LONG_STEP, hash_file)
	dfTimeShort = timeGroup(dfTemp, conf.SHORT_STEP, hash_short_file)
	
	#Counts
	a = totalCount(df, dfTimeAll, total_file, total_html)
	b = totalCount(dfTemp, dfTimeShort, total_short_file, total_short_html)
	
	#Write Info
	all = str(len(a.index))
	some = str(len(b.index))
	if all == some:
		some = 'all'
	info_str = "<p>You have had<b> "+all+" </b>miners active,<b> "+some+" </b>of which  have been active in the last "+sps+". Your logfile size is <b>"+file_size(conf.LOG_FILE_PATH)+"</b>.</p>"
	writeToFile(info_str, info_html)
	
	#Clear scratch
	writeToFile("", scratch_file)
	
	#Log
	print "				...updated."

#Banner
print "----------------------------------------------------------------------------------------"
print "--- Monero Mining Monitor 0.1"
print "--- by u/taushet"
print "---"
print "--- Monitoring suite for xmr-proxy by Atredies (https://github.com/Atrides/xmr-proxy)"
print "--- (this won't work without it!)"
print "-----------------------------------------------------------------------------------------"

#Web
if (conf.INIT_WEB_SERVER):
	print "Web server active on http://127.0.0.1:" + str(conf.PORT) +"/mmm_web.html"
	from SimpleHTTPServer import SimpleHTTPRequestHandler
	from BaseHTTPServer import HTTPServer
	server = HTTPServer(('', conf.PORT), SimpleHTTPRequestHandler)
	thread = threading.Thread(target = server.serve_forever)
	thread.daemon = True
	thread.start()

#Run every conf.REPEAT seconds (locked to sys clock)
starttime=time.time()
while True:
  increment()
  time.sleep(conf.REPEAT - ((time.time() - starttime) % conf.REPEAT))

	
	


