import os
from datetime import datetime

import pytest
from aspose.gis import VectorLayer, Drivers, RasterDriver, Extent
from aspose.gis.formats.geotiff import GeoTiffDriver
from aspose.gis.raster import WarpOptions, RasterLayer, IRasterValues, BandTypes
from aspose.gis.spatialreferencing import SpatialReferenceSystem
from aspose.pycore import cast

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.FolderSettings import FolderSettings
from utils.LicenseHelper import LicenseHelper

class WarpRasterFormats_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    def ResizeToWgs84RasterLayerTest(self):
        input = os.path.join(FolderSettings.CommonTestFolder(), "raster_float32.tif")

        warpOpt = WarpOptions()
        warpOpt.width = 40
        warpOpt.height = 40
        warpOpt.target_spatial_reference_system = SpatialReferenceSystem.wgs84
        # ExStart: ResizeToWgs84RasterLayer
        with Drivers.geo_tiff.open_layer(input) as layer:
            with layer.warp(warpOpt) as warped:
                # warped = cast(RasterDriver, wrp)
                # Read and print raster properties
                cell_size = warped.cell_size
                extent = warped.get_extent()
                spatial_ref_sys = warped.spatial_reference_system
                code = spatial_ref_sys.epsg_code if spatial_ref_sys is not None else "'no srs'"
                bounds = warped.bounds
                band_count = warped.band_count

                print(f"cellSize: {cell_size}")
                assert str(cell_size) == "Width: 0,00032645569750044956; Height: 0,0002722297455713729"
                print(f"extent: {extent}")
                assert str(extent) == "Min (X = -117.64205693303224, Y = 33.89162681583117), Max (X = -117.62899870513222, Y = 33.90251600565402)"
                print(f"spatialRefSys: {code}")
                assert str(code) == "4326"
                print(f"bounds: {bounds}")
                assert str(bounds) == "X: 0; Y: 0; Width: 40; Height: 40;"
                print(f"bandCount: {band_count}")
                assert band_count == 1

                # Read and print bands
                for i in range(band_count):
                    data_type = warped.get_band(i).data_type
                    ndv = cast(IRasterValues, warped.no_data_values)
                    has_no_data = not ndv.is_null(i)
                    statistics = warped.get_statistics(i, True)

                    print()
                    print(f"Band: {i}")
                    print(f"dataType: {data_type}")
                    assert data_type == BandTypes.FLOAT
                    print(f"statistics: {statistics}")
                    assert str(statistics) == "Min: 74; Max: 255; Mean: 126,765; Sum: 202824; Count: 1600"
                    print(f"hasNoData: {has_no_data}")
                    if has_no_data:
                        print(f"noData: {warped.no_data_values[i]}")

    def RescaleCellsInSpecifiedExtentTest(self):
        input = os.path.join(FolderSettings.CommonTestFolder(),  "raster_float32.tif")
        with Drivers.geo_tiff.open_layer(input) as layer:
            source_extent = layer.get_extent()
            new_extent = Extent(
                source_extent.x_min,
                source_extent.y_min,
                source_extent.x_min + source_extent.width * 0.5,
                source_extent.y_max + source_extent.height * 0.5,
                layer.spatial_reference_system
            )

            warpOpt = WarpOptions()
            warpOpt.cell_width = 120
            warpOpt.cell_height = 120
            warpOpt.target_extent = new_extent

            with layer.warp(warpOpt) as warped:
                # Read and print raster properties
                cell_size = warped.cell_size
                extent = warped.get_extent()
                spatial_ref_sys = warped.spatial_reference_system
                code = spatial_ref_sys.epsg_code if spatial_ref_sys is not None else "'no srs'"
                bounds = warped.bounds

                print(f"cellSize: {cell_size}")
                assert str(cell_size) == "Width: 120; Height: 120"
                print(f"source extent: {source_extent}")
                assert str(source_extent) == "Min (X = 440720, Y = 3750120), Max (X = 441920, Y = 3751320)"
                print(f"target extent: {extent}")
                assert str(extent) == "Min (X = 440720, Y = 3750120), Max (X = 441320, Y = 3751920)"
                print(f"spatialRefSys: {code}")
                assert str(code) == "26711"
                print(f"bounds: {bounds}")
                assert str(bounds) == "X: 0; Y: 0; Width: 5; Height: 15;"
