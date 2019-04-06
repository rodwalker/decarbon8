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
    print(windsolar[0])
    allgen = ENTSOE.fetch_generation_forecast(country)
    print(allgen[0])
    ws=0
    for ag in allgen:
      allkwh = ag['value']
      alltime = ag['datetime']
      for q in range(4):
        windkwh=windsolar[ws]['production']['wind']
        solarkwh=windsolar[ws]['production']['solar']
        co2intensity=(allkwh-windkwh-solarkwh)*400/allkwh
        print(alltime, allkwh, windkwh,solarkwh,co2intensity)
        ws=ws+1
      
    self.intensity[country] = { 'created': arrow.utcnow(), 'data': allgen }
    return self.intensity[country]

   
    
if __name__ == '__main__':
  i = Intensity()
  print(i.getProfile('DE')['data'][-1])
#  time.sleep(11)
#  print (i.getProfile('DE')['data'][3])

  
