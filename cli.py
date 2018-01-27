#
# cli.py - CLI for OCIC Operations
#
# coding: utf-8
# Copyright (c) 2016, 2018, Oracle and/or its affiliates. All rights reserved.
#
# Maintainer: David Ryder
#
import os
import sys
import configparser
from operations import Operations

# Arguments
#
# python ocic-cli.py <config-file> <cmd>
#
nArgs = len(sys.argv)
if nArgs >= 3:
    configFile = sys.argv[1]
    cmd = sys.argv[2]
    config = configparser.ConfigParser()
    config.read( configFile )
else:
    cmd = "help"

if cmd == "auth":
    o = Operations()
    o.authenticate( config, show=True )
    print( o.auth )

elif cmd == "database":
    o = Operations()
    o.authenticate( config )
    r = o.databaseInstance()
    for i in r['services']:
        out = ", ".join( map( str, [ i['service_name'], i['version'], i['current_version'], i['dbUsableStorage'],
                           i['status'], i['sid'], i['created_by'], i['num_nodes'], i['edition'], i['shape'], i['rac_database'] ] ) )
        print( out )

elif cmd == "shapes":
    o = Operations()
    o.authenticate( config )
    o.getShapes(show=True)

elif cmd == "storage":
    o = Operations()
    o.authenticate( config )
    r = o.storageVolume()
    totals = { 'storage': 0, 'ocpus': 0, 'instances': 0 }
    for i in r['result']:
        out = ", ".join( map( str, [ i['name'], i['size'], i['status'] ] ) )
        totals['storage'] += int( i['size'] )
        totals['instances'] += 1
        print( out )
    print( ", ".join( map( str, [ totals['instances'], totals['storage'] ] ) ) )

elif cmd == "compute":
    o = Operations()
    o.authenticate( config )
    o.getShapes()
    r = o.computeInstance()
    totals = { 'storage': 0, 'ocpus': 0, 'instances': 0 }
    for i in r['result']:
        shape = o.shapeDetails( i['shape'] )
        instanceStor = o.totalStorageAttached( i['storage_attachments'] )
        totals['storage'] += instanceStor
        totals['ocpus'] += shape['ocpus']
        totals['instances'] += 1
        print( ", ".join( map( str, [ i['hostname'], i['shape'], shape['ocpus'], shape['ram'], instanceStor, i['name'] ] ) ) )
    print( ", ".join( map( str, [ totals['instances'], totals['ocpus'], totals['storage'] ] ) ) )

elif cmd == "deleteCompute":
    instanceName = sys.argv[2]
    o = Operations()
    o.authenticate( config )
    o.getShapes()
    r = o.computeDeleteInstance( instanceName )
    print( r)

else:
    print( "Usage: python ocic-cli.py <config-file> <cmd>" )
    print( "Commands: auth, compute, database, storage, shapes" )
#
# END
#
