import json
import os


def main():
    features = {
        "type": "FeatureCollection",
        "features": []
    }
    directory = "poly/"
    for file in os.listdir(directory):
        if file.endswith(".poly"):
            name = os.path.basename(file).split(".")[0]
            with open(os.path.join(directory, file)) as poly_file:
                polygon = list()
                polygons = list()
                line = poly_file.readline()
                while line:
                    line = poly_file.readline()
                    if line.startswith(" "):
                        coordinates = line.split()
                        polygon.append([float(coordinates[0]), float(coordinates[1])])
                    elif len(polygon) > 0:
                        polygons.append(polygon)
                        polygon = list()

            feature = {
                "properties": {"NAME": name},
                "type": "Feature",
                "geometry": {
                   "type": "MultiPolygon" if len(polygons) > 1 else "Polygon",
                   "coordinates": [polygons] if len(polygons) > 1 else polygons
                }
            }
            features["features"].append(feature)

    with open('countries.geojson', 'w') as outfile:
        json.dump(features, outfile)


if __name__ == "__main__":
    main()
