import io
import os
from datetime import datetime

import pytest
from aspose.gis import VectorLayer, Drivers, RasterDriver, Extent, FeatureAttribute, AttributeDataType, AbstractPath
from aspose.gis.formats.geotiff import GeoTiffDriver
from aspose.gis.geometries import Point

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.FolderSettings import FolderSettings
from utils.LicenseHelper import LicenseHelper

class WriteLayer_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    def WriteFeaturesToTopoJsonTest(self):
        output = os.path.join(FolderSettings.BaseTestOutputFolder(), "sample_out.topojson")
        reference = os.path.join(FolderSettings.CommonTestFolder(), "sample_ref_out.topojson")
        with Drivers.topo_json.create_layer(output) as layer:
            # Add attributes that we are going to set
            layer.attributes.add(FeatureAttribute("name", AttributeDataType.STRING))
            layer.attributes.add(FeatureAttribute("measurement", AttributeDataType.DOUBLE))
            layer.attributes.add(FeatureAttribute("id", AttributeDataType.INTEGER))

            feature0 = layer.construct_feature()
            feature0.set_value("name", "name_0")
            feature0.set_value("measurement", 1.03)
            feature0.set_value("id", 0)
            feature0.geometry = Point(1.3, 2.3)
            layer.add(feature0)

            feature1 = layer.construct_feature()
            feature1.set_value("name", "name_1")
            feature1.set_value("measurement", 10.03)
            feature1.set_value("id", 1)
            feature1.geometry = Point(241.32, 23.2)
            layer.add(feature1)
        Comparison.compare_binary_files(output, reference)

    def WriteGeoJsonToStreamTest(self):
        reference = os.path.join(FolderSettings.CommonTestFolder(), "geojsonstream.ref.txt")
        with io.BytesIO() as memory_stream:
            with Drivers.geo_json.create_layer(AbstractPath.from_stream(memory_stream)) as layer:
                layer.attributes.add(FeatureAttribute("name", AttributeDataType.STRING))
                layer.attributes.add(FeatureAttribute("age", AttributeDataType.INTEGER))

                first_feature = layer.construct_feature()
                first_feature.geometry = Point(33.97, -118.25)
                first_feature.set_value("name", "John")
                first_feature.set_value("age", 23)
                layer.add(first_feature)

                second_feature = layer.construct_feature()
                second_feature.geometry = Point(35.81, -96.28)
                second_feature.set_value("name", "Mary")
                second_feature.set_value("age", 54)
                layer.add(second_feature)

            # Print the contents of the memory stream as a UTF-8 string
            memory_stream.seek(0)  # Move to the start of the stream before reading
            res = memory_stream.getvalue().decode('utf-8')
            print(res)
            res = res.replace("\r\n", "\n")
            refText = Comparison.read_file(reference).replace("\r\n", "\n")
            assert res.strip() == refText
