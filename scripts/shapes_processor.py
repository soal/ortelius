import geojson
from sys import argv
import os
from ortelius.types.historical_date import HistoricalDate as hd, DateError
from ortelius.models.Coordinates import Shape, Coordinates, Quadrant

def split(path):
    periods = [p for p in range(-3000, 2000, 300)]
    # print(periods)
    with open(path, mode='r') as source_file:
        data = geojson.load(source_file)
        for feature in data['features']:
            period = None
            for p in periods:
                if int(feature['properties']['timespan']['begin']) <= p:
                    period = p
                    break
            directory = os.path.dirname(path) + '/' + os.path.basename(path).split('.')[0] + '/' + str(period)

            if not os.path.exists(directory):
                os.makedirs(directory)

            feature_file = open(directory + '/' + feature['properties']['name'] + '.geojson', mode='w')
            feature_file.write(str(feature))


def parse(path):
    with open(path, mode='r') as source_file:
        data = geojson.load(source_file)

        shapes = []
        for feature in data['features']:
            coordinates = []
            for dot in feature['geometry']['coordinates']:
                if isinstance(dot, list):

                point = Coordinates(dot[0], dot[1], Quadrant.get(dot[0], dot[1]))
                coordinates.append(point)

            shape = Shape(start_date=hd(feature['properties']['timespan']['begin']),
                          end_date=hd(feature['properties']['timespan']['end']),
                          stroke_color=feature['properties']['stroke'],
                          stroke_opacity=feature['properties']['stroke-opacity'],
                          fill_color=feature['properties']['fill'],
                          fill_opacity=feature['properties']['fill-opacity'],
                          type='Polygon',
                          coordinates=coordinates
                         )
            shapes.append(shape)



def main():
    if argv[1] == 'split':
        if not argv[2]:
            print('Please, set path to geojson file')
        split(argv[2])

if __name__ == '__main__':
    main()
