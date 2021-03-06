##########################################################################
#
#  Copyright (c) 2010-2015, Image Engine Design Inc. All rights reserved.
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

import hou
import imath
import IECore
import IECoreScene
import IECoreHoudini
import unittest
import os, shutil
import random

class TestToHoudiniGroupConverter( IECoreHoudini.TestCase ) :

	if hou.applicationVersion()[0] >= 16:
		PointPositionAttribs = ['P']
	else:
		PointPositionAttribs = ['P', 'Pw']

	__testOTL = "test/IECoreHoudini/data/otls/testHDAs.otl"
	__testOTLBackups = os.path.join( os.path.dirname( __testOTL ), "backup" )
	__testOTLCopy = os.path.join( __testOTLBackups, os.path.basename( __testOTL ) )

	def points( self ) :
		pData = IECore.V3fVectorData( [
			imath.V3f( 0, 1, 2 ), imath.V3f( 1 ), imath.V3f( 2 ), imath.V3f( 3 ),
			imath.V3f( 4 ), imath.V3f( 5 ), imath.V3f( 6 ), imath.V3f( 7 ),
			imath.V3f( 8 ), imath.V3f( 9 ), imath.V3f( 10 ), imath.V3f( 11 ),
		] )

		points = IECoreScene.PointsPrimitive( pData )

		floatData = IECore.FloatData( 1.5 )
		v2fData = IECore.V2fData( imath.V2f( 1.5, 2.5 ) )
		v3fData = IECore.V3fData( imath.V3f( 1.5, 2.5, 3.5 ) )
		color3fData = IECore.Color3fData( imath.Color3f( 1.5, 2.5, 3.5 ) )
		intData = IECore.IntData( 1 )
		v2iData = IECore.V2iData( imath.V2i( 1, 2 ) )
		v3iData = IECore.V3iData( imath.V3i( 1, 2, 3 ) )
		stringData = IECore.StringData( "this is a string" )

		intRange = range( 1, 13 )
		floatVectorData = IECore.FloatVectorData( [ x+0.5 for x in intRange ] )
		v2fVectorData = IECore.V2fVectorData( [ imath.V2f( x, x+0.5 ) for x in intRange ] )
		v3fVectorData = IECore.V3fVectorData( [ imath.V3f( x, x+0.5, x+0.75 ) for x in intRange ] )
		color3fVectorData = IECore.Color3fVectorData( [ imath.Color3f( x, x+0.5, x+0.75 ) for x in intRange ] )
		intVectorData = IECore.IntVectorData( intRange )
		v2iVectorData = IECore.V2iVectorData( [ imath.V2i( x, -x ) for x in intRange ] )
		v3iVectorData = IECore.V3iVectorData( [ imath.V3i( x, -x, x*2 ) for x in intRange ] )
		stringVectorData = IECore.StringVectorData( [ "string number %d!" % x for x in intRange ] )

		detailInterpolation = IECoreScene.PrimitiveVariable.Interpolation.Constant
		pointInterpolation = IECoreScene.PrimitiveVariable.Interpolation.Vertex

		# add all valid detail attrib types
		points["floatDetail"] = IECoreScene.PrimitiveVariable( detailInterpolation, floatData )
		points["v2fDetail"] = IECoreScene.PrimitiveVariable( detailInterpolation, v2fData )
		points["v3fDetail"] = IECoreScene.PrimitiveVariable( detailInterpolation, v3fData )
		points["color3fDetail"] = IECoreScene.PrimitiveVariable( detailInterpolation, color3fData )
		points["intDetail"] = IECoreScene.PrimitiveVariable( detailInterpolation, intData )
		points["v2iDetail"] = IECoreScene.PrimitiveVariable( detailInterpolation, v2iData )
		points["v3iDetail"] = IECoreScene.PrimitiveVariable( detailInterpolation, v3iData )
		points["stringDetail"] = IECoreScene.PrimitiveVariable( detailInterpolation, stringData )

		# add all valid point attrib types
		points["floatPoint"] = IECoreScene.PrimitiveVariable( pointInterpolation, floatVectorData )
		points["v2fPoint"] = IECoreScene.PrimitiveVariable( pointInterpolation, v2fVectorData )
		points["v3fPoint"] = IECoreScene.PrimitiveVariable( pointInterpolation, v3fVectorData )
		points["color3fPoint"] = IECoreScene.PrimitiveVariable( pointInterpolation, color3fVectorData )
		points["intPoint"] = IECoreScene.PrimitiveVariable( pointInterpolation, intVectorData )
		points["v2iPoint"] = IECoreScene.PrimitiveVariable( pointInterpolation, v2iVectorData )
		points["v3iPoint"] = IECoreScene.PrimitiveVariable( pointInterpolation, v3iVectorData )
		points["stringPoint"] = IECoreScene.PrimitiveVariable( pointInterpolation, stringVectorData, IECore.IntVectorData( range( 0, 12 ) ) )

		points.blindData()['name'] = "pointsGroup"

		return points

	def mesh( self ) :
		vertsPerFace = IECore.IntVectorData( [ 4, 4, 4, 4, 4, 4 ] )
		vertexIds = IECore.IntVectorData( [ 1, 5, 4, 0, 2, 6, 5, 1, 3, 7, 6, 2, 0, 4, 7, 3, 2, 1, 0, 3, 5, 6, 7, 4 ] )
		mesh = IECoreScene.MeshPrimitive( vertsPerFace, vertexIds )

		floatData = IECore.FloatData( 1.5 )
		v2fData = IECore.V2fData( imath.V2f( 1.5, 2.5 ) )
		v3fData = IECore.V3fData( imath.V3f( 1.5, 2.5, 3.5 ) )
		color3fData = IECore.Color3fData( imath.Color3f( 1.5, 2.5, 3.5 ) )
		intData = IECore.IntData( 1 )
		v2iData = IECore.V2iData( imath.V2i( 1, 2 ) )
		v3iData = IECore.V3iData( imath.V3i( 1, 2, 3 ) )
		stringData = IECore.StringData( "this is a string" )

		intRange = range( 1, 25 )
		floatVectorData = IECore.FloatVectorData( [ x+0.5 for x in intRange ] )
		v2fVectorData = IECore.V2fVectorData( [ imath.V2f( x, x+0.5 ) for x in intRange ] )
		v3fVectorData = IECore.V3fVectorData( [ imath.V3f( x, x+0.5, x+0.75 ) for x in intRange ] )
		color3fVectorData = IECore.Color3fVectorData( [ imath.Color3f( x, x+0.5, x+0.75 ) for x in intRange ] )
		intVectorData = IECore.IntVectorData( intRange )
		v2iVectorData = IECore.V2iVectorData( [ imath.V2i( x, -x ) for x in intRange ] )
		v3iVectorData = IECore.V3iVectorData( [ imath.V3i( x, -x, x*2 ) for x in intRange ] )
		stringVectorData = IECore.StringVectorData( [ "string number %d!" % x for x in intRange ] )

		detailInterpolation = IECoreScene.PrimitiveVariable.Interpolation.Constant
		pointInterpolation = IECoreScene.PrimitiveVariable.Interpolation.Vertex
		primitiveInterpolation = IECoreScene.PrimitiveVariable.Interpolation.Uniform
		vertexInterpolation = IECoreScene.PrimitiveVariable.Interpolation.FaceVarying

		# add all valid detail attrib types
		mesh["floatDetail"] = IECoreScene.PrimitiveVariable( detailInterpolation, floatData )
		mesh["v2fDetail"] = IECoreScene.PrimitiveVariable( detailInterpolation, v2fData )
		mesh["v3fDetail"] = IECoreScene.PrimitiveVariable( detailInterpolation, v3fData )
		mesh["color3fDetail"] = IECoreScene.PrimitiveVariable( detailInterpolation, color3fData )
		mesh["intDetail"] = IECoreScene.PrimitiveVariable( detailInterpolation, intData )
		mesh["v2iDetail"] = IECoreScene.PrimitiveVariable( detailInterpolation, v2iData )
		mesh["v3iDetail"] = IECoreScene.PrimitiveVariable( detailInterpolation, v3iData )
		mesh["stringDetail"] = IECoreScene.PrimitiveVariable( detailInterpolation, stringData )

		# add all valid point attrib types
		pData = IECore.V3fVectorData( [
			imath.V3f( 0, 1, 2 ), imath.V3f( 1 ), imath.V3f( 2 ), imath.V3f( 3 ),
			imath.V3f( 4 ), imath.V3f( 5 ), imath.V3f( 6 ), imath.V3f( 7 ),
		], IECore.GeometricData.Interpretation.Point )
		mesh["P"] = IECoreScene.PrimitiveVariable( pointInterpolation, pData )
		mesh["floatPoint"] = IECoreScene.PrimitiveVariable( pointInterpolation, floatVectorData[:8] )
		mesh["v2fPoint"] = IECoreScene.PrimitiveVariable( pointInterpolation, v2fVectorData[:8] )
		mesh["v3fPoint"] = IECoreScene.PrimitiveVariable( pointInterpolation, v3fVectorData[:8] )
		mesh["color3fPoint"] = IECoreScene.PrimitiveVariable( pointInterpolation, color3fVectorData[:8] )
		mesh["intPoint"] = IECoreScene.PrimitiveVariable( pointInterpolation, intVectorData[:8] )
		mesh["v2iPoint"] = IECoreScene.PrimitiveVariable( pointInterpolation, v2iVectorData[:8] )
		mesh["v3iPoint"] = IECoreScene.PrimitiveVariable( pointInterpolation, v3iVectorData[:8] )
		mesh["stringPoint"] = IECoreScene.PrimitiveVariable( pointInterpolation, stringVectorData[:8], IECore.IntVectorData( range( 0, 8 ) ) )

		# add all valid primitive attrib types
		mesh["floatPrim"] = IECoreScene.PrimitiveVariable( primitiveInterpolation, floatVectorData[:6] )
		mesh["v2fPrim"] = IECoreScene.PrimitiveVariable( primitiveInterpolation, v2fVectorData[:6] )
		mesh["v3fPrim"] = IECoreScene.PrimitiveVariable( primitiveInterpolation, v3fVectorData[:6] )
		mesh["color3fPrim"] = IECoreScene.PrimitiveVariable( primitiveInterpolation, color3fVectorData[:6] )
		mesh["intPrim"] = IECoreScene.PrimitiveVariable( primitiveInterpolation, intVectorData[:6] )
		mesh["v2iPrim"] = IECoreScene.PrimitiveVariable( primitiveInterpolation, v2iVectorData[:6] )
		mesh["v3iPrim"] = IECoreScene.PrimitiveVariable( primitiveInterpolation, v3iVectorData[:6] )
		mesh["stringPrim"] = IECoreScene.PrimitiveVariable( primitiveInterpolation, stringVectorData[:6], IECore.IntVectorData( range( 0, 6 ) ) )

		# add all valid vertex attrib types
		mesh["floatVert"] = IECoreScene.PrimitiveVariable( vertexInterpolation, floatVectorData )
		mesh["v2fVert"] = IECoreScene.PrimitiveVariable( vertexInterpolation, v2fVectorData )
		mesh["v3fVert"] = IECoreScene.PrimitiveVariable( vertexInterpolation, v3fVectorData )
		mesh["color3fVert"] = IECoreScene.PrimitiveVariable( vertexInterpolation, color3fVectorData )
		mesh["intVert"] = IECoreScene.PrimitiveVariable( vertexInterpolation, intVectorData )
		mesh["v2iVert"] = IECoreScene.PrimitiveVariable( vertexInterpolation, v2iVectorData )
		mesh["v3iVert"] = IECoreScene.PrimitiveVariable( vertexInterpolation, v3iVectorData )
		mesh["stringVert"] = IECoreScene.PrimitiveVariable( vertexInterpolation, stringVectorData, IECore.IntVectorData( range( 0, 24 ) ) )

		mesh.blindData()['name'] = "meshGroupA"

		return mesh

	def meshGroup( self ) :
		group = IECoreScene.Group()
		group.addChild( self.mesh() )
		return group

	def twoMeshes( self ) :
		group = self.meshGroup()
		mesh = self.mesh()
		mesh.blindData()['name'] = "meshGroupB"
		group.addChild( mesh )
		return group

	def pointTwoBox( self ) :
		group = IECoreScene.Group()
		points = self.points()
		points.blindData()['name'].value = "boxPoints"
		group.addChild( points )
		mesh = self.mesh()
		del mesh.blindData()['name']
		group.addChild( mesh )
		mesh = self.mesh()
		del mesh.blindData()['name']
		group.addChild( mesh )
		group.blindData()['name'] = "curveBoxGroup"
		return group

	def buildScene( self ) :
		group = IECoreScene.Group()
		group.addChild( self.points() )
		group.addChild( self.twoMeshes() )
		group.addChild( self.pointTwoBox() )
		return group

	def geo( self ) :
		geo = hou.node( "/obj/geo1" )
		if not geo :
			obj = hou.node( "/obj" )
			geo = obj.createNode( "geo", run_init_scripts=False )

		return geo

	def emptySop( self ) :
		return self.geo().createNode( "null" )

	def testCreateConverter( self )  :
		converter = IECoreHoudini.ToHoudiniGroupConverter( self.meshGroup() )
		self.failUnless( converter.isInstanceOf( IECore.TypeId( IECoreHoudini.TypeId.ToHoudiniGroupConverter ) ) )

	def testFactory( self ) :
		scene = self.buildScene()
		converter = IECoreHoudini.ToHoudiniGeometryConverter.create( scene )
		self.failUnless( converter.isInstanceOf( IECore.TypeId( IECoreHoudini.TypeId.ToHoudiniGroupConverter ) ) )

		converter = IECoreHoudini.ToHoudiniGeometryConverter.create( self.points() )
		self.failUnless( converter.isInstanceOf( IECore.TypeId( IECoreHoudini.TypeId.ToHoudiniPointsConverter ) ) )

		converter = IECoreHoudini.ToHoudiniGeometryConverter.create( self.mesh() )
		self.failUnless( converter.isInstanceOf( IECore.TypeId( IECoreHoudini.TypeId.ToHoudiniPolygonsConverter ) ) )

		converter = IECoreHoudini.ToHoudiniGeometryConverter.create( self.twoMeshes() )
		self.failUnless( converter.isInstanceOf( IECore.TypeId( IECoreHoudini.TypeId.ToHoudiniGroupConverter ) ) )

		converter = IECoreHoudini.ToHoudiniGeometryConverter.create( self.pointTwoBox() )
		self.failUnless( converter.isInstanceOf( IECore.TypeId( IECoreHoudini.TypeId.ToHoudiniGroupConverter ) ) )

		self.failUnless( IECoreScene.TypeId.Group in IECoreHoudini.ToHoudiniGeometryConverter.supportedTypes() )

	def testConvertScene( self ) :
		null = self.emptySop()
		self.failUnless( IECoreHoudini.ToHoudiniGroupConverter( self.buildScene() ).convert( null ) )
		geo = null.geometry()
		nameAttr = geo.findPrimAttrib( "name" )
		names = [ "curveBoxGroup", "curveBoxGroup/boxPoints", "meshGroupA", "meshGroupB", "pointsGroup" ]
		self.assertEqual( sorted(nameAttr.strings()), names )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "meshGroupA" ]), 6 )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "meshGroupB" ]), 6 )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "curveBoxGroup" ]), 12 )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "pointsGroup" ]), 1 )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "curveBoxGroup/boxPoints" ]), 1 )

		result = IECoreHoudini.FromHoudiniGroupConverter( null ).convert()
		self.assertEqual( result.blindData(), IECore.CompoundData() )
		children = result.children()
		for i in range ( 0, len(children) ) :
			name = names[i]
			self.failUnless( name in nameAttr.strings() )
			self.assertEqual( children[i].variableSize( IECoreScene.PrimitiveVariable.Interpolation.Uniform ), len([ x for x in geo.prims() if x.attribValue( "name" ) == name ] ) )

	def testAppending( self ) :
		null = self.emptySop()
		scene = self.buildScene()
		self.failUnless( IECoreHoudini.ToHoudiniGroupConverter( scene ).convert( null ) )
		geo = null.geometry()
		nameAttr = geo.findPrimAttrib( "name" )
		names = [ "curveBoxGroup", "curveBoxGroup/boxPoints", "meshGroupA", "meshGroupB", "pointsGroup" ]
		self.assertEqual( sorted(nameAttr.strings()), names )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "meshGroupA" ]), 6 )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "meshGroupB" ]), 6 )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "curveBoxGroup" ]), 12 )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "pointsGroup" ]), 1 )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "curveBoxGroup/boxPoints" ]), 1 )

		result = IECoreHoudini.FromHoudiniGroupConverter( null ).convert()
		self.assertEqual( result.blindData(), IECore.CompoundData() )
		children = result.children()
		for i in range ( 0, len(children) ) :
			name = names[i]
			self.failUnless( name in nameAttr.strings() )
			if isinstance( children[i], IECoreScene.PointsPrimitive ) :
				numPoints = sum( [ len(x.vertices()) for x in geo.prims() if x.attribValue( "name" ) == name ] )
				self.assertEqual( children[i].variableSize( IECoreScene.PrimitiveVariable.Interpolation.Uniform ), 1 )
				self.assertEqual( children[i].variableSize( IECoreScene.PrimitiveVariable.Interpolation.Vertex ), numPoints )
			else :
				self.assertEqual( children[i].variableSize( IECoreScene.PrimitiveVariable.Interpolation.Uniform ), len([ x for x in geo.prims() if x.attribValue( "name" ) == name ] ) )

		self.failUnless( IECoreHoudini.ToHoudiniGroupConverter( scene ).convert( null, append=True ) )
		geo = null.geometry()
		nameAttr = geo.findPrimAttrib( "name" )
		names = [ "curveBoxGroup", "curveBoxGroup/boxPoints", "meshGroupA", "meshGroupB", "pointsGroup" ]
		self.assertEqual( sorted(nameAttr.strings()), names )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "meshGroupA" ]), 12 )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "meshGroupB" ]), 12 )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "curveBoxGroup" ]), 24 )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "pointsGroup" ]), 2 )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "curveBoxGroup/boxPoints" ]), 2 )

		result = IECoreHoudini.FromHoudiniGroupConverter( null ).convert()
		self.assertEqual( result.blindData(), IECore.CompoundData() )
		children = result.children()
		for i in range ( 0, len(children) ) :
			name = names[i]
			self.failUnless( name in nameAttr.strings() )
			if isinstance( children[i], IECoreScene.PointsPrimitive ) :
				numPoints = sum( [ len(x.vertices()) for x in geo.prims() if x.attribValue( "name" ) == name ] )
				self.assertEqual( children[i].variableSize( IECoreScene.PrimitiveVariable.Interpolation.Uniform ), 1 )
				self.assertEqual( children[i].variableSize( IECoreScene.PrimitiveVariable.Interpolation.Vertex ), numPoints )
			else :
				self.assertEqual( children[i].variableSize( IECoreScene.PrimitiveVariable.Interpolation.Uniform ), len([ x for x in geo.prims() if x.attribValue( "name" ) == name ] ) )

	def testConvertGroupedPoints( self ) :
		null = self.emptySop()
		group = IECoreScene.Group()
		group.addChild( self.points() )
		self.failUnless( IECoreHoudini.ToHoudiniGroupConverter( group ).convert( null ) )
		primGroups = null.geometry().primGroups()

		self.assertEqual( len(primGroups), 0 )

	def testConvertGroupedMesh( self ) :
		null = self.emptySop()
		group = IECoreScene.Group()
		group.addChild( self.mesh() )
		self.failUnless( IECoreHoudini.ToHoudiniGroupConverter( group ).convert( null ) )
		geo = null.geometry()
		nameAttr = geo.findPrimAttrib( "name" )
		self.assertEqual( nameAttr.strings(), tuple( [ "meshGroupA" ] ) )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "meshGroupA" ]), 6 )

	def testConvertGroupedMultiMeshes( self ) :
		null = self.emptySop()
		self.failUnless( IECoreHoudini.ToHoudiniGroupConverter( self.twoMeshes() ).convert( null ) )
		geo = null.geometry()
		nameAttr = geo.findPrimAttrib( "name" )
		self.assertEqual( nameAttr.strings(), tuple( [ "meshGroupA", "meshGroupB" ] ) )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "meshGroupA" ]), 6 )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "meshGroupB" ]), 6 )

	def testConvertGroupedPointsAndPolygons( self ) :
		null = self.emptySop()
		self.failUnless( IECoreHoudini.ToHoudiniGroupConverter( self.pointTwoBox() ).convert( null ) )
		geo = null.geometry()
		nameAttr = geo.findPrimAttrib( "name" )
		self.assertEqual( sorted( nameAttr.strings() ), [ "curveBoxGroup", "curveBoxGroup/boxPoints" ] )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "curveBoxGroup" ]), 12 )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "curveBoxGroup/boxPoints" ]), 1 )

	def testAdjustedStringVectorIndices( self ) :
		null = self.emptySop()
		group = self.twoMeshes()
		group.children()[0]["commonString"] = IECoreScene.PrimitiveVariable( IECoreScene.PrimitiveVariable.Interpolation.Uniform, IECore.StringVectorData( [ "first" ] ), IECore.IntVectorData( [ 0 ] * 6 ) )
		group.children()[1]["commonString"] = IECoreScene.PrimitiveVariable( IECoreScene.PrimitiveVariable.Interpolation.Uniform, IECore.StringVectorData( [ "second" ] ), IECore.IntVectorData( [ 0 ] * 6 ) )
		self.failUnless( IECoreHoudini.ToHoudiniGroupConverter( group ).convert( null ) )
		geo = null.geometry()
		nameAttr = geo.findPrimAttrib( "name" )
		self.assertEqual( nameAttr.strings(), tuple( [ "meshGroupA", "meshGroupB" ] ) )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "meshGroupA" ]), 6 )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "meshGroupB" ]), 6 )
		for prim in geo.prims() :
			expected = "first" if prim.attribValue( "name" ) == "meshGroupA" else "second"
			self.assertEqual( prim.stringListAttribValue( "commonString" ), tuple( [ expected ] ) )
			self.assertEqual( prim.attribValue( "commonString" ), expected )

	def testTransforms( self ) :

		def add( parent, child, vec ) :
			child.setTransform( IECoreScene.MatrixTransform( imath.M44f().translate( vec ) ) )
			parent.addChild( child )
			if random.random() > 0.75 :
				child.addChild( self.mesh() )

		group = IECoreScene.Group()
		group.setTransform( IECoreScene.MatrixTransform( imath.M44f().translate( imath.V3f( 5, 0, 0 ) ) ) )
		for i in range( 0, 50 ) :
			add( group, self.meshGroup(), imath.V3f( random.random(), random.random(), random.random() ) * 3 )

		null = self.emptySop()
		self.failUnless( IECoreHoudini.ToHoudiniGroupConverter( group ).convert( null ) )

		houdiniBound = null.geometry().boundingBox()
		bound = imath.Box3f( imath.V3f( list(houdiniBound.minvec()) ), imath.V3f( list(houdiniBound.maxvec()) ) )
		self.assertEqual( group.bound(), bound )

	def testCannotConvertIntoReadOnlyHOMGeo( self ) :

		group = self.buildScene()
		sop = self.emptySop()

		converter = IECoreHoudini.ToHoudiniGroupConverter( group )
		self.failUnless( not converter.convertToGeo( sop.geometry() ) )

		self.assertEqual( sop.geometry().points(), tuple() )
		self.assertEqual( sop.geometry().prims(), tuple() )

	def testConvertIntoWritableHOMGeo( self ) :

		if not os.path.isdir( TestToHoudiniGroupConverter.__testOTLBackups ) :
			os.mkdir( TestToHoudiniGroupConverter.__testOTLBackups )

		shutil.copyfile( TestToHoudiniGroupConverter.__testOTL, TestToHoudiniGroupConverter.__testOTLCopy )
		hou.hda.installFile( TestToHoudiniGroupConverter.__testOTLCopy )

		sop = hou.node( "/obj" ).createNode( "geo", run_init_scripts=False ).createNode( "testPythonSop" )
		geo = sop.geometry()
		self.assertEqual( sop.geometry().points(), tuple() )
		self.assertEqual( sop.geometry().prims(), tuple() )

		sop.type().definition().sections()["PythonCook"].setContents( """
import imath
import IECore
import IECoreScene
import IECoreHoudini
group = IECoreScene.Group()
mesh = IECoreScene.MeshPrimitive.createBox( imath.Box3f( imath.V3f( -1 ), imath.V3f( 1 ) ) )
mesh.blindData()["name"] = IECore.StringData( "mesh" )
points = IECoreScene.PointsPrimitive( IECore.V3fVectorData( [ imath.V3f( x ) for x in range( 0, 20 ) ] ) )
points.blindData()["name"] = IECore.StringData( "points" )
curves = IECoreScene.CurvesPrimitive( IECore.IntVectorData( [ 4 ] ), IECore.CubicBasisf.linear(), False, IECore.V3fVectorData( [ imath.V3f( x ) for x in range( 0, 4 ) ] ) )
curves.blindData()["name"] = IECore.StringData( "curves" )
group.addChild( mesh )
group.addChild( points )
group.addChild( curves )
IECoreHoudini.ToHoudiniGroupConverter( group ).convertToGeo( hou.pwd().geometry() )"""
		)

		self.assertEqual( len(sop.geometry().points()), 32 )
		self.assertEqual( len(sop.geometry().prims()), 8 )

		torus = sop.createInputNode( 0, "torus" )
		torus.parm( "rows" ).set( 10 )
		torus.parm( "cols" ).set( 10 )

		self.assertEqual( len(sop.geometry().points()), 32 )
		self.assertEqual( len(sop.geometry().prims()), 8 )

		code = sop.type().definition().sections()["PythonCook"].contents()
		sop.type().definition().sections()["PythonCook"].setContents( code.replace( "convertToGeo( hou.pwd().geometry() )", "convertToGeo( hou.pwd().geometry(), append=True )" ) )

		self.assertEqual( len(sop.geometry().points()), 132 )
		self.assertEqual( len(sop.geometry().prims()), 108 )

		sop.destroy()

	def testAttributeFilter( self ) :

		group = self.buildScene()
		sop = self.emptySop()

		converter = IECoreHoudini.ToHoudiniGroupConverter( group )
		self.assertTrue( converter.convert( sop ) )
		self.assertEqual( sorted([ x.name() for x in sop.geometry().pointAttribs() ]), TestToHoudiniGroupConverter.PointPositionAttribs + ['color3fPoint', 'floatPoint', 'intPoint', 'stringPoint', 'v2fPoint', 'v2iPoint', 'v3fPoint', 'v3iPoint'] )
		self.assertEqual( sorted([ x.name() for x in sop.geometry().primAttribs() ]), ['color3fPrim', 'floatPrim', 'ieMeshInterpolation', 'intPrim', 'name', 'stringPrim', 'v2fPrim', 'v2iPrim', 'v3fPrim', 'v3iPrim'] )
		self.assertEqual( sorted([ x.name() for x in sop.geometry().vertexAttribs() ]), ['color3fVert', 'floatVert', 'intVert', 'stringVert', 'v2fVert', 'v2iVert', 'v3fVert', 'v3iVert'] )
		self.assertEqual( sorted([ x.name() for x in sop.geometry().globalAttribs() ]), ['color3fDetail', 'floatDetail', 'intDetail', 'stringDetail', 'v2fDetail', 'v2iDetail', 'v3fDetail', 'v3iDetail'] )

		converter.parameters()["attributeFilter"].setTypedValue( "P *3f*" )
		self.assertTrue( converter.convert( sop ) )
		self.assertEqual( sorted([ x.name() for x in sop.geometry().pointAttribs() ]),  TestToHoudiniGroupConverter.PointPositionAttribs + ['color3fPoint', 'v3fPoint'] )
		self.assertEqual( sorted([ x.name() for x in sop.geometry().primAttribs() ]), ['color3fPrim', 'ieMeshInterpolation', 'name', 'v3fPrim'] )
		self.assertEqual( sorted([ x.name() for x in sop.geometry().vertexAttribs() ]), ['color3fVert', 'v3fVert'] )
		self.assertEqual( sorted([ x.name() for x in sop.geometry().globalAttribs() ]), ['color3fDetail', 'v3fDetail'] )

		converter.parameters()["attributeFilter"].setTypedValue( "* ^*Detail ^int*" )
		self.assertTrue( converter.convert( sop ) )
		self.assertEqual( sorted([ x.name() for x in sop.geometry().pointAttribs() ]), TestToHoudiniGroupConverter.PointPositionAttribs + ['color3fPoint', 'floatPoint', 'stringPoint', 'v2fPoint', 'v2iPoint', 'v3fPoint', 'v3iPoint'] )
		self.assertEqual( sorted([ x.name() for x in sop.geometry().primAttribs() ]), ['color3fPrim', 'floatPrim', 'ieMeshInterpolation', 'name', 'stringPrim', 'v2fPrim', 'v2iPrim', 'v3fPrim', 'v3iPrim'] )
		self.assertEqual( sorted([ x.name() for x in sop.geometry().vertexAttribs() ]), ['color3fVert', 'floatVert', 'stringVert', 'v2fVert', 'v2iVert', 'v3fVert', 'v3iVert'] )
		self.assertEqual( sorted([ x.name() for x in sop.geometry().globalAttribs() ]), [] )

		# verify we can filter uvs
		mesh = IECoreScene.MeshPrimitive.createPlane( imath.Box2f( imath.V2f( 0 ), imath.V2f( 1 ) ) )
		IECoreScene.TriangulateOp()( input=mesh, copyInput=False )
		IECoreScene.MeshNormalsOp()( input=mesh, copyInput=False )
		mesh["Cs"] = IECoreScene.PrimitiveVariable( IECoreScene.PrimitiveVariable.Interpolation.FaceVarying, IECore.V3fVectorData( [ imath.V3f( 1, 0, 0 ) ] * 6, IECore.GeometricData.Interpretation.Color ) )
		mesh["width"] = IECoreScene.PrimitiveVariable( IECoreScene.PrimitiveVariable.Interpolation.Vertex, IECore.FloatVectorData( [ 1 ] * 4 ) )
		mesh["Pref"] = mesh["P"]
		group = IECoreScene.Group()
		group.addChild( mesh )
		group.addChild( mesh.copy() )
		group.addChild( mesh.copy() )

		converter = IECoreHoudini.ToHoudiniGroupConverter( group )
		converter.parameters()["attributeFilter"].setTypedValue( "*" )
		self.assertTrue( converter.convert( sop ) )
		self.assertItemsEqual( sorted([ x.name() for x in sop.geometry().pointAttribs() ]), TestToHoudiniGroupConverter.PointPositionAttribs + ['N', 'pscale', 'rest'] )
		self.assertEqual( sorted([ x.name() for x in sop.geometry().primAttribs() ]), ['ieMeshInterpolation', ] )
		self.assertEqual( sorted([ x.name() for x in sop.geometry().vertexAttribs() ]), ['Cd', 'uv'] )
		self.assertEqual( sorted([ x.name() for x in sop.geometry().globalAttribs() ]), [] )

		# have to filter the source attrs
		converter.parameters()["attributeFilter"].setTypedValue( "* ^uv ^pscale ^rest" )
		self.assertTrue( converter.convert( sop ) )
		self.assertItemsEqual( sorted([ x.name() for x in sop.geometry().pointAttribs() ]), TestToHoudiniGroupConverter.PointPositionAttribs + ['N', 'pscale', 'rest'] )
		self.assertEqual( sorted([ x.name() for x in sop.geometry().primAttribs() ]), ['ieMeshInterpolation'] )
		self.assertEqual( sorted([ x.name() for x in sop.geometry().vertexAttribs() ]), ['Cd'] )
		self.assertEqual( sorted([ x.name() for x in sop.geometry().globalAttribs() ]), [] )

		converter.parameters()["attributeFilter"].setTypedValue( "* ^width ^Pref" )
		self.assertTrue( converter.convert( sop ) )
		self.assertItemsEqual( sorted([ x.name() for x in sop.geometry().pointAttribs() ]), TestToHoudiniGroupConverter.PointPositionAttribs + ['N'] )
		self.assertEqual( sorted([ x.name() for x in sop.geometry().primAttribs() ]), ['ieMeshInterpolation'] )
		self.assertEqual( sorted([ x.name() for x in sop.geometry().vertexAttribs() ]), ['Cd', 'uv'] )
		self.assertEqual( sorted([ x.name() for x in sop.geometry().globalAttribs() ]), [] )

		converter.parameters()["attributeFilter"].setTypedValue( "* ^width ^Cs" )
		self.assertTrue( converter.convert( sop ) )
		self.assertItemsEqual( sorted([ x.name() for x in sop.geometry().pointAttribs() ]), TestToHoudiniGroupConverter.PointPositionAttribs + ['N', 'rest'] )
		self.assertEqual( sorted([ x.name() for x in sop.geometry().primAttribs() ]), ['ieMeshInterpolation'] )
		self.assertEqual( sorted([ x.name() for x in sop.geometry().vertexAttribs() ]), ['uv'] )
		self.assertEqual( sorted([ x.name() for x in sop.geometry().globalAttribs() ]), [] )

	def testStandardAttributeConversion( self ) :

		sop = self.emptySop()

		mesh = IECoreScene.MeshPrimitive.createPlane( imath.Box2f( imath.V2f( 0 ), imath.V2f( 1 ) ) )
		IECoreScene.TriangulateOp()( input=mesh, copyInput=False )
		IECoreScene.MeshNormalsOp()( input=mesh, copyInput=False )
		mesh["Cs"] = IECoreScene.PrimitiveVariable( IECoreScene.PrimitiveVariable.Interpolation.FaceVarying, IECore.V3fVectorData( [ imath.V3f( 1, 0, 0 ) ] * 6, IECore.GeometricData.Interpretation.Color ) )
		mesh["width"] = IECoreScene.PrimitiveVariable( IECoreScene.PrimitiveVariable.Interpolation.Vertex, IECore.FloatVectorData( [ 1 ] * 4 ) )
		mesh["Pref"] = mesh["P"]

		self.assertTrue( mesh.arePrimitiveVariablesValid() )

		group = IECoreScene.Group()
		group.addChild( mesh )
		group.addChild( mesh.copy() )
		group.addChild( mesh.copy() )

		converter = IECoreHoudini.ToHoudiniGroupConverter( group )
		self.assertTrue( converter.convert( sop ) )
		geo = sop.geometry()
		self.assertItemsEqual( sorted([ x.name() for x in geo.pointAttribs() ]), TestToHoudiniGroupConverter.PointPositionAttribs + ['N', 'pscale', 'rest'] )
		self.assertEqual( sorted([ x.name() for x in geo.primAttribs() ]), ['ieMeshInterpolation'] )
		self.assertEqual( sorted([ x.name() for x in geo.vertexAttribs() ]), ['Cd', 'uv'] )
		self.assertEqual( sorted([ x.name() for x in geo.globalAttribs() ]), [] )

		uvData = mesh["uv"].data.copy()
		uvData.extend( mesh["uv"].data )
		uvData.extend( mesh["uv"].data )
		uvs = geo.findVertexAttrib( "uv" )

		i = 0
		for prim in geo.prims() :
			verts = list(prim.vertices())
			verts.reverse()
			for vert in verts :
				uvValues = vert.attribValue( uvs )
				self.assertAlmostEqual( uvValues[0], uvData[i][0] )
				self.assertAlmostEqual( uvValues[1], uvData[i][1] )
				i += 1

		converter["convertStandardAttributes"].setTypedValue( False )
		self.assertTrue( converter.convert( sop ) )
		geo = sop.geometry()
		self.assertItemsEqual( sorted([ x.name() for x in geo.pointAttribs() ]), TestToHoudiniGroupConverter.PointPositionAttribs + ['N', 'Pref', 'width'] )
		self.assertEqual( sorted([ x.name() for x in geo.primAttribs() ]), ['ieMeshInterpolation'] )
		self.assertEqual( sorted([ x.name() for x in geo.vertexAttribs() ]), ['Cs', 'uv'] )
		self.assertEqual( sorted([ x.name() for x in geo.globalAttribs() ]), [] )

		i = 0
		uvs = geo.findVertexAttrib( "uv" )
		for prim in geo.prims() :
			verts = list(prim.vertices())
			verts.reverse()
			for vert in verts :
				uvValues = vert.attribValue( uvs )
				self.assertAlmostEqual( uvValues[0], uvData[i][0] )
				self.assertAlmostEqual( uvValues[1], uvData[i][1] )
				i += 1

	def testInterpolation( self ) :

		sop = self.emptySop()
		group = self.twoMeshes()
		group.children()[0].interpolation = "catmullClark"
		group.children()[1].interpolation = "linear"
		self.assertTrue( IECoreHoudini.ToHoudiniGroupConverter( group ).convert( sop ) )
		self.assertTrue( "ieMeshInterpolation" in [ x.name() for x in sop.geometry().primAttribs() ] )
		attrib = sop.geometry().findPrimAttrib( "ieMeshInterpolation" )
		for prim in sop.geometry().prims() :
			if prim.attribValue( "name" ) == "meshGroupA" :
				self.assertEqual( prim.attribValue( attrib ), "subdiv" )
			else :
				self.assertEqual( prim.attribValue( attrib ), "poly" )

	def testNameParameter( self ) :

		sop = self.emptySop()
		group = self.pointTwoBox()
		converter = IECoreHoudini.ToHoudiniGroupConverter( group )

		# blindData still works for backwards compatibility
		self.assert_( converter.convert( sop ) )
		geo = sop.geometry()
		nameAttr = geo.findPrimAttrib( "name" )
		self.assertEqual( sorted( nameAttr.strings() ), [ "curveBoxGroup", "curveBoxGroup/boxPoints" ] )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "curveBoxGroup" ]), 12 )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "curveBoxGroup/boxPoints" ]), 1 )

		# we can still override the top level group name
		converter["name"].setTypedValue( "nameOverride" )
		self.assert_( converter.convert( sop ) )
		geo = sop.geometry()
		nameAttr = geo.findPrimAttrib( "name" )
		self.assertEqual( sorted( nameAttr.strings() ), [ "nameOverride", "nameOverride/boxPoints" ] )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "nameOverride" ]), 12 )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "nameOverride/boxPoints" ]), 1 )

		# no blindData and no parameter value means no top level name
		del group.blindData()["name"]
		self.assert_( IECoreHoudini.ToHoudiniGroupConverter( group ).convert( sop ) )
		geo = sop.geometry()
		nameAttr = geo.findPrimAttrib( "name" )
		self.assertEqual( sorted( nameAttr.strings() ), [ "boxPoints" ] )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "" ]), 12 )
		self.assertEqual( len([ x for x in geo.prims() if x.attribValue( "name" ) == "boxPoints" ]), 1 )

	def tearDown( self ) :

		if TestToHoudiniGroupConverter.__testOTLCopy in "".join( hou.hda.loadedFiles() ) :
			hou.hda.uninstallFile( TestToHoudiniGroupConverter.__testOTLCopy )

		if os.path.isdir( TestToHoudiniGroupConverter.__testOTLBackups ) :
			shutil.rmtree( TestToHoudiniGroupConverter.__testOTLBackups )

if __name__ == "__main__":
    unittest.main()
