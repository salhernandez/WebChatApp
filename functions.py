def getBotResponse(someString):
    if '!! about' in someString:
        msg = "This webapp is a chatroom"
    
    elif '!! help' in someString:
        msg = "type '!! about' '!! help', '!! say <something>', '!! bot <chat with the bot>', '!! potato' "
        
    elif '!! say' in someString:
        theText = str(someString)
        msg = "someone told me to say "+str(theText[len('!! say '):len(theText)])
        
    elif '!! potato' in someString:
        # Get a response for some unexpected input
        msg = "potatos are delicious"
        
    elif '!! weather' in someString:
        theText = someString
        address = (theText[len('!! weather'):len(theText)])
        
        #checks that there is an address, if not let the user know
        if len(address) == 0:
            msg = "need to provide city or address"
            
        else:
            #gets lat and long based on address
            location = geolocator.geocode(address)
            
            lat = location.latitude
            lng = location.longitude
            
            #gets forecast based on latitude and longitude
            forecast = forecastio.load_forecast(api_key, lat, lng)
            
            #print "CURRENT FORECAST"
            
            weather = str(forecast.currently())
            msg = address+": "+weather[len('ForecastioDataPoint instance: '):len(weather)]+" UTC"
    else:
        msg = "can't recognize that command fam"
    
    return msg