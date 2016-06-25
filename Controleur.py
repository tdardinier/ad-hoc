# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 18:44:33 2014

@author: Thibault

Controlleur

"""

import Algo1_inondation_naive
import Algo2_vision_globale
import Algo3_inondation
import Algo4_autoproclamation
import Algo5_relais
import Gestion_reseau
import math
import random
import time
import datetime

# constantes

duree = 110 # tours

algos = []
algos.append(Algo1_inondation_naive)
algos.append(Algo2_vision_globale)
algos.append(Algo3_inondation)
algos.append(Algo4_autoproclamation)
algos.append(Algo5_relais)

def log(*texte):
    print("Controleur : ", texte)
    return None

def alea(min, max):
    return random.random() * (max - min) + min

def save(id_algos, mini, maxi, pas, cartes, mode, src):
    mon_fichier = open(src + ".tipe", "w")
    now = datetime.datetime.now()
    mon_fichier.write(str(now.day) + "/" + str(now.month) + "/" + str(now.year))
    mon_fichier.write("\n")
    mon_fichier.write(mode)
    mon_fichier.write(", de " + str(mini) + " à " + str(maxi) + " avec un pas de " + str(pas) + " sur " + str(cartes))
    mon_fichier.write("\n")
    t0 = time.time()
    etendue = maxi - mini
    ns = [mini + k * pas for k in range(int(etendue // pas) + 1)]
    for n in ns:
        for k in id_algos:
            for carte in cartes:
                (gros, petits) = go(k, 0.1, n, 15, carte) if mode == "n" else go(k, n, 20, 15, carte)
                S = ""
                S += str(k) + ","
                S += str(n) + ",0.1," if mode == "n" else "20," + str(n) + ","      
                S += str(carte) + ",15,"       
                S += str(duree) + ","       
                S += str(gros) + ","
                S += str(petits) + "\n"
                mon_fichier.write(S)
        log("Fini :", n)
    log("Go", time.time() - t0)
    mon_fichier.close()

def go(ialgo, frequence = 0.1, n = 20, demi_periode = 15, carte = 833):
    t0 = time.time()
    Gestion_reseau.gros_envoyes = 0
    Gestion_reseau.petits_envoyes = 0
    Gestion_reseau.ordinateurs = generate_connexe(n, carte)
    #Gestion_reseau.afficher_parc(Gestion_reseau.ordinateurs)
    Gestion_reseau.demi_periode = demi_periode
    #Gestion_reseau.afficher_parc(Gestion_reseau.ordinateurs)
    log("Duree : ", duree)
    for t in range(1, duree + 1):
        Gestion_reseau.tour = t
        if (t % max(duree//20, 1)) == 0:
            log("Tour :", t, "Algo :", ialgo)
        for ordi in Gestion_reseau.ordinateurs:
            algos[ialgo].lire_messages(ordi, t)
            if t >= 10 and random.random() < frequence:
                destinataire = random.randint(0, n - 1)
                if destinataire != ordi.id:
                    algos[ialgo].envoyer_message(ordi, destinataire, t)
        Gestion_reseau.distribution_messages()
    log("Temps : ", time.time() - t0)
    return (Gestion_reseau.gros_envoyes, Gestion_reseau.petits_envoyes)

def voir_graphe(n, carte):
    Gestion_reseau.afficher_parc(generate_connexe(n, carte))

def generate_connexe(n, carte):
    random.seed(carte)
    Ordis = [Gestion_reseau.Ordinateur(0, (0., 0.))]
    for k in range(1, n):
        ordi_voisin = (Ordis[random.randint(0, (len(Ordis)) - 1)]).position
        angle = alea(0, 2 * math.pi)
        x = ordi_voisin[0] + math.cos(angle) * 0.99
        y = ordi_voisin[1] + math.sin(angle) * 0.99
        Ordis.append(Gestion_reseau.Ordinateur(k, (x, y)))
    return Ordis
