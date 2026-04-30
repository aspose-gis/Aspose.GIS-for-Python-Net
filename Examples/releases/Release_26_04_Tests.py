import pytest
from aspose.gis import Drivers, VectorLayer, ConversionOptions
from aspose.gis.formats.gml import GmlOptions

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper

class Release_26_04_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Osm To GeoPackage (incorrect attribute name)
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-75
    # https://issue.saltov.dynabic.com/issues/GISNET-2010
    def GISNET2010Test(self):
        source_path = self.GetFileInBaseFolder("1.osm")
        destination_path = self.GetFileInOutputFolder("1.gpkg")
        reference_file = self.GetFileInBaseFolder("1.gpkg")
        VectorLayer.convert(source_path, Drivers.osm_xml, destination_path, Drivers.geo_package)
        with VectorLayer.open(destination_path, Drivers.geo_package) as layer:
            assert layer.count == 30
            assert layer.attributes.count == 35

        Comparison.compare_binary_files(destination_path, reference_file)
        print(f" Successful convert to {destination_path}")

    # Osm To Gml (incorrect attribute name)
    # https://issue.saltov.dynabic.com/issues/GISNET-2011
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-76
    def GISNET2011Test(self):
        source_path = self.GetFileInBaseFolder("1.osm")
        destination_path = self.GetFileInOutputFolder("output.gml")
        reference_file = self.GetFileInBaseFolder("output.gml")

        # Convert OSM to GML
        VectorLayer.convert(source_path, Drivers.osm_xml, destination_path, Drivers.gml)

        opt = GmlOptions()
        opt.restore_schema = True
        # Verify the conversion results with restored schema
        with VectorLayer.open(destination_path, Drivers.gml, opt) as layer:
            assert layer.count == 30
            assert layer.attributes.count == 37

        Comparison.compare_binary_files(destination_path, reference_file)
        print(f" Successful convert to {destination_path}")

    # Gml to Gml throw exception and also to all other formats
    # https://issue.saltov.dynabic.com/issues/GISNET-1977
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-77
    def GISNET1977Test(self):
        # Configure conversion options with schema restoration for source GML
        opt = GmlOptions()
        opt.restore_schema = True

        conversion_options = ConversionOptions()
        conversion_options.source_driver_options = opt

        source_path = self.GetFileInBaseFolder("101_features.gml")
        destination_path = self.GetFileInOutputFolder("output.gml")
        reference_file = self.GetFileInBaseFolder("output.gml")

        # Convert GML to GML using the configured options
        VectorLayer.convert(source_path, Drivers.gml, destination_path, Drivers.gml, conversion_options)
        Comparison.compare_binary_files(destination_path, reference_file)
        print(f" Successful convert to {destination_path}")

    # GML Conversion Produces Some Errors
    # https://issue.saltov.dynabic.com/issues/GISNET-2000
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-78
    def GISNET2000Test(self):
        # Configure conversion options with schema restoration for source GML
        opt = GmlOptions()
        opt.restore_schema = True

        conversion_options = ConversionOptions()
        conversion_options.source_driver_options = opt

        source_path = self.GetFileInBaseFolder("zak.gml")
        destination_path = self.GetFileInOutputFolder("output.gml")
        reference_file = self.GetFileInBaseFolder("output.gml")

        # Convert GML to GML using the configured options
        VectorLayer.convert(source_path, Drivers.gml, destination_path, Drivers.gml, conversion_options)
        Comparison.compare_binary_files(destination_path, reference_file)
        print(f" Successful convert to {destination_path}")