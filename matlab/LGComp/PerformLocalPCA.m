function [LPCA] = PerformLocalPCA(Data, NNIdx)

[NumDps,SizeDps] = size(Data);
LPCA.EMat = zeros(NumDps,SizeDps,SizeDps);
LPCA.Means = zeros(NumDps,SizeDps);

for i=1:NumDps
    LKNNs = Data(NNIdx(i,:),:);
    [Forward, Backward, MeanVector, EValues] = TrainingPCAWrap(LKNNs);
    LPCA.EMat(i,:,:) = Forward;
    LPCA.Means(i,:) = MeanVector;
end
