import csv
from math import sin, cos, sqrt, atan2, radians


closest_distances = []

MAX_DISTANCE = 1000


def get_closest_location():
    with open('addresses.csv') as f:
        addresses = f.readlines()

    for first_address in addresses:
        first_address = first_address.split(',')
        first_address_id = first_address[0]
        first_address_lat = first_address[1]
        first_address_lon = first_address[2]

        # Loop over all the other addresses and find the closest
        closest_distance_id = None
        closest_distance = MAX_DISTANCE
        for second_address in addresses:
            second_address = second_address.split(',')
            second_address_id = second_address[0]
            second_address_lat = second_address[1]
            second_address_lon = second_address[2]

            if second_address_id == first_address_id:
                continue

            current_distance = _get_distance(float(first_address_lat),
                                             float(first_address_lon),
                                             float(second_address_lat),
                                             float(second_address_lon))

            # If the distance to the current address is less than the last closes distance,
            # add it as the current closes distance
            if current_distance < closest_distance:
                closest_distance = current_distance
                closest_distance_id = second_address_id
                closest_distance_lat = second_address_lat
                closest_distance_lon = second_address_lon

        # Add the closest address to the route, and mark it is as 'visited'
        if closest_distance_id:
            closest_distances.append({
                'id': first_address_id,
                'closest_location_id': closest_distance_id,
                'distance': closest_distance
            })

        write_to_csv(closest_distances)


def _get_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    lon1 = radians(lon1)
    lat1 = radians(lat1)
    lon2 = radians(lon2)
    lat2 = radians(lat2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def write_to_csv(closest_distances):
    with open('closest_locations.csv', 'w') as out_file:
        csv_writer = csv.writer(out_file)
        csv_writer.writerow(['id', 'closest_location_id', 'distance'])
        for closest_distance in closest_distances:
            csv_writer.writerow([closest_distance['id'], closest_distance['closest_location_id'], closest_distance['distance']])


if __name__ == '__main__':
    get_closest_location()