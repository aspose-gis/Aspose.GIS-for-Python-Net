import filecmp
from io import BytesIO
from os import listdir
from os.path import isfile, join

from utils.OpenHelper import OpenHelper


class Comparison:

    def compare_binary_files(file1_path, file2_path):
        differences = []
        are_equal = True

        with open(file1_path, 'rb') as file1, open(file2_path, 'rb') as file2:
            position = 0
            byte1 = file1.read(1)
            byte2 = file2.read(1)
            while byte1 or byte2:  # Continue until both files are completely read
                # Read the next byte
                byte1 = file1.read(1)
                byte2 = file2.read(1)
                position += 1
                if byte1 != byte2:
                    are_equal = False
                    differences.append((position, byte1, byte2))


        return are_equal, differences

    def read_file(file_path):
        with open(file_path) as f:
            text = f.read()
            return text

    def SerializeValues(values):
        res = ', '.join([str(x) for x in values])
        return res

    def SerializeLayer(layer):
        i = 0
        result = ""
        a = layer.count
        for feature in layer:
            i += 1
            result = "Feature: " + str(i) + "\n"
            result += "  Geometry: " + feature.geometry.as_text() + " "
            result = result.strip()
            valueCount = feature.count
            all_values = feature.get_values(valueCount, None)
            values_res = values_res + " " + ', '.join([str(x) for x in all_values])
            result += "\n  Values: " + values_res
        return result

    import os
    import filecmp

    def compare_folders(folder1, folder2):
        # List all files in both folders
        files1 = listdir(folder1)
        files2 = listdir(folder2)

        # Check if the number of files is the same
        if len(files1) != len(files2):
            print("Folders have different number of files.")
            return False

        # Create a dictionary to store file comparisons
        comparison_results = {}

        for filename in files1:
            if filename in files2:
                # Compare files only if they exist in both folders
                file1_path = join(folder1, filename)
                file2_path = join(folder2, filename)
                comparison_results[filename] = filecmp.cmp(file1_path, file2_path, shallow=False)
            else:
                print(f"File {filename} is missing in {folder2}.")
                raise f"File {filename} is missing in {folder2}."

        # Check the comparison results
        for filename, are_equal in comparison_results.items():
            if not are_equal:
                print(f"Files {filename} differ in content.")
                raise f"Files {filename} differ in content."

        return True

    def compare_images(self, referenceImage, testingImage):
        if (referenceImage.width != testingImage.width):
            raise Exception("Comparison Error", "Width is different")
        if referenceImage.height != testingImage.height:
            raise Exception("Comparison Error", "Height is different")
        refPixels = referenceImage.load_argb_32_pixels(referenceImage.bounds)
        testPixels = referenceImage.load_argb_32_pixels(referenceImage.bounds)
        if refPixels.length != testPixels.length:
            raise Exception("")
        for i in range(refPixels.length):
            if (refPixels[i] != testPixels[i]):
                raise Exception("Pixel are different", "Issue in pixel number " + i)

    def compare_psd(self, referenceImage, testingImage):
        self.compare_images(referenceImage, testingImage)

        if (referenceImage.layers.length != testingImage.layers.length):
            raise Exception("Count of Layers is different",
                            "Expected " + referenceImage.layers.lenth + ", but was " + testingImage.layers.length)

    @staticmethod
    def compare_as_streams(output_file, reference_file, allowed_diff=0):
        errors = 0
        comparisons = 0
        with open(output_file, "rb", buffering=0) as filestream1:
            output = BytesIO(filestream1.read())
            output.seek(0)
            with open(reference_file, "rb", buffering=0) as filestream2:
                reference = BytesIO(filestream2.read())
                reference.seek(0)

                for x, y in zip(output, reference):
                    comparisons = comparisons + 1
                    if x != y:
                        errors = errors + 1
                        if errors > allowed_diff:
                            raise Exception("Streams has differences. Last mistaken byte is number " + str(comparisons))
                return True

    @staticmethod
    def check_against_ethalon(output_file, reference_file, allowed_diff, allowed_diff_pixels=0):
        compare = Comparison()
        with OpenHelper.open_file_by_path(reference_file) as referenceImage:
            with OpenHelper.open_file_by_path(output_file) as testingImage:
                compare.compare_psd(referenceImage, testingImage)

