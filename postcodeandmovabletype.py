from math import floor, sin, cos, atan2, sqrt, radians, degrees

centrals = ["EC", "WC"]
centralscentres = [90, 270]
cardinals = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
cardinalscentres = [0, 45, 90, 135, 180, 225, 270, 315]
outward_ex = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "M", "N", "P", "R", "S", "T", "U", "V", "W", "X", "Y"]
inward_first = ["A", "B", "D", "E", "F", "G", "H", "J", "L", "N", "P", "Q", "R", "S", "T", "U", "W", "X", "Y", "Z"]
inward_subtractive = ["A", "D", "F", "H", "L", "P", "R", "T", "W", "Y"]
inward_additive = ["B", "E", "G", "J", "N", "Q", "S", "U", "X", "Z"]

# --- Movable Type Scripts Geodesic Calculations ---
print("--- Origin Coordinates ---")
lat1 = float(input("Please enter origin latitude: "))
lon1 = float(input("Please enter origin longitude: "))

print("\n--- Destination Coordinates ---")
lat2 = float(input("Please enter destination latitude: "))
lon2 = float(input("Please enter destination longitude: "))

# Convert degrees to radians
phi1 = radians(lat1)
phi2 = radians(lat2)
delta_phi = radians(lat2 - lat1)
delta_lambda = radians(lon2 - lon1)

# Haversine Distance Formula
a = sin(delta_phi / 2)**2 + cos(phi1) * cos(phi2) * sin(delta_lambda / 2)**2
c = 2 * atan2(sqrt(a), sqrt(1 - a))
earth_radius_miles = 3958.8  # Using Earth radius in miles
distance = earth_radius_miles * c

# Spherical Initial Bearing Formula
y = sin(delta_lambda) * cos(phi2)
x = cos(phi1) * sin(phi2) - sin(phi1) * cos(phi2) * cos(delta_lambda)
initial_bearing = degrees(atan2(y, x))
bearing = (initial_bearing + 360) % 360  # Normalise bearing to 0-360°

print(f"\n[Calculated Distance: {distance:.4f} miles]")
print(f"[Calculated Bearing: {bearing:.2f}°]\n")

# --- Original System Functions ---
def sectorsearch(angle, directions, centres, width):
	for a in range(len(directions)):
		if centres[a] - (width/2) <= angle < centres[a] + (width/2):
			return a
		if centres[a] - (width/2) <= (angle - 360) < centres[a] + (width/2):
			return a
			
def distancenotation(d, outwardletters):
    if d < 1:
        num1 = floor(d/0.25) + 1
        letterdeterminant = 84*(d - (num1-1)*(0.25))
        letter = outwardletters[floor(letterdeterminant)]
        num2 = floor(10*(letterdeterminant - floor(letterdeterminant)))
        return (str(num1) + str(letter) + " " + str(num2))
    elif d < 2:
        num1 = 1
        letterdeterminant = 21*(d - 1)
        letter = outwardletters[floor(letterdeterminant)]
        num2 = floor(10*(letterdeterminant - floor(letterdeterminant)))
        return (str(num1) + str(letter) + " " + str(num2))
    else:
        num1 = floor(d)
        num2 = (floor(10*(d - num1)))
        return (str(num1) + " " + str(num2))
        
def anglecode(angle, centre, width, first, sub, add):
    if angle - centre < 0:
        calc = (20/width)*(centre - angle)
        firstdet = floor(calc)
        print(f"Index 1: {firstdet}")
        seconddet = floor(10*(calc - floor(calc)))
        print(f"Index 2: {seconddet}")
        firstlet = first[firstdet]
        secondlet = sub[seconddet]
        return (str(firstlet) + str(secondlet))
    else:
        calc = (20/width)*(angle - centre)
        if calc > 20:
            centre = 360
            calc = (20/width)*(centre - angle)
            firstdet = floor(calc)
            print(f"Index 1: {firstdet}")
            seconddet = floor(10*(calc - floor(calc)))
            print(f"Index 2: {seconddet}")
            firstlet = first[firstdet]
            secondlet = sub[seconddet]
            return (str(firstlet) + str(secondlet))
        else:
            firstdet = floor(calc)
            print(f"Index 1: {firstdet}")
            seconddet = floor(10*(calc - floor(calc)))
            print(f"Index 2: {seconddet}")
            firstlet = first[firstdet]
            secondlet = add[seconddet]
            return (str(firstlet) + str(secondlet))

# --- Formatting & Output Code Assembly ---
code = ""
if distance < 1:
	sector = sectorsearch(bearing, centrals, centralscentres, 180)
	code = code + str(centrals[sector])
	code = code + str(distancenotation(distance, outward_ex))
	code = code + str(anglecode(bearing, centralscentres[sector], 90, inward_first, inward_subtractive, inward_additive))
else:
	sector = sectorsearch(bearing, cardinals, cardinalscentres, 45)
	code = code + str(cardinals[sector])
	code = code + str(distancenotation(distance, outward_ex))
	code = code + str(anglecode(bearing, cardinalscentres[sector], 22.5, inward_first, inward_subtractive, inward_additive))

print(f"Generated Location Code: {code}")
