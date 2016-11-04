function [SLabels] = ActiveLabelSuggestion(GInv, CandIdx, LabelFlag)

%%% [length(LabelFlag),length(LabelFlag)] == size(GInv)
%%% CandIdx should be a subset of [1:length(LabelFlag)];

LIdx = find(LabelFlag==1);
ULIdx = find(LabelFlag~=1);

CandIdx = setdiff(CandIdx,LIdx);
OrgPredUnc = diag(GInv);

%%% estimate the updated predictive variance
    VarRed = ones(length(CandIdx),1)*-1e10;        
    for j=1:length(CandIdx)
        %%% for rank 1 update
            GInvTemp = GInv;
            GITemp = GInvTemp(:,CandIdx(j));
            PredUnc = diag(GInvTemp)-1/(1+GInvTemp(CandIdx(j),CandIdx(j)))*(GITemp.^2);
        %%% for rank 1 update
        VarRed(j) = sum(OrgPredUnc(ULIdx)-PredUnc(ULIdx))/length(ULIdx);
    end
%%% estimate updated predictive variance

[~,VarLabel] = sort(VarRed,'descend');
SLabels = CandIdx(VarLabel);

% GInvUpdate = GInv;
% for j=1:length(SLabels)
%     GITemp = GInvUpdate(:,SLabels(j));
%     GInvUpdate = GInvUpdate-1/(1+GInvUpdate(SLabels(j),SLabels(j)))*(GITemp*GITemp');
% end
