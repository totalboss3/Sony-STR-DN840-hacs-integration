###Add these lines to configuration.yaml and change it to correspond to your mqtt broker (usually host is home assistant ip address and if its not you likely know what to do already)

sony_address="receiver" ### the ip of the sony
sony_port_status=50001 ### command port of the sony (try nmap)
sony_port_control=8080 ### etc...

sony_myid="TVSideView:aa-bb-cc-dd-ee-ff" 		### ID for this remote control, this is for sony to have a unique id to interface with.
sony_myname="PythonSonyController" 				# name for this remote control
sony_mydevinfo='PythonScript' 					# some info about this device
sony_myuseragent='PythonScript' 				# used user agent

mqtt_host = "mqtt" ### ip address for your mqtt broker. Probably your home assistant.
mqtt_port = 1883
mqtt_topic = "sony_av_receiver"
