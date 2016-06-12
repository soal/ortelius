import geojson
from sys import argv
import os
def main():
    periods = [p for p in range(-3000, 2000, 300)]
    # print(periods)
    with open(argv[1], mode='r') as source_file:
        data = geojson.load(source_file)
        for feature in data['features']:
            period = None
            for p in periods:
                if int(feature['properties']['timespan']['begin']) <= p:
                    period = p
                    break
            directory = os.path.dirname(argv[1]) + '/' + os.path.basename(argv[1]).split('.')[0] + '/' + str(period)

            if not os.path.exists(directory):
                os.makedirs(directory)

            feature_file = open(directory + '/' + feature['properties']['name'] + '.geojson', mode='w')
            feature_file.write(str(feature))

if __name__ == '__main__':
    main()
