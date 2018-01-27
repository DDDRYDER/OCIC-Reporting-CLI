#
# operations.py - OCIC Operations
#
# coding: utf-8
# Copyright (c) 2016, 2018, Oracle and/or its affiliates. All rights reserved.
#
# Maintainer: David Ryder
#
import requests
import json

class Operations:
    def __init__(self):
        self.s = None # Session
        self.shapes = None
        self.auth = None
        self.valid = False

    def authenticate( self, config, show=False ):
        self.auth = config['AUTHENTICATE']
        self.s = requests.Session()
        headers = { "content-type": "application/oracle-compute-v3+json" } # OCIC-IAAS
        data = { "user": "/{container}/{user}".format( container=self.auth['container'], user=self.auth['user'] ),"password": self.auth['password'] }
        uri = "https://{host}/authenticate/".format( host=self.auth['iaasHost'] )
        r = self.s.post( uri, data=json.dumps( data ), headers=headers )
        if show:
                print( uri, data, headers, r.text )
                print( "status code: ", r.status_code )
        if r.status_code == 204:
            self.valid = True
        else:
            print( "Authentication failed" )
            self.valid = False

    def session(self):
        return self.auth

    def getShapes(self, show=False):
        r = self.s.get( "https://{host}/shape/".format( host=self.auth['iaasHost'] ) )
        s = json.loads( r.text )['result'] # list of shapes
        self.shapes = { i['name']: { 'ram': i['ram'], 'ocpus': i['cpus'] / 2, 'cpus': i['cpus'] } for i in s }
        if show:
            for i in sorted( self.shapes.keys() ):
                print( ", ".join( map( str, [ i, self.shapes[i]['ocpus'], self.shapes[i]['ram'] ] ) ) )
        return s

    def shapeDetails(self, shape ):
        return self.shapes[ shape ]

    def storageVolume(self):
        r = self.s.get( "https://{host}/storage/volume/{container}/{user}/".format( host=self.auth['iaasHost'], container=self.auth['container'], user=self.auth['user']) )
        return json.loads( r.text )

    def databaseInstance(self):
        headers = { "X-ID-TENANT-NAME": self.auth['identityDomain'] } # OCIC-PAAS
        params = { 'outputLevel': 'verbose' } # all dbaas details
        uri = "https://{host}/paas/service/dbcs/api/v1.1/instances/{iddom}".format( host=self.auth['paasHost'], iddom=self.auth['identityDomain'] )
        r = self.s.get( uri, auth = ( self.auth['user'], self.auth['password'] ), headers=headers, params=params )
        print( "status code: ", r.status_code )
        if r.status_code != 200:
            print( "Authentication failed" )
            print( uri )
        return json.loads( r.text )

    def computeInstance(self):
        r = self.s.get( "https://{host}/instance/{container}/{user}/".format( host=self.auth['iaasHost'], container=self.auth['container'], user=self.auth['user']) )
        return json.loads( r.text )

    def computeDeleteInstance(self, name):
        uri = "https://{host}/instance{name}".format( host=self.auth['iaasHost'], name=name)
        print( uri )
        r = self.s.delete( uri )
        print( r.text )

    def storageVolumeDetails( self, volName ):
        r = self.s.get( "https://{host}/storage/volume{volName}".format( host=self.auth['iaasHost'], container=self.auth['container'], user=self.auth['user'], volName=volName) )
        return json.loads( r.text )

    def totalStorageAttached( self, storageAttachment ):
        return sum( [ int( self.storageVolumeDetails( i['storage_volume_name'] )['size'] ) for i in storageAttachment if 'storage_volume_name' in i.keys() ] )

    def logout(self):
        return self.valid
