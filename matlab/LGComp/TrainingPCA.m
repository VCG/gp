function [Forward, Backward, MeanVector, EValues] = TrainingPCA(Data)

[NumPtns, OutputSize] = size(Data);
MeanVector = mean(Data,1);
for i=1:NumPtns
    Data(i,:) = Data(i,:)-MeanVector;
end
%     Data = (Data-repmat(MeanVector,NumPtns,1));

%     Cov = Data'*Data;
%     if NumPtns>1
%         Cov = Cov/(NumPtns-1);
%     end
Cov = cov(Data);
[evecs,evals] = eig(Cov);
evals = diag(evals)';

if OutputSize > 1
    if evals(1)<evals(end)
        evecs = fliplr(evecs);
        evals = fliplr(evals);
    else
        display('ho.');
    end
end

Forward = evecs';
Backward = Forward';
EValues = evals;

%     StdDev = sqrt(Evals);
%     for i=1:LatDim,
%         Forward(i,:) = Forward(i,:)/StdDev(i);
%     end
%     for i=1:LatDim,
%         Backward(:,i) = Backward(:,i)*StdDev(i);
%     end

%     a=diag(Backward*Forward);
%     a(1:20)
%     clear a;

clear evecs evals Cov;
