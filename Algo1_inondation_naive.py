# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 18:25:08 2014

@author: Thibault

Algo 0

"""

import Gestion_reseau

def log(*texte):
    #print("Algo 0 : ", texte)
    return None

def lire_messages(ordinateur, date):
    q = ordinateur.messages_non_lus
    while not q.empty():
        message = q.get()
        if ordinateur.non_lu(message):
            ordinateur.lu(message)
            if ordinateur.id == message.infos[-1]: # Si destinataire
                log("Recu !", message.contenu)
            else:
                # Relai
                log(ordinateur.id, "relaie", message.contenu, message.infos)
                Gestion_reseau.envoi_message(message, ordinateur.id)
            
def envoyer_message(ordinateur, destinataire, date):
    contenu = str(ordinateur.id) + " dit bonjour a " + str(destinataire) + " !"
    message = Gestion_reseau.Message(ordinateur.id, "MESSAGE", contenu, date, [destinataire])
    Gestion_reseau.envoi_message(message, ordinateur.id)
    log("Envoye !", message.contenu)