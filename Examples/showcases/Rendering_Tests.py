import os
from datetime import datetime

import pytest
from aspose.pydrawing import Color
from aspose.gis import VectorLayer, Drivers, ConversionOptions, PointFormats, GeoConvert, GisException, PrecisionModel, \
    NumericFormat, Feature, Dataset, FeatureAttribute, AttributeDataType, RasterDriverOptions, Extent
from aspose.gis.formats.csv import CsvOptions
from aspose.gis.formats.filegdb import FileGdbOptions
from aspose.gis.formats.geojson import GeoJsonOptions
from aspose.gis.formats.geotiff import GeoTiffOptions
from aspose.gis.formats.gpx import GpxOptions
from aspose.gis.formats.shapefile import ShapefileOptions
from aspose.gis.formats.topojson import TopoJsonOptions
from aspose.gis.geometries import IPoint, ILineString, Geometry, Point, LineString, GeometryCollection, CircularString, \
    CompoundCurve, ICircularString, CurvePolygon, MultiCurve, MultiLineString, MultiPoint, LinearRing, Polygon, \
    MultiPolygon, MultiSurface, GeometryType, WkbVariant, WktVariant
from aspose.gis.raster import RasterRect, RasterLayer, IRasterValues, BandTypes
from aspose.gis.rendering import Map, VectorMapLayer, Renderers, Measurement
from aspose.gis.rendering.colorizers import MultiBandColor, BandColor
from aspose.gis.rendering.sld import SldImportOptions
from aspose.gis.spatialreferencing import SpatialReferenceSystem, ProjectedSpatialReferenceSystemParameters, Unit, \
    AxisDirection, ProjectedAxisesOrder, Identifier, Axis
from aspose.pycore import cast

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.FolderSettings import FolderSettings
from utils.LicenseHelper import LicenseHelper

class Rendering_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    def ImportSldTest(self):
            output = os.path.join(FolderSettings.BaseTestOutputFolder(), "lines_sld_style_out.png")
            reference = os.path.join(FolderSettings.CommonTestFolder(), "lines_sld_style_out.png")
            with Map(Measurement.pixels(500), Measurement.pixels(300)) as map_instance:
                # Open a layer containing the data
                layer = VectorLayer.open(os.path.join(FolderSettings.CommonTestFolder(), "lines.geojson"), Drivers.geo_json)

                # Create a map layer (a styled representation of the data)
                map_layer = VectorMapLayer(layer)

                # Import a style from an SLD document
                map_layer.import_sld(os.path.join(FolderSettings.CommonTestFolder(), "lines.sld"), SldImportOptions())

                # Add the styled layer to the map and render it
                map_instance.add(map_layer)
                map_instance.render((output), Renderers.png)

            Comparison.check_against_ethalon(output, reference, 0)

    def DrawRasterDefaultSettingsTest(self):
        output = os.path.join(FolderSettings.BaseTestOutputFolder(), "raster_float32_out.svg")
        reference = os.path.join(FolderSettings.CommonTestFolder(), "raster_float32_out.svg")
        bandColor = BandColor()

        bandColor.band_index = 0
        bandColor.min = 0
        bandColor.max = 255

        color = MultiBandColor()
        color.red_band = bandColor

        with Map(Measurement.pixels(500), Measurement.pixels(500)) as map_instance:
            layer = Drivers.geo_tiff.open_layer(os.path.join(FolderSettings.CommonTestFolder(), "raster_float32.tif"))
            # Conversion to colors is detected automatically.
            # The maximum and minimum values are calculated and linear interpolation is used.
            map_instance.add(layer, color, False)
            map_instance.render(output, Renderers.svg)

        Comparison.compare_as_streams(output, reference)

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

    def DrawSkewRasterTest(self):
        input = os.path.join(FolderSettings.CommonTestFolder(), "raster_skew.tif")
        output = os.path.join(FolderSettings.BaseTestOutputFolder(), "raster_skew_out.svg")
        reference = os.path.join(FolderSettings.CommonTestFolder(), "raster_skew_out.svg")

        # Create a new Map instance with specified dimensions
        with Map(Measurement.pixels(500), Measurement.pixels(500)) as map_instance:
            # Use background color
            map_instance.background_color = Color.azure  # Assuming you can set the background color as a string

            # Open the GeoTiff layer
            layer = Drivers.geo_tiff.open_layer(input)

            # Add the layer to the map.
            # The conversion to colors is detected automatically, and interpolation is handled internally.
            map_instance.add(layer, self.GetGrayBand(), False)

            # Render the map to an SVG file
            map_instance.render(output, Renderers.svg)

        Comparison.compare_as_streams(output, reference)

    def DrawPolarRasterExtentTest(self):
        input = os.path.join(FolderSettings.CommonTestFolder(), "raster_countries.tif")
        output = os.path.join(FolderSettings.BaseTestOutputFolder(), "raster_countries_gnomonic_out.png")
        reference = os.path.join(FolderSettings.CommonTestFolder(), "raster_countries_gnomonic_out.png")


        # Create a new Map instance with specified dimensions
        with Map(Measurement.pixels(500), Measurement.pixels(500)) as map_instance:
            # Set up the polar extent and coordinate system (gnomonic spatial reference)
            map_instance.spatial_reference_system = SpatialReferenceSystem.create_from_epsg(102034)
            map_instance.extent = Extent(-180, 60, 180, 90, SpatialReferenceSystem.wgs84)
            map_instance.background_color = Color.azure  # Set background color

            # Open the GeoTIFF layer
            layer = Drivers.geo_tiff.open_layer(input)

            # Draw the layer with the specified colorizer
            map_instance.add(layer, self.GetGrayBand(), False)

            # Render the map to a PNG file
            map_instance.render(output, Renderers.png)

        Comparison.check_against_ethalon(output, reference, 0)


    def ComplexDrawingOnLayers(self):
        def DrawRasterDefaultSettingsTest(self):
            output = os.path.join(FolderSettings.BaseTestOutputFolder(), "raster_float32_out.svg")
            reference = os.path.join(FolderSettings.CommonTestFolder(), "raster_float32_out.svg")
            bandColor = BandColor()

            bandColor.band_index = 0
            bandColor.min = 0
            bandColor.max = 255

            color = MultiBandColor()
            color.red_band = bandColor

            with Map(Measurement.pixels(500), Measurement.pixels(500)) as map_instance:
                layer = Drivers.geo_tiff.open_layer(
                    os.path.join(FolderSettings.CommonTestFolder(), "raster_float32.tif"))
                # Conversion to colors is detected automatically.
                # The maximum and minimum values are calculated and linear interpolation is used.
                map_instance.add(layer, color, False)
                map_instance.render(output, Renderers.svg)

            Comparison.compare_as_streams(output, reference)
