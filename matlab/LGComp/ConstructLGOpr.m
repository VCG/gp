function [L] = ConstructLGOpr(Nodes, NNIdx, ManDim)

[NumNodes,AmbDim] = size(Nodes);

%%% sparse version
    BlSpMatSize = 300000;
    MaxNumNN = size(NNIdx,2);
    NumNonzero = NumNodes*MaxNumNN^2;
    BlSpMatNum = ceil(NumNonzero/BlSpMatSize);
    BlSpL = cell(BlSpMatNum,1);
%%% sparse version

SpMatIdx = 1;
SpEleCounter = 1;
SpRowIdx = zeros(BlSpMatSize,1);
SpColIdx = zeros(BlSpMatSize,1);
LVal = zeros(BlSpMatSize,1);
for i=1:NumNodes
    NumNeighbors = find(NNIdx(i,:)<=0,1);
    if ~isempty(NumNeighbors)
        NumNeighbors = NumNeighbors-1;
    else
        NumNeighbors = length(NNIdx(i,:));
    end
    G = Nodes(NNIdx(i,1:NumNeighbors),:);   

    CtBase = Nodes(i,:);
    [NG,TS] = GetNormalCoordGDim(CtBase, G, ManDim);
    [NBase,TS] = GetNormalCoordGGivenTS(CtBase,TS);
    BaseIndexInG = find(NNIdx(i,1:NumNeighbors)==i,1);
    
    %%% Adaptively choose the SigmaSq
        %%% recalculate distances for normal coordinates
            NGNormSq = sum(NG.^2,2)';
            NBaseNormSq = sum(NBase.^2,2)';
            DistSq = NG*NBase';
            DistSq = DistSq';
            DistSq = abs(NGNormSq-2*DistSq+NBaseNormSq);
        %%% recalculate distances for normal coordinates
        RParam = mean(sqrt(DistSq))*0.1;
        %RParam = mean(sqrt(DistSq))*0.01;
        RParam = RParam^2;
    %%% Adaptively choose the SigmaSq
    [LocalL] = ConstructLocalRegOperatorGaussianBZLN(NG, RParam, BaseIndexInG);
    for j=1:NumNeighbors
        GRIdx = NNIdx(i,j);

        GCIdx = NNIdx(i,1:NumNeighbors);
        SpRowIdx(SpEleCounter:SpEleCounter+NumNeighbors-1) = GRIdx;
        SpColIdx(SpEleCounter:SpEleCounter+NumNeighbors-1) = GCIdx;
        LVal(SpEleCounter:SpEleCounter+NumNeighbors-1) = LocalL(j,1:NumNeighbors);
        SpEleCounter = SpEleCounter+NumNeighbors;
    end
    if SpEleCounter > BlSpMatSize-NumNeighbors-1
        NonZeroIdx = length(find(SpRowIdx>0));
        SpRowIdx = SpRowIdx(1:NonZeroIdx);
        SpColIdx = SpColIdx(1:NonZeroIdx);
        LVal = LVal(1:NonZeroIdx);
        BlSpL{SpMatIdx} = sparse(SpRowIdx,SpColIdx,LVal,NumNodes,NumNodes);
        
        SpMatIdx = SpMatIdx+1;
        SpEleCounter = 1;
        SpRowIdx = zeros(BlSpMatSize,1);
        SpColIdx = zeros(BlSpMatSize,1);
        LVal = zeros(BlSpMatSize,1);
%         KVal = zeros(BlSpMatSize,1);
    end
end

if SpEleCounter > 1
    NonZeroIdx = length(find(SpRowIdx>0));
    SpRowIdx = SpRowIdx(1:NonZeroIdx);
    SpColIdx = SpColIdx(1:NonZeroIdx);
    LVal = LVal(1:NonZeroIdx);
    BlSpL{SpMatIdx} = sparse(SpRowIdx,SpColIdx,LVal,NumNodes,NumNodes);        
    SpMatIdx = SpMatIdx+1;
end

L = sparse([],[],[],NumNodes,NumNodes,0);
for i=1:SpMatIdx-1
    L = L+BlSpL{i};
end

L = (L+L')/2;
