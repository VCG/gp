function [StNodes] = GetNNStructure(Input, K)

StNodes.Nodes.x = Input;

%%% alternative
%     [NumNodes,SizeNode] = size(Input);
% %     [StNodes.NNIdx,StNodes.KDistance] = getKNN5(Input',K);
%     [StNodes.NNIdx,StNodes.KDistance] = NGetTransInvKNN(Input',K);
% 
%     StNodes.NNIdx = StNodes.NNIdx';
%     StNodes.NNIdx = single(StNodes.NNIdx);
%     StNodes.KDistance = StNodes.KDistance';
% 
%     for i=1:NumNodes
%         [SVal,SIdx] = sort(StNodes.KDistance(i,:),'ascend');
%         StNodes.KDistance(i,:) = StNodes.KDistance(i,SIdx);
%         StNodes.NNIdx(i,:) = StNodes.NNIdx(i,SIdx);
%     end
%     
%     StNodes.NNIdx(:,2:end) = StNodes.NNIdx(:,1:end-1);
%     StNodes.KDistance(:,2:end) = StNodes.KDistance(:,1:end-1);
% 
%     for i=1:NumNodes
%         StNodes.NNIdx(i,1) = i;
%     end
%     StNodes.KDistance(:,1) = 0;
%%% alternative

%%% original
    [StNodes.NNIdx, StNodes.KDistance, Temp] = GetKNN(StNodes.Nodes.x, K, StNodes.Nodes.x);
%%% original

StNodes.KNNFlag = 1;
% %%% For each node, to obtain the indices of nodes whose nearest neighbors include that node
%     [NumNodes,Dim] = size(StNodes.Nodes.x);
%     StNodes.NumINN = zeros(1,NumNodes);
%     for i=1:NumNodes
%         StNodes.NumINN(i) = length(find(StNodes.NNIdx==i));
%     end
%     for i=1:NumNodes
%         if StNodes.NumINN(i) ~= 0
%             StNodes.INNIdx{i} = zeros(1,StNodes.NumINN(i));
%             StNodes.INNLocalIdx{i} = zeros(1,StNodes.NumINN(i));
%         end
%         INNCounter = 0;
%         for j=1:NumNodes
%             LocalIdx = find(StNodes.NNIdx(j,:)==i);
%             if ~isempty(LocalIdx)
%                 INNCounter = INNCounter+1;
%                 StNodes.INNIdx{i}(INNCounter) = j;
%                 StNodes.INNLocalIdx{i}(INNCounter) = LocalIdx;
%             end
%         end
%         if mod(i,1000) == 0
%             display(sprintf('Proc. node to node %d/%d.', i, NumNodes));
%             pause(0.01);
%         end
%     end
% %%% For each node, to obtain the indices of nodes whose nearest neighbors include that node
