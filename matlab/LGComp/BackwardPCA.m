function [Original] = BackwardPCA(Feature, Backward, Mean, LatDim)

Backward = Backward(:,1:LatDim);

[ISize, FSize] = size(Backward);
[FNum, FeatureSize] = size(Feature);

if FSize ~= FeatureSize
    display('Incompatible model..');
    return;
end

Original = Backward*Feature';
Original = Original';
Original = (Original+repmat(Mean,FNum,1));
