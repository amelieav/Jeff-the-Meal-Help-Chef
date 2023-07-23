bannedIngredients = []

def getDietList(dietReq):
    switchCase = dietReq.lower()
    tempBannedIngred = []
    #fake switch statement coz python doesn't have one :(
    if (switchCase == "none"):
        return []
    elif (switchCase == "vegan"):
        tempBannedIngred = tempBannedIngred + (getIngredFromFile("DietaryRequirementLists/animalDerivative.txt"))
    elif (switchCase == "vegetarian"):
        tempBannedIngred = tempBannedIngred + (getIngredFromFile("DietaryRequirementLists/meat.txt"))
   # elif (switchCase == "pescitarian"):
    #    bannedIngred.append(getIngredFromFile("meat.txt").diff)
    elif (switchCase == "lactose" or switchCase == "dairy"):
        tempBannedIngred = tempBannedIngred + (getIngredFromFile("DietaryRequirementLists/dairy.txt"))
    elif (switchCase == "nut" or switchCase == "nuts"):
        tempBannedIngred = tempBannedIngred + (getIngredFromFile("DietaryRequirementLists/nuts.txt"))
    elif (switchCase == "gluten"):
        tempBannedIngred = tempBannedIngred + (getIngredFromFile("DietaryRequirementLists/gluten.txt"))
    return tempBannedIngred
    bannedIngredients = tempBannedIngred

def getIngredFromFile(fileName):
    f = open(fileName, "r")
    ingredients = []
    while True:
        currentLine = f.readline()
        if "new:" in currentLine:
            ingredients = ingredients + (currentLine[4:]).split(',')
            break
        else:
            ingredients = ingredients + (getIngredFromFile("DietaryRequirementLists/" + currentLine[0:-1] + ".txt"))

    return ingredients