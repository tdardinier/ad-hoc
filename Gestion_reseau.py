# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 17:57:17 2014

@author: Thibault

Gestion reseau

"""

import Queue
import pylab
import math
import random
import copy

# constantes

gros_envoyes = 0
petits_envoyes = 0
messages_en_attente = Queue.Queue()
ordinateurs = []
demi_periode = 10 # Periode à partir de laquelle on considère un lien comme non valide
# On envoie un message de lien à la demi-période
ecart = 3 # Demi-periode à +- 3
tour = 1

def log(*texte):
    print("Gestion reseau : ", texte)
    return None

def afficher_parc(ordinateurs):
    nb = 0
    for ordi1 in ordinateurs:
        ordi1.affichage()
        for ordi2 in ordinateurs:
            if distance(ordi1, ordi2) <= 1.:
                x = pylab.array([ordi1.position[0], ordi2.position[0]])
                y = pylab.array([ordi1.position[1], ordi2.position[1]])
                pylab.plot(x, y, "r")
                nb += 1
    log(nb)
    pylab.axis('equal')
    log("Debut")
    pylab.show()
    log("Fin")

class Message :
    def __init__(self, auteur, type, contenu, date, infos = []):
        self.auteur = auteur
        self.type = type
        self.contenu = contenu
        self.infos = infos
        self.date = date
        pass

class Ordinateur :
    
    def __init__(self, id, position) :
        self.position = position
        self.id = id
        self.messages_lus = Queue.Queue()
        self.messages_non_lus = Queue.Queue()
        self.vision_du_reseau = set() #liens
        self.restant = 0
        self.selecteurs_relais = set()
        pass
    
    def restart_periode(self):
        self.restant = random.randint(demi_periode - ecart, demi_periode + ecart)
    
    def non_lu(self, message):
        #Recherche dico ?
        for (contenu, date, tour) in self.messages_lus.queue:
            if (contenu == message.contenu and message.date == date):
                return False
        return True

    def lu(self, message):
        self.messages_lus.put((message.contenu, message.date, tour))

    def recevoir_message(self, message, provenance):
        self.messages_non_lus.put(message) # Provenance ?
    
    
    def affichage(self):
        (x0, y0) = self.position
        pylab.text(x0, y0, self.id, fontsize = 20)

def distance(ordi1, ordi2):
    return math.sqrt((ordi1.position[0] - ordi2.position[0])**2 + (ordi1.position[1] - ordi2.position[1])**2)

def envoi_message(message, provenance):
    # Efface les anciens
    for ordi in ordinateurs:
        msg = ordi.messages_lus
        if not msg.empty():
            while msg.queue[0][2] + (2 * demi_periode) < tour:
                msg.get()
    
    global gros_envoyes
    global petits_envoyes
 
    if tour >= 10:
        if message.type == "MESSAGE":
            gros_envoyes += 1
        petits_envoyes += len(message.infos)
    messages_en_attente.put((message, provenance))
    # Provenance : id de l'ordinateur qui envoie le message

def distribution_messages():
    q = messages_en_attente
    while not q.empty():
        (message, provenance) = q.get()
        ordi0 = ordinateurs[provenance]
        for ordi in ordinateurs:
            if distance(ordi, ordi0) <= 1 and ordi.id != provenance:
                message_2 = copy.deepcopy(message)
                ordi.recevoir_message(message_2, provenance)
                
                
