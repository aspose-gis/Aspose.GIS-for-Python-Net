import os

import pytest
from aspose.gis import License

from utils.BaseTests import BaseTests
from utils.FolderSettings import FolderSettings
from utils.LicenseHelper import LicenseHelper

class License_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        pass

    def ExceptionOnIncorrectLicenseTest(self):
        pass
        #LicenseHelper.remove_license()
        #wasError = False
        #try:
        #    license = License()
        #    licenseFolder = FolderSettings.BaseLicenseFolder()
        #    licensePath = os.path.join(licenseFolder, licenseName)
        #    license.set_license(licensePath)
        #except Exception:
        #    wasError = True

        #if not wasError:
        #    raise Exception("Incorrect License was applied successfully, but must not : " + licenseName)

    def CorrectLicenseShouldBeAppliedTest(self):
        pass
        #try:
        #    license = License()
        #    licenseFolder = FolderSettings.BaseLicenseFolder()
        #    licensePath = os.path.join(licenseFolder, licenseName)
        #    license.set_license(licensePath)
        #except Exception:
        #    raise Exception("Correct License was not applied successfully, but must be: " + licenseName)
