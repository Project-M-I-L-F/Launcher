'''
    JavaChecker - class for checking Java version and installing it if it is not installed.
'''
__author__ = "Igor Co"
__version__ = "1.0.0"

#Base imports
import os
import subprocess
import re
#Custom imports
import jdk

JAVA_VERSION = '17'
DEFAULT_JAVA_HOME = 'C:/Java'

class JavaChecker:
    '''
    JavaChecker - class for checking Java version and installing it if it is not installed.

    Methods:
    __init__ - constructor of the class, checks Java version and installs it if it is not installed.
    jdk_installer - installs Java Development Kit 17.
    __check_java - checks Java version and installs it if it is not installed.
    __location_jdk_by_java_pror - gets Java home directory from Java properties.
    __location_jdk - gets Java home directory from JAVA_HOME environment variable or from Java properties.
    __check_version_jdk - checks Java version.
    __jdk_check_is_version_avaible - checks if Java version is 8.0 or higher.
    __str__ - returns string representation of the class.

    Attributes:
    __home - Java home directory.
    __installed - True if Java is installed, False otherwise.
    __version - Java version.

    Usage:
    java_checker = JavaChecker()
    
'''
    __home = None
    __set_location_if_not_found = DEFAULT_JAVA_HOME
    __installed = False
    __version = None
    __version_if_not_found = JAVA_VERSION

    def __init__(self, reserved_location: str = DEFAULT_JAVA_HOME, reserved_version: int = JAVA_VERSION):
        """
            Constructor of the class, checks Java version and installs it if it is not installed.
        """
        self.__set_location_if_not_found = reserved_location
        self.__version_if_not_found = reserved_version
        self.__check_java()
        self.__location_jdk_by_java_pror()

    def jdk_status(self):
        """
            Returns Java Development Kit status.
        """
        self.__update_data_jdk()
        return self.__installed

    def set_location(self, location: str):
        """
            Sets reserved location for JDK.
        """
        self.__set_location_if_not_found = location
        self.__update_data_jdk()

    def get_location(self):
        """
            Returns Java home directory.
        """
        self.__location_jdk()
        return self.__home

    def install(self):
        """
            Installs Java Development Kit 17.
        """
        if not self.__installed:
            self.__install_jdk()
    
    def ignore_install(self):
        """
            Ignores Java Development Kit installation.
        """
        self.__install_jdk()

#Private methods
    #Private methods
    def __install_jdk(self):
        """
            Installs Java Development Kit 17.
        """
        jdk.install(self.__version_if_not_found, path=self.__set_location_if_not_found)
        self.__update_data_jdk()
        
        new_path = self.__set_location_if_not_found.replace("/", "\\")
        all_elem = os.listdir(self.__set_location_if_not_found)
        fol = [i for i in all_elem if os.path.isdir(os.path.join(self.__set_location_if_not_found, i))]
        if fol[0] is not None:
            new_path += "\\"+fol[0]
        os.system(f'setx JAVA_HOME "{new_path}"')

    def __update_data_jdk(self):
        """
            Updates Java Development Kit data.
        """
        self.__location_jdk()
        self.__jdk_check_is_version_avaible()

        self.__installed = self.__home and self.__version is not None

    def __check_java(self):
        """
            Checks Java version and installs it if it is not installed.
        """
        self.__location_jdk()
        self.__jdk_check_is_version_avaible()

        print(self)

    def __location_jdk_by_java_pror(self):
        """
            Gets Java home directory from Java properties.'
        
            Returns:
            Java home directory.
        """
        try:
            result = subprocess.run(
                ['java', '-XshowSettings:properties', '-version'],
                capture_output=True,
                text=True,
                check=True
                )

            if result.returncode == 0:
                java_home_match = re.search(r'java.home = (.+)', result.stderr)
                self.__home = java_home_match.group(1)
                self.__installed = True
            else:
                self.__home = None
                self.__installed = False
            return self.__home
        except subprocess.CalledProcessError:
            return None

    def __location_jdk(self):
        """
            Gets Java home directory from JAVA_HOME environment variable or from Java properties.
        
            Returns:
            Java home directory.
        """
        java_home = os.getenv('JAVA_HOME')

        if java_home not in [None, "", " "]:
            self.__home = java_home
            self.__installed = True

        elif self.__location_jdk_by_java_pror() is not None:
            self.__home = self.__location_jdk_by_java_pror()
            self.__installed = True
        else:
            self.__home = None
            self.__installed = False
            self.__install_jdk()
            self.__location_jdk()
        return self.__home

    def __check_version_jdk(self):
        """
            Checks Java version.

            Returns:
            True if Java version is 8.0 or higher, False otherwise.
        """
        result = subprocess.run(
            ['java', '-version'],
            capture_output=True,
            text=True,
            check=True
            )

        if result.returncode == 0:
            version_match = re.search(r'(\d+\.\d+)', result.stderr)
            self.__version = float(version_match.group(1))
            self.__installed = True
        else:
            self.__version = None
            self.__installed = False
        return self.__installed

    def __jdk_check_is_version_avaible(self):
        """
            Checks if Java version is 8.0 or higher.

            Returns:
            True if Java version is 8.0 or higher, False otherwise.
        """
        self.__check_version_jdk()
        return self.__version >= 8.0

    def __str__(self):
        """
            Returns string representation of the class.
        """
        return f"Java version: {self.__version}, Java home: {self.__home}"
