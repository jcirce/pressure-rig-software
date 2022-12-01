digpotdata = [
    255 2.0;
    250 2.0;
    230 2.2;
    223 2.2;
    219 2.3;
    207 2.4;
    196 2.5;
    188 2.6;
    181 2.7;
    172 2.8;
    166 2.9;
    160 3.0;
    154 3.1;
    148 3.2;
    143 3.3;
    137 3.4;
    136 3.4;
    133 3.5;
    130 3.6;
    125 3.7;
    119 3.8;
    117 3.9;
    113 4.0;
    110 4.1;
    107 4.2;
    104 4.3;
    101 4.4;
     99 4.5;
     97 4.6;
     93 4.7;
     91 4.8;
     88 4.9;
     87 5.0;
     84 5.1;
     82 5.2;
     80 5.3;
     78 5.4;
     77 5.5;
     76 5.6;
     74 5.7;
     72 5.8;
     71 5.9;
     69 6.0;
     67 6.1;
     66 6.2;
     65 6.3;
     63 6.4;
     62 6.5;
     61 6.6;
     60 6.7;
     59 6.8;
     58 6.9;
     56 7.0;
     55 7.1;
     54 7.2;
     53 7.3;
     52 7.4;
     51 7.5;
     50 7.6;
     49 7.8;
     48 7.9;
     47 8.0;
     46 8.1;
     45 8.3;
     44 8.4;
     43 8.5;
     42 8.7;
     41 8.8;
     40 9.0;
     39 9.1;
     38 9.3;
     37 9.5;
     36 9.6;
     35 9.8;
     34 10.0;
     33 10.2;
     32 10.4;
     31 10.6;
     30 10.8;
     29 11.0;
     28 11.3;
     27 11.5;
     26 11.9;
     25 12.1;
     24 12.4;
     23 12.7;
     22 13.0;
     21 13.4;
     20 13.8;
     19 14.1;
     18 14.6;
     17 15.0;
     16 15.4;
     15 15.9;
     14 16.4;
     13 16.9;
     12 17.5;
     11 18.1;
     10 18.8;
      9 19.4;
      8 20.2;
      7 21.0;
      6 21.9;
      5 22.9;
      4 24.0;
];

bits = digpotdata(:,1);
psi = digpotdata(:,2);

plot(psi, bits, '.', 'Color','k')
ylabel('0-255 pot input') 
xlabel('Pressure [psi]') 
hold on



p = polyfit(psi, bits, 7);

fit = polyval(p,psi);
plot(psi, fit, 'LineWidth',3)