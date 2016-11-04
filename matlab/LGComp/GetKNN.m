function [StoredIdx, KDistance, Input, Stored] = GetKNN(Input, K, Stored)

if nargin >= 3
    [NumTstPtns,TstInputSize] = size(Input);
    [NumStoredPtns,StoredInputSize] = size(Stored);
    if TstInputSize==StoredInputSize
        StoredIdx = zeros(NumTstPtns,K);
        KDistance = zeros(NumTstPtns,K);
        StoredNormSq = sum(Stored.^2,2)';
        TstNormSq = sum(Input.^2,2)';
        for i=1: NumTstPtns
            InnerProduct = Input(i,:)*Stored';
            DistanceSq = abs(StoredNormSq-2*InnerProduct+TstNormSq(i));
%             Distance = sqrt(DistanceSq);
            Distance = DistanceSq;
            if K>1
                [Sorted, KIndex] = sort(Distance, 'ascend');
                StoredIdx(i,:) = KIndex(1:K);
                KDistance(i,:) = Sorted(1:K);
            else
                KDistance(i) = min(Distance);
                Temp = find(Distance==KDistance(i));
                StoredIdx(i) = Temp(1);
            end
            if mod(i,1000) == 0
                display(sprintf('Pattern: %d/%d', i, NumTstPtns));
                pause(0.01);
            end
        end
    else
        display('Model incompatible..');
    end
else    
    [NumTstPtns,TstInputSize] = size(Input);
    StoredIdx = zeros(NumTstPtns,K);
    KDistance = zeros(NumTstPtns,K);
    TstNormSq = sum(Input.^2,2)';
    for i=1: NumTstPtns
        InnerProduct = Input(i,:)*Input';
        DistanceSq = abs(TstNormSq-2*InnerProduct+TstNormSq(i));
        Distance = sqrt(DistanceSq);
        if K>1
            [Sorted, KIndex] = sort(Distance, 'ascend');
            StoredIdx(i,:) = KIndex(1:K);
            KDistance(i,:) = Sorted(1:K);
        else
            KDistance(i) = min(Distance);
            Temp = find(Distance==KDistance(i));
            StoredIdx(i) = Temp(1);
        end
%         if mod(i,1000) == 0
%             display(sprintf('Pattern: %d/%d', i, NumTstPtns));
%             pause(0.01);
%         end
    end
end
