function [NCoordsRef,TS] = GetNormalCoordGDim(CtBase, CtRef, ManDim)

[NumRef,SizeSpRef] = size(CtRef);

%%% estimate tangent space
    [TS.Forward, TS.Backward, TS.MeanVector, EValues] = TrainingPCAWrap(CtRef);
    TS.NCoordDim = ManDim;
%%% estimate tangent space
[NCoordBase] = ForwardPCA(CtBase, TS.Forward, TS.MeanVector, TS.NCoordDim);
TS.Base = NCoordBase;
%%% project data onto the tangent space        
    [NCoordsRef] = ForwardPCA(CtRef, TS.Forward, TS.MeanVector, TS.NCoordDim);
%%% project data onto the tangent space        
%%% center at base
    for i=1:NumRef
        NCoordsRef(i,:) = NCoordsRef(i,:)-TS.Base;
    end
%%% center at base    
