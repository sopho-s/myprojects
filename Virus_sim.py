import random
import matplotlib.pyplot as plt

class person:
    def __init__(self, social_distancing=0, mortality=1, virality=1, immunitylast=15, length_of_infection=0,
                 isinfected=False, time_of_recover=15, space=(100, 100), chanceofimmune=0.05, mortalityinhos=0.001,
                 house=(1, 1), timetillsymptom=9, prior_healthissues=0.02):
        self.timetillsymptom = timetillsymptom  # This is the time till the infected person show symptoms
        self.social_distancing = social_distancing  # This reduces the amount people move
        self.morality = mortality  # This increases the chance of people dying from the virus
        self.virality = virality  # This increases the chance of people getting the virus from another infected person
        self.house = house  # This is where the person will self isolate when infected
        self.immunitylast = immunitylast  # This is how long the immunity of the person will keep immunity
        self.length_of_infection = length_of_infection  # This is how long the person has had a virus
        self.x = random.randint(0, space[0])  # The person's x position
        self.y = random.randint(0, space[1])  # The person's y position
        self.isinfected = isinfected  # This stores whether the person is infected or not
        self.time_of_recover = time_of_recover  # This will determine how long the virus will last
        self.timeofimmunity = 0  # This stores how long the person has had immunity
        self.space = space  # This stores the edges of the area
        self.hasimmunity = False  # This stores whether the person has immunity
        self.mortalityinhos = mortalityinhos  # This will determine the chance of dying in hospital
        self.inhospital = False  # This stores whether the person is in hospital
        self.beentested = False  # This stores whether the person has been tested
        self.showingsymptoms = False  # This stores whether the person is showing symptoms
        if random.random() <= prior_healthissues:  # This determines whether the person has a health issue
            self.healthissue = True
        else:
            self.healthissue = False
        if chanceofimmune >= random.random():  # Determines whether the person has a natural immunity
            self.hasimmunity = True
            self.isallredimmune = True
        else:
            self.isallredimmune = False
        self.selfisolating = False  # This stores whether the person is self isolating
        self.hasbeeninfected = False  # This stores whether the person has been infected

    def returndata(self):  # This returns data to be used
        return (self.social_distancing, self.morality, self.virality, self.immunitylast, self.length_of_infection,
                self.isinfected, self.time_of_recover, self.x, self.y, self.hasimmunity, self.inhospital,
                self.healthissue)

    def movement(self, usedhouse):  # This determines where the person moves
        if self.inhospital == False and self.selfisolating == False:  # This checks whether the person should move
            move = random.random() * 2  # This calculates the x movement
            total_movement = 2  # This stores the total movement
            if self.social_distancing != 0:  # This calculates the movement if social_distancing is not 0
                minusmove = move / 2  # This calculates how much y movment the person has
                move -= self.social_distancing * minusmove * 2  # This calculates how much there should be taken away from the movement
                if move < 0:  # This set movement to 0 if it is less than 0
                    move = 0
                total_movement -= self.social_distancing * 2  # This changes the total_movement depending on the social distancing
            if random.randint(0,
                              1) == 1:  # These next few lines randomly choose whether the person moving to a negitive or positive x/y
                self.x += move
                a = False
            else:
                self.x -= move
                a = True
            if random.randint(0, 1) == 1:
                self.y += total_movement - move
                b = False
            else:
                self.y -= total_movement - move
                b = True
            for i in usedhouse:  # This checks whether the person can move into the space
                if int(self.x) == i[0] and (self.y) == i[
                    1]:  # These next few lines move the person back their original place if they are in a person place who is self isolating
                    if a == False:
                        self.x -= move
                    else:
                        self.x += move
                    if b == False:
                        self.y -= total_movement - move
                    else:
                        self.y += total_movement - move
            if self.y < 0:  # These next few lines stop the person from moving out the area
                self.y = self.y * -1
            elif self.y > self.space[1]:
                self.y -= self.y - self.space[1]
            if self.x < 0:
                self.x = self.x * -1
            elif self.x > self.space[0]:
                self.x -= self.x - self.space[0]

    def infection(self):  # This sets the person to infected depending on certain variables
        if random.random() < self.virality and self.hasimmunity == False and self.isallredimmune == False:  # This calculates whether the person should be infected, depending also on whether the person is allready immune
            self.isinfected = True

    def recovery(self):  # This check whether people have recovered from the infection
        if self.isinfected == True:  # This checks whether the person is infected
            if self.time_of_recover == self.length_of_infection:  # This checks whether the person has had the infectection long enough to recover
                self.isinfected = False  # The next few lines changes certain variables eg whether a person is infected, immune, ect
                self.hasimmunity = True
                self.inhospital = False
                self.showingsymptoms = False
                self.hasbeeninfected = True
                self.length_of_infection = 0
            else:
                self.length_of_infection += 1  # This adds a day to the amount of iteration the person has had the infection

    def immunitykept(self):  # This checks whether the person does not have immunity
        if self.hasimmunity == True and self.isallredimmune == False:  # This checks whether the person has immunity and whether the person has a natural immunity
            self.timeofimmunity += 1  # This adds time to the total time the person has had immunity
            if self.timeofimmunity == self.immunitylast:  # This removes immunity of the person if they have had the immunity as long as the pre-determined variable is equal to it
                self.hasimmunity = False
                self.timeofimmunity = 0

    def dying(self, hospitals):  # This calculates whether the person will die or not
        dead = False
        if self.isinfected == True and self.showingsymptoms == True:  # This will only continue to check whether the person will die only if they show symptoms
            if self.healthissue == True:  # This adds a chance to die if they have health issues
                addmort = 0.2
            else:
                addmort = 0
            if random.random() <= self.morality + addmort and self.inhospital == False:  # This checks if someone is about to die if they aren't in hospitals
                for i in hospitals:  # The next few lines check if there is a hospital nearby
                    dis = 0
                    if i[0] > self.x:
                        dis += i[0] - self.x
                    else:
                        dis += self.x - i[0]
                    if i[1] > self.y:
                        dis += i[1] - self.y
                    else:
                        dis += self.y - i[1]
                    if int(dis) <= 2:  # The next few lines move a person to a hospital if the requirements are met
                        self.inhospital = True
                        self.x = i[0]
                        self.y = i[1]
                        if self.inhospital == True and random.random() <= self.mortalityinhos:  # This calculates whether the person should die in hospital
                            dead = True
                    else:
                        dead = True
            elif self.inhospital == True and random.random() <= self.mortalityinhos:  # This calculates whether the person should die in hospital
                dead = True
        return dead

    def testing(self, symptomtest=False):  # This returns whether the person tested positive or not
        ting = False
        if self.isinfected == True and symptomtest == False:  # The next lines returns whether the person is infected or not and if so they self-isolate
            self.x = self.house[0]
            self.y = self.house[1]
            self.beentested = True
            self.selfisolating = True
        elif self.beentested == False and symptomtest == True and self.isinfected == True:
            self.x = self.house[0]
            self.y = self.house[1]
            self.beentested = True
            self.selfisolating = True
            ting = True
        elif self.isinfected == False and self.selfisolating == True:
            self.beentested = False
            self.selfisolating = False
        return self.house, self.isinfected, ting

    def showsymptoms(self):
        if self.timetillsymptom <= self.length_of_infection and self.isinfected == True:
            self.showingsymptoms = True
            return True
        return False


def makepeople(amount=1, social_distancing=0, mortality=0, virality=1, immunitylast=15, length_of_infection=0,
               time_of_recover=15, space=(100, 100), chanceofimmune=0.01, mortalityinhos=0.001, timetillsymptom=9,
               healthissues=0.02):
    global person  # Used global because i'm lazy and can't be bothered to change it
    people = []
    houses = []
    if amount != 0:  # The next few lines set the houses where people will self-isolate and makes sure that two houses aren't in the same place
        x = random.randint(0, space[0])
        y = random.randint(0, space[1])
        houses.append((x, y))
    for i in range(amount - 1):
        run = True
        while run == True:
            thin = False
            x = random.randint(0, space[0])
            y = random.randint(0, space[1])
            for t in houses:
                if x == t[0] and y == t[1]:
                    thin = True
            if thin == False:
                run = False
        houses.append((x, y))
    num = random.randint(0, amount - 1)
    for i in range(amount):  # the next few lines makes the people and also makes one infected person
        if i == num:
            per = person(social_distancing, mortality, virality, immunitylast, length_of_infection, isinfected=True,
                         time_of_recover=time_of_recover, space=space, house=houses[i], timetillsymptom=9,
                         prior_healthissues=healthissues)
        else:
            per = person(social_distancing, mortality, virality, immunitylast, length_of_infection,
                         time_of_recover=time_of_recover, space=space, isinfected=False, chanceofimmune=chanceofimmune,
                         house=houses[i], timetillsymptom=9, prior_healthissues=healthissues)
        people.append(per)
    return people


def makehospitals(hospitalnum=1, space=(10, 10)):  # This makes all hospitals
    hospital = []
    if hospitalnum != 0:  # The next new lines makes the hospitals and makes sure that two aren't in the same place
        x = random.randint(0, space[0])
        y = random.randint(0, space[1])
        hospital.append((x, y))
    for i in range(hospitalnum - 1):
        run = True
        while run == True:
            thin = False
            x = random.randint(0, space[0])
            y = random.randint(0, space[1])
            for t in hospital:
                if x == t[0] and y == t[1]:
                    thin = True
            if thin == False:
                run = False
        hospital.append((x, y))
    return hospital

def performsim(reps, people, numnum, hospitals, testing=10): # This perform the simulation
    totalinfected = []
    totalimmunity = []
    totaldead = []
    hospitilized = []
    testedinfected = []
    totalsymptoms = []
    totalhealthprob = []
    num = 0
    for t in range(reps): # The next few lines check if any two people are in the same spot
        currentdata = []
        for i in people:
            currentdata.append(i.returndata()[7:9])
        a = 0
        for m in currentdata:
            for c in range(len(currentdata)):
                if int(currentdata[a][0]) == int(currentdata[c][0]) and a != c and int(currentdata[a][1]) == int(currentdata[c][1]):
                    if (people[a].returndata()[5] == True or people[c].returndata()[5] == True) and people[a].returndata()[5] != people[c].returndata()[5]:
                        if people[a].returndata()[5] == False:
                            people[a].infection()
                        else:
                            people[c].infection()
            a += 1
        infected = 0
        immune = 0
        hospitilise = 0
        numnum = 0
        symptom = 0
        healthprob = 0
        if t % testing == 0: # This checks if people are about to be tested
            usedplace = []
            tested = 0
        for i in people: # These next few lines perform the calculations of how the infection has infected the people
            i.recovery()
            i.immunitykept()
            if t % testing == 0:
                house, isinfected, _ = i.testing()
                if isinfected == True:
                    tested += 1
                    usedplace.append(house)
            symptoms = i.showsymptoms()
            if symptoms == True:
                symptom += 1
                house, _, innfected = i.testing(symptomtest=True)
                if innfected == True:
                    tested += 1
                    usedplace.append(house)
            isdead = i.dying(hospitals)
            if isdead == True:
                people.pop(numnum)
                numnum -= 1
                num += 1
            if i.returndata()[5] == True:
                infected += 1
            if i.returndata()[9] == True:
                immune += 1
            if i.returndata()[10] == True:
                hospitilise += 1
            if i.returndata()[11] == True:
                healthprob += 1
            numnum += 1
        for i in people:
            i.movement(usedplace)
        totalhealthprob.append(healthprob)
        totalsymptoms.append(symptom)
        testedinfected.append(tested)
        totaldead.append(num)
        totalinfected.append(infected)
        totalimmunity.append(immune)
        hospitilized.append(hospitilise)
    plt.plot(totalinfected) # These next few lines plot the graphs
    plt.plot(totalimmunity)
    plt.plot(totaldead)
    plt.plot(hospitilized)
    plt.plot(testedinfected)
    plt.plot(totalsymptoms)
    plt.plot(totalhealthprob)

hospitals = makehospitals(20, space=(10, 10))
num = 100
people = makepeople(num, space=(10, 10), mortality=0.01, social_distancing=0.7, virality=0.7, chanceofimmune=0.,
                    mortalityinhos=0.0001, healthissues=0.1)
performsim(200, people, num, hospitals, 20)