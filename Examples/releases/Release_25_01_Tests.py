import os

import pytest
from aspose.gis import Drivers, VectorLayer
import codecs
from aspose.gis.formats.osmxml import OsmXmlOptions
from aspose.gis.rendering import Map, Renderers
from aspose.gis.rendering.colorizers import MultiBandColor, BandColor
from aspose.pycore import cast

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper

class Release_25_01_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    def GetGrayBand(self):
        bandColor = BandColor()
        bandColor.band_index = 0
        bandColor.min = 0
        bandColor.max = 255

        color = MultiBandColor()
        color.red_band = bandColor
        color.blue_band = bandColor
        color.green_band = bandColor

        return color

    # Automatic calculation of map size for quick export
    # https://issue.saltov.dynabic.com/issues/GISNET-1071
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-2
    def GISNET1071Test(self):
        input1 = self.GetFileInBaseFolder("world1.jpg")
        input2 = self.GetFileInBaseFolder("ug.shp")

        output = self.GetFileInOutputFolder("result1071.jpg")
        reference = self.GetFileInBaseFolder("result1071.jpg")

        # Open the JPEG layer
        layer_1 = Drivers.jpeg_w.open_layer(input1)

        # Open the Shapefile layer
        layer_2 = Drivers.shapefile.open_layer(input2)

        # Create a new Map instance
        map_instance = Map()

        # Add the layers to the map
        map_instance.add(layer_1, self.GetGrayBand(), False)
        map_instance.add(layer_2)

        # Render the map to a JPEG file
        map_instance.render(output, Renderers.jpeg)
        Comparison.check_against_ethalon(output, reference, 0)

    # Aspose.GIS didn’t copy the tags when loaded nodes from one OSM to another one
    # https://issue.saltov.dynabic.com/issues/GISNET-1742
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-3
    def GISNET1742Test(self):
        # Set up the OSM XML options
        options = OsmXmlOptions()
        options.write_common_attributes = True
        options.report_common_attributes = True

        input = self.GetFileInBaseFolder("fountain.osm")
        output = self.GetFileInOutputFolder("result1742.xml")
        reference = self.GetFileInBaseFolder("result1742.xml")

        # Create a new layer with the specified options
        with VectorLayer.create(output, Drivers.osm_xml, options) as new_layer:
            # Open the existing layer
            with VectorLayer.open(input, Drivers.osm_xml, options) as layer:
                # Add each feature from the existing layer to the new layer
                for feature in layer:
                    new_layer.add(feature)

        Comparison.compare_binary_files(output, reference)

    # Aspose.GIS uses System Regional Settings for the saving of OSM Map that leads to , instead on . in XML Lon and Lat XML Node Attributes
    # https://issue.saltov.dynabic.com/issues/GISNET-1741
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-4
    def GISNET1741Test(self):
        # Set up the OSM XML options
        options = OsmXmlOptions()
        options.write_common_attributes = True
        options.report_common_attributes = True

        input = self.GetFileInBaseFolder("Wellington.osm")
        output = self.GetFileInOutputFolder("WellingtonResaved.osm")

        with VectorLayer.create(output, Drivers.osm_xml) as new_layer:
            with VectorLayer.open(input, Drivers.osm_xml) as layer:
                for attr in layer.attributes:
                    new_layer.attributes.add(attr)

                for feature in layer:
                    new_layer.add(feature)

        with codecs.open(output, 'r', "utf_8_sig") as file:
            data = file.read()
            dot_count = data.split('.')
            comma_count = data.split(',')

            # Count of commas and dots are calculated by eyes
            assert len(dot_count) >= 29059 and len(comma_count) <= 13


