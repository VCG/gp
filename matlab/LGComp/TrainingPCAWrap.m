function [Forward, Backward, MeanVector, EValues] = TrainingPCAWrap(Data)

[NumPtns, OutputSize] = size(Data);

if NumPtns > OutputSize*2;
    [Forward, Backward, MeanVector, EValues] = TrainingPCA(Data);
else
    [Forward, Backward, MeanVector, EValues] = TrainingPCAInDual(Data);
end
