import os
from datetime import datetime
from time import sleep

import pytest
from aspose.gis import VectorLayer, Drivers, ConversionOptions, PointFormats, GeoConvert, GisException, PrecisionModel, \
    NumericFormat, Feature, Dataset, FeatureAttribute, AttributeDataType
from aspose.gis.formats.filegdb import FileGdbOptions
from aspose.gis.formats.geojson import GeoJsonOptions
from aspose.gis.formats.kml import KmlOptions
from aspose.gis.formats.shapefile import ShapefileOptions
from aspose.gis.formats.topojson import TopoJsonOptions
from aspose.gis.geometries import IPoint, ILineString, Geometry, Point, LineString, GeometryCollection, CircularString, \
    CompoundCurve, ICircularString, CurvePolygon, MultiCurve, MultiLineString, MultiPoint, LinearRing, Polygon, \
    MultiPolygon, MultiSurface, GeometryType, WkbVariant, WktVariant
from aspose.gis.spatialreferencing import SpatialReferenceSystem, ProjectedSpatialReferenceSystemParameters, Unit, \
    AxisDirection, ProjectedAxisesOrder, Identifier, Axis
from aspose.pycore import cast

from showcases.ZipPath import ZipPath
from utils.BaseTests import BaseTests

from utils.Comparison import Comparison
from utils.FolderSettings import FolderSettings
from utils.LicenseHelper import LicenseHelper
class Layers_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    def AbstractPathDemoTest(self):
        pass
        #files_folder = FolderSettings.CommonTestFolder()
        #zip_filename = os.path.join(files_folder, "land_shp.zip")

        #with open(zip_filename, "rb") as stream:

         #   with ZipPath("land.shp", stream) as zip_path:
          #      with Drivers.shapefile.open_layer(zip_path.as_abstract_path()) as layer:
           #         print(layer.spatial_reference_system)
            #        for feature in layer:
             #           print(feature.geometry.as_text())

    def AccessFeaturesInTopoJsonTest(self):
        sample_topo_json_path = os.path.join(FolderSettings.CommonTestFolder(), "sample.topojson")
        outputFile = os.path.join(FolderSettings.BaseTestOutputFolder(), "sample.out.topojson")
        referenceFile = os.path.join(FolderSettings.CommonTestFolder(), "sample.out.topojson")
        builder = []

        with VectorLayer.open(sample_topo_json_path, Drivers.topo_json) as layer:
            for item in layer:
                # get id property
                feature = cast(Feature, item)
                id = feature.get_value("id")

                # get name of the object that contains this feature
                object_name = feature.get_value_or_default("topojson_object_name", "")

                # get name attribute property, located inside 'properties' object
                #name = feature.get_value_or_default("name", "")

                name = feature.get_value("name")

                # get geometry of the feature.
                geometry = feature.geometry.as_text()

                builder.append(f"Feature with ID {id}:\n")
                builder.append(f"Object Name = {object_name}\n")
                builder.append(f"Name        = {name}\n")
                builder.append(f"Geometry    = {geometry}\n")

        print("Output:")
        output = "".join(builder)

        print(output)
        with open(outputFile, "w") as f:
            f.write(output)
            f.close()

        Comparison.compare_binary_files(outputFile, referenceFile)

    def AddLayerToFileGdbDatasetTest(self):
        # -- copy test dataset, to avoid modification of test data.
        path = os.path.join(FolderSettings.CommonTestFolder(), "ThreeLayers.gdb")
        dataset_path = os.path.join(FolderSettings.BaseTestOutputFolder(), "AddLayerToFileGdbDataset_out.gdb")
        FolderSettings.copy_folder(path, dataset_path)
        # --

        with Dataset.open(dataset_path, Drivers.file_gdb) as dataset:
            print(dataset.can_create_layers)  # True

            with dataset.create_layer("data", SpatialReferenceSystem.wgs84) as layer:
                layer.attributes.add(FeatureAttribute("Name", AttributeDataType.STRING))
                feature = cast(Feature, layer.construct_feature())
                feature.set_value("Name", "Name_1")
                feature.geometry = Point(12.21, 23.123, 20, -200)
                layer.add(feature)

            with dataset.open_layer("data", FileGdbOptions()) as layer:
                print(layer.count)  # 1
                assert layer.count == 1
                print(layer[0].get_value("Name"))  # "Name_1"
                assert layer[0].get_value("Name") == "Name_1"

    def ConvertGeoJsonLayerToLayerInFileGdbDatasetTest(self):
        # Define the paths
        geoJsonPath = os.path.join(FolderSettings.BaseTestOutputFolder(),
                                   "ConvertGeoJsonLayerToLayerInFileGdbDataset_out.json")
        geoJsonPathReference = os.path.join(FolderSettings.CommonTestFolder(),
                                   "ConvertGeoJsonLayerToLayerInFileGdbDataset_out.json")

        # Create a GeoJSON layer
        with VectorLayer.create(geoJsonPath, Drivers.geo_json) as layer:
            layer.attributes.add(FeatureAttribute("name", AttributeDataType.STRING))
            layer.attributes.add(FeatureAttribute("age", AttributeDataType.INTEGER))

            # Create the first feature
            firstFeature = layer.construct_feature()
            firstFeature.geometry = Point(33.97, -118.25)
            firstFeature.set_value("name", "John")
            firstFeature.set_value("age", 23)
            layer.add(firstFeature)

            # Create the second feature
            secondFeature = layer.construct_feature()
            secondFeature.geometry = Point(35.81, -96.28)
            secondFeature.set_value("name", "Mary")
            secondFeature.set_value("age", 54)
            layer.add(secondFeature)

        # -- Copy test dataset, to avoid modification of test data.

        # -- copy test dataset, to avoid modification of test data.
        sourceFile = os.path.join(FolderSettings.CommonTestFolder(), "ThreeLayers.gdb")
        destinationFile = os.path.join(FolderSettings.BaseTestOutputFolder(), "ThreeLayersCopy_out.gdb")
        FolderSettings.copy_folder(sourceFile, destinationFile)
        # --

        # -- Open the GeoJSON layer and copy it to a File Geodatabase
        with VectorLayer.open(geoJsonPath, Drivers.geo_json) as geoJsonLayer:
            with Dataset.open(destinationFile, Drivers.file_gdb) as fileGdbDataset:
                with fileGdbDataset.create_layer("new_layer", SpatialReferenceSystem.wgs84) as fileGdbLayer:
                    fileGdbLayer.copy_attributes(geoJsonLayer)
                    for feature in geoJsonLayer:
                        fileGdbLayer.add(feature)

        Comparison.compare_binary_files(geoJsonPath, geoJsonPathReference)

    def ConvertPolygonShapeFileToLineStringShapeFileTest(self):
        # Define the data directory
        openPath = os.path.join(FolderSettings.CommonTestFolder(), "PolygonShapeFile.shp")
        createPath = os.path.join(FolderSettings.BaseTestOutputFolder(), "PolygonShapeFileToLineShapeFile_out.shp")
        createPathRef = os.path.join(FolderSettings.CommonTestFolder(), "PolygonShapeFileToLineShapeFile_out.shp")

        # Convert Polygon ShapeFile to LineString ShapeFile
        with VectorLayer.open(openPath, Drivers.shapefile) as source:
            with VectorLayer.create(createPath, Drivers.shapefile) as destination:
                for sourceFeature in source:
                    polygon = sourceFeature.geometry  # Assuming sourceFeature.geometry returns a Polygon
                    line = LineString(polygon.exterior_ring)  # Assuming exterior_ring is accessible
                    destinationFeature = destination.construct_feature()
                    destinationFeature.geometry = line
                    destination.add(destinationFeature)

        Comparison.compare_binary_files(createPath, createPathRef)

    def CreateFileGdbDatasetTest(self):
        # Check if the FileGDB driver can create datasets
        print(Drivers.file_gdb.can_create_datasets)  # Should return True
        assert Drivers.file_gdb.can_create_datasets == True

        # Define the path for the File Geodatabase
        path = os.path.join(FolderSettings.BaseTestOutputFolder(), "CreateFileGdbDataset_out.gdb")

        # Create the File Geodatabase dataset
        with Dataset.create(path, Drivers.file_gdb) as dataset:
            print(dataset.layers_count)  # Should print 0
            assert dataset.layers_count == 0

            # Create the first layer
            with dataset.create_layer(name = "layer_1", spatial_reference_system = None) as layer:
                featureAttr = FeatureAttribute("value", AttributeDataType.INTEGER)
                layer.attributes.add(featureAttr)

                for i in range(10):
                    feature = layer.construct_feature()
                    feature.set_value("value", i)
                    feature.geometry = Point(i, i)
                    layer.add(feature)

            # Create the second layer
            with dataset.create_layer(name = "layer_2", spatial_reference_system = None) as layer:
                feature = layer.construct_feature()
                lineString = LineString()
                lineString.add_point(1, 2)
                lineString.add_point(3, 4)
                feature.geometry = lineString
                layer.add(feature)

            print(dataset.layers_count)  # Should print 2
            assert dataset.layers_count == 2

    def CreateFileGdbDatasetWithSingleLayerTest(self):
        # Define the path for the File Geodatabase
        path = os.path.join(FolderSettings.BaseTestOutputFolder(), "CreateFileGdbDatasetWithSingleLayer_out.gdb")
        options = FileGdbOptions()

        # Create the File Geodatabase dataset with a single layer
        with VectorLayer.create(path, Drivers.file_gdb, options, SpatialReferenceSystem.wgs84) as layer:
            feature = layer.construct_feature()
            lineString = LineString()
            lineString.add_point(1, 2)
            lineString.add_point(3, 4)
            feature.geometry = lineString
            layer.add(feature)

        # Open the dataset and layer to check the feature count
        with Dataset.open(path, Drivers.file_gdb) as dataset:
            with dataset.open_layer(name="layer", options=None) as layer:
                print("Features count: {}".format(layer.count))  # Should print: Features count: 1
                assert layer.count == 1

    def CreateNewShapeFileTest(self):
        # Define the data directory
        outputPath = os.path.join(FolderSettings.BaseTestOutputFolder(), "CreateNewShapeFile_out.shp")
        referencePath = os.path.join(FolderSettings.CommonTestFolder(), "CreateNewShapeFile_out.shp")

        # Create a new shapefile
        with VectorLayer.create(outputPath, Drivers.shapefile) as layer:
            # Add attributes before adding features
            layer.attributes.add(FeatureAttribute("name", AttributeDataType.STRING))
            layer.attributes.add(FeatureAttribute("age", AttributeDataType.INTEGER))
            layer.attributes.add(FeatureAttribute("dob", AttributeDataType.DATE_TIME))

            # Case 1: Set values for the first feature
            firstFeature = layer.construct_feature()
            firstFeature.geometry = Point(33.97, -118.25)
            firstFeature.set_value("name", "John")
            firstFeature.set_value("age", 23)
            firstFeature.set_value("dob", datetime(1982, 2, 5, 16, 30, 0))
            layer.add(firstFeature)

            # Set values for the second feature
            secondFeature = layer.construct_feature()
            secondFeature.geometry = Point(35.81, -96.28)
            secondFeature.set_value("name", "Mary")
            secondFeature.set_value("age", 54)
            secondFeature.set_value("dob", datetime(1984, 12, 15, 15, 30, 0))
            layer.add(secondFeature)

            # Case 2: Set new values for all of the attributes for a third feature
            thirdFeature = layer.construct_feature()
            thirdFeature.geometry = Point(34.81, -92.28)
            data = ["Alex", 25, datetime(1989, 4, 15, 15, 30, 0)]
            thirdFeature.set_values(data)  # Assuming set_values accepts a list/array of values
            layer.add(thirdFeature)

        Comparison.compare_binary_files(outputPath, referencePath)

    def CreateVectorLayerWithSpatialReferenceSystemTest(self):
        # Define the data directory
        dataDir = FolderSettings.BaseTestOutputFolder()

        # Define the parameters for the projected spatial reference system
        parameters = ProjectedSpatialReferenceSystemParameters()
        parameters.name = "WGS 84 / World Mercator"
        parameters.base=SpatialReferenceSystem.wgs84
        parameters.projection_method_name = "Mercator_1SP"
        parameters.linear_unit = Unit.meter
        parameters.x_axis = Axis("Easting", AxisDirection.EAST)
        parameters.y_axis = Axis("Northing", AxisDirection.NORTH)
        parameters.axises_order = ProjectedAxisesOrder.XY

        # Add projection parameters
        parameters.add_projection_parameter("central_meridian", 0)
        parameters.add_projection_parameter("scale_factor", 1)
        parameters.add_projection_parameter("false_easting", 0)
        parameters.add_projection_parameter("false_northing", 0)

        # Create the projected spatial reference system
        projected_srs = SpatialReferenceSystem.create_projected(parameters, Identifier.epsg(3395))

        # Create a shapefile layer with the specified spatial reference system
        with Drivers.shapefile.create_layer(os.path.join(dataDir, "filepath_out.shp"), ShapefileOptions(),
                                            projected_srs) as layer:
            feature = layer.construct_feature()
            feature.geometry = Point(1, 2)
            layer.add(feature)

            feature = layer.construct_feature()
            feature.geometry = Point(1, 2)
            feature.geometry.spatial_reference_system = SpatialReferenceSystem.nad83  # Assuming this is how to set it

            wasException = False
            try:
                layer.add(feature)  # Attempt to add the feature with a different SRS
            except Exception as e:
                wasException = True
                print(e)

            assert wasException

        # Open the layer to check its spatial reference system
        with Drivers.shapefile.open_layer(os.path.join(dataDir, "filepath_out.shp")) as layer:
            srs_name = layer.spatial_reference_system.name  # "WGS 84 / World Mercator"
            assert srs_name == "WGS_84_World_Mercator"
            is_equivalent = layer.spatial_reference_system.is_equivalent(projected_srs)  # Should return True
            assert is_equivalent

    def CropLayerTest(self):
        # Define the data directory
        inputPath = os.path.join(FolderSettings.CommonTestFolder(), "geodetic_world.tif")
        outputPath = os.path.join(FolderSettings.BaseTestOutputFolder(), "geodetic_world.tif")
        FolderSettings.copy_file(inputPath, outputPath)
        with Drivers.geo_tiff.open_layer(outputPath) as layer:
            with layer.crop(Geometry.from_text("POLYGON ((-160 0, 0 60, 160 0, 0 -160, -160 0))"), None) as warped:
                # read and print raster
                cell_size = warped.cell_size
                extent = warped.get_extent()
                spatial_ref_sys = warped.spatial_reference_system
                code = "'no srs'" if spatial_ref_sys is None else str(spatial_ref_sys.epsg_code)
                bounds = warped.bounds

                print(f"cellSize: {cell_size}")
                assert f"cellSize: {cell_size}" == "cellSize: Width: 0,9; Height: 0,9"
                print(f"source extent: {layer.get_extent()}")
                assert f"source extent: {layer.get_extent()}" == "source extent: Min (X = -180, Y = -90), Max (X = 180, Y = 90)"
                print(f"target extent: {extent}")
                assert f"target extent: {extent}" == "target extent: Min (X = -159.3, Y = -90), Max (X = 159.3, Y = 59.4)"
                print(f"spatialRefSys: {code}")
                assert code == "4326"
                print(f"bounds: {bounds}")
                assert f"bounds: {bounds}" == "bounds: X: 0; Y: 0; Width: 354; Height: 166;"

    def EditLayerTest(self):
        output = os.path.join(FolderSettings.BaseTestOutputFolder(), "edit_me_out.kml")
        # arrange temp file
        self.create_temp_layer(output)
        out = ""

        # Python doesn't close files quickly
        for i in range(1):
            try:
                with Drivers.kml.edit_layer(output, KmlOptions()) as layer:
                    # add
                    feature_to_add = layer.construct_feature()
                    feature_to_add.set_value("string_field", "new_value")
                    feature_to_add.geometry = Point(5, 5)
                    layer.add(feature_to_add)

                    # update
                    feature_to_replace = layer.construct_feature()
                    feature_to_replace.set_value("string_field", "updated_value")
                    feature_to_replace.geometry = Point(12, 12)
                    layer.replace_at(1, feature_to_replace)

                    # remove
                    layer.remove_at(0)


                    out = ', '.join([str(x.geometry) for x in layer])
                    print(out)
                    assert out == "LINESTRING (0 0, 0 0), LINESTRING (0 0, 1 1), LINESTRING (0 0, 2 2)"
                    break
            except:
                sleep(1)


    def create_temp_layer(self, filepath):
        with Drivers.kml.create_layer(filepath) as layer:
            layer.attributes.add(FeatureAttribute("string_field", AttributeDataType.STRING))

            for i in range(3):
                feature = layer.construct_feature()
                feature.set_value("string_field", f"value_{i}")
                lineString = LineString()
                lineString.add_point(0, 0)
                lineString.add_point(i, i)
                feature.geometry = lineString

                layer.add(feature)

        return True

    def ExtractFeaturesFromShapeFileToGeoJSONTest(self):
        input = os.path.join(FolderSettings.CommonTestFolder(), "InputShapeFile.shp")
        output = os.path.join(FolderSettings.BaseTestOutputFolder(), "ExtractFeaturesFromShapeFileToGeoJSON_out.json")
        reference = os.path.join(FolderSettings.CommonTestFolder(), "ExtractFeaturesFromShapeFileToGeoJSON_out.json")

        # ExStart: ExtractFeaturesFromShapeFileToGeoJSON
        with VectorLayer.open(input, Drivers.shapefile) as input_layer:
            with VectorLayer.create(output, Drivers.geo_json) as output_layer:
                output_layer.copy_attributes(input_layer)
                for input_feature in input_layer:
                    date = datetime.fromisoformat(input_feature.get_value("dob"))
                    if date is None or date < datetime(1982, 1, 1):
                        continue

                    # Construct a new feature
                    output_feature = output_layer.construct_feature()
                    output_feature.geometry = input_feature.geometry
                    output_feature.copy_values(input_feature)
                    output_layer.add(output_feature)

        Comparison.compare_binary_files(output, reference)

    # Created task https://issue.saltov.dynabic.com/issues/GISNET-1749
    # At this moment it's not supported
    def FilterFeaturesByAttributeValueTest(self):
        #input = os.path.join(FolderSettings.CommonTestFolder(), "InputShapeFile.shp")
        # ExStart: FilterFeaturesByAttributeValue

        #res = ""
        #with VectorLayer.open(input, Drivers.shapefile) as layer:
            # all features with the date value in the attribute "dob" later than 1982-01-01.
        #    for feature in layer.where_greater("dob", datetime(1982, 1, 1, 0, 0, 0)):
        #        res = res + str(feature.get_value("dob").date())
        #       print(feature.get_value("dob").date())
        #    assert res == ""
        pass

    def GetFeatureCountInLayerTest(self):
        input = os.path.join(FolderSettings.CommonTestFolder(), "InputShapeFile.shp")
        with VectorLayer.open(input, Drivers.shapefile) as layer:
            print("Total Features in this file: " + str(layer.count))
            assert layer.count == 2

    def GetInformationAboutLayerAttributesTest(self):
        input = os.path.join(FolderSettings.CommonTestFolder(), "InputShapeFile.shp")
        with VectorLayer.open(input, Drivers.shapefile) as layer:
            print(f"The layer has {layer.attributes.count} attributes defined.\n")
            res = ""
            for attribute in layer.attributes:
                print(f"Name: {attribute.name}")
                print(f"Data type: {attribute.data_type}")
                print(f"Can be null: {attribute.can_be_null}")
                res += f"Name: {attribute.name}. Data type: {attribute.data_type}. Can be null: {attribute.can_be_null}."
            print(res)
            assert res == "Name: name. Data type: 8. Can be null: True.Name: age. Data type: 1. Can be null: True.Name: dob. Data type: 8. Can be null: True."

    def GetValueOfAFeatureAttributeTest(self):
        input = os.path.join(FolderSettings.CommonTestFolder(), "InputShapeFile.shp")

        res = ""
        with VectorLayer.open(input, Drivers.shapefile) as layer:
            for i in range(layer.count):
                feature = layer[i]

                # case 1
                name_value = feature.get_value("name")  # attribute name is case-sensitive
                age_value = feature.get_value("age")
                dob_value = datetime.fromisoformat(feature.get_value("dob")).strftime("%Y-%m-%d")
                print(f"Attribute value for feature #{i} is: {name_value}, {age_value}, {dob_value}")
                res += f"{name_value}, {age_value}, {dob_value}"


                # case 2
                obj_name = feature.get_value("name")  # attribute name is case-sensitive
                obj_age = feature.get_value("age")
                obj_dob = feature.get_value("dob")
                print(f"Attribute object for feature #{i} is: {obj_name}, {obj_age}, {obj_dob}")
                res += f"; {obj_name}, {obj_age}, {obj_dob}"

            assert res == "John, 23, 1982-02-05; John, 23, 1982-02-05T16:30:00Mary, 54, 1984-12-15; Mary, 54, 1984-12-15T15:30:00"

    def GetValueOfNullFeatureAttributeTest(self):
        input = os.path.join(FolderSettings.CommonTestFolder(), "InputShapeFile.shp")

        # ExStart: GetValueOfNullFeatureAttribute
        with VectorLayer.open(input, Drivers.shapefile) as layer:
            index = 0
            res = ""
            for feature in layer:
                date = feature.get_value("dob")
                print(f"Feature #{index}")
                print(f"\tAttribute value present: {date is not None}")
                res += f"Feature #{index} "
                if date is not None:
                    print(f"\tAttribute value: {date}")
                    res += f"Attribute value: {date} "
                index += 1

            assert res.strip() == "Feature #0 Attribute value: 1982-02-05T16:30:00 Feature #1 Attribute value: 1984-12-15T15:30:00"
    def GetValueOrDefaultOfFeatureTest(self):
        #os.remove(os.path.join(data_dir, "data1_out.json"))
        #os.remove(os.path.join(data_dir, "data2_out.json"))
        output1 = os.path.join(FolderSettings.BaseTestOutputFolder(), "data1_out.json")

        # You can set default value for a feature of attribute in a layer
        with Drivers.geo_json.create_layer(output1) as layer:
            attribute = FeatureAttribute("attribute", AttributeDataType.INTEGER)
            attribute.can_be_null = True
            attribute.can_be_unset = True

            layer.attributes.add(attribute)

            feature = layer.construct_feature()
            null_value = feature.get_value_or_default("attribute", None)  # value == None
            def_value1 = feature.get_value_or_default("attribute", 10)  # value == 10
            def_value2 = feature.get_value_or_default("attribute", 25)  # value == 10
            print(f"'{null_value}' vs '{def_value1}' vs '{def_value2}'")
            assert f"'{null_value}' vs '{def_value1}' vs '{def_value2}'" == "'None' vs '10' vs '25'"

        output2 = os.path.join(FolderSettings.BaseTestOutputFolder(), "data2_out.json")
        # Another example where we set the default value to 100
        with Drivers.geo_json.create_layer(output2) as layer:
            attribute = FeatureAttribute("attribute", AttributeDataType.DOUBLE)
            attribute.can_be_null = False
            attribute.can_be_unset = False
            attribute.default_value = 100

            layer.attributes.add(attribute)

            feature = layer.construct_feature()
            def_value1 = feature.get_value_or_default("attribute", None)  # value == 100
            def_value2 = feature.get_value_or_default("attribute", None)  # value == 100
            feature.set_value("attribute", 50)
            new_value = feature.get_value_or_default("attribute", None)  # value == 50
            print(f"'{def_value1}' vs '{def_value2}' vs '{new_value}'")

            assert f"'{def_value1}' vs '{def_value2}' vs '{new_value}'" == "'100' vs '100' vs '50.0'"

    def GetValuesOfAFeatureAttributeTest(self):
        input = os.path.join(FolderSettings.CommonTestFolder(), "InputShapeFile.shp")
        res = ""
        with VectorLayer.open(input, Drivers.shapefile) as layer:
            for feature in layer:
                # reads all the attributes into an array.
                all_values = feature.get_values(3, None)
                res = res  + " " + ', '.join([str(x) for x in all_values])
                print(f"res   : {res}")

                # reads several attributes into an array.
                several = feature.get_values(2, None)
                res = res  + " " + ', '.join([str(x) for x in several])
                print(f"several: {res}")

                # reads the attributes as a dump of objects.
                dump = feature.get_values_dump(None)
                res = res + " " + ', '.join([str(x) for x in dump])
                print(f"res   : {res}")
        print(res)
        assert res.strip() == "John, 23, 1982-02-05T16:30:00 John, 23 John, 23, 1982-02-05T16:30:00 Mary, 54, 1984-12-15T15:30:00 Mary, 54 Mary, 54, 1984-12-15T15:30:00"

