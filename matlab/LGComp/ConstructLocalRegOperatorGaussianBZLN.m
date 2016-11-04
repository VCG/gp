function [L] = ConstructLocalRegOperatorGaussianBZLN(Nodes, SigmaSq, BaseIndexInG)

% [K] = ComputeGaussianKernel(Nodes, SigmaSq);
[K] = ComputeGaussianKernelL(Nodes, SigmaSq);

%%% construct the null operator
    IndMat = zeros(size(K));
    IndMat(:,BaseIndexInG) = 1;
    LIdxMat = eye(size(K))-IndMat;
    %%% add linear functions to the null space
%         [X] = ComputeLinearX(Nodes);
%         X = X(:,1:end-1);
        X = Nodes;
        try
            %spparms('spumoni',2)
            %PInvX = inv(X'*X)*X';
            PInvX = (X'*X) \ X';
        catch
            PInvX = pinv(X);
        end
        LIdxMat = X*PInvX*LIdxMat;
%         LIdxMat = X*pinv(X)*LIdxMat;
        LIdxMat = eye(size(LIdxMat))-IndMat-LIdxMat;
    %%% add linear functions to the null space
%%% construct the null operator

%%% unregularized
    try
%         L = inv(K);
        L = pinv(K);
%         SMALLNUM = 1e-11;
%         L = inv(K+SMALLNUM*eye(size(K)));
    catch
        L = pinv(K);
    end
%     try
%         L = pinv(K);
%     catch
%         SMALLNUM = 1e-11;
%         L = inv(K+SMALLNUM*eye(size(K)));
%     end
%%% unregularized
% %%% partially regularized
%     lambda = 1e-7;
%     L = inv(K+lambda*eye(size(K)));    
% %%% partially regularized
% %%% fully regularized
%     lambda = 1e-5;
%     T = inv(K+lambda*eye(size(K)));
%     L = T'*K*T;
% %%% fully regularized

%%% subtract out the null space
    L = LIdxMat'*L*LIdxMat;
%%% subtract out the null space
