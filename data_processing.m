% Input: nx2 matrix, with points appended as [p1; p2 ... pn-1; pn]
%        Where pi = [xi, yi]
scan = [];

[n, m] = size(scan); % M = 2, obv.

% Curvature
kt = zeros(1,n);

% Curvature Appendage
for i = linspace(1,(n-2),1) % Index starts at 1, but we skip the first and last entry for curvature
    % Triangle Area
    A = .5*abs(((scan(i,1)-scan(i-1,1))*(scan(i+1,2)-scan(i,2))) - ((scan(i,2)-scan(i-1,2))*(scan(i+1,1)-scan(i,1))));

    % Line segments
    h = sqrt((scan(i,1)   - scan(i-1,1))^2 + (scan(i,2)   - scan(i-1,2))^2);
    f = sqrt((scan(i+1,1) - scan(i,1))^2   + (scan(i+1,2) - scan(i,2))^2);
    g = sqrt((scan(i-1,1) - scan(i+1,1))^2 + (scan(i-1,2) - scan(i+1,2))^2);
    
    % Menger curvature
    curve = 4*A/(f*g*h);

    % Value insert
    kt(i+1) = curve;

    % Or if you prefer appending  (entry row is i+1)
    %kt = [kt curve];
end

scan = [scan kt']; % Append curvature onto point matrix

% Distance
dist = zeros(1,n);

% Back Distance Appendage, ie Dist(j) = P(j) - P(j-1)
for j = linspace(2,n,1)
    dist(i) = sqrt((scan(i,1)-scan(i-1,1))^2 + (scan(i,2)-scan(i-1,2))^2) + dist(i-1);
end

scan = [scan dist']; % Append curvature onto point/curve matrix

% Length Calculation
length = 0;

for a = linspace(2,n,1)
    length = length + dist(a,4);
end

disp(length) % Check units