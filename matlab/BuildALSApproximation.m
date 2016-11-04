function BInv = BuildALSApproximation( LGReg, Lambda, StartingLabelFlags )
% Build the structures needed for Kwang In's active label suggestion
% approximation

% Kwang In's example uses a sub-sampled matrix, but apparently it will work
% at full resolution quickly enough for small (< 10000) datasets.
% As we won't need anything greater, let's go for the full hog.


B = Lambda * full(LGReg) + diag(StartingLabelFlags);

% build inverse full regularization matrix
try
	CholB = chol(B);
	CholBInv = inv(CholB);
	BInv = CholBInv*CholBInv';
catch
    BInv = inv(B + 1e-9 * eye(size(B)) );
end

% Inputs:
% - GInv is BInv.
% - SubCandIdx is an array of indices of labelled examples into the full array
% E.G., a 10-large number, with items 5,6 labelled, SubCandIdx would
% contain [5,6];
% - SubLabelFlag is full length, e.g, [0,0,0,0,1,1,0,0,0,0].
%
% Outputs:
% - SLabels, a list of indices in descending order of variance.
%[SLabels] = ActiveLabelSuggestion(GInv, SubCandIdx, SubLabelFlag);

