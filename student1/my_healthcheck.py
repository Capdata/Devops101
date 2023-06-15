"""
# @(#) =======================================================================================================
# @(#) Source : my_healthcheck.py
# @(#) Aut    : dbaffaleuf@capdata-osmozium.com
# @(#) Crdate : 2023/06/07
# @(#) Object : sample python health checker for MySQL for DEVOPS101 training purposes
# @(#)
# @(#) Revision
# @(#) -------------------------------------------------------------------------------------------------------
# @(#) 2023/06/07       1.0         dbaffaleuf         Creation
# @(#) -------------------------------------------------------------------------------------------------------
"""

# PRIVATE IMPORTS -----------------------------------------------------------------------------------------------
from my.myconnect import alldbmyconnection
from my.myGetVersion import  myGetVersion

# BUILTIN IMPORTS -----------------------------------------------------------------------------------------------
import sys, getopt, re, string, os.path

# --------------------------------------------------------------------------------------------------------------
# FUNCTION usage()
def usage():
    print "# ================================================================================================== \n" \
        " my_healthcheck.py \n" \
        " Object : connects to MySQL and checks instance health \n" \
        " \n" \
        " -h / --help       : help & usage\n" \
        " -c / --configfile \n" \
          " \n"     \
        "Example : python3 my_healthcheck.py --configfile=/full/path/to/my/cs.xml"
    print "# -------------------------------------------------------------------------------------------------- \n" \

    sys.exit(3)


#  -------------------------------------------------------------------------------------------------------------
# FUNCTION main()
def main():

    rootdirectory=os.path.dirname(os.path.abspath(__file__))
    secretfile=rootdirectory+"/my/cs.xml"

    """ARGV -------------------------------------------------------------------------------------------------------------------"""
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "hc:", ["help", "configfile"])
        for opt, arg in optlist:
            if opt in ("-h","--help"):
                usage()
            elif opt in ("-c", "--configfile"):
                secretfile = arg

    except getopt.GetoptError as err:
        print str(err)
        usage()
    
    if secretfile == "":
        usage()

    mydbconn = alldbmyconnection(secretfile)
    myGetVersion = myGetVersion()
    myGetVersionRes = mydbconn.runquery(myGetVersion.myGetVersionSQL)

    for row in myGetVersionRes:
        try:
            myversion = row['myversion']
            print "Version detectee : " + myversion

         except BaseException as err:
            print err.message
    return

#  -------------------------------------------------------------------------------------------------------------
# Entry Point

if __name__ == "__main__":
    main()
