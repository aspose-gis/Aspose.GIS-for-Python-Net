import os
from zipfile import ZipFile

import pytest

import inspect

from utils.FolderSettings import FolderSettings
from utils.LicenseHelper import LicenseHelper


class BaseTests:
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    unzipped_files = []

    def get_file_with_respect_to_archives(self, file_path):
        if os.path.exists(file_path):
            return file_path

        file_name = os.path.basename(file_path)
        zip_file_path = os.path.splitext(file_path)[0] + ".zip"

        if os.path.exists(zip_file_path):
            with ZipFile(zip_file_path, 'r') as zip_file:
                if file_name in zip_file.namelist():
                    extracted_file_path = os.path.join(os.path.dirname(file_path), file_name)
                    zip_file.extract(file_name, path=os.path.dirname(file_path))
                    self.unzipped_files.append(file_path)
                    return extracted_file_path

        return None

    def remove_all_unzipped_files(self):
        for item in self.unzipped_files:
            if (os.path.exists(item)):
                os.remove(item)

    def GetFileInBaseFolderByIssue(self, issueFolder, fileName):
        baseFolder = FolderSettings.BaseTestFolder()
        finalPath = os.path.join(baseFolder, issueFolder, fileName)
        finalPath = self.get_file_with_respect_to_archives(finalPath)
        return finalPath

    def GetFileInOutputFolderByIssue(self, issueFolder, fileName):
        outputFolder = FolderSettings.BaseTestOutputFolder()
        fullOutputFolder = os.path.join(outputFolder, issueFolder)
        FolderSettings.create_folder_if_not_exists(fullOutputFolder)
        outputPath = os.path.join(outputFolder, issueFolder, fileName)

        return outputPath

    def GetFileInBaseFolder(self, fileName):
        testName = inspect.stack()[1][3]
        issueFolder = FolderSettings.GetFolderNameFromTestName(testName)
        finalPath = self.GetFileInBaseFolderByIssue(issueFolder, fileName)
        return finalPath

    def GetFileInOutputFolder(self, fileName):
        testName = inspect.stack()[2][4][0]
        issueFolder = FolderSettings.GetFolderNameFromTestName(testName)
        outputPath = self.GetFileInOutputFolderByIssue(issueFolder, fileName)

        return outputPath



    # Runs all methods of class that end with "Test"
    def RunAllTests(self):
        example = self.__class__()
        attrs = (getattr(example, name) for name in dir(example))

        for method in attrs:
            try:
                if hasattr(method, '__name__'):
                    if (method.__name__.endswith("Test")):
                        example.exampleMode = True
                        example.exampleMethod = "Tests." + method.__name__ + "()"
                        method()
            except TypeError:
                # Can't handle methods with required arguments.
                raise