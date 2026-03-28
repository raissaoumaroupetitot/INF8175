% Raissa Oumarou Petitot (2180935)
% NOM_ETUDIANT_2 (MATRICULE_2)

include "globals.mzn";

%-----------------------------------------------------------------------------%
% Variables de décisions
%-----------------------------------------------------------------------------%

% Nombre devant satisfaire les critères
var 1000..9999: nombre;

% Décomposition du nombre en un ensemble de chiffres
array[1..4] of var 1..9: chiffres;

%-----------------------------------------------------------------------------%
% Objectif
%-----------------------------------------------------------------------------%

% Variable à minimiser
var int: p;

%-----------------------------------------------------------------------------%
% Partie étudiant
%-----------------------------------------------------------------------------%
constraint p = chiffres[2]*chiffres[3]*chiffres[4];
constraint chiffres[1] = nombre div 1000;
constraint chiffres[2] = (nombre div 100) mod 10;
constraint chiffres[3] = (nombre div 10) mod 10;
constraint chiffres[4] = nombre mod 10;
constraint chiffres[1] > chiffres[2];
constraint chiffres[2] > chiffres[4];
constraint chiffres[3] < chiffres[4];
constraint chiffres[4] mod 2 = 0;
constraint sum(chiffres) > 15;

solve minimize p;
%-----------------------------------------------------------------------------%

output [
  show(nombre)
];

