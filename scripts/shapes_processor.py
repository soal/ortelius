from sys import argv
import os
import datetime
import geojson
from ortelius.types.historical_date import DateError


def split(path):
    periods = [p for p in range(-3000, 2000, 300)]
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


def parse(hd, Shape, Coordinates, Quadrant, Date, path):
    with open(path, mode='r') as source_file:
        data = geojson.load(source_file)

        shapes = []
        for feature in data['features']:
            coordinates = []
            print(feature['geometry']['coordinates'][0][0])
            return
            for dot in feature['geometry']['coordinates'][0]:
                print(dot)
                point = Coordinates(dot[0], dot[1], Quadrant.get(dot[0], dot[1]))
                coordinates.append(point)

            try:
                start = Date.create(date=hd(feature['properties']['timespan']['begin']))
            except:
                start = Date.create(date=hd(-50000101))
            try:
                end = Date.create(date=hd(feature['properties']['timespan']['end']))
            except:
                end = Date.create(date=hd(datetime.datetime.now()))

            shape = Shape(start_date=start,
                          end_date=end,
                          stroke_color=feature['properties']['stroke'],
                          stroke_opacity=feature['properties']['stroke-opacity'],
                          fill_color=feature['properties']['fill'],
                          fill_opacity=feature['properties']['fill-opacity'],
                          type='Polygon'
                         )
            for cp in coordinates:
                shape.coordinates.append(cp)
            shapes.append(shape)
    print(shapes[0].coordinates)
    return shapes


def main():
    if argv[1] == 'split':
        if not argv[2]:
            print('Please, set path to geojson file')
        split(argv[2])

    if argv[1] == 'parse':
        if not argv[2]:
            print('Please, set path to geojson file')
        parse(argv[2])

if __name__ == '__main__':
    main()
