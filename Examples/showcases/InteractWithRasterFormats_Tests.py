import os
from datetime import datetime

import pytest
from aspose.gis import VectorLayer, Drivers, ConversionOptions, PointFormats, GeoConvert, GisException, PrecisionModel, \
    NumericFormat, Feature, Dataset, FeatureAttribute, AttributeDataType
from aspose.gis.formats.csv import CsvOptions
from aspose.gis.formats.filegdb import FileGdbOptions
from aspose.gis.formats.geojson import GeoJsonOptions
from aspose.gis.formats.gpx import GpxOptions
from aspose.gis.formats.shapefile import ShapefileOptions
from aspose.gis.formats.topojson import TopoJsonOptions
from aspose.gis.geometries import IPoint, ILineString, Geometry, Point, LineString, GeometryCollection, CircularString, \
    CompoundCurve, ICircularString, CurvePolygon, MultiCurve, MultiLineString, MultiPoint, LinearRing, Polygon, \
    MultiPolygon, MultiSurface, GeometryType, WkbVariant, WktVariant
from aspose.gis.raster import RasterRect, RasterLayer, IRasterValues, BandTypes
from aspose.gis.spatialreferencing import SpatialReferenceSystem, ProjectedSpatialReferenceSystemParameters, Unit, \
    AxisDirection, ProjectedAxisesOrder, Identifier, Axis
from aspose.pycore import cast

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.FolderSettings import FolderSettings
from utils.LicenseHelper import LicenseHelper

class InteractWithRasterFormats_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    def ReadGeneralDataInGeoTiffTest(self):
        input = os.path.join(FolderSettings.CommonTestFolder(), "raster50x50.tif")
        reference = os.path.join(FolderSettings.CommonTestFolder(), "geotiffref1.txt")

        res = ""
        with Drivers.geo_tiff.open_layer(input) as layer:
            # Read and print raster information
            cell_size = layer.cell_size
            extent = layer.get_extent()
            spatial_ref_sys = layer.spatial_reference_system
            code = "'no srs'" if spatial_ref_sys is None else str(spatial_ref_sys.epsg_code)
            bounds = layer.bounds
            band_count = layer.band_count
            
            res += f"cellSize: {cell_size}\n"
            res += f"extent: {extent}\n"
            res += f"spatialRefSys: {code}\n"
            res += f"bounds: {bounds}\n"
            res += f"bandCount: {band_count}\n"

            # Read and print bands
            for i in range(layer.band_count):
                data_type = layer.get_band(i).data_type
                has_no_data = layer.no_data_values is not None
                statistics = layer.get_statistics(i, True)

                res += "\n"
                res += f"Band: {i}\n"
                res += f"dataType: {data_type}\n"
                res += f"statistics: {statistics}\n"
                res += f"hasNoData: {has_no_data}\n"
                if has_no_data:
                    res += f"noData: {layer.no_data_values[i]}\n"

        assert Comparison.read_file(reference) == res

    def ReadValuesWithSpecifiedTypeTest(self):
        input = os.path.join(FolderSettings.CommonTestFolder(), "raster_float32.tif")
        with Drivers.geo_tiff.open_layer(input) as layer:
            # Get band values in corner cell.
            band_values = layer.get_values(0, 0)

            # We read data from the same strip with type float32, but all values are integers less than 255
            # so the next auto-cast is correct.
            print(f"byte: {band_values.as_byte(0)}")
            assert band_values.as_byte(0) == 107
            print(f"integer: {band_values.as_integer(0)}")
            assert band_values.as_integer(0) == 107
            print(f"float: {band_values.as_float(0)}")
            assert band_values.as_float(0) == 107.0
            # The next two lines are equivalent
            print(f"double: {band_values.as_double(0)}")
            assert band_values.as_double(0) == 107.0
            print(f"double with []: {band_values[0]}")
            assert band_values[0] == 107

    def ReadValuesByLineTest(self):
        input = os.path.join(FolderSettings.CommonTestFolder(), "raster_float32.tif")
        with Drivers.geo_tiff.open_layer(input) as layer:
            count = 0
            for i in range(layer.height):
                line_rect = RasterRect(0, i, layer.width, 1)
                line_dump = layer.get_values_dump(line_rect)
                count += len(line_dump)  # Assuming line_dump is a list or similar iterable

            print(f"total read values: {count}")
            assert count == 400

    def ReadRawBytesInGeoTiffTest(self):
        files_path = os.path.join(FolderSettings.CommonTestFolder(), "raster_int10.tif")
        ref_path = os.path.join(FolderSettings.CommonTestFolder(), "raw_bits_ref.txt")
        res = ""
        with Drivers.geo_tiff.open_layer(files_path) as layer:
            dump = layer.get_values_dump(layer.bounds)
            for value in dump:
                typedValue = cast(IRasterValues, value)
                if (typedValue.get_data_type(0) == BandTypes.RAW_BITS):
                    bits = str(typedValue)
                    res += bits
                # Later will be method as_raw_bits

            print("raw bits is read")
            assert res == Comparison.read_file(ref_path)

    def ReadSingleBandEsriAsciiTest(self):
        files_path = os.path.join(FolderSettings.CommonTestFolder(), "raster_single.asc")
        ref_path = os.path.join(FolderSettings.CommonTestFolder(), "raster_single_ref.txt")
        with Drivers.esri_ascii.open_layer(files_path) as layer:
            # The EsriAscii format always has only one band.
            cell_size = layer.cell_size
            extent = layer.get_extent()
            spatial_ref_sys = layer.spatial_reference_system
            code = "'no srs'" if spatial_ref_sys is None else str(spatial_ref_sys.epsg_code)
            bounds = layer.bounds
            band_count = layer.band_count
            nodata = layer.no_data_values[0]
            data_type = layer.get_band(0).data_type
            statistics = layer.get_statistics(0, True)

            res = ""
            res += f"cellSize: {cell_size}\n"
            res += f"extent: {extent}\n"
            res += f"spatialRefSys: {code}\n"
            res += f"bounds: {bounds}\n"
            res += f"bandCount: {band_count}\n"
            res += f"nodata: {nodata}\n"
            res += f"dataType: {data_type}\n"
            res += f"statistics: {statistics}"

        assert res == Comparison.read_file(ref_path)

          #  layer.get_values_on_expression(layer.bounds, lambda context, values: print(
            #    f"x: {context.cell_x}; y: {context.cell_y}; v: {values[0]}; e: {values.equals_no_data()}"))

    # At this moment not supported
    def AnalyzeValuesInGeoTiffTest(self):
        pass
        # input = os.path.join(FolderSettings.CommonTestFolder(), "raster50x50.tif")
        # with Drivers.geo_tiff.open_layer(input) as lyr:
        #     layer = cast(RasterLayer, lyr)
        #     # Get all values
        #     dump = layer.get_values_dump(layer.bounds)
        #
        #     # Compute cells count where values in all bands are 'no data'
        #     nodata_count = sum(1 for t in dump if t.equals_no_data(0) and t.equals_no_data(1) and t.equals_no_data(2))
        #     # Compute cells count where values resemble a blue color (<35, <35, >235)
        #     like_blue_count = sum(1 for t in dump if t[0] < 35 and t[1] < 35 and t[2] > 235)
        #
        #     print("")
        #     print("we use LINQ ")
        #     print(f"no data count: {nodata_count}")
        #     print(f"like blue color count: {like_blue_count}")
        #
        #     layer.get_values_on_expression(layer.bounds, inner)
        #
        #     print("")
        #     print("we use the 'GetValuesOnExpression' ")
        #     print(f"no data counter: {nodata}")
        #     print(f"like blue color counter: {like_blue}")

    # def delegate_method(context, values):
    #     # Use the 'GetValuesOnExpression' method to avoid additional memory allocation.
    #     nodata = 0
    #     like_blue = 0
    #     if values.equals_no_data(0) and values.equals_no_data(1) and values.equals_no_data(2):
    #         nodata += 1
    #
    #     if (values[0] < 35 and values[1] < 35 and values[2] > 235):
    #         like_blue += 1
