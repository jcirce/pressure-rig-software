digpotdata = [
    %255 2.0;
    255 2.8;
    246 2.9;
    236 3.0;
    228 3.1;
    218 3.2;
    209 3.3;
    204 3.4;
    195 3.5;
    190 3.6;
    184 3.7;
    179 3.8;
    174 3.9;
    167 4.0;
    164 4.1;
    158 4.2;
    153 4.3;
    149 4.4;
    147 4.5;
    142 4.6;
    140 4.7;
    136 4.8;
    132 4.9;
    130 5.0;
    127 5.1;
    124 5.2;
    121 5.3;
    119 5.4;
    116 5.5;
    113 5.6;
    111 5.7;
    108 5.8;
    106 5.9;
    104 6.0;
    102 6.1;
    100 6.2;
    99 6.3;
    97 6.4;
    95 6.5;
    93 6.6;
    91 6.7;
    90 6.8;
    88 6.9;
    86 7.0;
    85 7.1;
    83 7.2;
    82 7.3;
    81 7.4;
    79 7.5;
    78 7.6;
    77 7.7;
    76 7.8;
    75 7.9;
    74 8.0;
    73 8.1;
    71 8.2;
    70 8.3;
    69 8.4;
    68 8.5;
    67 8.6;
    66 8.7;
    65 8.8;
    64 8.9;
    63 9.0;
    61 9.3;
    60 9.4;
    59 9.5;
    58 9.7;
    57 9.8;
    56 9.9;
    55 10.0;
    54 10.1;
    53 10.3;
    52 10.4;
    51 10.6;
    50 10.8;
    49 10.9;
    48 11.1;
    47 11.3;
    46 11.5;
    45 11.6;
    44 11.8;
    43 12.0;
    42 12.2;
    41 12.4;
    40 12.6;
    39 12.8;
    38 13.1;
    37 13.3;
    36 13.6;
    35 13.8;
    34 14.0;
    33 14.3;
    32 14.7;
    31 14.9;
    30 15.2;
    29 15.6;
    28 15.9;
    27 16.3;
    26 16.6;
    25 17.1;
    24 17.5;
    23 17.9;
    22 18.3;
    21 18.9;
    20 19.3;
    19 19.9;
    18 20.4;
    17 21.0;
    16 21.7;
    15 22.3;
    14 23.0;
    13 23.7;
    12 24.6;
    11 25.4;
    10 26.4;
    %9 27.3;
    %8 27.6; %wrong 
];


bits = digpotdata(:,1);
psi = digpotdata(:,2);

plot(psi, bits, '.', 'Color','b')
ylabel('0-255 pot input') 
xlabel('Pressure [psi]') 

