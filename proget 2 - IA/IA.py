import random
import math

def sigmoid(x):

    if x >= 0:
        z = math.exp(-x)
        sig = 1 / (1 + z)
    else:
        z = math.exp(x)
        sig = z / (1 + z)
    return sig

class IA:
    
    def __init__(self,réseau_layers,réseau_links):
        
        
        
        self.layers = réseau_layers
        
        self.links = réseau_links
        
    
    def add_neurone(self,couche):
        """
        self.layers[couche].append(1)
        
        for i in range(len(self.links[couche-1])):
            self.links[couche-1][i].append(1)
        
        
        self.links[couche].append([])
        
        for i in range(len(self.layers[couche+1])):
            self.links[couche][-1].append(1)"""
        
        self.layers[couche].append(0)

        # Adds a link from each neuron in the previous layer to the new neuron
        for i in range(len(self.links[couche-1])):
            self.links[couche-1][i].append(0)

        # Adds a list for links from the new neuron to neurons in the next layer
        self.links[couche].append([])

        # Adds links from the new neuron to neurons in the next layer
        for i in range(len(self.layers[couche+1])):
            self.links[couche][-1].append(0)
    
    def remove_neurone(self,couche,neurone):
        
        del self.layers[couche][neurone]
        
        del self.links[couche][neurone]
        
        for i in range(len(self.links[couche-1])):
            try:
                del self.links[couche-1][i][neurone]
            except IndexError:
                print(couche, i, neurone)
                print(self.links)
                del self.links[couche-1][i][neurone]
    
    
    def mutation(self):

        neud_mofif = 10
        
        if random.randint(0,neud_mofif) == 0:
            self.add_neurone(random.randint(1,len(self.layers)-2))
        
        
        if random.randint(0,neud_mofif) == 0:
            couche = random.randint(1,len(self.layers)-2)
            if len(self.layers[couche]) > 1:
                self.remove_neurone(couche,random.randint(0,len(self.layers[couche])-1))
        
        
        marge_aléatoire = 3 * 100000
        pourcentage_aléatoire = 3
        randomness = 25
        
        #modification des layers
        for i in range(len(self.layers)):
            for a in range(len(self.layers[i])):
                if random.randint(0,randomness) == 0 :
                    self.layers[i][a] += (random.randint((-abs(int(self.layers[i][a]*100000)))-marge_aléatoire,abs(int(self.layers[i][a]*100000))+marge_aléatoire)/100000)*pourcentage_aléatoire
        
        
        #modification des liens
        for i in range(len(self.links)):
            for a in range(len(self.links[i])):
                for b in range(len(self.links[i][a])):
                    if random.randint(0,randomness) == 0 :
                        self.links[i][a][b] += (random.randint((-abs(int(self.links[i][a][b]*100000)))-marge_aléatoire,abs(int(self.links[i][a][b]*100000))+marge_aléatoire)/100000)*pourcentage_aléatoire
        
        
        
        
        
        

    def fonction(self,inputs):
        
        
        values = []
        
        for a in range(len(self.layers)):
            values.append([])
            for b in range(len(self.layers[a])):
                values[a].append(0)
        
        values[0] = inputs
        
        for a in range(len(self.layers)-1):
            for cb in range(len(self.layers[a])):
                values[a][cb] = values[a][cb] * self.layers[a][cb]
            for lb in range(len(self.links[a])):
                for lc in range(len(self.links[a][lb])):
                    values[a+1][lc] += values[a][lb] * self.links[a][lb][lc]
            for cc in range(len(self.layers[a+1])):
                values[a+1][cc] = sigmoid(values[a+1][cc])
        
        return values[-1]

    def get_layers(self):
        return self.layers.copy()
    def get_links(self):
        return self.links.copy()

