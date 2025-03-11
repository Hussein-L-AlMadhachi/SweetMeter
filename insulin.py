import time

insulin_injection_time = None
insulin_injection_sgv = None

tolerance = 100
insulin_response = 100

insulin_active_period = 5400 # 1 hours 30 minutes 
sgv_rise_limit = None

expected_peak_time = None

def function( unixtime , a , b ):
    return  -1 * a * (unixtime**2) + b


# 5400 seconds = 1hours and 30 minutes
def set_insulin_injection_point( sgv , unixtime ) :
    insulin_injection_sgv = sgv
    insulin_injection_time = unixtime

    f_offset = sgv + tolerance
    
    expected_peak_time = unixtime - insulin_active_period

    effective_period_end = unixtime + 


