Ai_immage = False

if Ai_immage :
    import base64
    import requests
    import os

    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

    body = {
    "steps": 40,
    "width": 1024,
    "height": 1024,
    "seed": 0,
    "cfg_scale": 5,
    "samples": 1,
    "style_preset": "digital-art",
    "text_prompts": [
        {
        "text": "a galaxie in the space",
        "weight": 1
        },
        {
        "text": "astraunaut",
        "weight": -1
        }
    ],
    }

    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer sk-n8KjdvWiufDHJXB7ZeE0BAAcyrugyPPA4VmhCjmc6JKpusno",
    }

    response = requests.post(
    url,
    headers=headers,
    json=body,
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    # make sure the out directory exists
    if not os.path.exists("space image"):
        os.makedirs("space image")

    for i, image in enumerate(data["artifacts"]):
        image_espace = f'space image/txt2img_{image["seed"]}.png'
        with open(f'space image/txt2img_{image["seed"]}.png', "wb") as f:
            f.write(base64.b64decode(image["base64"]))
    
else :
    image_espace = "space image/default.png"



import copy
import random
import math
import pygame
import IA
import marshal
import gc

pygame.init()


debug = False

arrière_plan = False

acceleration = 0.1

vitesses = [0,0]

coordinate_in_chunk = [0,0]


chunk_coordinate = [0,0]

objectif = [0,0,10]

entrainement_IA = False
pilotage_IA = False

#marshal.dump([[[[1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1],[1,1,1],[1,1,1,1]],[[[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]],[[1,1,1],[1,1,1],[1,1,1]],[[1,1,1,1],[1,1,1,1],[1,1,1,1]]]]],open("IA_save","wb"))

IA_reseau = marshal.load(open("IA_save","rb"))

pilotage_auto = IA.IA(IA_reseau[0][0],IA_reseau[0][1])
#pilotage_auto = IA.IA(IA_reseau[0],IA_reseau[1])


nombre_IA_références = 50


"""
for i in range(1000):
    pilotage_auto.mutation()
"""
"""
print(pilotage_auto.layers)
print(pilotage_auto.links)

"""

vaisseau = pygame.surface.Surface.subsurface(pygame.image.load("sprites/vaisseau.png"),(10,7,24,23))
vaisseau.set_colorkey((0,0,0))

vaisseau_directions = {"g" : pygame.surface.Surface.subsurface(pygame.image.load("sprites/vaisseau.png"),(41,10,4,17)),
                       "d" : pygame.surface.Surface.subsurface(pygame.image.load("sprites/vaisseau.png"),(67,10,4,17)),
                       "h" : pygame.surface.Surface.subsurface(pygame.image.load("sprites/vaisseau.png"),(47,4,18,4)),
                       "b" : pygame.surface.Surface.subsurface(pygame.image.load("sprites/vaisseau.png"),(47,29,18,4))
                       }

for a in ["g","b","d","h"]:
    vaisseau_directions[a].set_colorkey((0,0,0))


toile_vaisseau = pygame.surface.Surface((30,29),pygame.SRCALPHA)

def redessiner_espace(nb_étoile,taille_étoile,debug,total_aléatoir,nb_chunks,taille_chunk):
    chunks = []
    for x in range(nb_chunks):
        chunks.append([])
        for y in range(nb_chunks):
            chunks[x].append(pygame.surface.Surface((taille_chunk,taille_chunk),pygame.SRCALPHA))
            if debug :
                chunks[x][y].fill((255,0,0))
                chunks[x][y].fill((0,0,0,0),(1,1,taille_chunk-1,taille_chunk-1))
            for a in range(nb_étoile):
                taille = random.randint(1,taille_étoile)
                étoile_x = random.randint(0,taille_chunk-taille)
                étoile_y = random.randint(0,taille_chunk-taille)
                if total_aléatoir:
                    pygame.draw.ellipse(chunks[x][y],(random.randint(0,255),random.randint(0,255),random.randint(0,255)),(étoile_x,étoile_y,taille,taille))
                else:
                    pygame.draw.ellipse(chunks[x][y],(random.randint(180,220),random.randint(180,220),random.randint(80,120)),(étoile_x,étoile_y,taille,taille))
            if debug :
                pygame.draw.ellipse(chunks[x][y],(random.randint(200,255),random.randint(0,150),random.randint(0,150)),(random.randint(0,taille_chunk-taille_étoile*2),random.randint(0,taille_chunk-taille_étoile*2),taille_étoile*2,taille_étoile*2))
    return chunks

nb_chunk = 20
chunk_size = 200

chunks = redessiner_espace(10,20,False,True,nb_chunk,chunk_size)

# "grande vue" , "zoom"
vision = "grande vue"

# sauvegarde
def save_data(save): 
    sauvegarde = ""
    for line in save :
        if sauvegarde != "":
            if sauvegarde[-1] != "\n" :
                sauvegarde += "\n"
        sauvegarde += str(line)
    open("save","w").write(sauvegarde)

save = open("save","r").readlines()

# écran

screen_size = (int(save[0]),int(save[1]))

screen = pygame.display.set_mode(screen_size,pygame.RESIZABLE)
(screen_size)

toile_espace_large = pygame.surface.Surface((850,850))
toile_espace_large.fill((0,0,0))
if arrière_plan :
    toile_espace_large.blit(pygame.transform.scale(pygame.image.load(image_espace),(850,850)),(0,0))
for x in range(20):
    for y in range(20):
        toile_espace_large.blit(pygame.transform.scale(chunks[x][y],(42.5,42.5)),(x*42.5,y*42.5))
        

toile_map_espace_large = pygame.surface.Surface((850,850))

toile_espace_restrein = pygame.surface.Surface((850,850))

toile_interface = pygame.surface.Surface((1600,900))
toile_interface.fill((255,255,255))


pygame.draw.rect(toile_interface,(128,128,128),(940,80,120,40))
label = pygame.font.Font("font/undertale.ttf",20).render("Avancer",False,(0,0,0))
toile_interface.blit(label,(950,90))

pygame.draw.rect(toile_interface,(128,128,128),(940,140,120,40))
label = pygame.font.Font("font/undertale.ttf",20).render("Arêter",False,(0,0,0))
toile_interface.blit(label,(955,150))

pygame.draw.rect(toile_interface,(100,100,200),(940,230,180,40))
label = pygame.font.Font("font/undertale.ttf",20).render("plan large",False,(0,0,0))
toile_interface.blit(label,(955,240))

pygame.draw.rect(toile_interface,(100,100,200),(1200,230,180,40))
label = pygame.font.Font("font/undertale.ttf",20).render("gros plan",False,(0,0,0))
toile_interface.blit(label,(1215,240))

pygame.draw.rect(toile_interface,(100,200,100),(940,300,230,40))
label = pygame.font.Font("font/undertale.ttf",20).render("mod developeur",False,(0,0,0))
toile_interface.blit(label,(955,310))

pygame.draw.rect(toile_interface,(200,100,200),(940,350,300,40))
label = pygame.font.Font("font/undertale.ttf",20).render("couleurs alléatoires",False,(0,0,0))
toile_interface.blit(label,(955,360))

pygame.draw.rect(toile_interface,(200,100,100),(940,800,300,40))
label = pygame.font.Font("font/undertale.ttf",20).render("redessiner l'espace",False,(0,0,0))
toile_interface.blit(label,(955,810))

pygame.draw.rect(toile_interface,(200,150,100),(940,400,300,40))
label = pygame.font.Font("font/undertale.ttf",20).render("friction du vide",False,(0,0,0))
toile_interface.blit(label,(955,410))

pygame.draw.rect(toile_interface,(50,50,50),(1300,300,200,40))
label = pygame.font.Font("font/undertale.ttf",20).render("arrière plan",False,(0,0,0))
toile_interface.blit(label,(1310,310))

pygame.draw.rect(toile_interface,(100,50,50),(1200,80,50,40))
label = pygame.font.Font("font/undertale.ttf",20).render("IA",False,(0,0,0))
toile_interface.blit(label,(1210,90))

pygame.draw.rect(toile_interface,(100,50,50),(1200,140,250,40))
label = pygame.font.Font("font/undertale.ttf",20).render("IA entrainement",False,(0,0,0))
toile_interface.blit(label,(1210,150))


friction = False
random_color = True
atension = ""
buton_atension = ""
lettre_appuye = []
run = True

value_toile = {"acceleration" : pygame.surface.Surface((195,30)),"étoiles" : pygame.surface.Surface((195,30)),"taille" : pygame.surface.Surface((195,30)),"taille_chunk" : pygame.surface.Surface((195,30)),"nombre_chunk" : pygame.surface.Surface((195,30))}
values = {"acceleration" : str(acceleration),"étoiles" : "20","taille" : "10","taille_chunk" : str(chunk_size),"nombre_chunk" : str(nb_chunk)}


label = pygame.font.Font("font/undertale.ttf",20).render("accélération",False,(0,0,0))
toile_interface.blit(label,(950,500))

label = pygame.font.Font("font/undertale.ttf",20).render("taille des étoiles",False,(0,0,0))
toile_interface.blit(label,(950,600))

label = pygame.font.Font("font/undertale.ttf",20).render("étoiles par chunk",False,(0,0,0))
toile_interface.blit(label,(950,700))

label = pygame.font.Font("font/undertale.ttf",20).render("taille des chunks",False,(0,0,0))
toile_interface.blit(label,(1300,500))

label = pygame.font.Font("font/undertale.ttf",20).render("nombre de chunks",False,(0,0,0))
toile_interface.blit(label,(1300,600))

génération = 0
top = IA_reseau
temps = 0


simulation_circuit = 0


while run :
    
            
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            run = False
    
    if entrainement_IA :
        
        boucle = 1
        if génération % 1 == 0 or pygame.mouse.get_pressed()[0] or max_touche > 2:
            boucle = 0
            for i in temps_simulation[:max_touche+1]:
                boucle += i
            temps = 0
        pilotage_IA = True
    else :
        boucle = 1
        
    for boucle_entrainement_ia_meilleur_IA in range(boucle):
        
        temps += 1
    
        # récupération d'évents

        if pygame.mouse.get_pressed()[0]:
            souris += 1
        else : 
            souris = 0

        if souris == 1 :
            souris_pressed = True
        else : 
            souris_pressed = False
        
        #changement de la taille de la fenêtre
        if screen_size != screen.get_size():
            
            screen_size = screen.get_size()
            
            save = open("save","r").readlines()
            print(save)
            save[0],save[1] = screen_size[0],screen_size[1]
            save_data(save)
        
        #détection pressage de bouton de l'interface
        if souris_pressed : 
            
            temps = 0
            
            souris_pos = pygame.mouse.get_pos()[0]/screen_size[0]*1600,pygame.mouse.get_pos()[1]/screen_size[1]*900
            
            print(souris_pos)
            print(chunk_coordinate)
            print(coordinate_in_chunk)
            
            
            atension = ""
            buton_atension = ""
            
            if pygame.rect.Rect(940,230,180,40).collidepoint(souris_pos[0],souris_pos[1]):
                vision = "grande vue"
                
            if pygame.rect.Rect(1200,230,180,40).collidepoint(souris_pos[0],souris_pos[1]):
                vision = "petite vue"
                
            if pygame.rect.Rect(940,80,120,40).collidepoint(souris_pos[0],souris_pos[1]):
                vitesses[0] += acceleration*50
                
            if pygame.rect.Rect(940,140,120,40).collidepoint(souris_pos[0],souris_pos[1]):
                vitesses = [0,0]
                
            if pygame.rect.Rect(950,550,195,30).collidepoint(souris_pos[0],souris_pos[1]):
                atension = "valeur"
                buton_atension = "acceleration"
                
            if pygame.rect.Rect(950,650,195,30).collidepoint(souris_pos[0],souris_pos[1]):
                atension = "valeur"
                buton_atension = "taille"
                
            if pygame.rect.Rect(950,750,195,30).collidepoint(souris_pos[0],souris_pos[1]):
                atension = "valeur"
                buton_atension = "étoiles"
                
            if pygame.rect.Rect(1300,550,195,30).collidepoint(souris_pos[0],souris_pos[1]):
                atension = "valeur"
                buton_atension = "taille_chunk"
                
            if pygame.rect.Rect(1300,650,195,30).collidepoint(souris_pos[0],souris_pos[1]):
                atension = "valeur"
                buton_atension = "nombre_chunk"
                
            if pygame.rect.Rect(940,300,230,40).collidepoint(souris_pos[0],souris_pos[1]):
                debug = not debug
                
            if pygame.rect.Rect(940,350,300,40).collidepoint(souris_pos[0],souris_pos[1]):
                random_color = not random_color
                
            if pygame.rect.Rect(940,800,300,40).collidepoint(souris_pos[0],souris_pos[1]):
                chunks = redessiner_espace(int(values["étoiles"]),int(values["taille"]),debug,random_color,int(values["nombre_chunk"]),int(values["taille_chunk"]))
                toile_espace_large.fill((0,0,0))
                if arrière_plan :
                    toile_espace_large.blit(pygame.transform.scale(pygame.image.load(image_espace),(850,850)),(0,0))
                nb_chunk = int(values["nombre_chunk"])
                chunk_size = int(values["taille_chunk"])
                for x in range(nb_chunk):
                    for y in range(nb_chunk):
                        toile_espace_large.blit(pygame.transform.scale(chunks[x][y],(850/nb_chunk,850/nb_chunk)),(x*850/nb_chunk,y*850/nb_chunk))
                        
            if pygame.rect.Rect(940,400,300,40).collidepoint(souris_pos[0],souris_pos[1]):
                friction = not friction

            if pygame.rect.Rect(1300,300,200,40).collidepoint(souris_pos[0],souris_pos[1]):
                arrière_plan = not arrière_plan
                
            if pygame.rect.Rect(1200,80,50,40).collidepoint(souris_pos[0],souris_pos[1]):
                pilotage_IA = not pilotage_IA
                
            if pygame.rect.Rect(1200,140,250,40).collidepoint(souris_pos[0],souris_pos[1]):
                entrainement_IA = not entrainement_IA

        # affichage + changement de valeurs des boutons de l'interface
        for butons in ["acceleration","étoiles","taille","nombre_chunk","taille_chunk"]:
            if atension == "valeur" and butons == buton_atension:
                value_toile[butons].fill((128,128,128))
                    
                keys = pygame.key.get_pressed()
                for key in range(len(keys)):
                    
                    if keys[key] :
                        lettre = pygame.key.name(key)
                        if not key in lettre_appuye:
                            if lettre in "1234567890":
                                if values[buton_atension] == "0" :
                                    values[buton_atension] = lettre
                                else :
                                    values[buton_atension] += lettre
                            elif lettre in ",;":
                                if buton_atension == "acceleration":
                                    values[buton_atension] += "."
                            elif lettre in ["escape","return"]:
                                atension = ""
                            elif lettre in ["backspace"]:
                                values[buton_atension] = values[buton_atension][:len(values[buton_atension])-1]
                                if values[buton_atension] == "":
                                    values[buton_atension] = "0"
                            else :
                                print(lettre)
                            print(values[buton_atension])
                            print(lettre_appuye)
                            lettre_appuye.append(key)
                    
                    else :
                        if key in lettre_appuye:
                            lettre_appuye.remove(key)
            else :
                value_toile[butons].fill((100,100,100))
                acceleration = float(values["acceleration"])
            
            label = pygame.font.Font("font/undertale.ttf",20).render(str(values[butons]),False,(0,0,0))
            value_toile[butons].blit(label,(0,0))
        
        #if not entrainement_IA:
        
        if True:
        
            toile_vaisseau.fill((0,0,0,0))
            toile_vaisseau.blit(vaisseau,(3,3))
            
            # appuyer sur les boutons
            if not pilotage_IA : 
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    vitesses[0] -= acceleration
                    toile_vaisseau.blit(vaisseau_directions["d"],(26,6))
                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    vitesses[0] += acceleration
                    toile_vaisseau.blit(vaisseau_directions["g"],(0,6))
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    vitesses[1] += acceleration
                    toile_vaisseau.blit(vaisseau_directions["h"],(6,0))
                if pygame.key.get_pressed()[pygame.K_UP]:
                    vitesses[1] -= acceleration
                    toile_vaisseau.blit(vaisseau_directions["b"],(6,25))
            
            
            coordonées = [(chunk_coordinate[0]*chunk_size+coordinate_in_chunk[0])*850/nb_chunk/chunk_size,(chunk_coordinate[1]*chunk_size+coordinate_in_chunk[1])*850/nb_chunk/chunk_size]
            taille_vaisseau = round(85000/(nb_chunk*chunk_size))
            
            if abs((coordonées[0]+taille_vaisseau/2)-(objectif[0]+objectif[2]/2)) < 425 :
                dist_x = abs((coordonées[0]+taille_vaisseau/2)-(objectif[0]+objectif[2]/2))
            else :
                dist_x = 850-abs((coordonées[0]+taille_vaisseau/2)-(objectif[0]+objectif[2]/2))
            
            if abs((coordonées[1]+taille_vaisseau/2)-(objectif[1]+objectif[2]/2)) < 425 :
                dist_y = abs((coordonées[1]+taille_vaisseau/2)-(objectif[1]+objectif[2]/2))
            else :
                dist_y = 850-abs((coordonées[1]+taille_vaisseau/2)-(objectif[1]+objectif[2]/2))
            
            
            if dist_x <= (taille_vaisseau+objectif[2])/2 and dist_y <= (taille_vaisseau+objectif[2])/2:
                print(temps)
                temps = 0
                if entrainement_IA:
                    num_objectif += 1
                    if num_objectif == len(liste_pos_objectif):
                        num_objectif = 0
                    objectif[0] = int(liste_pos_objectif[num_objectif][0])
                    objectif[1] = int(liste_pos_objectif[num_objectif][1])
                else :
                    objectif[0] = random.randint(0,850-objectif[2])
                    objectif[1] = random.randint(0,850-objectif[2])
            
            
            # pilotage automatique, appuis sur les boutons
            if pilotage_IA :
                

                
                inputs_pilotage = []

                
                
                #coordonées du vaisseau
                inputs_pilotage.append(coordonées[0])
                inputs_pilotage.append(coordonées[1])
                
                #vitesse du vaisseau
                inputs_pilotage.append(vitesses[0])
                inputs_pilotage.append(vitesses[1])
                
                #accélération du vaisseau
                inputs_pilotage.append(acceleration)
                
                #taille de la map
                inputs_pilotage.append(nb_chunk*chunk_size)
                
                #friction du vide activée
                if friction :
                    inputs_pilotage.append(1)
                else :
                    inputs_pilotage.append(0)
                
                # coordonées de l'objectif
                inputs_pilotage.append(objectif[0])
                inputs_pilotage.append(objectif[1])
                
                #taille de l'objectif
                inputs_pilotage.append(objectif[2])
                
                #distance de la cible
                inputs_pilotage.append(dist_x)
                inputs_pilotage.append(dist_y)
                
                # longueure de l'input :  12
                
                output_pilotage = pilotage_auto.fonction(inputs_pilotage)
                
                
                
                #haut
                if output_pilotage[0] > 0.9 :
                    vitesses[1] -= acceleration
                    toile_vaisseau.blit(vaisseau_directions["b"],(6,25))
                #bas
                if output_pilotage[1] > 0.9 :
                    vitesses[1] += acceleration
                    toile_vaisseau.blit(vaisseau_directions["h"],(6,0))
                #gauche
                if output_pilotage[2] > 0.9 :
                    vitesses[0] -= acceleration
                    toile_vaisseau.blit(vaisseau_directions["d"],(26,6))
                #droite
                if output_pilotage[3] > 0.9 :
                    vitesses[0] += acceleration
                    toile_vaisseau.blit(vaisseau_directions["g"],(0,6))
            
            
            coordinate_in_chunk[0] += vitesses[0]
            coordinate_in_chunk[1] += vitesses[1]
            
            
            
            # effet de la fricion du vide
            if friction :
                if vitesses[0] < 0 :
                    vitesses[0] -= vitesses[0]/100
                    if vitesses[0] > 0 :
                        vitesses[0] = 0
                if vitesses[1] < 0 :
                    vitesses[1] -= vitesses[1]/100
                    if vitesses[1] > 0 :
                        vitesses[1] = 0
                if vitesses[0] > 0 :
                    vitesses[0] -= vitesses[0]/100
                    if vitesses[0] < 0 :
                        vitesses[0] = 0
                if vitesses[1] > 0 :
                    vitesses[1] -= vitesses[1]/100
                    if vitesses[1] < 0 :
                        vitesses[1] = 0
            
            #reglage position du joueur par rapport aux chunks
            while coordinate_in_chunk[0] > chunk_size :
                chunk_coordinate[0] += 1
                coordinate_in_chunk[0] -= chunk_size
            while coordinate_in_chunk[0] < 0 :
                chunk_coordinate[0] -= 1
                coordinate_in_chunk[0] += chunk_size
            while coordinate_in_chunk[1] > chunk_size :
                chunk_coordinate[1] += 1
                coordinate_in_chunk[1] -= chunk_size
            while coordinate_in_chunk[1] < 0 :
                chunk_coordinate[1] -= 1
                coordinate_in_chunk[1] += chunk_size
            
            while chunk_coordinate[0] > nb_chunk-1:
                chunk_coordinate[0] -= nb_chunk
            while chunk_coordinate[0] < 0:
                chunk_coordinate[0] += nb_chunk
            while chunk_coordinate[1] > nb_chunk-1:
                chunk_coordinate[1] -= nb_chunk
            while chunk_coordinate[1] < 0:
                chunk_coordinate[1]  += nb_chunk

            
            
            # affichage de la grande vue
            if vision == "grande vue" :
                
                coordonées = [(chunk_coordinate[0]*chunk_size+coordinate_in_chunk[0])*850/nb_chunk/chunk_size,(chunk_coordinate[1]*chunk_size+coordinate_in_chunk[1])*850/nb_chunk/chunk_size]
                
                
                if taille_vaisseau < 5 : 
                    taille_vaisseau = 5
                
                toile_map_espace_large.blit(toile_espace_large,(0,0))
                coordonées = [(chunk_coordinate[0]*chunk_size+coordinate_in_chunk[0])*850/nb_chunk/chunk_size,(chunk_coordinate[1]*chunk_size+coordinate_in_chunk[1])*850/nb_chunk/chunk_size]
                toile_map_espace_large.blit(pygame.transform.scale(toile_vaisseau,(taille_vaisseau,taille_vaisseau)),coordonées)
                
                
                
                
                redessine = 0
                if coordonées[0] > 850-taille_vaisseau :
                    toile_map_espace_large.blit(pygame.transform.scale(toile_vaisseau,(taille_vaisseau,taille_vaisseau)),(coordonées[0]-850,coordonées[1]))
                    redessine += 1
                if coordonées[1] > 850-taille_vaisseau:
                    toile_map_espace_large.blit(pygame.transform.scale(toile_vaisseau,(taille_vaisseau,taille_vaisseau)),(coordonées[0],coordonées[1]-850))
                    redessine += 1
                
                if redessine == 2 :
                    toile_map_espace_large.blit(pygame.transform.scale(toile_vaisseau,(taille_vaisseau,taille_vaisseau)),(coordonées[0]-850,coordonées[1]-850))
                
                
                pygame.draw.ellipse(toile_map_espace_large,(255,255,255),(objectif[0],objectif[1],objectif[2],objectif[2]))
                
                toile_interface.blit(toile_map_espace_large,(50,25))
                
                
            
            # affichage de la petite vue
            if vision == "petite vue" :
                
                toile_interface.blit(toile_espace_restrein,(50,25))
                toile_espace_restrein.fill((0,0,0))
                for plan_x in range(round(850/chunk_size+1.5)):
                    
                    pos_plan_x = plan_x
                    chunk_plan_x = plan_x-round(425/chunk_size)+chunk_coordinate[0]
                    
                    while chunk_plan_x < 0 :
                        chunk_plan_x += nb_chunk
                    while chunk_plan_x > nb_chunk-1 :
                        chunk_plan_x -= nb_chunk
                        
                    for plan_y in range(round(850/chunk_size+1.5)):
                        
                        pos_plan_y = plan_y
                        chunk_plan_y = plan_y-round(425/chunk_size)+chunk_coordinate[1]
                        
                        while chunk_plan_y < 0 :
                            chunk_plan_y += nb_chunk
                        while chunk_plan_y > nb_chunk-1 :
                            chunk_plan_y -= nb_chunk
                        
                        toile_espace_restrein.blit(chunks[chunk_plan_x][chunk_plan_y],(pos_plan_x*chunk_size-coordinate_in_chunk[0],pos_plan_y*chunk_size-coordinate_in_chunk[1]))
                
                
                
                toile_interface.blit(pygame.transform.scale(toile_vaisseau,(50,50)),(425,412))
            
        
            toile_interface.blit(value_toile["acceleration"],(950,550))
            toile_interface.blit(value_toile["taille"],(950,650))
            toile_interface.blit(value_toile["étoiles"],(950,750))
            toile_interface.blit(value_toile["taille_chunk"],(1300,550))
            toile_interface.blit(value_toile["nombre_chunk"],(1300,650))
            
            screen.blit(pygame.transform.scale(toile_interface,screen_size),(0,0))
            
            pygame.display.update()

    
    if entrainement_IA:
        
        
        friction = 1
        
        """
        #if top == []:
        if True :
        
            Résaux_de_nerones = [[pilotage_auto.get_layers(),pilotage_auto.get_links()]]
        
            for création_réseau in range(1,100):
                réseau_temporaire = IA.IA(pilotage_auto.get_layers().copy(),pilotage_auto.get_links().copy())
                for i in range(random.randint(1,10)):
                    réseau_temporaire.mutation()
                Résaux_de_nerones.append([copy.deepcopy(réseau_temporaire.get_layers()),copy.deepcopy(réseau_temporaire.get_links())])
        
        else :
        """
        Résaux_de_nerones = []
        for a in range(nombre_IA_références) :
            
            Résaux_de_nerones.append(top[a])
            
            for création_réseau in range(1,20):
                réseau_temporaire = IA.IA(copy.deepcopy(top[a][0]),copy.deepcopy(top[a][1]))
                réseau_temporaire.mutation()
                Résaux_de_nerones.append([copy.deepcopy(réseau_temporaire.get_layers()),copy.deepcopy(réseau_temporaire.get_links())])
                del réseau_temporaire
                
                

        longueure_réseau = len(Résaux_de_nerones)
        print(longueure_réseau)
        
        # définir la coordonée de l'objectif
        """
        liste_pos_objectif = []
        
        liste_pos_objectif.append((random.randint(0,850-objectif[2]),random.randint(0,850-objectif[2])))
        for a in range(1,100):
            liste_pos_objectif.append((random.randint(0,850-objectif[2]),random.randint(0,850-objectif[2])))
            while pygame.rect.Rect(liste_pos_objectif[a-1][0]-100,liste_pos_objectif[a-1][1]-100,objectif[2]+200,objectif[2]+200).colliderect([liste_pos_objectif[a][0],liste_pos_objectif[a][1],objectif[2],objectif[2]]):
                liste_pos_objectif[a] = (random.randint(0,850-objectif[2]),random.randint(0,850-objectif[2]))
        """
        
        list_score = []
        
        pos_sim_chunk = [random.randint(0,nb_chunk),random.randint(0,nb_chunk)]
        pos_sim_in_chunk = [random.randint(0,chunk_size),random.randint(0,chunk_size)]
        coordonées = [(chunk_coordinate[0]*chunk_size+coordinate_in_chunk[0])*850/nb_chunk/chunk_size,(chunk_coordinate[1]*chunk_size+coordinate_in_chunk[1])*850/nb_chunk/chunk_size]
        
        # définir la coordonné du vaisseau
        """
        while pygame.rect.Rect(liste_pos_objectif[0][0]-100,liste_pos_objectif[0][1]-100,objectif[2]+200,objectif[2]+200).colliderect([coordonées[0],coordonées[1],taille_vaisseau,taille_vaisseau]):
            pos_sim_chunk = [random.randint(0,nb_chunk),random.randint(0,nb_chunk)]
            pos_sim_in_chunk = [random.randint(0,chunk_size),random.randint(0,chunk_size)]
            coordonées = [(chunk_coordinate[0]*chunk_size+coordinate_in_chunk[0])*850/nb_chunk/chunk_size,(chunk_coordinate[1]*chunk_size+coordinate_in_chunk[1])*850/nb_chunk/chunk_size]
        """
        
        
        print(coordonées)
        au_dessus_de_100 = 0
        touche_3 = 0
        max_touche = 0
        
        for gen in range(0,longueure_réseau):
            
            IA_entrainement = IA.IA(Résaux_de_nerones[gen][0],Résaux_de_nerones[gen][1])
            score = 0
            touche = 0
            
            print(gen,end="\r")
            
            for simulation_circuit in range(1,5):
            
                if simulation_circuit == 1:
                    liste_pos_objectif = [(300,191),(191,191),(50,100),(800,200),(0,200)]
                    temps_simulation = [200,200,200,300,200]
                    pos_sim_chunk = [4,6]
                    pos_sim_in_chunk = [100,100]
                    coordonées = [(pos_sim_chunk[0]*chunk_size+pos_sim_in_chunk[0])*850/nb_chunk/chunk_size,(pos_sim_chunk[1]*chunk_size+pos_sim_in_chunk[1])*850/nb_chunk/chunk_size]
                if simulation_circuit == 2:
                    liste_pos_objectif = [(500,500),(600,500),(600,700),(450,700)]
                    temps_simulation = [250,300,250,250]
                    pos_sim_chunk = [13,13]
                    pos_sim_in_chunk = [200,200]
                    coordonées = [(pos_sim_chunk[0]*chunk_size+pos_sim_in_chunk[0])*850/nb_chunk/chunk_size,(pos_sim_chunk[1]*chunk_size+pos_sim_in_chunk[1])*850/nb_chunk/chunk_size]
                if simulation_circuit == 3:
                    liste_pos_objectif = [(100,500),(425,425),(500,500),(400,400),(600,600),(0,0)]
                    temps_simulation = [300,400,250,300,250,500]
                    pos_sim_chunk = [10,10]
                    pos_sim_in_chunk = [0,0]
                    coordonées = [(pos_sim_chunk[0]*chunk_size+pos_sim_in_chunk[0])*850/nb_chunk/chunk_size,(pos_sim_chunk[1]*chunk_size+pos_sim_in_chunk[1])*850/nb_chunk/chunk_size]
                if simulation_circuit == 4:
                
                    liste_pos_objectif = []
                    liste_pos_objectif.append((random.randint(0,850-objectif[2]),random.randint(0,850-objectif[2])))
                    temps_simulation = [750]
                    for a in range(1,5):
                        liste_pos_objectif.append((random.randint(0,850-objectif[2]),random.randint(0,850-objectif[2])))
                        while pygame.rect.Rect(liste_pos_objectif[a-1][0]-100,liste_pos_objectif[a-1][1]-100,objectif[2]+200,objectif[2]+200).colliderect([liste_pos_objectif[a][0],liste_pos_objectif[a][1],objectif[2],objectif[2]]):
                            liste_pos_objectif[a] = (random.randint(0,850-objectif[2]),random.randint(0,850-objectif[2]))
                        temps_simulation.append(500)
                
                simulation_max = len(temps_simulation)
                
                pos_sim_chunk = [random.randint(0,nb_chunk),random.randint(0,nb_chunk)]
                pos_sim_in_chunk = [random.randint(0,chunk_size),random.randint(0,chunk_size)]
                coordonées = [(pos_sim_chunk[0]*chunk_size+pos_sim_in_chunk[0])*850/nb_chunk/chunk_size,(pos_sim_chunk[1]*chunk_size+pos_sim_in_chunk[1])*850/nb_chunk/chunk_size]
                while pygame.rect.Rect(liste_pos_objectif[0][0]-100,liste_pos_objectif[0][1]-100,objectif[2]+200,objectif[2]+200).colliderect([coordonées[0],coordonées[1],taille_vaisseau,taille_vaisseau]):
                    pos_sim_chunk = [random.randint(0,nb_chunk),random.randint(0,nb_chunk)]
                    pos_sim_in_chunk = [random.randint(0,chunk_size),random.randint(0,chunk_size)]
                    coordonées = [(chunk_coordinate[0]*chunk_size+coordinate_in_chunk[0])*850/nb_chunk/chunk_size,(chunk_coordinate[1]*chunk_size+coordinate_in_chunk[1])*850/nb_chunk/chunk_size]
                
                simulation_circuit = 0
                
                
                num_objectif = 0
                coordinate_in_chunk = list(pos_sim_in_chunk)
                chunk_coordinate = list(pos_sim_chunk)
                vitesses = [0,0]
                objectif[0] = int(liste_pos_objectif[0][0])
                objectif[1] = int(liste_pos_objectif[0][1])
                
                
                for sim_count in range(simulation_max):
                    
                    sim = touche == sim_count
                    gc.collect()
                    for simulation in range(temps_simulation[sim_count]):
                        
                        if sim:
                            
                            coordonées = [(chunk_coordinate[0]*chunk_size+coordinate_in_chunk[0])*850/nb_chunk/chunk_size,(chunk_coordinate[1]*chunk_size+coordinate_in_chunk[1])*850/nb_chunk/chunk_size]
                            
                            
                            if abs((coordonées[0]+taille_vaisseau/2)-(objectif[0]+objectif[2]/2)) < 425 :
                                dist_x = abs((coordonées[0]+taille_vaisseau/2)-(objectif[0]+objectif[2]/2))
                            else :
                                dist_x = 850-abs((coordonées[0]+taille_vaisseau/2)-(objectif[0]+objectif[2]/2))
                            
                            if abs((coordonées[1]+taille_vaisseau/2)-(objectif[1]+objectif[2]/2)) < 425 :
                                dist_y = abs((coordonées[1]+taille_vaisseau/2)-(objectif[1]+objectif[2]/2))
                            else :
                                dist_y = 850-abs((coordonées[1]+taille_vaisseau/2)-(objectif[1]+objectif[2]/2))
                            
                            
                            if dist_x <= (taille_vaisseau+objectif[2])/2 and dist_y <= (taille_vaisseau+objectif[2])/2:
                                num_objectif += 1
                                if num_objectif == len(liste_pos_objectif):
                                    num_objectif = 0
                                objectif[0] = int(liste_pos_objectif[num_objectif][0])
                                objectif[1] = int(liste_pos_objectif[num_objectif][1])
                                touche += 1
                                score += (touche**3)*1000000/simulation
                                sim = False

                            #pilotage de l'IA
                            
                        
                            inputs_pilotage = []
                            

                            #coordonées du vaisseau
                            inputs_pilotage.append(coordonées[0])
                            inputs_pilotage.append(coordonées[1])
                            
                            #vitesse du vaisseau
                            inputs_pilotage.append(vitesses[0])
                            inputs_pilotage.append(vitesses[1])
                            
                            #accélération du vaisseau
                            inputs_pilotage.append(acceleration)
                            
                            #taille de la map
                            inputs_pilotage.append(nb_chunk*chunk_size)
                            
                            #friction du vide activée
                            if friction :
                                inputs_pilotage.append(1)
                            else :
                                inputs_pilotage.append(0)
                            
                            # coordonées de l'objectif
                            inputs_pilotage.append(objectif[0])
                            inputs_pilotage.append(objectif[1])
                            
                            #taille de l'objectif
                            inputs_pilotage.append(objectif[2])
                            
                            #distance de la cible
                            inputs_pilotage.append(dist_x)
                            inputs_pilotage.append(dist_y)
                            
                            # longueure de l'input :  12
                        
                            output_pilotage = IA_entrainement.fonction(inputs_pilotage)
                            
                            #haut
                            if output_pilotage[0] > 0.9 :
                                vitesses[1] -= acceleration
                                if output_pilotage[1] > 0.9 :
                                    score -= 5
                            #bas
                            if output_pilotage[1] > 0.9 :
                                vitesses[1] += acceleration
                            #gauche
                            if output_pilotage[2] > 0.9 :
                                vitesses[0] -= acceleration
                                if output_pilotage[3] > 0.9 :
                                    score -= 5
                            #droite
                            if output_pilotage[3] > 0.9 :
                                vitesses[0] += acceleration
                                
                            coordinate_in_chunk[0] += vitesses[0]
                            coordinate_in_chunk[1] += vitesses[1]
                            
                            
                            # effet de la fricion du vide
                            if friction :
                                if vitesses[0] < 0 :
                                    vitesses[0] -= vitesses[0]/100
                                    if vitesses[0] > 0 :
                                        vitesses[0] = 0
                                if vitesses[1] < 0 :
                                    vitesses[1] -= vitesses[1]/100
                                    if vitesses[1] > 0 :
                                        vitesses[1] = 0
                                if vitesses[0] > 0 :
                                    vitesses[0] -= vitesses[0]/100
                                    if vitesses[0] < 0 :
                                        vitesses[0] = 0
                                if vitesses[1] > 0 :
                                    vitesses[1] -= vitesses[1]/100
                                    if vitesses[1] < 0 :
                                        vitesses[1] = 0
                            
                            
                            
                            #reglage position du joueur par rapport aux chunks
                            while coordinate_in_chunk[0] > chunk_size :
                                chunk_coordinate[0] += 1
                                coordinate_in_chunk[0] -= chunk_size
                            while coordinate_in_chunk[0] < 0 :
                                chunk_coordinate[0] -= 1
                                coordinate_in_chunk[0] += chunk_size
                            while coordinate_in_chunk[1] > chunk_size :
                                chunk_coordinate[1] += 1
                                coordinate_in_chunk[1] -= chunk_size
                            while coordinate_in_chunk[1] < 0 :
                                chunk_coordinate[1] -= 1
                                coordinate_in_chunk[1] += chunk_size
                            
                            while chunk_coordinate[0] > nb_chunk-1:
                                chunk_coordinate[0] -= nb_chunk
                            while chunk_coordinate[0] < 0:
                                chunk_coordinate[0] += nb_chunk
                            while chunk_coordinate[1] > nb_chunk-1:
                                chunk_coordinate[1] -= nb_chunk
                            while chunk_coordinate[1] < 0:
                                chunk_coordinate[1]  += nb_chunk
                            
                            
                            score += 1000/math.sqrt(dist_x**2+dist_y**2)
                    
                        
                        
            if touche > max_touche:
                max_touche = touche
            #print(gen,touche)
            if score > 1000 :
                au_dessus_de_100 += 1
            list_score.append(score)
            if touche == simulation_max:
                touche_3 += 1
            del IA_entrainement
            
            gc.collect()
            
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    run = False
        
            pygame.display.update()
            
        nombre_IA_références = 50
        
        
        # Crée une liste de tuples (valeur, indice) à partir de la liste d'entrée
        lst_indexee = [(valeur, indice) for indice, valeur in enumerate(list_score)]
        
        # Trie la liste de tuples dans l'ordre décroissant en fonction de la valeur
        lst_triee = sorted(lst_indexee, reverse=True)
        
        # Extrait les indices des dix premières valeurs
        indices_top = [indice for _, indice in lst_triee[:nombre_IA_références]]
        del top
        top = []
        for a in range(nombre_IA_références):
            top.append(Résaux_de_nerones[indices_top[a]])
        
        génération += 1
        
        print("*****************************************************************************************")
        print("score maximale")
        print(list_score[indices_top[0]])
        print(indices_top)
        print(f"touché {simulation_max}")
        print(touche_3)
        print(f"max de touche")
        print(max_touche)
        print("génération")
        print(génération)
        print("circuit")
        print(simulation_circuit)
        print()
        print("*****************************************************************************************")
        
        
        del pilotage_auto
        pilotage_auto = IA.IA(top[0][0],top[0][1])
        marshal.dump(top,open("IA_save","wb"))
        
        
        score = 0
        touche = 0
        num_objectif = 0
        coordinate_in_chunk = list(pos_sim_in_chunk)
        chunk_coordinate = list(pos_sim_chunk)
        vitesses = [0,0]
        objectif[0] = int(liste_pos_objectif[0][0])
        objectif[1] = int(liste_pos_objectif[0][1])
        
        del Résaux_de_nerones
        del indices_top
        del lst_indexee
        del lst_triee
        
        
        