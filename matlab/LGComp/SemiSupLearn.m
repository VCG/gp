function [f,L] = SemiSupLearn(Labels, L, Lambda)  % K on paper is L here.

[SizeL,~] = size(L);
[NumNodes] = length(Labels.y);

if SizeL ~= NumNodes
    error('L size should be the same as Y');
    return;
end

A = Lambda*L;
c = zeros(NumNodes,1);  % c is Ly

% Looping?!
% Can we do this? A + diag(Labels.LFlag)
% c is just Labels.y (implicitly LFlag will be set correctly on passing in)
for u=1:NumNodes
    if Labels.LFlag(u) > 0
        c(u) = Labels.y(u);
        A(u,u) = A(u,u)+1;
    end
end

f = A\c;


% Inverse of A (inv(A)) and extracting the diagonal component of the
% result will capture the 'invariance' - the larger the value, the less
% certain (larger the variance). Sample this for k largest values to pick
% sample.

% If not invertible, add along diagonal very small values (1e-9) and then
% invert.

%try
%    InvA = inv(A);
%catch
%    InvA = inv(A+1e-9*eye(size(A)));
%end