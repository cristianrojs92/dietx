/*
Author Cristian Rojas
Date 2 de Dic del 2018
*/

//Importamos los alimentos
const { foods } = require('./foods');

//Se declaran variables globales.
let gl_sex = null; //Sexo
let gl_weight = null; //Peso
let gl_height = null; //Altura
let gl_age = null; //Años
let gl_Tmb = 0; //Tasa Metabolica Basal
let gl_act_intense = 0; //Actividad fisica intensa (6 veces por semana)
let gl_rate_objective = 0; //Objetivo del cliente.
const act =[{
            id : 'S', //Sedentario
            activity : 1.2
        },
        {
            id : 'L', //Actividad fisica ligera (1 o 2 veces por semana)
            activity : 1.37
        },
        {
            id : 'M',//Actividad moderada (3,5 veces por semana) 
            activity : 1.55
        },
        {
            id : 'I', //Actividad fisica muy intensa (6 veces deporte de alto rendimiento)
            activity : 1.90
        }
        ];

 const objective =[{
            id : 'P', //Pereder peso
            rate : -20
        },
        {
            id : 'G', //Ganar peso
            rate : 20
        }
        ];


//Esta funcion se encarga de calcular la taza metabolica basal
function calculateTMB() {
    var number_sex = 0;
    if (gl_sex == "M" || gl_sex == 'MASCULINO'){
      number_sex = 5; 
    } else if (gl_sex == "F" || gl_sex == 'FEMENINO') {
      number_sex = -161;
    }
    gl_Tmb = (parseFloat(10) * parseFloat(gl_weight)) + (parseFloat(6.25) * parseFloat(gl_height)) - ( 5 * parseInt(gl_age)) + number_sex;
    console.log( '--------------------------------------\n'+
                 '        Taza metabolica basal\n'+
                  `Se obtuvo un TMB de: ${gl_Tmb}\n`+
                  '--------------------------------------'
    );
}

/*Esta funcion se encarga de calcular las calorias metabolicas
 para mantener las funciones del organismo activas.
    rate: recibe el porcentaje a sumar o restar
 */
function calculateCalories(rate){
    let calories = parseFloat(gl_Tmb) * parseFloat(gl_act_intense);

    //Se calcula el porcentaje de calorias
    let porcent_calories = (calories * Number(rate)) / 100;

    calories = calories + porcent_calories;


    console.log( '--------------------------------------\n'+
    '        Calorias\n'+
     `Las calorias necesarias son: ${calories}\n`+
     '--------------------------------------'
    );
    return calories;
}

/*
   Esta funcion se encarga de calcular los macronutrientes necesarios
*/
function calculateMacros(calories){
    let macros = {
        protein : 0,
        carbs : 0,
        fat : 0
    }

    /*El porcentaje comun seran:
        20% proteinas
        10% grasas
        70% carbohidratos
    */
    //Calculamos las proteinas
    macros.protein = ((Number(calories) * 20)/100) / 4;

    //Calculamos las grasas
    macros.fat = ((Number(calories) * 10)/100) / 9;   

    //Calculamos los carbos
    macros.carbs = ((Number(calories) * 70)/100) / 4;  

    console.log(`gramos de proteina ${macros.protein}`);
    console.log(`gramos de carbos ${macros.carbs}`);
    console.log(`gramos de grasa ${macros.fat}`);

    return macros;
}

// When user input data and click enter key.
function inputData(text){
    const standard_input = process.stdin;

    //Seteamos el encoding del los caracteres que vamos a recibir
    standard_input.setEncoding('utf-8');

    console.log(text);
    return new Promise((resolve) => {
        standard_input.on('data', function (data) {
            if(data){
                //Texto en mayuscula
                let dataToUpper = data.toString().toUpperCase();
                dataToUpper = dataToUpper.trim();
                resolve(dataToUpper);
                //process.stdin.pause();
            } 
            //Renovemos el listener creado para escuchar
            standard_input.removeAllListeners();
        });
    });
}

async function  Main(){

    //Obtenemos el sexo.
    await inputData('Ingrese el sexo M: Masculino o F: Femenino').then(sex => gl_sex = sex);

    //Obtenemos el peso
    await inputData('Ingrese el su peso en kg').then(weight => gl_weight = weight);

    //Obtenemos la altura
    await inputData('Ingrese el su altura en cm').then(height => gl_height = height);

    //Obtenemos la edad.
    await inputData('Ingrese su edad').then(age => gl_age = age);

    //Obtenemos la actividad fisica
    let showTex = 'Ingrese el nivel de actividad fisica que realiza:\n'+
    'S: Sedendario, no realizo actividad fisica\n'+
    'L: Actividad ligera, me ejercito 1 o 2 veces por semana\n'+
    'M: Actividad moderada, me ejercito de 3 a 5 veces por senaba\n'+
    'I: Actividad fisica intensa, me ejercito 6 veces a la semana';

    await inputData(showTex).then(data_act => gl_act_intense = act.find(a => a.id == data_act).activity);
    
    //Calcula y muestra la taza metabolica vasal
    calculateTMB();

    //Objetivo del cliente
    showTex = 'Cual es su objetivo?\n' +
              'P: Peder peso\n'+
              'G: Ganar peso\n' ; 

    await inputData(showTex).then(data_obj => gl_rate_objective = objective.find(a => a.id == data_obj).rate);

    //Se debe calcular las calorias a consumir.
    let calories = calculateCalories(gl_rate_objective);

    const macros = calculateMacros(calories);

    //Cantidad de comidas al dia
    showTex = 'Cantidad de comidas al dia?\n';

    const quantityMeal = await inputData(showTex);

    calculateMeals(macros, Number(quantityMeal));
}

async function calculateMeals(macros, quantityMeal) {

    //Recorremos la cantidad de comidas
    for (let i = 0; i  < quantityMeal; i ++) {

        let foodsSelect = [];
        console.log("Comida numero " + (i + 1) + "\n");

        let selectFood = async (name, foods) => {
            let food;
            let showTex =  `Listado de ${name}\n` ;
    
            for(let indexFood in foods) {
                let number = Number(indexFood) + 1;
                showTex += `${number} - ${foods[indexFood].name}\n`;
            }
            showTex += "N - Nada\n" ;
            let foodSelected = await inputData(showTex);
            if ( !isNaN(foodSelected)) {
                food = foods[foodSelected - 1];          
            } 
            return food;
        }

        //Obtenemos las proteinas
        let foodProtein = await selectFood("proteinas", foods.proteins);

        if (foodProtein !== undefined) {
            foodsSelect.push(foodProtein);
        }

        //Obtenemos las carbohidratos
        let foodCarbohydrate = await selectFood("carbohidratos", foods.carbohydrates);

        if (foodCarbohydrate !== undefined) {
            foodsSelect.push(foodCarbohydrate);
        }

        //Obtenemos las grasas
        let foodFats = await selectFood("grasas", foods.fats);
        if (foodFats !== undefined) {
            foodsSelect.push(foodFats);
        } 
    
        console.log(foodsSelect);
    }
}
Main();
