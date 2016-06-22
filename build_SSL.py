#-------------------------------------------------------------------------------
# Name:        模块1
# Purpose:
#
# Author:      1
#
# Created:     25/02/2016
# Copyright:   (c) 1 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from werkzeug.serving import make_ssl_devcert

make_ssl_devcert('./', host='localhost')
('./key.crt', './key.key')