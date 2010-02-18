##########################################################################
#
#  Copyright (c) 2010, Image Engine Design Inc. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#     * Neither the name of Image Engine Design nor the names of any
#       other contributors to this software may be used to endorse or
#       promote products derived from this software without specific prior
#       written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##########################################################################

import re

import IECore

class IDXReader( IECore.Reader ) :

	def __init__( self, fileName=None ) :
	
		IECore.Reader.__init__(
			self,
			"Reads Leica Geosystems IDX files"
		)

		if fileName is not None :
			self["fileName"].setTypedValue( fileName )

	@staticmethod
	def canRead( fileName ) :
	
		try :
			f = open( fileName, "r" )
			return f.read( 6 )=="HEADER"
		except :
			return False
		
	def doOperation( self, args ) :
	
		f = open( args["fileName"].value, "r" )
		
		l = "".join( f.readlines() )
			
		dbMatch = re.search( "^DATABASE(.*)END DATABASE", l, re.MULTILINE | re.DOTALL )
		if dbMatch is None :
			raise RunTimeError( "Unable to find database block in file \"%s\"" % args["fileName"].value )
		
		pointsMatch = re.search( "POINTS\(([^)]*)\)(.*)END POINTS", dbMatch.group( 1 ), re.MULTILINE | re.DOTALL )
		if pointsMatch is None :
			raise RunTimeError( "Unable to find points block in file \"%s\"" % args["fileName"].value )

		columnNames = [ x.strip() for x in pointsMatch.group( 1 ).split( "," ) ]
		numColumns = len( columnNames )
		
		try :
			eastIndex = columnNames.index( "East" )
			northIndex = columnNames.index( "North" )
			elevationIndex = columnNames.index( "Elevation" )
			pointIDIndex = columnNames.index( "PointID" )
			classIndex = columnNames.index( "CLASS" )
		except ValueError :
			raise RunTimeError( "Unable to find column labels in file \"%s\"" % args["fileName"].value )
		
		p = IECore.V3fVectorData()
		ids = IECore.StringVectorData()
			
		rows = pointsMatch.group( 2 ).split( "\n" )
		for row in rows :
		
			columns = [ x.strip( " \t\r;\"\'" ) for x in row.split( "," ) ]
			if len( columns ) != numColumns :
				continue
				
			if columns[classIndex] != "MEAS" :
				continue
				
			try :
				x = float( columns[eastIndex] )
				y = float( columns[elevationIndex] )
				z = float( columns[northIndex] )
			except ValueError :
				# some rows seem to have missing data - not much we can do about that
				continue
			
			p.append( IECore.V3f( x, y, z ) )
			ids.append( columns[pointIDIndex] )
				
		result = IECore.PointsPrimitive( p )
		result["PointID"] = IECore.PrimitiveVariable( IECore.PrimitiveVariable.Interpolation.Vertex, ids )
		
		return result
		
IECore.registerRunTimeTyped( IDXReader, 100028, IECore.Reader )
IECore.Reader.registerReader( "idx", IDXReader.canRead, IDXReader, IDXReader.staticTypeId() )
