function [K] = ComputeGaussianKernel(Input, SigmaSq)

[NumTrnPtns,TrnInputSize] = size(Input);
K = zeros(NumTrnPtns,NumTrnPtns);
LineNormSq = sum(Input.^2,2)';
for i=1:NumTrnPtns,
    InnerProduct = Input(i,:)*Input';
    DistanceSq = abs(LineNormSq(i)+LineNormSq-2*InnerProduct);
    K(i,:) = exp(-DistanceSq/SigmaSq);
end
