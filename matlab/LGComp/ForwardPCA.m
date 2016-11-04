function [Feature] = ForwardPCA(Input, Forward, Mean, LatDim)

[FSize, ISize] = size(Forward);
[INum, InputSize] = size(Input);

if ISize ~= InputSize
    display('Incompatible model..');
    return;
end

Forward = Forward(1:LatDim,:);

CenteredInput = (Input-repmat(Mean,INum, 1));
% CenteredInput = Input;
% Feature = Forward*CenteredInput';
% Feature = Feature';
Feature = CenteredInput*Forward';

clear CenteredInput;
