let cabezal = document.getElementById("cabezal");
var cabezal_pos = cabezal.getBoundingClientRect();
var width = window.innerWidth;
var pos = 0;
var lon = document.getElementById("feature");
var list = document.getElementsByClassName("row");
// console.log("cajas="+lon.offsetWidth );
// console.log(list.length*lon.offsetWidth);
var rect = lon.getBoundingClientRect();
var lisre = list[0].getBoundingClientRect();
var end = list[2].getBoundingClientRect()
// console.log(rect.top, rect.right, rect.bottom, rect.left);
// console.log(lisre.top, lisre.right, lisre.bottom, lisre.left);
cabezal.style.left = ((lisre.left-rect.left)/2) + rect.left + "px";
pos = rect.left
// Movimiento
window.addEventListener('keydown', (event) => {
    // console.log('key='+event.code);
    cabezal.style.background = "red"
    console.log(width);
    if (event.code == "KeyD"){
        if (pos < list[2].getBoundingClientRect().right - (list[2].getBoundingClientRect().right * 0.07)){
            pos+=8;
            console.log("derecha==> "+pos)
            console.log("cabezal"+cabezal_pos.right)
            cabezal.style.left = pos + "px";
            // cabezal.style.transition = "linear .5s"

        }
    }else if (event.code == "KeyA"){
        console.log(pos)
        if (pos > rect.left){
            pos-=8;
            cabezal.style.left = pos + "px";
            // cabezal.style.transition = "linear .5s"
        }
    }
});

