% -----------------------------------------
% 2. úkol
%
% Naprogramujte faktorizační algoritmus GreConD nebo Asso.
% Pomocí tohoto algoritmu analyzujte dataset Somerville Happiness Survey, 
% který najdete na webu
% https://archive.ics.uci.edu/dataset/479/somerville+happiness+survey.
% Hodnoty v tabulce je nejprve potřeba vhodným způsobem binarizovat, například takto:
% - vícehodnotový atribut X3 (kvalita veřejných škol) rozdělíte na tři binární atributy X3+, X3n, X3-
% - význam těchto nových atributů je následující:
%
%	X3+ je pozitivní hodnocení kvality (X3+ = 1 iff X3 = 1 nebo X3 = 2)
%	X3n je neutrální hodnocení kvality (X3n = 1 iff X3 = 3)
%	X3- je negativní hodnocení kvality (X3- = 1 iff X3 = 4 nebo X3 = 5)
%
% Binarizovanou matici rozložíte pomocí jednoho z uvedených algoritmů tak, 
% aby rozklad pokrýval alespoň 95% jedniček ve vstupním (binarizovaném) datasetu.
% Pokuste se slovně popsat význam tří nejvýznamnějších faktorů.

A = csvread("SomervilleHappinessSurvey2015.csv",1,0);

[m,n] = size(A);
C = zeros(m,1 + ((n-1)*3));

C(:,1)=A(:,1);
%C(:,2)=~A(:,1);

for i=2:n
    C(:,i*3-4) = A(:,i)<3;  % pozitivni
    C(:,i*3-3) = A(:,i)==3; % neutralni
    C(:,i*3-2) = A(:,i)>3;  % negativni
end

C=logical(C);

[A, B] = grecond_(C, 0.95);
res = A*B>0;
coverage = sum((res & C), 'all')*100/sum(C(:));

fprintf('Pokrytí jedniček je: %.2f%%\n', coverage);

% Popis sloupcu z webu:
%
% D = decision attribute (D) with values 0 (unhappy) and 1 (happy)
% X1 = the availability of information about the city services
% X2 = the cost of housing
% X3 = the overall quality of public schools
% X4 = your trust in the local police
% X5 = the maintenance of streets and sidewalks 
% X6 = the availability of social community events

% Faktor 1 = <{...},{X1-, X5-, X6-}> 
% (70 výskytů)
%   Faktor ukazuje, že lidé jsou často nespokojeni s 
%   informacemi o městských službách, údržbou ulic a
%   počtem komunitních akcí ve městě.
%
%   Tento faktor by mohl poukazovat na to, že město je
%   nedostatečně spravované a koná se zde málo akcí.
% 

% Faktor 2 = <{...},{D, X1-, X4-}> 
% (45 výskytů)
%   Faktor ukazuje, že spokojenost s bydlením není ovlivněna 
%   informacemi o městských službách a důvěrou lokální policii.
%
%   Lidé zde tedy nejspíš tyto věci ke spokojenosti nepotřebují.
%

% Faktor 3 = <{...},{X2+, X6-}>
% (55 výskytů)
%   Faktor ukazuje, že lidé jsou spokojeni s cenou bydlení a 
%   také, že komunitní akce se ve městě příliš nekonají.
%
%   Tento faktor opět poukazuje na slabý komunitní život,
%   ale levné bydlení.
%




function [A, B] = grecond_(I, cov)
[m, n] = size(I);
I = logical(I);
U = I;

A = false(m, 0);
B = false(0, n);

k = 0;

while ((sum(and((A*B), I),"all") / sum(I,"all")) < cov)
    D = false(1, n);    % set D to ∅
    v = 0;              % set V to 0            

    atr = find(any(U, 1));
    max_j = 1;


    while any(~D,"all")

        for j = atr(~D(atr))
            coverage = sum(max_cover(D, j, U, I),"all");
            if coverage > v
                v = coverage;
                max_j = j;
            end
        end
       
        old_D = D;
        D(max_j) = 1;
        D_down = downarrow(D,I);
        D = uparrow(D_down,I);

        temp = D_down * D;
        v = sum(temp & U,"all");

        if D == old_D
            break;
        end
        
    end

    k = k + 1;

    C = downarrow(D,I);
    A(:, k) = C;
    B(k, :) = D;

    U(C, D) = false;
end
    disp(['Počet faktorů = ', num2str(k)]);

end


function v = downarrow(C, I)
    cols = C;
    v = all(I(:,cols),2);
end



function v = uparrow(D, I)
    rows = D;
    v = all(I(rows,:));
end



function j = max_cover(D, j, U, I)
    D(j) = 1;
    D_union_j = D;
    
    D_down = downarrow(D_union_j, I);
    D_down_up = uparrow(D_down, I);

    
    temp = D_down * D_down_up;
    j = temp & U;
end

