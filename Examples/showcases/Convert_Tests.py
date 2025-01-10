import os

import pytest
from aspose.gis import VectorLayer, Drivers, ConversionOptions
from aspose.gis.formats.topojson import TopoJsonOptions
from aspose.pycore import cast

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.FolderSettings import FolderSettings
from utils.LicenseHelper import LicenseHelper
class Convert_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Convert GeoJson To TopoJson
    def ConvertGeoJsonToTopoJsonTest(self):
        # Define the paths
        sample_geojson_path = os.path.join(FolderSettings.CommonTestFolder(), "sample.geojson")
        reference_file_path = os.path.join(FolderSettings.CommonReferenceTestFolder(), "convertedSample_out.topojson")
        output_file_path = os.path.join(FolderSettings.BaseTestOutputFolder(), "convertedSample_out.topojson")

        # Perform the conversion
        VectorLayer.convert(sample_geojson_path, Drivers.geo_json, output_file_path, Drivers.topo_json)
        Comparison.compare_binary_files(reference_file_path, output_file_path)

    def ConvertGeoJsonToTopoJsonAndSpecifyObjectNameTest(self):
        # Define the paths
        sample_geojson_path = os.path.join(FolderSettings.CommonTestFolder(), "sample.geojson")
        reference_file_path = os.path.join(FolderSettings.CommonReferenceTestFolder(), "convertedSampleWithObjectName_out.topojson")
        output_file_path = os.path.join(FolderSettings.BaseTestOutputFolder(), "convertedSampleWithObjectName_out.topojson")

        # Set up the conversion options
        options = ConversionOptions()
        topoJsonOptions = TopoJsonOptions()
        topoJsonOptions.default_object_name = "name_of_the_object"
        options.destination_driver_options = topoJsonOptions
        # Perform the conversion
        VectorLayer.convert(sample_geojson_path, Drivers.geo_json, output_file_path, Drivers.topo_json, options)

        Comparison.compare_binary_files(reference_file_path, output_file_path)

    def ConvertGeoJsonToTopoJsonWithGroupingIntoObjectsTest(self):
        # Define the paths
        sample_geojson_path = os.path.join(FolderSettings.CommonTestFolder(), "sample.geojson")
        reference_file_path = os.path.join(FolderSettings.CommonReferenceTestFolder(), "convertedSampleWithGrouping_out.topojson")
        output_file_path = os.path.join(FolderSettings.BaseTestOutputFolder(), "convertedSampleWithGrouping_out.topojson")

        # Set up the conversion options
        options = ConversionOptions()
        topoJsonOptions = TopoJsonOptions()
        topoJsonOptions.default_object_name = "unnamed"
        topoJsonOptions.object_name_attribute = "group"
        options.destination_driver_options = topoJsonOptions
        # Perform the conversion
        VectorLayer.convert(sample_geojson_path, Drivers.geo_json, output_file_path, Drivers.topo_json, options)

        Comparison.compare_binary_files(reference_file_path, output_file_path)

    def ConvertGeoJsonToTopoJsonWithQuantizationTest(self):
        # Define the paths
        sample_geojson_path = os.path.join(FolderSettings.CommonTestFolder(), "sample.geojson")
        reference_file_path = os.path.join(FolderSettings.CommonReferenceTestFolder(),
                                           "convertedSampleWithQuantization_out.topojson")
        output_file_path = os.path.join(FolderSettings.BaseTestOutputFolder(),
                                        "convertedSampleWithQuantization_out.topojson")

        # Set up the conversion options
        options = ConversionOptions()
        topoJsonOptions = TopoJsonOptions()
        topoJsonOptions.quantization_number = 100_000
        options.destination_driver_options = topoJsonOptions
        # Perform the conversion
        VectorLayer.convert(sample_geojson_path, Drivers.geo_json, output_file_path, Drivers.topo_json, options)

        Comparison.compare_binary_files(reference_file_path, output_file_path)

    def ConvertShapeFileToGeoJSONTest(self):
        # Define the paths
        shapefile_path = os.path.join(FolderSettings.CommonTestFolder(), "InputShapeFile.shp")
        reference_file_path = os.path.join(FolderSettings.CommonReferenceTestFolder(), "output_out.json")
        output_file_path = os.path.join(FolderSettings.BaseTestOutputFolder(), "output_out.json")

        # Perform the conversion
        VectorLayer.convert(shapefile_path, Drivers.shapefile, output_file_path, Drivers.geo_json)

        Comparison.compare_binary_files(reference_file_path, output_file_path)

    def ConvertTopoJsonToGeoJsonTest(self):
        # Define the paths
        topo_json_path = os.path.join(FolderSettings.CommonTestFolder(), "sample.topojson")
        reference_file_path = os.path.join(FolderSettings.CommonReferenceTestFolder(), "convertedSample_out.geojson")
        output_file_path = os.path.join(FolderSettings.BaseTestOutputFolder(), "convertedSample_out.geojson")

        # Perform the conversion
        VectorLayer.convert(topo_json_path, Drivers.topo_json, output_file_path, Drivers.geo_json)

        Comparison.compare_binary_files(reference_file_path, output_file_path)

