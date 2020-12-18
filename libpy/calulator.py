import numpy as np
from scipy.optimize import linprog
import json
import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

class source:
  def __init__(self, proteins, carbohydrates, fats, portion):
    self.proteins = proteins
    self.carbohydrates = carbohydrates
    self.fats = fats
    self.portion = portion

class Macronutrients:
  def __init__(self, proteins, carbohydrates, fats):
    self.proteins = proteins
    self.carbohydrates = carbohydrates
    self.fats = fats

class Food:
  def __init__(self, name, percentage, portion, proteins, carbohydrates, fats, source):
    self.name = name
    self.percentage = percentage
    self.portion = portion
    self.macronutrients = Macronutrients(proteins, carbohydrates, fats)
    self.source = source

#Obtiene los macronutrientes restantes de una fuente de proteinas
def getMacronutrientsBySourceProteins(needProteins, foodsSourceProteins) :
  carbohydratesBySourceProteins = 0
  fatsBySourceProteins = 0

  #Recorremos el listado de alimentos proteicos
  for food in foodsSourceProteins: 

    #Calculamos la necesidad de este alimento en la receta
    #porcentaje utilizado en la receta X proteina necesaria = proteina necesaria en la receta
    needProteinsByFood = (food.percentage * needProteins) / 100

    #Calculamos la porcion a utilizar para completar la necesidad de proteinas
    portionByFood = (food.portion * needProteinsByFood) / food.macronutrients.proteins

    #Calculamos los carbos resultantes
    carbohydratesByFood = (portionByFood * food.macronutrients.carbohydrates) / food.portion

    #Calculamos las grasas resultantes
    fatsByFood = (portionByFood * food.macronutrients.fats) / food.portion

    #Sumarisamos los carbos y las grasas
    carbohydratesBySourceProteins = carbohydratesBySourceProteins + carbohydratesByFood
    fatsBySourceProteins = fatsBySourceProteins + fatsByFood

    
  #Armamos los macros de la fuente de proteinas
  macronutrientsSourceProteins = Macronutrients(needProteins, carbohydratesBySourceProteins, fatsBySourceProteins)
  return macronutrientsSourceProteins

#Obtiene los macronutrientes restantes de una fuente de carbohidratos
def getMacronutrientsBySourceCarbohydrates(needCarbohydrates, foodsSourceCarbohydrates) :
  proteinsBySourceCarbohydrates = 0
  fatsBySourceCarbohydrates = 0

  #Recorremos el listado de alimentos proteicos
  for food in foodsSourceCarbohydrates: 

    #Calculamos la necesidad de este alimento en la receta
    #porcentaje utilizado en la receta X proteina necesaria = proteina necesaria en la receta
    needCarbohydratesByFood = (food.percentage * needCarbohydrates) / 100

    #Calculamos la porcion a utilizar para completar la necesidad de carbos
    portionByFood = (food.portion * needCarbohydratesByFood) / food.macronutrients.carbohydrates

    #Calculamos las proteinas resultantes
    proteinsByFood = (portionByFood * food.macronutrients.proteins) / food.portion

    #Calculamos las grasas resultantes
    fatsByFood = (portionByFood * food.macronutrients.fats) / food.portion

    #Sumarisamos los carbos y las grasas
    proteinsBySourceCarbohydrates = proteinsBySourceCarbohydrates + proteinsByFood
    fatsBySourceCarbohydrates = fatsBySourceCarbohydrates + fatsByFood

    
  #Armamos los macros de la fuente de proteinas
  macronutrientsSourceCarbohydrates = Macronutrients(proteinsBySourceCarbohydrates, needCarbohydrates, fatsBySourceCarbohydrates)
  return macronutrientsSourceCarbohydrates

#Obtiene los macronutrientes restantes de una fuente de grasas
def getMacronutrientsBySourceFats(needFats, foodsSourceFats) :
  proteinsBySourceFats = 0
  carbohydratesBySourceFats = 0

  #Recorremos el listado de alimentos grasos
  for food in foodsSourceFats: 

    

    #Calculamos la necesidad de este alimento en la receta
    #porcentaje utilizado en la receta X proteina necesaria = proteina necesaria en la receta
    needFatsByFood = (food.percentage * needFats) / 100

    #Calculamos la porcion a utilizar para completar la necesidad de grasas
    portionByFood = (food.portion * needFatsByFood) / food.macronutrients.fats

    #Calculamos las proteinas resultantes
    proteinsByFood = (portionByFood * food.macronutrients.proteins) / food.portion

    #Calculamos los carbos resultantes
    carbohydratesByFood = (portionByFood * food.macronutrients.carbohydrates) / food.portion

    #Sumarisamos los carbos y las grasas
    proteinsBySourceFats = proteinsBySourceFats + proteinsByFood
    carbohydratesBySourceFats = carbohydratesBySourceFats + carbohydratesByFood

    
  #Armamos los macros de la fuente de proteinas
  macronutrientsSourceFats = Macronutrients(proteinsBySourceFats, carbohydratesBySourceFats, needFats)
  return macronutrientsSourceFats


#Obtenemos las porciones de los alimentos
def calculatePortionsFood(neededProteins, neededCarbohydrates, neededFats, foods):
  portionsFood = []

  #Recorremos el listado de alimentos
  for food in foods: 

    #Si es una fuente de proteina
    if food.source == "SP":
        #Calculamos la necesidad de este alimento en la receta
        #porcentaje utilizado en la receta X proteina necesaria = proteina necesaria en la receta
        needProteinsByFood = (food.percentage * neededProteins) / 100

        #Calculamos la porcion a utilizar para completar la necesidad de proteinas
        portionByFood = (food.portion * needProteinsByFood) / food.macronutrients.proteins

        #Calculamos los carbos resultantes
        carbohydratesByFood = (portionByFood * food.macronutrients.carbohydrates) / food.portion

        #Calculamos las grasas resultantes
        fatsByFood = (portionByFood * food.macronutrients.fats) / food.portion

        portionsFood.append(Food(food.name, food.percentage, portionByFood , needProteinsByFood, carbohydratesByFood,fatsByFood, "SP"))

    #Si es una fuente de carbohidratos
    elif food.source == "SC":

      #Calculamos la necesidad de este alimento en la receta
      #porcentaje utilizado en la receta X proteina necesaria = proteina necesaria en la receta
      needCarbohydratesByFood = (food.percentage * neededCarbohydrates) / 100

      #Calculamos la porcion a utilizar para completar la necesidad de carbos
      portionByFood = (food.portion * needCarbohydratesByFood) / food.macronutrients.carbohydrates

      #Calculamos las proteinas resultantes
      proteinsByFood = (portionByFood * food.macronutrients.proteins) / food.portion

      #Calculamos las grasas resultantes
      fatsByFood = (portionByFood * food.macronutrients.fats) / food.portion

      portionsFood.append(Food(food.name, food.percentage, portionByFood , proteinsByFood, needCarbohydratesByFood, fatsByFood, "SC"))

    #Si es una fuente de grasa
    elif food.source == "SF":

      #Calculamos la necesidad de este alimento en la receta
      #porcentaje utilizado en la receta X proteina necesaria = proteina necesaria en la receta
      needFatsByFood = (food.percentage * neededFats) / 100

      #Calculamos la porcion a utilizar para completar la necesidad de grasas
      portionByFood = (food.portion * needFatsByFood) / food.macronutrients.fats

      #Calculamos las proteinas resultantes
      proteinsByFood = (portionByFood * food.macronutrients.proteins) / food.portion

      #Calculamos los carbos resultantes
      carbohydratesByFood = (portionByFood * food.macronutrients.carbohydrates) / food.portion

      portionsFood.append(Food(food.name, food.percentage, portionByFood , proteinsByFood, carbohydratesByFood, needFatsByFood, "SF"))

  return portionsFood


def calculateRemainingMacronutrientsByFoodsSource(neededMacronutrients, foods, priority) :

  #Fuentes de proteinas
  foodsSourceProteins = []
  #Fuentes de carbohidratos
  foodsSourceCarbohydrates = []
  #Fuentes de grasas
  foodsSourceFats = []

  #Recorremos el listado de alimentos
  for food in foods: 

    #Si es una fuente de proteina
    if food.source == "SP":
      foodsSourceProteins.append(food)

    #Si es una fuente de carbohidratos
    elif food.source == "SC":
      foodsSourceCarbohydrates.append(food)

    #Si es una fuente de grasa
    elif food.source == "SF":
      foodsSourceFats.append(food)

  #Calculamos los macronutrientes restantes en la fuente de proteinas
  macronutrientsBySourceProteins = getMacronutrientsBySourceProteins(neededMacronutrients.proteins, foodsSourceProteins)
  macronutrientsBySourceCarbohydrates = getMacronutrientsBySourceCarbohydrates(neededMacronutrients.carbohydrates, foodsSourceCarbohydrates)
  macronutrientsBySourceFats = getMacronutrientsBySourceFats(neededMacronutrients.fats, foodsSourceFats)
  #print("---------------------------------")
  #print("Funte de proteinas")
  #print("  proteinas " + str(macronutrientsBySourceProteins.proteins))
  #print("  carbos " + str(macronutrientsBySourceProteins.carbohydrates))
  #print("  grasas " + str(macronutrientsBySourceProteins.fats))
  #print("---------------------------------")
  #print("Funte de carbohidratos")
  #print("  proteinas " + str(macronutrientsBySourceCarbohydrates.proteins))
  #print("  carbos " + str(macronutrientsBySourceCarbohydrates.carbohydrates))
  #print("  grasas " + str(macronutrientsBySourceCarbohydrates.fats))
  #print("---------------------------------")
  #print("Funte de grasas")
  #print("  proteinas " + str(macronutrientsBySourceFats.proteins))
  #print("  carbos " + str(macronutrientsBySourceFats.carbohydrates))
  #print("  grasas " + str(macronutrientsBySourceFats.fats))
  #print("---------------------------------")

  #Ajustamos los macronutrientes
  #Formamos la matriz a resolver de 3 x 3
  # FP = FUENTE DE PROTEINAS  
  # FC = FUENTE DE CARBOHIDRATOS                                                        
  # FG = FUENTE DE GRASAS    
  # P = PROTEINAS
  # C = CARBOHIDRATOS
  # G = GRASAS

  #           FP.G   FC.G   FG.G  = Grasas necesarias
  #           FP.C   FC.C   FG.C  = Carbohidratos necesarios
  #           FP.P   FC.P   FG.P  = Proteinas necesarias

  #PCF : PROTEIN, CARBS, FAT
  if priority == "PCF" :
    A = np.array([[-macronutrientsBySourceProteins.fats, -macronutrientsBySourceCarbohydrates.fats, -macronutrientsBySourceFats.fats],
                  [-macronutrientsBySourceProteins.carbohydrates, -macronutrientsBySourceCarbohydrates.carbohydrates, -macronutrientsBySourceFats.carbohydrates],
                  [-macronutrientsBySourceProteins.proteins,-macronutrientsBySourceCarbohydrates.proteins, -macronutrientsBySourceFats.proteins]])

    b = np.array([-neededMacronutrients.fats,-neededMacronutrients.carbohydrates,-neededMacronutrients.proteins])

    c = np.array([1,1,1])

    #Resolvemos la matriz con simplex minimizacion
    res = linprog(c, A_ub=A, b_ub=b,bounds=(0, None))
    #print('Optimal value:', res.fun, '\nX:', res.x)
    x = res.x

    #Resultado

    macronutrientsBySourceProteins.fats = macronutrientsBySourceProteins.fats  * x[0]
    macronutrientsBySourceCarbohydrates.fats = macronutrientsBySourceCarbohydrates.fats  * x[0]
    macronutrientsBySourceFats.fats = macronutrientsBySourceFats.fats  * x[0]

    macronutrientsBySourceProteins.carbohydrates = macronutrientsBySourceProteins.carbohydrates  * x[1]
    macronutrientsBySourceCarbohydrates.carbohydrates = macronutrientsBySourceCarbohydrates.carbohydrates  * x[1]
    macronutrientsBySourceFats.carbohydrates = macronutrientsBySourceFats.carbohydrates  * x[1]

    macronutrientsBySourceProteins.proteins = macronutrientsBySourceProteins.proteins * x[2]
    macronutrientsBySourceCarbohydrates.proteins = macronutrientsBySourceCarbohydrates.proteins * x[2]
    macronutrientsBySourceFats.proteins = macronutrientsBySourceFats.proteins * x[2]


  #PFC : PROTEIN, FAT, CARBS 
  if priority == "PFC" :
    A = np.array([[-macronutrientsBySourceProteins.carbohydrates, -macronutrientsBySourceCarbohydrates.carbohydrates, -macronutrientsBySourceFats.carbohydrates],
                  [-macronutrientsBySourceProteins.fats, -macronutrientsBySourceCarbohydrates.fats, -macronutrientsBySourceFats.fats],
                  [-macronutrientsBySourceProteins.proteins,-macronutrientsBySourceCarbohydrates.proteins, -macronutrientsBySourceFats.proteins]])

    b = np.array([-neededMacronutrients.carbohydrates,-neededMacronutrients.fats,-neededMacronutrients.proteins])

    c = np.array([1,1,1])

    #Resolvemos la matriz con simplex minimizacion
    res = linprog(c, A_ub=A, b_ub=b,bounds=(0, None))
    #print('Optimal value:', res.fun, '\nX:', res.x)
    x = res.x

    #Resultado

    macronutrientsBySourceProteins.carbohydrates = macronutrientsBySourceProteins.carbohydrates  * x[0]
    macronutrientsBySourceCarbohydrates.carbohydrates = macronutrientsBySourceCarbohydrates.carbohydrates  * x[0]
    macronutrientsBySourceFats.carbohydrates = macronutrientsBySourceFats.carbohydrates  * x[0]

    macronutrientsBySourceProteins.fats = macronutrientsBySourceProteins.fats  * x[1]
    macronutrientsBySourceCarbohydrates.fats = macronutrientsBySourceCarbohydrates.fats  * x[1]
    macronutrientsBySourceFats.fats = macronutrientsBySourceFats.fats  * x[1]

    macronutrientsBySourceProteins.proteins = macronutrientsBySourceProteins.proteins * x[2]
    macronutrientsBySourceCarbohydrates.proteins = macronutrientsBySourceCarbohydrates.proteins * x[2]
    macronutrientsBySourceFats.proteins = macronutrientsBySourceFats.proteins * x[2]

  #CPF : CARBS, PROTEIN, FAT
  if priority == "CPF" :
    A = np.array([[-macronutrientsBySourceProteins.fats, -macronutrientsBySourceCarbohydrates.fats, -macronutrientsBySourceFats.fats],
                  [-macronutrientsBySourceProteins.proteins,-macronutrientsBySourceCarbohydrates.proteins, -macronutrientsBySourceFats.proteins],
                  [-macronutrientsBySourceProteins.carbohydrates, -macronutrientsBySourceCarbohydrates.carbohydrates, -macronutrientsBySourceFats.carbohydrates]])

    b = np.array([-neededMacronutrients.fats, -neededMacronutrients.proteins,-neededMacronutrients.carbohydrates])

    c = np.array([1,1,1])

    #Resolvemos la matriz con simplex minimizacion
    res = linprog(c, A_ub=A, b_ub=b,bounds=(0, None))
    #print('Optimal value:', res.fun, '\nX:', res.x)
    x = res.x

    #Resultado

    macronutrientsBySourceProteins.fats = macronutrientsBySourceProteins.fats  * x[0]
    macronutrientsBySourceCarbohydrates.fats = macronutrientsBySourceCarbohydrates.fats  * x[0]
    macronutrientsBySourceFats.fats = macronutrientsBySourceFats.fats  * x[0]

    macronutrientsBySourceProteins.proteins = macronutrientsBySourceProteins.proteins * x[1]
    macronutrientsBySourceCarbohydrates.proteins = macronutrientsBySourceCarbohydrates.proteins * x[1]
    macronutrientsBySourceFats.proteins = macronutrientsBySourceFats.proteins * x[1]

    macronutrientsBySourceProteins.carbohydrates = macronutrientsBySourceProteins.carbohydrates  * x[2]
    macronutrientsBySourceCarbohydrates.carbohydrates = macronutrientsBySourceCarbohydrates.carbohydrates  * x[2]
    macronutrientsBySourceFats.carbohydrates = macronutrientsBySourceFats.carbohydrates  * x[2]

  #CFP : CARBS, FAT, PROTEIN
  if priority == "CFP" :
    A = np.array([[-macronutrientsBySourceProteins.proteins,-macronutrientsBySourceCarbohydrates.proteins, -macronutrientsBySourceFats.proteins],
                  [-macronutrientsBySourceProteins.fats, -macronutrientsBySourceCarbohydrates.fats, -macronutrientsBySourceFats.fats],
                  [-macronutrientsBySourceProteins.carbohydrates, -macronutrientsBySourceCarbohydrates.carbohydrates, -macronutrientsBySourceFats.carbohydrates]])

    b = np.array([-neededMacronutrients.proteins, -neededMacronutrients.fats,-neededMacronutrients.carbohydrates])

    c = np.array([1,1,1])

    #Resolvemos la matriz con simplex minimizacion
    res = linprog(c, A_ub=A, b_ub=b,bounds=(0, None))
    #print('Optimal value:', res.fun, '\nX:', res.x)
    x = res.x

    #Resultado

    macronutrientsBySourceProteins.proteins = macronutrientsBySourceProteins.proteins * x[0]
    macronutrientsBySourceCarbohydrates.proteins = macronutrientsBySourceCarbohydrates.proteins * x[0]
    macronutrientsBySourceFats.proteins = macronutrientsBySourceFats.proteins * x[0]

    macronutrientsBySourceProteins.fats = macronutrientsBySourceProteins.fats  * x[1]
    macronutrientsBySourceCarbohydrates.fats = macronutrientsBySourceCarbohydrates.fats  * x[1]
    macronutrientsBySourceFats.fats = macronutrientsBySourceFats.fats  * x[1]

    macronutrientsBySourceProteins.carbohydrates = macronutrientsBySourceProteins.carbohydrates  * x[2]
    macronutrientsBySourceCarbohydrates.carbohydrates = macronutrientsBySourceCarbohydrates.carbohydrates  * x[2]
    macronutrientsBySourceFats.carbohydrates = macronutrientsBySourceFats.carbohydrates  * x[2]

  #FCP : FAT, CARBS, PROTEIN
  if priority == "FCP" :
    A = np.array([[-macronutrientsBySourceProteins.proteins,-macronutrientsBySourceCarbohydrates.proteins, -macronutrientsBySourceFats.proteins],
                  [-macronutrientsBySourceProteins.carbohydrates, -macronutrientsBySourceCarbohydrates.carbohydrates, -macronutrientsBySourceFats.carbohydrates],
                  [-macronutrientsBySourceProteins.fats, -macronutrientsBySourceCarbohydrates.fats, -macronutrientsBySourceFats.fats]])

    b = np.array([-neededMacronutrients.proteins, -neededMacronutrients.carbohydrates,-neededMacronutrients.fats ])

    c = np.array([1,1,1])

    #Resolvemos la matriz con simplex minimizacion
    res = linprog(c, A_ub=A, b_ub=b,bounds=(0, None))
    #print('Optimal value:', res.fun, '\nX:', res.x)
    x = res.x

    #Resultado

    macronutrientsBySourceProteins.proteins = macronutrientsBySourceProteins.proteins * x[0]
    macronutrientsBySourceCarbohydrates.proteins = macronutrientsBySourceCarbohydrates.proteins * x[0]
    macronutrientsBySourceFats.proteins = macronutrientsBySourceFats.proteins * x[0]

    macronutrientsBySourceProteins.carbohydrates = macronutrientsBySourceProteins.carbohydrates  * x[1]
    macronutrientsBySourceCarbohydrates.carbohydrates = macronutrientsBySourceCarbohydrates.carbohydrates  * x[1]
    macronutrientsBySourceFats.carbohydrates = macronutrientsBySourceFats.carbohydrates  * x[1]

    macronutrientsBySourceProteins.fats = macronutrientsBySourceProteins.fats  * x[2]
    macronutrientsBySourceCarbohydrates.fats = macronutrientsBySourceCarbohydrates.fats  * x[2]
    macronutrientsBySourceFats.fats = macronutrientsBySourceFats.fats  * x[2]

  #FPC : FAT, PROTEIN, CARBS
  if priority == "FCP" :
    A = np.array([[-macronutrientsBySourceProteins.proteins,-macronutrientsBySourceCarbohydrates.proteins, -macronutrientsBySourceFats.proteins],
                  [-macronutrientsBySourceProteins.carbohydrates, -macronutrientsBySourceCarbohydrates.carbohydrates, -macronutrientsBySourceFats.carbohydrates],
                  [-macronutrientsBySourceProteins.fats, -macronutrientsBySourceCarbohydrates.fats, -macronutrientsBySourceFats.fats]])

    b = np.array([-neededMacronutrients.proteins, -neededMacronutrients.carbohydrates ,-neededMacronutrients.fats ])

    c = np.array([1,1,1])

    #Resolvemos la matriz con simplex minimizacion
    res = linprog(c, A_ub=A, b_ub=b,bounds=(0, None))
    #print('Optimal value:', res.fun, '\nX:', res.x)
    x = res.x

    #Resultado

    macronutrientsBySourceProteins.proteins = macronutrientsBySourceProteins.proteins * x[0]
    macronutrientsBySourceCarbohydrates.proteins = macronutrientsBySourceCarbohydrates.proteins * x[0]
    macronutrientsBySourceFats.proteins = macronutrientsBySourceFats.proteins * x[0]

    macronutrientsBySourceProteins.carbohydrates = macronutrientsBySourceProteins.carbohydrates  * x[1]
    macronutrientsBySourceCarbohydrates.carbohydrates = macronutrientsBySourceCarbohydrates.carbohydrates  * x[1]
    macronutrientsBySourceFats.carbohydrates = macronutrientsBySourceFats.carbohydrates  * x[1]

    macronutrientsBySourceProteins.fats = macronutrientsBySourceProteins.fats  * x[2]
    macronutrientsBySourceCarbohydrates.fats = macronutrientsBySourceCarbohydrates.fats  * x[2]
    macronutrientsBySourceFats.fats = macronutrientsBySourceFats.fats  * x[2]


  #print("------------FUENTES AJUSTADAS------------")
  #print("Funte de proteinas")
  #print("  proteinas " + str(macronutrientsBySourceProteins.proteins))
  #print("  carbos " + str(macronutrientsBySourceProteins.carbohydrates))
  #print("  grasas " + str(macronutrientsBySourceProteins.fats))
  #print("---------------------------------")
  #print("Funte de carbohidratos")
  #print("  proteinas " + str(macronutrientsBySourceCarbohydrates.proteins))
  #print("  carbos " + str(macronutrientsBySourceCarbohydrates.carbohydrates))
  #print("  grasas " + str(macronutrientsBySourceCarbohydrates.fats))
  #print("---------------------------------")
  #print("Funte de grasas")
  #print("  proteinas " + str(macronutrientsBySourceFats.proteins))
  #print("  carbos " + str(macronutrientsBySourceFats.carbohydrates))
  #print("  grasas " + str(macronutrientsBySourceFats.fats))
  #print("---------------------------------")


  #print("------------TOTAL MACROS------------")
  #print("  proteinas " + str(macronutrientsBySourceProteins.proteins + macronutrientsBySourceCarbohydrates.proteins + macronutrientsBySourceFats.proteins))
  totalProteins = macronutrientsBySourceProteins.proteins + macronutrientsBySourceCarbohydrates.proteins + macronutrientsBySourceFats.proteins

  #print("  carbos " + str(macronutrientsBySourceProteins.carbohydrates + macronutrientsBySourceCarbohydrates.carbohydrates + macronutrientsBySourceFats.carbohydrates))
  totalCarbs = macronutrientsBySourceProteins.carbohydrates + macronutrientsBySourceCarbohydrates.carbohydrates + macronutrientsBySourceFats.carbohydrates
  
  #print("  grasas " + str(macronutrientsBySourceProteins.fats + macronutrientsBySourceCarbohydrates.fats + macronutrientsBySourceFats.fats))
  totalFats = macronutrientsBySourceProteins.fats + macronutrientsBySourceCarbohydrates.fats + macronutrientsBySourceFats.fats

  #Ajustamos las necesidades
  portionFoods = calculatePortionsFood(macronutrientsBySourceProteins.proteins, macronutrientsBySourceCarbohydrates.carbohydrates, macronutrientsBySourceFats.fats, foods)

  portionFoodsJson = ''

  #Suma de los macronutrientes obtenidos en los alimentos
  resultTotalProteins = 0
  resultTotalCarbs = 0
  resultTotalFats = 0

  #Recorremos el listado de alimentos
  for index in range(0,len(portionFoods)):

    #Abrimos json y array
    if index == 0 :
      portionFoodsJson = '['

    #Separamos datos
    elif index != (len(portionFoods)) :
      portionFoodsJson += ','

    #Generamos json del alimento
    portionFoodsJson += "{"
    portionFoodsJson += '"name" : ' + '"' + portionFoods[index].name + '",'
    portionFoodsJson += '"portion" : ' + str(portionFoods[index].portion) + ','
    portionFoodsJson += '"proteins" : ' + str(portionFoods[index].macronutrients.proteins) + ','
    portionFoodsJson += '"carbohydrates" : ' + str(portionFoods[index].macronutrients.carbohydrates) + ','
    portionFoodsJson += '"fats" : ' + str(portionFoods[index].macronutrients.fats) + ','
    portionFoodsJson += '"source" : ' + '"' + str(portionFoods[index].source) + '"'
    portionFoodsJson += "}"

    #print("---------------------------------")
    #print("  nombre " + portionFoods[0].name)
    #print("  porcion " + str(portionFoods[0].portion) + " gramos") 
    #print("  proteinas " + str(portionFoods[0].macronutrients.proteins))
    #print("  carbos " + str(portionFoods[0].macronutrients.carbohydrates))
    #print("  grasas " + str(portionFoods[0].macronutrients.fats))
    #print("---------------------------------")
    #Cerramos json
    if index == len(portionFoods) -1 :
      portionFoodsJson += ']'

    #Sumarizamos los totales
    resultTotalProteins += portionFoods[index].macronutrients.proteins
    resultTotalCarbs += portionFoods[index].macronutrients.carbohydrates
    resultTotalFats += portionFoods[index].macronutrients.fats


  #Total de macronutrientes ajustados a la necesidad
  totalMacronutrientsJson = '{' + '"proteins":' + str(resultTotalProteins) + ', "carbohydrates":' + str(resultTotalCarbs) + ', "fats":' + str(resultTotalFats) + '}'

  result = totalMacronutrientsJson + '@' + portionFoodsJson

  return result
