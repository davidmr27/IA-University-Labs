var cabezal = document.getElementById("cabezal");
var log = document.getElementById("log");
var allow = document.getElementsByClassName("of");
var list = NaN;
// var cabezal_pos = cabezal.getBoundingClientRect();
// var width = window.innerWidth;
var pos = 0;
var rect = NaN;

var first_caracter = true;
var cadena = ""
var save = NaN
var valid = false
var conta = NaN;
var i = 0

const machine = {
    "q0": {
        "a": ["0","R","q1"],
        "1": ["1","R","q3"]
    },
    "q1":
    {
        "a":["a","R","q1"],
        "b":["1","L","q2"],
        "1":["1","R","q1"]
    },
    "q2":
    {
        "a":["a","L","q2"],
        "1":["1","L","q2"],
        "0":["0","R","q0"]
    },
    "q3":
    {
        " ": [" ","R","q4"], 
        "1": ["1","R","q3"]
    },
    "q4":
    {
        "" : [" ", "exit", "q4"]
    }
}

function generarEspacios(){
    let textInput = document.getElementById("cadena");
    let cinta = document.getElementById("cinta");

    first_caracter = true;
    cadena = ""
    save = NaN
    valid = false
    conta = NaN;
    i = 0

    cadena = textInput.value
    textInput.value = ""
    cinta.innerHTML = "";
    log.innerHTML = ""
    allow[0].classList.remove("correct")
    allow[1].classList.remove("incorrect")
    
    for (let index = 0; index < cadena.length; index++) {
       let row = document.createElement("div");
       row.classList.add("row")
       row.innerText = cadena[index]
       cinta.appendChild(row)
    }

    list = document.getElementsByClassName("row");
    rect = list[0].getBoundingClientRect()
    console.log(cadena)
    pos = rect.left;
    let pos_cabezal = rect.left + "px";
    cabezal.style.left = pos_cabezal;
    cabezal.classList.add("cabezal")
}

function startAnimation(){
    let timer = setInterval(() => {
        if (conta != "q4" && conta != "exit"){
            move(cadena[i])
        }else{
            if (conta == "q4"){
                allow[0].classList.add("correct")
            }else{
                allow[1].classList.add("incorrect")
            }
            clearInterval(timer)
        }
    }, 500);

}

function moveCabezal(direccion,pos){
    if(direccion == "R"){
        animationRight(pos)
    }else{
        animationLeft(pos)
    }
}

async function animationLeftSimple(rdpos, value_write){
    left = list[rdpos].getBoundingClientRect().left + 25;
    cabezal.style.transition = "ease .1s"
    cabezal.style.left = left + "px"
    await sleep(500)
    list[rdpos].style.transition = "ease .2s"
    list[rdpos].style.background = "#003C63";
    list[rdpos].innerHTML = value_write
}
function writeCinta(rdpos, value_write){
    list[rdpos].innerHTML = value_write
}
async function animationRightSimple(rdpos, value_write){
    right = list[rdpos].getBoundingClientRect().right - 70
    cabezal.style.transition = "ease .1s"
    cabezal.style.left = right + "px"
    await sleep(500)
    list[rdpos].style.transition = "ease .5s"
    list[rdpos].style.background = "#181B3D";
    list[rdpos].innerHTML = value_write
}
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function move(input){
    if (first_caracter){
        save = machine["q0"][input]
        first_caracter = false
        if (save[1] == "R"){
            cadena = replaceChar(cadena,save[0],i)
            animationRightSimple(i, save[0])
            i++;
        }
    }else{
        if(typeof input === "undefined"){
           if (save[2] == "q3"){
               valid = true
               conta = "q4"
           }else{
               conta ="exit"
           }
        }else{
            if(save[2] != "q4"){
                save = machine[save[2]][input]
                if (save[1] == "R"){
                    cadena = replaceChar(cadena,save[0],i)
                    addLog(cadena)
                    animationRightSimple(i,save[0])
                    i++;
                }else{
                    cadena = replaceChar(cadena,save[0],i)
                    addLog(cadena)
                    animationLeftSimple(i,save[0])
                    i--;
                }
                conta = save[2]
            }
        }
    }
}

function replaceChar(origString, replaceChar, index) {
    let newStringArray = origString.split("");

    newStringArray[index] = replaceChar;

    let newString = newStringArray.join("");

    return newString;
}

function addLog(info){
    let data = document.createElement("div");
    data.classList.add("data")
    data.innerText = info
    log.appendChild(data)
}