# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 18:25:08 2014

@author: Thibault

Algo 1

"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 18:25:08 2014

@author: Thibault

Algo 3

"""

import Gestion_reseau

def log(*texte):
    #print("Algo 5 : ", texte)
    return None

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
            elif message.type == "VOISIN_TROUVE":
                if (message.infos[0] == ordinateur.id):
                    ordinateur.vision_du_reseau.add((ordinateur.id, message.auteur))
                    new_voisins.append(message.auteur)
            elif message.type == "RECHERCHE_VOISIN":
                message_2 = Gestion_reseau.Message(ordinateur.id, "VOISIN_TROUVE", str((message.auteur, ordinateur.id)), date, [message.auteur])
                Gestion_reseau.envoi_message(message_2, ordinateur.id)
            elif message.type == "RECHERCHE_CHEMIN":
                if message.contenu == ordinateur.id:
                    log("Recherche terminée")
                    message_2 = Gestion_reseau.Message(ordinateur.id, "RETOUR_CHEMIN", str(message.infos), date, message.infos)
                    Gestion_reseau.envoi_message(message_2, ordinateur.id)                
                elif message.auteur != ordinateur.id:
                    new_chemin = message.infos
                    new_chemin.append(ordinateur.id)
                    message_2 = Gestion_reseau.Message(message.auteur, message.type, message.contenu, message.date, new_chemin)
                    futurs_messages_si_relais.append(message_2)                      
            elif message.type == "RETOUR_CHEMIN":
                if ordinateur.id == message.infos[0]: # Si destinataire  
                    log(ordinateur.id, "peut envoyer à", message.auteur)                  
                    contenu = str(ordinateur.id) + " dit bonjour a " + str(message.auteur) + " !"
                    new_chemin = message.infos[1:] + [message.auteur]
                    message_2 = Gestion_reseau.Message(ordinateur.id, "MESSAGE", contenu, date, new_chemin)
                    Gestion_reseau.envoi_message(message_2, ordinateur.id)
                elif ordinateur.id in message.infos: # Si dans le chemin
                    Gestion_reseau.envoi_message(message, ordinateur.id)
            elif message.type == "MESSAGE":
                if ordinateur.id == message.infos[-1]: # Si destinataire
                    log(message.contenu)
                    log(message.infos) 
                elif ordinateur.id in message.infos: # Si dans le chemin
                    Gestion_reseau.envoi_message(message, ordinateur.id)
    if est_relais(ordinateur):
        for message in futurs_messages_si_relais:
            Gestion_reseau.envoi_message(message, ordinateur.id)
        log(ordinateur.id, "est relai !")
        #log(ordinateur.vision_du_reseau)
    if len(new_voisins) > 0:
        #log("New voisins", ordinateur.id, new_voisins)
        message = Gestion_reseau.Message(ordinateur.id, "LIEN", "Voisins de" + str(ordinateur.id), date, [ordinateur.id] + new_voisins)
        Gestion_reseau.envoi_message(message, ordinateur.id)

def envoyer_message(ordinateur, destinataire, date):
    message = Gestion_reseau.Message(ordinateur.id, "RECHERCHE_CHEMIN", destinataire, date, [ordinateur.id])
    Gestion_reseau.envoi_message(message, ordinateur.id)

"""
def MPR(ordi_id, vision_du_reseau):
    n = ordi_id
    
    
    for (ordi1, ordi2) in vision_du_reseau:
        n = max(n, ordi1, ordi2)
    n = n + 1
    tableau_voisins = [set() for k in range(n)]
    for lien in vision_du_reseau:
        tableau_voisins[lien[0]].add(lien[1])
        tableau_voisins[lien[1]].add(lien[0])
    voisins = [i for i in tableau_voisins[ordi_id]]
    couvert = set([ordi_id])
    MPR = []
   
   # On cherche les voisins a 2 sauts    
    total = set([ordi_id])
    for voisin in voisins:
        total.add(voisin)
        for v in tableau_voisins[voisin]:
            total.add(v)
    n_tot = len(total)
      
    def efficacite(ordi):
        couvert_2 = set()
        for x in couvert:
            couvert_2.add(x)
        for voisin in tableau_voisins[ordi]:
            couvert_2.add(voisin)
        couvert_2.add(ordi)
        return len(couvert_2)
        
        
    while len(couvert) < n_tot:
        choisi = voisins[0]
        eff_m = efficacite(choisi)
        for voisin in voisins:
            if efficacite(voisin) > eff_m:
                eff_m = efficacite(voisin)
                choisi = voisin
        MPR.append(choisi)
        for voisin in tableau_voisins[choisi]:
            couvert.add(voisin)
        couvert.add(choisi)
    
    log("MPR", ordi_id, voisins, MPR)    
    
    return MPR
"""