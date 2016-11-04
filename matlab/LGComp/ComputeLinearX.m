function [X] = ComputeLinearX(Nodes)

[NumNodes,Dim] = size(Nodes);
CoordCombSize = Dim+1;

X = zeros(NumNodes,CoordCombSize);

for NIdx = 1:NumNodes
    RIdx = 1;

    for i=1:Dim
        X(NIdx,RIdx) = Nodes(NIdx,i);
        RIdx = RIdx+1;
    end

    X(NIdx,RIdx) = 1;
end
