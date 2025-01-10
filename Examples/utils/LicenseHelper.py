import os.path
from aspose.gis import License, Metered

from utils.FolderSettings import FolderSettings


class LicenseHelper:

    isLicensed = False

    @staticmethod
    def is_licensed():
        return LicenseHelper.isLicensed

    @staticmethod
    def set_license():
        if LicenseHelper.is_licensed():
            return
        license = License()
        licenseFolder = FolderSettings.BaseLicenseFolder()
        licensePath = os.path.join(licenseFolder, "Aspose.GIS.Python.via.NET.lic")
        license.set_license(licensePath)
        LicenseHelper.isLicensed = True

    @staticmethod
    def remove_license():
        if not LicenseHelper.is_licensed():
            return
        license = License()
        license.set_license("")
        LicenseHelper.isLicensed = False

        metered = Metered()
        metered.set_metered_key("000", "000")
