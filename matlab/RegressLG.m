function LGf = RegressLG( LGReg, y, LFlag, Lambda )

addpath './LGComp/';

%%% parameters for LG
%    LGParam.ManDim    = 17;   %%% 5:5:20
%    LGParam.KNSize    = 30;   %%% [10:30]: small # data points(<1000) [20:60]: large # data points
%    LGParam.Lambda    = 1e-8; %%% 1e-9:1e-5 (orders of 10 increases)
%%% parameters for LG

Labels.y = y;
Labels.LFlag = LFlag;

%%% solving LG system
    [LGf,LGReg] = SemiSupLearn(Labels, LGReg, Lambda);
%%% solving LG system