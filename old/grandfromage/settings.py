# Settings for Grand Fromage

NAME = "wensleydale"                    # the name of the thing which Grand Fromage is monitoring

BASE_TOPIC = "grandfromage"             # the base MQTT topic

TRACKER_SIGNIFICANT_DISTANCE_METERS = 5 # meters, the minimum distance moved before the tracker logs the new location
TRACKER_PING_FREQUENCY = 60 * 60 * 3    # seconds, log the location after the specified time even if there is no significant distance


