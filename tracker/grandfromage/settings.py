# Settings for GrandFromage

OW_SERVER = 'owserver'
GPSD_SERVER = "gpsd"
MOSQUITTO_SERVER = "mosquitto"
MOSQUITTO_BASE_NAME = "wensleydale"     # the name of the thing which Grand Fromage is monitoring

TRACKER_SIGNIFICANT_DISTANCE_METERS = 5 # meters, the minimum distance moved before the tracker logs the new location
TRACKER_PING_FREQUENCY = 60 * 60 * 3    # seconds, log the location after the specified time even if there is no significant distance
SENSOR_READ_FREQUENCY = 60 * 5 # seconds, log the temperatures, air pressures at this interval
