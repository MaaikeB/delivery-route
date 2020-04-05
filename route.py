import csv
from math import sin, cos, sqrt, atan2, radians

addresses_dict = {}
route = []

MAX_DISTANCE = 10000


def get_route():
    addresses_dict = _get_addresses_dict()

    # Add the first address to the journey as the starting point
    first_address_id = '402'
    current_address = addresses_dict[first_address_id]
    route.append({
        'id': first_address_id,
        'lon': current_address['lon'],
        'lat': current_address['lat'],
        'distance': 0
    })
    addresses_dict[first_address_id]['visited'] = True

    while True:
        # Loop over all the other addresses and find the closest
        closest_distance = MAX_DISTANCE
        closest_distance_id = None
        for other_address_id, other_address in addresses_dict.items():
            # If the address was already 'visited' (added to the journey),
            # skip it as a possible next stop
            if 'visited' in addresses_dict[other_address_id]:
                continue

            current_distance = _get_distance(float(current_address['lat']),
                                             float(current_address['lon']),
                                             float(other_address['lat']),
                                             float(other_address['lon']))

            # If the distance to the current address is less than the last closes distance,
            # add it as the current closes distance
            if current_distance < closest_distance:
                closest_distance = current_distance
                closest_distance_id = other_address_id

        # Add the closest address to the route, and mark it is as 'visited'
        if closest_distance_id:
            route.append({
                'id': closest_distance_id,
                'lon': addresses_dict[closest_distance_id]['lon'],
                'lat': addresses_dict[closest_distance_id]['lat'],
                'distance': closest_distance
            })

            addresses_dict[closest_distance_id]['visited'] = True

            # Take the closest found address as the address for the 'next round'
            current_address = addresses_dict[closest_distance_id]

        else:
            # If no more closest address was found (all addresses were visited), write the results to the file
            write_to_csv(route)
            break


def _get_addresses_dict():
    addresses_dict = {}
    with open('addresses.csv') as f:
        addresses = f.readlines()
        for address in addresses:
            address = address.split(',')
            id = address[0]
            addresses_dict[id] = {
                'lat': address[1],
                'lon': address[2][:-1],
            }

    return addresses_dict


def _get_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def write_to_csv(journey):
    with open('route.csv', 'w') as out_file:
        csv_writer = csv.writer(out_file)
        csv_writer.writerow(['id', 'lat,lon', 'distance'])
        for address in journey:
            csv_writer.writerow([address['id'], address['lat'] + ',' + address['lon'], address['distance']])


if __name__ == '__main__':
    get_route()