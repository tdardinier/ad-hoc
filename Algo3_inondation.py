# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 18:25:08 2014

@author: Thibault

Algo 2

"""

import Gestion_reseau

def log(*texte):
    #print("Algo 2 : ", texte)
    return None

def lire_messages(ordinateur, date):
    q = ordinateur.messages_non_lus
    while not q.empty():
        message = q.get()
        if ordinateur.non_lu(message):
            ordinateur.lu(message)
            if message.type == "RECHERCHE_CHEMIN":
                if message.contenu == ordinateur.id:
                    log("Recherche terminée")
                    message_2 = Gestion_reseau.Message(ordinateur.id, "RETOUR_CHEMIN", str(message.infos), date, message.infos)
                    Gestion_reseau.envoi_message(message_2, ordinateur.id)                
                elif message.auteur != ordinateur.id:
                    new_chemin = message.infos
                    new_chemin.append(ordinateur.id)
                    message_2 = Gestion_reseau.Message(message.auteur, message.type, message.contenu, message.date, new_chemin)
                    Gestion_reseau.envoi_message(message_2, ordinateur.id)
            elif message.type == "RETOUR_CHEMIN":
                if ordinateur.id == message.infos[0]: # Si destinataire  
                    log(ordinateur.id, "peut envoyer à", message.auteur)                  
                    contenu = str(ordinateur.id) + " dit bonjour a " + str(message.auteur) + " !"
                    new_chemin = message.infos[1:] + [message.auteur]
                    message_2 = Gestion_reseau.Message(ordinateur.id, "MESSAGE", contenu, date, new_chemin)
                    Gestion_reseau.envoi_message(message_2, ordinateur.id)
                elif ordinateur.id in message.infos:
                    Gestion_reseau.envoi_message(message, ordinateur.id)
            elif message.type == "MESSAGE":
                if ordinateur.id == message.infos[-1]: # Si destinataire
                    log(message.contenu)
                    log(message.infos) 
                elif ordinateur.id in message.infos:
                    Gestion_reseau.envoi_message(message, ordinateur.id)

def envoyer_message(ordinateur, destinataire, date):
    message = Gestion_reseau.Message(ordinateur.id, "RECHERCHE_CHEMIN", destinataire, date, [ordinateur.id])
    Gestion_reseau.envoi_message(message, ordinateur.id)