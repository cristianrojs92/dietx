//Proteinas

const claradehuevo =  {
  name : "Claras de huevo",
  percentage: 100,
  portion: 100,
  proteins: 11.0,
  carbohydrates: 0.0,
  fats: 0.2,
  source: "SP"
};

const huevoentero =  {
  name : "Huevo entero",
  percentage: 100,
  portion: 100,
  proteins: 13,
  carbohydrates: 1,
  fats: 11,
  source: "SP"
};

const cerdo =  {
  name : "Cerdo",
  percentage: 100,
  portion: 100,
  proteins: 20,
  carbohydrates: 0.0,
  fats: 6.8,
  source: "SP"
};

const suprema =  {
  name : "Suprema",
  percentage: 100,
  portion: 100,
  proteins: 23,
  carbohydrates: 0.0,
  fats: 2.1,
  source: "SP"
};

const patamuslo =  {
  name : "Pata y muslo",
  percentage: 100,
  portion: 100,
  proteins: 19.6,
  carbohydrates: 0.0,
  fats: 5.7,
  source: "SP"
};

const carnemagra =  {
  name : "Carne Magra",
  percentage: 100,
  portion: 100,
  proteins: 19,
  carbohydrates: 0.0,
  fats: 13,
  source: "SP"
};

//Carbohidratos
const avena = {
  name : "Avena",
  percentage: 100,
  portion: 100,
  proteins: 16.8,
  carbohydrates: 66.27,
  fats: 2.90,
  source: "SC"
};

const arrozblanco = {
  name : "Arroz blanco",
  percentage: 100,
  portion: 100,
  proteins: 79,
  carbohydrates: 7,
  fats: 0.6,
  source: "SC"
};

const arrozintegral = {
  name : "Arroz integral",
  percentage: 100,
  portion: 100,
  proteins: 8,
  carbohydrates: 77,
  fats: 2.9,
  source: "SC"
};

const fideos = {
  name : "Fideos",
  percentage: 100,
  portion: 100,
  proteins: 12.5,
  carbohydrates: 75,
  fats: 1.2,
  source: "SC"
};

//Grasas
const mani =   {
  name : "Mani",
  percentage: 100,
  portion: 100,
  proteins: 26.0,
  carbohydrates: 16.0,
  fats: 49.0,
  source: "SF"
};

const palta =   {
  name : "Palta",
  percentage: 100,
  portion: 100,
  proteins: 1,
  carbohydrates: 5,
  fats: 14,
  source: "SF"
};

exports.foods = {
  proteins: [
    claradehuevo,
    huevoentero,
    cerdo,
    suprema,
    patamuslo,
    carnemagra
  ],
  carbohydrates: [
    avena,
    arrozblanco,
    arrozintegral,
    fideos
  ],
  fats: [
    mani,
    palta
  ]
};