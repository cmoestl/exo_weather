"""

flare profiles for paper Bisikalo et al. 2018
https://doi.org/10.3847/1538-4357/aaed21





import warnings
warnings.filterwarnings('ignore')

"""
import matplotlib.pyplot as plt
from sunpy.timeseries import TimeSeries
from sunpy.time import TimeRange, parse_time
from sunpy.net import hek, Fido, attrs as a
import numpy as np

###############################################################################
# Let's first grab GOES XRS data for a particular time of interest

tr = TimeRange(['2011-06-07 06:00', '2011-06-07 10:00'])
results = Fido.search(a.Time(tr), a.Instrument('XRS'))
results

###############################################################################
# Then download the data and load it into a TimeSeries

files = Fido.fetch(results)
goes = TimeSeries(files)

###############################################################################
# Next lets grab the HEK data for this time from the NOAA Space Weather
# Prediction Center (SWPC)

client = hek.HEKClient()
flares_hek = client.search(hek.attrs.Time(tr.start, tr.end),
                           hek.attrs.FL, hek.attrs.FRM.Name == 'SWPC')

###############################################################################
# Finally lets plot everything together

plt.close('all')


goes.peek()
plt.axvline(parse_time(flares_hek[0].get('event_peaktime')))
plt.axvspan(parse_time(flares_hek[0].get('event_starttime')),
            parse_time(flares_hek[0].get('event_endtime')),
            alpha=0.6, label=flares_hek[0].get('fl_goescls'))
plt.legend(loc=2)
plt.show()

#################convert data to np.array
#https://www.ngdc.noaa.gov/stp/satellite/goes/doc/GOES_XRS_readme.pdf

AU_planet=0.0
xrsa=np.array(goes.data.xrsa.tolist())*1./(0.04747**2)
xrsb=np.array(goes.data.xrsb.tolist())*1./(0.04747**2)
print(goes.units)

print('seconds per datapoint')
print(goes.time_range.seconds/len(xrsb))
time_hours=np.arange(0,round(goes.time_range.seconds.to_value())-1,goes.time_range.seconds.to_value()/len(xrsb))/3600



plt.figure(3)

time_hours_minres=np.arange(0,time_hours[-1],1/60)
xrsa_interp=np.interp(time_hours_minres,time_hours,xrsa)
xrsb_interp=np.interp(time_hours_minres,time_hours,xrsb)


plt.plot(time_hours_minres,np.log10(xrsa_interp))
plt.plot(time_hours_minres,np.log10(xrsb_interp))
plt.xlabel('Time in hours')
plt.ylabel('log10 W / m^2')


forsaving =  np.column_stack((time_hours_minres, xrsa_interp,xrsb_interp))
np.savetxt('exo_flare_plots/flare_m_2_5.txt',forsaving, fmt='%10.10f',delimiter=" ") 

