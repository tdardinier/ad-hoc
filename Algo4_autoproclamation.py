# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 18:25:08 2014

@author: Thibault

Algo 3

"""

import Gestion_reseau

def log(*texte):
    #print("Algo 3 : ", texte)
    return None

def BFS(depart, arrivee, vision_du_reseau):
    n = depart
    for (ordi1, ordi2) in vision_du_reseau:
        n = max(n, ordi1, ordi2)
    n = n + 1
    tableau_voisins = [set() for k in range(n)]
    for lien in vision_du_reseau:
        tableau_voisins[lien[0]].add(lien[1])
        tableau_voisins[lien[1]].add(lien[0])
    q = [0, []]
    q[1].append(depart)
    actuel = depart
    vus = [-1 for k in range(n)]
    vus[depart] = depart
    while len(q[1]) > q[0] and actuel != arrivee:
        actuel = q[1][q[0]]
        q[0] += 1
        for voisin in tableau_voisins[actuel]:
            if vus[voisin] == -1:
                q[1].append(voisin)
                vus[voisin] = actuel
    if actuel != arrivee:
        return []
    else:
        chemin = []
        id_actuel = arrivee
        while id_actuel != depart:
            chemin.append(id_actuel)
            id_actuel = vus[id_actuel]
        chemin.reverse()
        return chemin

def est_relais(ordinateur):
    n = ordinateur.id
    for (ordi1, ordi2) in ordinateur.vision_du_reseau:
        n = max(n, ordi1, ordi2)
    n = n + 1
    tableau_voisins = [set() for k in range(n)]
    for lien in ordinateur.vision_du_reseau:
        tableau_voisins[lien[0]].add(lien[1])
        tableau_voisins[lien[1]].add(lien[0])
    voisinage = tableau_voisins[ordinateur.id]
    sous_voisinage = [voisin for voisin in voisinage if voisin > ordinateur.id]
    vu = {}
    for voisin in voisinage:
        vu[voisin] = False
    for voisin in sous_voisinage:
        for son_voisin in tableau_voisins[voisin]:
            if son_voisin in voisinage:
                vu[son_voisin] = True
    voisinage_couvert = True
    for voisin in voisinage:
        voisinage_couvert = voisinage_couvert and vu[voisin]
    return not voisinage_couvert

def lire_messages(ordinateur, date):
    ordinateur.restant -= 1
    if ordinateur.restant < 0 :
        message = Gestion_reseau.Message(ordinateur.id, "RECHERCHE_VOISIN", ordinateur.id, date)
        Gestion_reseau.envoi_message(message, ordinateur.id)
        ordinateur.restart_periode()
    q = ordinateur.messages_non_lus
    new_voisins = []
    futurs_messages_si_relais = []
    while not q.empty():
        message = q.get()
        if ordinateur.non_lu(message):
            ordinateur.lu(message)
            if message.type == "LIEN":
                pivot = message.infos[0]
                #log(ordinateur.id, "lien recu :", pivot, message.infos)
                for id in message.infos[1:]:                    
                    ordinateur.vision_du_reseau.add((pivot, id))
            elif message.type == "LIEN_RELAIS":
                pivot = message.infos[0]
                #log(ordinateur.id, "lien relais recu :", pivot, message.infos)
                for id in message.infos[1:]:                    
                    ordinateur.vision_du_reseau.add((pivot, id))
                futurs_messages_si_relais.append(message)
            elif message.type == "VOISIN_TROUVE":
                if (message.infos[0] == ordinateur.id):
                    ordinateur.vision_du_reseau.add((ordinateur.id, message.auteur))
                    new_voisins.append(message.auteur)
            elif message.type == "RECHERCHE_VOISIN":
                message_2 = Gestion_reseau.Message(ordinateur.id, "VOISIN_TROUVE", str((message.auteur, ordinateur.id)), date, [message.auteur])
                Gestion_reseau.envoi_message(message_2, ordinateur.id)
            elif message.type == "MESSAGE":
                if ordinateur.id == message.infos[-1]:
                # Si destinataire
                    log(message.contenu)
                    log(message.infos) 
                elif ordinateur.id in message.infos:
                    log(ordinateur.id, "relaie !")
                    Gestion_reseau.envoi_message(message, ordinateur.id)
    if est_relais(ordinateur):
        for message in futurs_messages_si_relais:
            Gestion_reseau.envoi_message(message, ordinateur.id)
        log(ordinateur.id, "est relai !")
        #log(ordinateur.vision_du_reseau)
    if len(new_voisins) > 0:
        #log("New voisins", ordinateur.id, new_voisins)
        type_message = "LIEN_RELAIS" if est_relais(ordinateur) else "LIEN"
        message = Gestion_reseau.Message(ordinateur.id, type_message, "Voisins de" + str(ordinateur.id), date, [ordinateur.id] + new_voisins)
        Gestion_reseau.envoi_message(message, ordinateur.id)

def envoyer_message(ordinateur, destinataire, date):
    chemin = BFS(ordinateur.id, destinataire, ordinateur.vision_du_reseau)
    contenu = str(ordinateur.id) + " dit bonjour a " + str(destinataire) + " !"
    message = Gestion_reseau.Message(ordinateur.id, "MESSAGE", contenu, date, chemin)
    if chemin != []:
        Gestion_reseau.envoi_message(message, ordinateur.id)
        log("De", ordinateur.id, "a", destinataire, "chemin", chemin)
    else:
        log("Annule !")