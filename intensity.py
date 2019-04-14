# https://www.co2signal.com/ only the latest value
# electricitymap.com has forecasts but need to pay
# entsoe give forecast for total generation and solar+wind generation
# Calculate gCO2/kWh for total-wind-sun, so for DE Fossils, Nuclear bit of water
# Call this base intensity assume it is constant.
# Assume wind + sun have zero intensity, then varying intensity is
# (total-wind-sun)*baseIntensity/total
# it does not capture everythng, such as varied mix of fossils, but will do fo now.



import ENTSOE
import arrow
import time

class Intensity:
  def __init__(self):
   # dict of countries with CO2 intensity forecast   
    self.intensity={}
    self.refreshSecs=15

  def getProfile(self, country):
    if (country in self.intensity.keys()):
     # Refresh once per hour
      now = arrow.utcnow()
      if (now.shift(seconds=-self.refreshSecs) < self.intensity[country]['created'] ):
        return self.intensity[country]
    print('Getting new')
    windsolar = ENTSOE.fetch_wind_solar_forecasts(country)
    print(windsolar[-1],len(windsolar))
# seems to only get 1 day
#    allgen = ENTSOE.fetch_generation_forecast(country)
    allgen = ENTSOE.fetch_consumption_forecast(country)
    print(allgen[-1],len(allgen))
    ws=0
    data=[]
    for ag in allgen:
      allkwh = ag['value']
      alltime = ag['datetime']
      for q in range(1):
        windkwh=windsolar[ws]['production']['wind']
        solarkwh=windsolar[ws]['production']['solar']
        if solarkwh is None: solarkwh=0
        #print(alltime, allkwh, windkwh,solarkwh)
        co2intensity=(allkwh-windkwh-solarkwh)*400/allkwh
        print(alltime, allkwh, windkwh,solarkwh,co2intensity)
        data.append({'datetime':windsolar[ws]['datetime'],'gco2':co2intensity})
        ws=ws+1
      
    self.intensity[country] = { 'created': arrow.utcnow(), 'data': data }
    return self.intensity[country]

  def getDelay(self,country,maxDelay=24):
    self.getProfile(country)
   # list of minute ranges with same power. Loop over these. 
    pprofile=[(0,10,2000),(10,120,100)]
    pprofile=[(0,10,2000)]
    
    now =  arrow.utcnow()
    then = now.shift(hours=maxDelay)
   # loop over start time from now to now+maxDelay (in hours)
    mingco2=999999
    for i in range(0,maxDelay+1):
      start=arrow.utcnow().shift(hours=i)
      gco2=0
      for pstep in pprofile:
        for min in range(pstep[0],pstep[1]):
          gco2+=pstep[2]/1000*self.intAtTime(country,start.shift(minutes=min))/60
      print (i,start,gco2)
      if i == 0: refgco2 = gco2
      if gco2<mingco2:
        mingco2=gco2
        delay=i
    print ('Best delay: ',delay, mingco2,refgco2)  
    return delay
  
  # Make lookup table of intensity at each minute
  
  def intAtTime(self,country,when):
   # return the gCO2/kWh at given time
    ilist = self.intensity[country]['data']
    for i in range(0,len(ilist)-1):
      if when >= ilist[i]['datetime'] and when < ilist[i+1]['datetime']: 
        #print (when,ilist[i]['datetime'],ilist[i]['gco2'])
        return ilist[i]['gco2']
    print('Not in range: ',when,ilist[-1]['datetime'])
    
if __name__ == '__main__':
  i = Intensity()
  
  i.getDelay('DE',24)
#  print(i.getProfile('DE')['data'][-1])
#  time.sleep(11)
#  print (i.getProfile('DE')['data'][3])

   
