function LGReg = BuildLGRegularizer( x, ManDim, KNSize )

addpath './LGComp/';

%%% parameters for LG
%    LGParam.ManDim    = 17;   %%% 5:5:20
%    LGParam.KNSize    = 30;   %%% [10:30]: small # data points(<1000) [20:60]: large # data points
%    LGParam.Lambda    = 1e-8; %%% 1e-9:1e-5 (orders of 10 increases)
%%% parameters for LG

[NumDataPoints,~] = size(x);

kNN = 200;
if( kNN > NumDataPoints )
    kNN = NumDataPoints;
end

if( KNSize > NumDataPoints )
    KNSize = NumDataPoints;
end

%[NNIdx,KDistanceSq] = GetKNN(Data.x, 4000);  % To compute LapParam.SigmaSq & ILapParam.SigmaSq
[NNIdx,KDistanceSq] = GetKNN(x, kNN);

%%% building LG regularizer
    LGNNIdx = NNIdx(:,1:KNSize);
    [LGReg] = ConstructLGOpr(x, LGNNIdx, ManDim);
%%% building LG regularizer
