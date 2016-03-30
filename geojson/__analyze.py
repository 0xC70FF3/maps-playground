import time
import geojson
import sys


def main(args=None):
    ps = list()
    c = list()

    t = time.time()
    file = args[1] if len(args) > 1 else "data.geojson"
    with open(file) as data_file:
        data = data_file.read()
        features = geojson.loads(data).features
        print(len(features))
        for feature in features:
            p = 0
            if feature.geometry.type == "Polygon":
                p = len(feature.geometry.coordinates[0])

            elif feature.geometry.type == "MultiPolygon":
                for polygon in feature.geometry.coordinates:
                    p += len(polygon[0])

            c.append((feature.properties["NAME"], p))

    def k(item):
        return item[1]

    c.sort(key=k, reverse=True)
    print(c)
    print("elapsed time: {0:.2f}".format(time.time() - t))


if __name__ == '__main__':
    main(sys.argv)
