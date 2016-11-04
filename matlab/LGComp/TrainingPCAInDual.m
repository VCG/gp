function [Forward, Backward, MeanVector, EValues] = TrainingPCAInDual(Data)

[NumPtns, OutputSize] = size(Data);

ADimData = min(NumPtns,OutputSize);

MeanVector = mean(Data,1);
for i=1:NumPtns
    Data(i,:) = Data(i,:)-MeanVector;
end

K = Data*Data';
[evecs,evals] = eig(K);
evals = diag(evals)';

if OutputSize > 1
    if evals(1)<evals(end)
        evecs = fliplr(evecs);
        evals = fliplr(evals);
    else
        display('ho.');
    end
end

for i=1:NumPtns
    if evals(i)>0
        evecs(:,i) = evecs(:,i)/sqrt(evals(i));
    end
end

Forward = evecs'*Data;
Forward = Forward(1:ADimData,:);
EValues = evals(1:ADimData)/(NumPtns-1);
Backward = Forward';
