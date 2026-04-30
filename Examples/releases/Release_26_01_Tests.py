import os

import pytest
from aspose.gis import Drivers, VectorLayer, Driver, Extent, Dataset, AbstractPath, DynamicFeature, NodeLink, \
    FeatureAttribute, AttributeDataType
from aspose.gis.formats.filegdb import FileGdbOptions
from aspose.gis.formats.geojson import GeoJsonOptions, GeoJsonLayer
from aspose.gis.formats.geopackage import GeoPackageOptions, GeoPackageDataset, GeoPackageTileMatrixSet, \
    GeoPackageTileOptions
from aspose.gis.formats.kml import KmlOptions, KmlLayer

from aspose.gis.geometries import Point, GeometryType, LineString, LinearRing, Polygon, Geometry
from aspose.gis.geotools import GeneratorTiles, GeneratorTilesRenderOptions
from aspose.gis.spatialreferencing import SpatialReferenceSystem
from aspose.pycore import cast

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper

class Release_26_01_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Enumerator in GeoJsonLayer doesn't work as expected
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-59
    # https://issue.saltov.dynabic.com/issues/GISNET-1944
    def GISNET1944Test(self):
        temp_path = self.GetFileInOutputFolder("custom_field.json")
        source_path = AbstractPath.from_local_path(temp_path)

        content = '''{ "type": "FeatureCollection", "features": [
            {"type": "Feature", "geometry": null, "properties": null },
            {"type": "Feature",  "geometry": null, "properties": null }
        ] }'''

        with open(temp_path, "w") as f:
            f.write(content)

        # Open GeoJson layer
        with Drivers.geo_json.open_as_geo_json_layer(source_path, GeoJsonOptions()) as layer:
            features = list(layer)
            print(f"Number of features: {len(features)}")
            assert len(features) == 2

    # Add Root Node to the Public API Method for GeoJsonLayer and KmlLayer
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-60
    # https://issue.saltov.dynabic.com/issues/GISNET-1948
    def GISNET1948Test(self):
        input_path = self.GetFileInBaseFolder("GoogleKmlSample.kml")
        open_path = AbstractPath.from_local_path(input_path)

        with Drivers.kml.open_as_kml_layer(open_path, KmlOptions()) as layer:
            print(f"Feature count: {layer.count}")

            # Check root node link of the layer
            root_node = layer.root
            custom_nodes = root_node.find_nodes_by_name("GroundOverlay")
            print(f"Number of GroundOverlay nodes: {len(custom_nodes)}")

            if len(custom_nodes) > 0:
                test_node = custom_nodes[0]
                look_at = test_node.get_node_by_name("LookAt")
                look_at_children = list(look_at.children)
                print(f"LookAt children count: {len(look_at_children)}")

                # Get values from nodes
                longitude_node = look_at.get_node_by_name("longitude")
                latitude_node = look_at.get_node_by_name("latitude")
                altitude_node = look_at.get_node_by_name("altitude")
                heading_node = look_at.get_node_by_name("heading")

                if longitude_node:
                    longitude = float(longitude_node.node_value)
                    print(f"Longitude: {longitude}")
                    assert abs(longitude - 15.02468937557116) <= 0.000001

                if latitude_node:
                    latitude = float(latitude_node.node_value)
                    print(f"Latitude: {latitude}")
                    assert abs(latitude - 37.67395167941667) <= 0.000001

                if altitude_node:
                    altitude = int(altitude_node.node_value)
                    print(f"Altitude: {altitude}")
                    assert altitude == 0

                if heading_node:
                    heading = heading_node.node_value
                    print(f"Heading: {heading}")
                    assert heading == "-16.5581842842829"

    # Support Conversion to GeoPackage (Check 14 Bugs During Conversion)
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-61
    # https://issue.saltov.dynabic.com/issues/GISNET-1943
    def GISNET1943Test(self):
        source_path = self.GetFileInBaseFolder("issue_504_input.json")
        temp_dir = os.path.join(os.path.expanduser("~"), "temp")
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        destination_path = os.path.join(temp_dir, "test.gpkg")

        # Convert from GeoJSON to GeoPackage
        VectorLayer.convert(source_path, Drivers.geo_json, destination_path, Drivers.geo_package)

        # Open and verify the converted layer
        with VectorLayer.open(destination_path, Drivers.geo_package) as layer:
            print(f"Feature count: {layer.count}")
            print(f"Attribute count: {layer.attributes.count}")

            # Iterate through features
            for i, feature in enumerate(layer):
                geometry = feature.geometry
                if geometry:
                    print(f"Feature {i} geometry: {geometry.as_text()}")
                    match i:
                        case 0:
                            assert geometry.as_text() == "POINT (33.97 -118.25)"
                        case 1:
                            assert geometry.as_text() == "POINT (35.81 -96.28)"

#LicenseHelper.set_license()
#tests = Release_26_01_Tests()
#tests.GISNET1943Test()