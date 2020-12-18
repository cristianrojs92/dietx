import sys
import json
from calulator import calculateRemainingMacronutrientsByFoodsSource, Macronutrients, Food

def error(message) :
  print('false@' + message)

def sucsess(result) :
  print('true@' + result)

def main():

  if len(sys.argv) < 2 :
     error('Faltan parametros')
  else :

    #Obtenemos la necesiad de macronutrientes
    #{
    #  "proteins": 2,
    #  "carbohydrates": 3,
    #  "fats" : 4
    # }

    neededMacronutrients=json.loads(sys.argv[1])

    #Necesidad
    neededMacronutrients = Macronutrients(neededMacronutrients['proteins'], neededMacronutrients['carbohydrates'], neededMacronutrients['fats'])

    #Obtenemos los alimentos
    #{
      #[
      # {
      #   "name" : "Huevo",
      #   "percentage": 100,
      #   "portion": 100,
      #   "proteins": 11.0,
      #   "carbohydrates": 0.0,
      #   "fats": 0.2,
      #   "source": "SP"
      # }  
      #]
    #}
    #Alimentos
    foodsParam = json.loads(sys.argv[2])
    foods = []

    #Prioridades
    #PCF : PROTEIN, CARBS, FAT
    #PFC : PROTEIN, FAT, CARBS
    #CPF : CARBS, PROTEIN, FAT
    #CFP : CARBS, FAT, PROTEIN
    #FCP : FAT, CARBS, PROTEIN
    #FPC : FAT, PROTEIN, CARBS
    #Por defecto la prioridad es  PCF
    priority = "PCF"
   
    if len(sys.argv) >= 4 :

      if sys.argv[3] == "PFC" or sys.argv[3] == "CPF" or sys.argv[3] == "CPF" or sys.argv[3] == "CFP" or sys.argv[3] == "FCP" or sys.argv[3] == "FPC" :
        priority = sys.argv[3]

    #Recorremos el listado de alimentos 
    for foodParam in foodsParam: 
      foods.append(Food(foodParam["name"], foodParam["percentage"], foodParam["portion"], foodParam["proteins"], foodParam["carbohydrates"], foodParam["fats"], foodParam["source"]))

    #Calculamos las porciones por comida
    result = calculateRemainingMacronutrientsByFoodsSource(neededMacronutrients, foods, priority)

    sucsess(result)
#main()


def test():

  neededMacronutrients = Macronutrients(24, 53, 25)


  #Alimentos	  #Alimentos
  
  fprotein = Food("Huevo", 100, 100, 11.0, 0.0, 0.2, "SP")
  fcarbs = Food("Avena", 100, 100, 16.8, 66.27, 2.90, "SC")
  ffats = Food("Mani", 100, 100, 26.0, 16.0, 49.0, "SG")


  #Receta	  #Receta
  foods = [fprotein, fcarbs, ffats]
  
  priority = "PCF"

  #Calculamos las porciones por comida
  result = calculateRemainingMacronutrientsByFoodsSource(neededMacronutrients, foods, priority)

  sucsess(result)

main()

