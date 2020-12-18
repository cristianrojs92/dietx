const { spawn } = require('child_process');
const path = require('path');

async function calculateFoods(neededMacronutrients, foods, priority) {
  const isValid = verify(neededMacronutrients, foods);
  if (isValid) {
    const response = await executeFoodsCalculator(neededMacronutrients, foods, priority);
    return response;
  }
  return false;
}

function verify(neededMacronutrients, foods) {
  let isValid = false;
  if(neededMacronutrients && Array.isArray(foods) && foods.length > 0) {
    isValid = true;
  }
  return isValid;
}

function executeFoodsCalculator(neededMacronutrients, foods, priority) {
  let promise = new Promise(function (resolve) {
    const pyFoodCalculator = path.join(__dirname, 'libpy/foodsCalculator.py');
    const pyProg = spawn('python', [pyFoodCalculator, JSON.stringify(neededMacronutrients), JSON.stringify(foods),priority]);    
    
    pyProg.stdout.on('data', function(data) {
      resolve(data.toString());
    });
  });
  return promise;
}

exports.calculate = async function(neededMacronutrients, foods) {

  /* Tipos de prioridades
  #PCF : PROTEIN, CARBS, FAT
  #PFC : PROTEIN, FAT, CARBS
  #CPF : CARBS, PROTEIN, FAT
  #CFP : CARBS, FAT, PROTEIN
  #FCP : FAT, CARBS, PROTEIN
  #FPC : FAT, PROTEIN, CARBS*/
  const priorities = ["PCF", "PFC" ,"CPF", "CFP", "FCP","FPC"];
  const receipts = [];

  //Obtenemos las recetas para cada prioridad
  for (const priority of priorities) {

    const receipt = await getReceipt(neededMacronutrients, foods, priority);
    receipts.push(receipt);
  }

  //Obtenemos la receta con el puntaje mas bajo
  const receipt = getMinorScoreReceipt(receipts);

  return receipt;

}

function getMinorScoreReceipt(receipts){

  function compareMinorScoreReceipt( receiptA, receiptB ) {
    if ( receiptA.score < receiptB.score ){
      return -1;
    }
    if ( receiptA.score > receiptB.score ){
      return 1;
    }
    return 0;
  }
  
  receipts.sort( compareMinorScoreReceipt );

  return receipts[0];
}

async function getReceipt(neededMacronutrients, foods, priority) {

  let response = await calculateFoods(neededMacronutrients, foods, priority);

  /*
    Si el resultado fue satisfactorio
    result:totalmacros@foods
  */
  let [ result, dataTotalMacros, dataFoods ] = response.split('@'); 
  if(result === 'true') {
      
      //Obtenemos los macros totales de la receta
      datatotalMacros = JSON.parse(dataTotalMacros);
      
      //Redondeamos los macros totales
      const totalMacros = {
        proteins: Number(datatotalMacros.proteins.toFixed(2)),
        carbohydrates: Number(datatotalMacros.carbohydrates.toFixed(2)),
        fats: Number(datatotalMacros.fats.toFixed(2))
      }

      //Obtenemos las porciones de alimentos
      dataFoods = JSON.parse(dataFoods);

      //Redondemos los resultados de los alimentos
      const rfoods = dataFoods.map((dataFood) => {
        return   {
          name: dataFood.name,
          portion: Number(dataFood.portion.toFixed(2)),
          proteins: Number(dataFood.proteins.toFixed(2)),
          carbohydrates: Number(dataFood.carbohydrates.toFixed(2)),
          fats: Number(dataFood.fats.toFixed(2)),
          source: dataFood.source
        }
      });

      //Calculamos el puntaje de proteinas
      let scoreProteins = neededMacronutrients.proteins - totalMacros.proteins;
      if(scoreProteins < 0) {
        scoreProteins = scoreProteins * -1;
      }

      //Calculamos el puntaje de carbos
      let scoreCarbs = neededMacronutrients.carbohydrates - totalMacros.carbohydrates; 
      if(scoreCarbs < 0) { 
        scoreCarbs = scoreCarbs * -1; 
      } 

      //Calculamos el puntaje de grasas
      let scoreFats = neededMacronutrients.fats - totalMacros.fats;
      if(scoreFats < 0) {
        scoreFats = scoreFats * -1;
      }

      //Puntaje de la receta
      let score = scoreProteins + scoreCarbs + scoreFats;

      const receipt = {
        macronutrients : totalMacros,
        foods: rfoods,
        priority: priority,
        score: score
      }
      return receipt;
  }

  return undefined;
}
