function BInv = UpdateALSApproximation( BInv, SLabels )

% Update ALS approximation matrix
% Inputs:
% - BInv is the approximation matrix
% - SLabels is a list of newly added label indices since the last update
% Outputs:
% - Updated BInv
for k=1:length(SLabels)
    GITemp = BInv(:,SLabels(k));
    BInv = BInv-1/(1+BInv(SLabels(k),SLabels(k)))*(GITemp*GITemp');
end