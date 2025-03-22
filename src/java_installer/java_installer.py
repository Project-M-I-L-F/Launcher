from .utils import jdk, os, subprocess, re
'''
    JavaChecker - class for checking Java version and installing it if it is not installed.
'''
__author__ = "Igor Co"
__version__ = "1.0.0"

JAVA_VERSION = '17'

class JavaChecker:
    '''
    JavaChecker - class for checking Java version and installing it if it is not installed.

    Methods:
    __init__ - constructor of the class, checks Java version and installs it if it is not installed.
    jdk_installer - installs Java Development Kit 17.
    __java_check - checks Java version and installs it if it is not installed.
    __jdk_location_by_java_pror - gets Java home directory from Java properties.
    __jdk_location - gets Java home directory from JAVA_HOME environment variable or from Java properties.
    __jdk_version_check - checks Java version.
    __jdk_check_is_version_avaible - checks if Java version is 8.0 or higher.
    __str__ - returns string representation of the class.

    Attributes:
    __home - Java home directory.
    __installed - True if Java is installed, False otherwise.
    __version - Java version.

    Usage:
    java_checker = JavaChecker()
    
'''
    __home = "C:/Java"
    __installed = False
    __version = None

    def __init__(self):
        """
            Constructor of the class, checks Java version and installs it if it is not installed.
        """
        self.__java_check()
        print(self.__jdk_location_by_java_pror())


    def jdk_installer(self):
        """
            Installs Java Development Kit 17.
        """
        jdk.install(JAVA_VERSION, path=self.__home)

    def __java_check(self):
        """
            Checks Java version and installs it if it is not installed.
        """
        self.__jdk_location()
        self.__jdk_check_is_version_avaible()

        print(self)

    def __jdk_location_by_java_pror(self):
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

    def __jdk_location(self):
        """
            Gets Java home directory from JAVA_HOME environment variable or from Java properties.
        
            Returns:
            Java home directory.
        """
        java_home = os.getenv('JAVA_HOME')

        if java_home not in [None, "", " "]:
            self.__home = java_home
            self.__installed = True

        elif self.__jdk_location_by_java_pror() is not None:
            self.__home = self.__jdk_location_by_java_pror()
            self.__installed = True
        else:
            self.__home = "C:/Java"
            self.__installed = False
            self.jdk_installer()
            self.__jdk_location()
        return self.__home

    def __jdk_version_check(self):
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
        self.__jdk_version_check()
        return self.__version >= 8.0

    def __str__(self):
        """
            Returns string representation of the class.
        """
        return f"Java version: {self.__version}, Java home: {self.__home}"

if __name__ == "__main__":
    java_checker = JavaChecker()
