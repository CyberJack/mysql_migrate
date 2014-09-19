#!/usr/bin/env python3

# Imports
import subprocess, sys, re, os

# Configuration
# Replace the path of the mysql executable and set the root username/password
mysql = {
    "cmd": "/usr/bin/mysql",
    "username": "root",
    "password": ""
}

# Settings
__prog__ = "MySQL Migrate"
__version__ = "0.1a"

class migrate:
    users = {}
    rights = []
    databases = []

    def __init__( self ):
        errors = []
        if self.is_exe( mysql["cmd"] ) == False:
            errors.append("MySQL executable not found or not executable")
        if "" == mysql["username"]:
            errors.append("Username must not be empty")
        if len(errors) > 0:
            print("The following errors occured:")
            for e in errors:
                print(" - %s" % e)
            print("\nAdjust these settings in the configuration section of the script.\n")
            sys.exit(1)
        else:
            self.get_users()
            self.get_databases()

    def is_exe( self, fpath ):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    def run_process( self, command ):
        p = subprocess.Popen( command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True )
        out, err = p.communicate()

        # Convert to normal text
        out = str( out, encoding='utf8' )
        err = str( err, encoding='utf8' )

        # Catch an error
        #if '' != err:
        #    raise Exception( err )
        return out

    def get_users( self ):
        print( "Gathering user information:", end="" )
        self.users = {}
        if mysql["password"] == "":
            cmd = "%s -u %s -s --skip-column-names -e \"SELECT concat(user,'|',host) FROM user\" mysql" % (mysql["cmd"], mysql["username"])
        else:
            cmd = "%s -u %s -p%s -s --skip-column-names -e \"SELECT concat(user,'|',host) FROM user\" mysql" % (mysql["cmd"], mysql["username"], mysql["password"])
        users = self.run_process( cmd ).split("\n")
        for line in users:
            # No empty lines
            if '' != line.strip():
                line = line.split('|')
                if "root" != line[0]:
                    # Add new username
                    if line[0] not in self.users:
                        self.users[ line[0] ] = []
                    # Append database
                    self.users[ line[0] ].append( line[1] )
        print(" done")

    def get_databases( self ):
        if 0 < len( self.users ):
            print( "Gathering rights and database information:", end="" )
            self.rights = []
            self.databases = []
            re_getdb = re.compile( r'grant(.*?)privileges on `(.*?)`', re.IGNORECASE )

            for user in self.users:
                for host in self.users[ user ]:
                    # Get rights
                    if mysql["password"] == "":
                        cmd = "%s -u %s -s --skip-column-names -e \"SHOW GRANTS FOR '%s'@'%s'\"" % (mysql["cmd"], mysql["username"], user, host)
                    else:
                        cmd = "%s -u %s -p%s -s --skip-column-names -e \"SHOW GRANTS FOR '%s'@'%s'\"" % (mysql["cmd"], mysql["username"], mysql["password"], user, host)
                    rights = self.run_process( cmd ).split("\n")

                    for line in rights:
                        line = line.strip()
                        if '' != line:
                            # Add the rights line
                            self.rights.append( '%s;' % line.replace("\\", "") )
                            #print( line )

                            # Check for database
                            for match in re_getdb.finditer( line.strip() ):
                                db = match.group(2).strip()
                                if db not in self.databases:
                                    self.databases.append( db.replace("\\", "") )
            print(" done")

    def overview( self ):
        print( "\nMigrate the following databases:" )
        for db in sorted(self.databases):
            print( "  %s" % db )

        print("\nMigrate the users with the following sql queries:")
        for line in self.rights:
            print( "  %s" % line )

        print("")


if "__main__" == __name__:
    print("%s = %s\n" % (__prog__, __version__));
    try:
        m = migrate()
        m.overview()
    except Exception as error:
        print( 'Error: %s' % error )
        sys.exit(1)
