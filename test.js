const { calculate } = require('./foodsCalculator');
const { 
  claradehuevo,
  huevoentero,
  cerdo,
  suprema,
  patamuslo,
  avena,
  arrozblanco,
  arrozintegral,
  fideos,
  mani,
  palta

} = require('./foods');

const neededMacronutrients = {
  proteins : 24.0,
  carbohydrates: 53.0,
  fats: 25
}

const foods = [];
foods.push(huevo);
foods.push(avena);
foods.push(palta);

async function main() {


const receipt =  await calculate(neededMacronutrients, foods);
console.log(receipt);

}

main();
