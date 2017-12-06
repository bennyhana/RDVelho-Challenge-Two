import time
from math import sin, cos, radians
from urllib.request import urlopen

data = ((0, 1, 2, 3, 4, 5), (0, 10, 22, 50, 88, 121), (0, 3, 3.5, 5, 8, 10.8))
geoLetters = {0: "N", 45: "NE", 90: "E", 135: "SE", 180: "S", 225: "SW", 270: "W", 315: "NE"}

def drivingCar(power, speed, consumption):
	direction = 0
	totalTrip = 0
	totalTime = 0
	consumedFuel = 0
	latitude = 60.170833
	longitude = 24.9375
	
	input("\nWelcome to the simulation.\nUse A, S, D and W keys to control the car.\n" + 
		  "You can refresh the dashboard by pressing Enter.\nType Q to quit.\n\nPress Enter to start:")

	while 1:
		startTime = time.time()
		
		key = input(": ")
		
		endTime = time.time() - startTime
		startTime = time.time()
		totalTime += endTime # Elapsed time in seconds since beginning of the journey.
		
		tempTrip = endTime * speed / 3.6 # Travelled distance in meters since previous iteration.
		totalTrip += tempTrip # Total travelled distance in meters.		 
		
		consumedFuel += tempTrip * consumption / 100000
		
		averages = getAverages(totalTrip, totalTime, consumedFuel)
		
		dx = tempTrip * sin(radians(direction)) # Calculate lateral and longitudinal distances.
		dy = tempTrip * cos(radians(direction))
		
		deltaLati = dy / 110540                             # Calculate changes in degrees.
		deltaLong = dx / (111320 * cos(radians(latitude)))
		
		latitude = latitude + deltaLati   # Add changes to previous coordinates.
		longitude = longitude + deltaLong
		
		if key in ("w", "W") and power != 5:
			power += 1
		elif key in ("s", "S")  and power != 1:
			power -= 1  
		elif key in ("a", "A"):
			if direction == 0:
				direction = 315
			else:
				direction -= 45
		elif key in ("d", "D"):
			if direction == 315:
				direction = 0
			else:
				direction += 45
		elif key in ("q", "Q"):
			break
			
		speed = data[1][power]
		consumption = data[2][power]
		
		urlopen("https://dweet.io/dweet/for/mun-kojelauta?power=%d&speed=%d&avg_speed=%2.1f&consumption=%f&"
				% (power, speed, averages[1], consumption) +
				"avg_consumption=%2.1f&total_trip=%d&direction=%d&geo_letter=%s&latitude=%f&longitude=%f"
				% (averages[0], totalTrip, direction, geoLetters[direction], latitude, longitude))

def getAverages(distance, time, consumedFuel):
	if distance > 0:
		avgConsumption = consumedFuel / distance * 100000
	else:
		return 0, 0
		
	if time > 0:
		avgSpeed = distance / time * 3.6
	else:
		return 0, 0
	
	return avgConsumption, avgSpeed
	
drivingCar(data[0][0], data[1][0], data[2][0])
