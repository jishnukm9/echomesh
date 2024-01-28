

from datetime import datetime 

def custom_variables(request):
    # Define your custom variables here
    app_version= "Version 24.01"
    publitio_key='Nvrtdz6pqMtg1uQk2quz'
    publitio_secret='8thJGkhdPuAyygsWkt0ywrA1butZz2t5'
    

    return {
        "app_version":app_version,
        "publitio_key":publitio_key,
        "publitio_secret":publitio_secret,
        "current_year":datetime.today().year
    }