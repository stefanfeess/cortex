//////////////////////////////////////////////////////////////////////////
//
//  Copyright (c) 2010-2011, Image Engine Design Inc. All rights reserved.
//
//  Redistribution and use in source and binary forms, with or without
//  modification, are permitted provided that the following conditions are
//  met:
//
//     * Redistributions of source code must retain the above copyright
//       notice, this list of conditions and the following disclaimer.
//
//     * Redistributions in binary form must reproduce the above copyright
//       notice, this list of conditions and the following disclaimer in the
//       documentation and/or other materials provided with the distribution.
//
//     * Neither the name of Image Engine Design nor the names of any
//       other contributors to this software may be used to endorse or
//       promote products derived from this software without specific prior
//       written permission.
//
//  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
//  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
//  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
//  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
//  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
//  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
//  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
//  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
//  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
//  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
//  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
//////////////////////////////////////////////////////////////////////////

#ifndef IECORESCENE_FACEVARYINGPROMOTIONOP_H
#define IECORESCENE_FACEVARYINGPROMOTIONOP_H

#include "IECoreScene/Export.h"
#include "IECoreScene/TypedPrimitiveOp.h"

#include "IECore/SimpleTypedParameter.h"
#include "IECore/VectorTypedParameter.h"

namespace IECoreScene
{

/// A MeshPrimitiveOp to promote PrimitiveVariables to FaceVarying interpolation.
/// \ingroup geometryProcessingGroup
class IECORESCENE_API FaceVaryingPromotionOp : public MeshPrimitiveOp
{
	public :

		FaceVaryingPromotionOp();
		~FaceVaryingPromotionOp() override;

		IE_CORE_DECLARERUNTIMETYPEDEXTENSION( FaceVaryingPromotionOp, FaceVaryingPromotionOpTypeId, MeshPrimitiveOp );

		//! @name Parameter accessors
		/// These provide convenient access to the parameters.
		///////////////////////////////////////////////////////////////
		IECore::StringVectorParameter *primVarNamesParameter();
		const IECore::StringVectorParameter *primVarNamesParameter() const;

		IECore::BoolParameter *promoteUniformParameter();
		const IECore::BoolParameter *promoteUniformParameter() const;

		IECore::BoolParameter *promoteVaryingParameter();
		const IECore::BoolParameter *promoteVaryingParameter() const;

		IECore::BoolParameter *promoteVertexParameter();
		const IECore::BoolParameter *promoteVertexParameter() const;
		//@}

	protected :

		void modifyTypedPrimitive( MeshPrimitive *mesh, const IECore::CompoundObject *operands ) override;

	private :

		struct Promoter;

};

IE_CORE_DECLAREPTR( FaceVaryingPromotionOp );


} // namespace IECoreScene

#endif // IECORESCENE_FACEVARYINGPROMOTIONOP_H

