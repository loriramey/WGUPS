from app_wgups.distance_matrix import load_distance_data, get_distance

# Load distance matrix
distance_matrix = load_distance_data("/Users/loriramey/PycharmProjects/WGUPSapp/data/distance_matrix.csv")

# Check if problematic addresses exist in the matrix
address_1 = "4100 S State St"
address_2 = "300 State St"

distance = get_distance(distance_matrix, address_1, address_2)
if distance is None:
    print(f"🚨 ERROR: Distance from {address_1} to {address_2} NOT FOUND in matrix!")
else:
    print(f"✅ Distance from {address_1} to {address_2}: {distance} miles")