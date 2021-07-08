function openMouth(){
    jaw = document.getElementById("jaw")
    jaw.style.bottom = "-40px"
}

function closeMouth(){    
    jaw = document.getElementById("jaw")
    jaw.style.bottom = "0px"
}

function blink(){
    var left = document.getElementById("left-lid");
    var right = document.getElementById("right-lid");
    left.style.height = "55px";
    right.style.height = "55px";
    setTimeout(() => {      
        left.style.height = "0px";
        right.style.height = "0px"; 
    }, 150);
}
