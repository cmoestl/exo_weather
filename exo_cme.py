'''
exo_cme
Author: C. Moestl 2017

profiles for paper Cherenkov et al. 2017



comments:
speed: linear deceleration - expansion law aus coronagraph observations (Gopal, schwenn), 
dann passt die speed, size der CME? wie das rein:

density: etwa bei 10 Rs 1e3 protons per cm^3 - how much in CME? absolute and or relative to the background?
density http://iopscience.iop.org/article/10.1088/0004-637X/693/1/267/pdf

speed of 200 km/s at 10 Rs density of wind at 10 Rs is 1e3 taken from 
roundup: http://www.aanda.org/articles/aa/pdf/2015/05/aa25300-14.pdf

5 part structure
http://download.springer.com/static/pdf/2/art%253A10.1007%252Fs11207-012-0084-8.pdf?originUrl=http%3A%2F%2Flink.springer.com%2Farticle%2F10.1007%2Fs11207-012-0084-8&token2=exp=1446129836~acl=%2Fstatic%2Fpdf%2F2%2Fart%25253A10.1007%25252Fs11207-012-0084-8.pdf%3ForiginUrl%3Dhttp%253A%252F%252Flink.springer.com%252Farticle%252F10.1007%252Fs11207-012-0084-8*~hmac=0ed4c5406ec0c89c1495638e4716083d1d5e950f5fc175617b9a25f0f618ef38

ratio of density of at least > 5 in CME after shock http://iopscience.iop.org/article/10.1088/0004-637X/693/1/267/pdf

'''




from scipy import stats
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import matplotlib as mpl
import numpy as np
import sunpy.time
import time
import pickle
import seaborn as sns

#initialize
#get current directory
#os.system('pwd')
#closes all plots
plt.close('all')





import warnings
warnings.filterwarnings('ignore')



#global Variables
dataset=200; #number of data points


#ambient stellar wind
ambient_vel=100
ambient_den=1e4


#time variable, in 0.1 hour timesteps
time=np.arange(0,20,0.1) #integer



####################################################make profiles

 
def make_profile(cme_speed):


	#arrays
	ambvel=np.zeros(dataset)+ambient_vel #floating points
	ambden=np.zeros(dataset)+ambient_den #floating points

	cmevel=np.zeros(dataset)+ambient_vel #floating points
	cmeden=np.zeros(dataset)+ambient_den #floating points


	#arrays relative
	relvel=np.zeros(dataset)+1#floating points
	relden=np.zeros(dataset)+1#floating points

	#parameters
	AU=149500000
	cme_size_Rs=20
	cme_size_km=cme_size_Rs*695000
	location_of_exoplanet_AU=0.05
 

	transit_time_hours=location_of_exoplanet_AU*AU/cme_speed/3600


	cme_dur=(cme_size_km/cme_speed)/3600.
	print('CME size Rs', cme_size_Rs)
	print('CME speed (km/s)', cme_speed)
	print('CME duration at planet(hours)', cme_dur)
	print('transit time to ', location_of_exoplanet_AU,' in hours ',transit_time_hours)



	#cme interval mit richtiger duration in cmevel reinsetzen 

	#this is the index for the time when the CME hits the exoplanet at the given distance
	startind=int(transit_time_hours*10)

	#coefficient which gives the amount of deceleration
	if cme_speed > 800:	deceleration=cme_speed/100 
	else: deceleration=0
	#linear decreasing profile for speed
	cme_linear_dec=cme_speed-deceleration*np.arange(int(cme_dur*10))

	#put in the speed profile
	cmevel[startind:startind+int(cme_dur*10)]=cme_linear_dec

	#print('CME linearly decelerates from leading edge ', cme_speed, ' km/s to trailing edge', cme_linear_dec[size(cme_linear_dec)-1)

	#same for density

	#sheath
	cmeden[startind:int(startind+cme_dur*10*1/3)]=ambient_den*10
	#void
	cmeden[int(startind+int(cme_dur*10)*1/3):int(startind+cme_dur*10*2/3)]=ambient_den
	#core
	cmeden[int(startind+int(cme_dur*10)*2/3):int(startind+cme_dur*10*3/3)]=ambient_den*5



	print
	print 
	print 

	#calculate relative values

	relv=cmevel/ambvel

	reld=cmeden/ambden
	
	return (relv,reld, cmevel, cmeden)




################################## MAIN


relvel, relden, cmevel, cmeden = make_profile(600)
relvel2, relden2,cmevel2, cmeden2 = make_profile(1300)
relvel3, relden3,cmevel3, cmeden3 = make_profile(3000)




#fontsize
fsize=21


#plot profiles relvel, relden


sns.set_context("talk")     
sns.set_style("white")  
sns.set_style("ticks")
fig=plt.figure(2,figsize=(11,11))

weite=3



ax1 = fig.add_subplot(411)

#plt.title('Speed and density profiles of CME at exoplanet at 0.05 AU = 11 Rs', fontsize=16)

plt.plot(time,cmevel,'g',linewidth=weite, label='V CME = 600 $\mathregular{km \\ s^{-1}}}$')
plt.plot(time,cmevel2,'r',linewidth=weite, label='V CME = 1300 $\mathregular{km \\ s^{-1}}}$')
plt.plot(time,cmevel3,'b',linewidth=weite, label='V CME = 3000 $\mathregular{km \\ s^{-1}}}$')
plt.plot(time,np.zeros(dataset)+ambient_vel,'k-',linewidth=weite-1,label='$\mathregular{v_w = 100 \\ km \\ s^{-1}}}$')



plt.ylabel('velocity [$\mathregular{km \\ s^{-1}}}$]', fontsize=fsize)
plt.ylim((0,3500))
plt.xlim((0,12))
plt.yticks(fontsize=fsize) 
plt.xticks(fontsize=fsize) 

plt.legend(loc=1,fontsize=fsize-7)
plt.tick_params(labelbottom=False)
#plt.grid()
plt.tight_layout()
 
 

ax2 = fig.add_subplot(412)
plt.plot(time,cmeden,'g',linewidth=weite, label='V CME = 600 $\mathregular{km \\ s^{-1}}$')
plt.plot(time,cmeden2,'r',linewidth=weite, label='V CME = 1300 $\mathregular{km \\ s^{-1}}}$')
plt.plot(time,cmeden3,'b',linewidth=weite, label='V CME = 3000 $\mathregular{km \\ s^{-1}}}$')
plt.plot(time,np.zeros(dataset)+ambient_den,'k-',linewidth=weite-1,label='$\mathregular{n_w = 10^4 \\ cm^{-3}}}$')

#plt.yticks(fontsize=11) 
plt.ylabel(r'density [$\mathregular{10^{5}}}]$ $\mathregular{cm^{-3}}]$', fontsize=fsize)
plt.ylim((0,2*1e5))
plt.xlim((0,12))

ytick=[0, 5e4, 1e5, 1.5e5, 2e5]
yticklabel=['0', '0.5','1','1.5','2.0']


plt.yticks(ytick,yticklabel, fontsize=fsize) 
plt.yticks(fontsize=fsize) 
plt.xticks(fontsize=fsize) 
plt.legend(loc=1,fontsize=fsize-7)
plt.tick_params(labelbottom=False)
#plt.grid()
plt.tight_layout()



# relative speeds

ax3 = fig.add_subplot(413)
plt.plot(time,relvel,'g',linewidth=weite)#, label='V CME = 600 km/s')
plt.plot(time,relvel2,'r',linewidth=weite)#, label='V CME = 1300 km/s')
plt.plot(time,relvel3,'b',linewidth=weite)#, label='V CME = 3000 km/s')
plt.plot(time,np.zeros(dataset)+1,'k-',linewidth=weite-1)

#plt.yticks(fontsize=11) 
plt.ylabel('relative velocity', fontsize=fsize)
plt.ylim((0,35))
plt.xlim((0,12))
plt.yticks(fontsize=fsize) 
plt.xticks(fontsize=fsize) 
plt.tick_params(labelbottom=False)
#plt.grid()
plt.tight_layout()
 


# relative densities 
ax4 = fig.add_subplot(414)
#plt.plot(time,zeros(dataset),'k--',linewidth=weite)
plt.plot(time,relden,'g',linewidth=weite)#, label='V CME = 500')
plt.plot(time,relden2,'r',linewidth=weite)#, label='V CME = 1500')
plt.plot(time,relden3,'b',linewidth=weite)#, label='V CME = 3000')
plt.plot(time,np.zeros(dataset)+1,'k-',linewidth=weite-1)
plt.yticks(fontsize=fsize) 
plt.xticks(fontsize=fsize) 
plt.ylabel('relative density', fontsize=fsize)
plt.xlabel('Hours since CME eruption from the star', fontsize=fsize)
plt.ylim((0,12))
plt.xlim((0,12))
plt.legend(loc=1,fontsize=fsize-5)

plt.yticks(fontsize=fsize) 
plt.xticks(fontsize=fsize) 

#plt.tick_params(labelbottom='False')
#plt.grid()
plt.tight_layout()

plt.savefig('exo_cme_plots/exo_cme_profiles.eps', format='eps',dpi=100)
plt.savefig('exo_cme_plots/exo_cme_profiles.png', format='png', dpi=100)



#write arrays to files

forsaving =  np.column_stack((time, relvel, relden, cmevel, cmeden))
np.savetxt('exo_cme_plots/profiles/cme_600kms.txt', forsaving, fmt='%10.1f', delimiter=" ") 

forsaving =  np.column_stack((time, relvel2, relden2, cmevel2, cmeden2))
np.savetxt('exo_cme_plots/profiles/cme_1300kms.txt', forsaving, fmt='%10.1f', delimiter=" ") 

forsaving =  np.column_stack((time, relvel3, relden3, cmevel3, cmeden3))
np.savetxt('exo_cme_plots/profiles/cme_3000kms.txt',forsaving, fmt='%10.1f',delimiter=" ") 







