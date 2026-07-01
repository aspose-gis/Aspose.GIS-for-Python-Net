import pytest
from aspose.gis import Drivers, VectorLayer, ConversionOptions
from aspose.gis.formats.gml import GmlOptions
from aspose.gis.formats.topojson import TopoJsonOptions

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper


class Release_26_05_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Object reference not set to an instance of an object during GPX-to-GPX
    # https://issue.saltov.dynabic.com/issues/GISNET-2017
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-81
    def GISNET2017Test(self):
        source_path = self.GetFileInBaseFolder("national_monuments_wgs84.gpx")
        destination_path = self.GetFileInOutputFolder("output_national_monuments_wgs84.gpx")
        reference_path = self.GetFileInBaseFolder("output_national_monuments_wgs84.gpx")
        # Ensure conversion does not raise an exception
        VectorLayer.convert(source_path, Drivers.gpx, destination_path, Drivers.gpx)

        Comparison.compare_binary_files(destination_path, reference_path)
        print(f" Successful convert to {destination_path}")

    # Shapefile To TopoJson - Results Does Not See in QGIS
    # https://issue.saltov.dynabic.com/issues/GISNET-2025
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-80
    def GISNET2025Test(self):
        options = ConversionOptions()
        topo_options = TopoJsonOptions()
        topo_options.trim_to_2d_geometry = True
        options.destination_driver_options = topo_options

        source_path = self.GetFileInBaseFolder("מחוזות מאוחד.shp")
        destination_path = self.GetFileInOutputFolder("output.json")
        reference_path = self.GetFileInBaseFolder("output.json")
        VectorLayer.convert(source_path, Drivers.shapefile, destination_path, Drivers.topo_json, options)

        Comparison.compare_binary_files(destination_path, reference_path)
        print(f" Successful convert to {destination_path}")

    # Shapefile To MapInfoInterChange - Results Does Not See in other solutions
    # https://issue.saltov.dynabic.com/issues/GISNET-2021
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-82
    def GISNET2021Test(self):
        source_path = self.GetFileInBaseFolder("מחוזות מאוחד.shp")
        destination_path = self.GetFileInOutputFolder("output.mif")
        reference_path = self.GetFileInBaseFolder("output.mif")
        VectorLayer.convert(source_path, Drivers.shapefile, destination_path, Drivers.map_info_interchange)

        with VectorLayer.open(destination_path, Drivers.map_info_interchange) as layer:
            assert layer.count == 6
            assert layer.attributes.count == 4

        Comparison.compare_binary_files(destination_path, reference_path)
        print(f" Successful convert to {destination_path}")

    # GML to MapInfoInterchange Corrupted in other solutions
    # https://issue.saltov.dynabic.com/issues/GISNET-2020
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-83
    def GISNET2020Test(self):
        source_path = self.GetFileInBaseFolder("1.osm")
        destination_path = self.GetFileInOutputFolder("output.gml")
        reference_path = self.GetFileInBaseFolder("output.gml")
        VectorLayer.convert(source_path, Drivers.osm_xml, destination_path, Drivers.gml)

        gmlOpt = GmlOptions()
        gmlOpt.restore_schema = True
        with VectorLayer.open(destination_path, Drivers.gml, gmlOpt) as layer:
            assert layer.count == 30
            assert layer.attributes.count == 37

        Comparison.compare_binary_files(destination_path, reference_path)
        print(f" Successful convert to {destination_path}")

    # Osm To MapInfoInterChange - Results Does Not See in other solutions
    # https://issue.saltov.dynabic.com/issues/GISNET-2013
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-84
    def GISNET2013Test(self):
        source_path = self.GetFileInBaseFolder("1.osm")
        destination_path = self.GetFileInOutputFolder("output.mif")
        reference_path = self.GetFileInBaseFolder("output.mif")
        VectorLayer.convert(source_path, Drivers.osm_xml, destination_path, Drivers.map_info_interchange)

        with VectorLayer.open(destination_path, Drivers.map_info_interchange) as layer:
            assert layer.count == 30
            assert layer.attributes.count == 36

        Comparison.compare_binary_files(destination_path, reference_path)
        print(f" Successful convert to {destination_path}")