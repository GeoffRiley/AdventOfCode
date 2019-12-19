from collections import defaultdict
from itertools import permutations


class TripMeter(object):
    def __init__(self, trips: list):
        self.destinations = set(t[0] for t in trips)
        self.destinations.update(set(t[2] for t in trips))
        self.distances = defaultdict(dict)
        for t in trips:
            self.distances[t[0]][t[2]] = int(t[4])
            self.distances[t[2]][t[0]] = int(t[4])

        # pprint(self.distances)

    def generate_routes(self):
        good_routes = defaultdict(int)
        for possibles in permutations(self.destinations):
            route_dist = 0
            route_detail = []
            here = possibles[0]
            route_detail.append(here)
            for there in possibles[1:]:
                if there in self.distances[here]:
                    route_detail.append(f'({self.distances[here][there]})')
                    route_detail.append(there)
                    route_dist += self.distances[here][there]
                else:
                    raise ValueError(f'Missing route from {here} to {there}')
                here = there
            good_routes['-'.join(route_detail)] = route_dist
        best = sorted(good_routes.items(), key=lambda x: -x[1])
        print(f'Part 1: {best[-1]}')
        print(f'Part 2: {best[0]}')
        # print(f'{best} : {good_routes[best]}')


if __name__ == '__main__':
    with open('input') as f:
        trip_text = f.readlines()
    trips = [v.strip().split() for v in trip_text]
    tripper = TripMeter(trips)
    tripper.generate_routes()
