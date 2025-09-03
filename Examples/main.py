# This is a main file of Aspose.GIS for Python via .NET Examples.
# You can debug any tests and check the showcases.
from aspose.gis import License

from releases.Release_24_12_Tests import Release_24_12_Tests
from releases.Release_25_01_Tests import Release_25_01_Tests
from releases.Release_25_02_Tests import Release_25_02_Tests
from releases.Release_25_03_Tests import Release_25_03_Tests
from releases.Release_25_04_Tests import Release_25_04_Tests
from releases.Release_25_05_Tests import Release_25_05_Tests
from releases.Release_25_06_Tests import Release_25_06_Tests
from releases.Release_25_07_Tests import Release_25_07_Tests
from releases.Release_25_08_Tests import Release_25_08_Tests
from showcases.Convert_Tests import Convert_Tests
from showcases.CsvLayers_Tests import CsvLayers_Tests

from showcases.Geometry_Tests import Geometry_Tests
from showcases.Geometry_Validation_Tests import Geometry_Validation_Tests
from showcases.GpxLayers_Tests import GpxLayers_Tests
from showcases.InteractWithRasterFormats_Tests import InteractWithRasterFormats_Tests
from showcases.JoinedLayer_Tests import JoinedLayer_Tests
from showcases.KmlLayer_Tests import KmlLayer_Tests
from showcases.LabelMap_Tests import LabelMap_Tests
from showcases.Layers_Tests import Layers_Tests
from showcases.License_Tests import License_Tests
from showcases.ModifyFeatures_Tests import ModifyFeatures_Tests
from showcases.ReadFeatures_Tests import ReadFeatures_Tests
from showcases.ReadingESRIFileGeoDatabaseFileGDB_Tests import ReadingESRIFileGeoDatabaseFileGDB_Tests
from showcases.Rendering_Tests import Rendering_Tests
from showcases.WarpRasterFormats_Tests import WarpRasterFormats_Tests
from showcases.WriteLayer_Tests import WriteLayer_Tests


def run_releases_tests():
    release25_08 = Release_25_08_Tests()
    release25_08.RunAllTests()

    release25_07 = Release_25_07_Tests()
    release25_07.RunAllTests()

    release25_06 = Release_25_06_Tests()
    release25_06.RunAllTests()

    release25_05 = Release_25_05_Tests()
    release25_05.RunAllTests()

    release25_04 = Release_25_04_Tests()
    release25_04.RunAllTests()

    release25_03 = Release_25_03_Tests()
    release25_03.RunAllTests()

    release25_02 = Release_25_02_Tests()
    release25_02.RunAllTests()

    release25_01 = Release_25_01_Tests()
    release25_01.RunAllTests()

    release24_12 = Release_24_12_Tests()
    release24_12.RunAllTests()



def run_showcases_tests():
    showcases = [
        Convert_Tests(),
        CsvLayers_Tests(),
        Geometry_Tests(),
        Geometry_Validation_Tests(),
        GpxLayers_Tests(),
        InteractWithRasterFormats_Tests(),
        JoinedLayer_Tests(),
        KmlLayer_Tests(),
        LabelMap_Tests(),
        Layers_Tests(),
        License_Tests(),
        ModifyFeatures_Tests(),
        ReadFeatures_Tests(),
        ReadingESRIFileGeoDatabaseFileGDB_Tests(),
        Rendering_Tests(),
        WarpRasterFormats_Tests(),
        WriteLayer_Tests()
    ]

    for showcase in showcases:
        showcase.RunAllTests()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Don't forget install Aspose.GIS for Python via .NET
    # pip install aspose-gis-net
    # Temporary license can be obtained on https://purchase.aspose.com/temporary-license/

    lic = License()
    lic.set_license("PathToLicense")
    run_showcases_tests()
    run_releases_tests()