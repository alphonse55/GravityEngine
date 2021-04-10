class Planet{
    constructor(pos, r, v, m, red, green, blue){
        this.pos = pos;
        this.r = r;
        this.v = v;
        this.m = m;
        this.red = red;
        this.green = green;
        this.blue = blue;
    }
    update(){
        var a = [0, 0];
        for (var p of planets){
            if (p != this){
                var dx = (this.pos[0] - p.pos[0])*1000*1000;
                var dy = (this.pos[1] - p.pos[1])*1000*1000;
                if ((dx**2 + dy**2) != 0){
                    var acc = 6.67408*10**-11*p.m/(dx**2 + dy**2);
                }
                if (dx != 0){
                    var alfa = Math.atan(abs(dy/dx));
                }
                else{
                    var alfa = Math.pi/2;
                }
                if (p.pos[0] > this.pos[0]){
                    a[0] += acc*Math.cos(alfa);
                }
                else{
                    a[0] -= acc*Math.cos(alfa);
                }
                if (p.pos[1] > this.pos[1]){
                    a[1] += acc*Math.sin(alfa);
                }
                else{
                    a[1] -= acc*Math.sin(alfa);
                }
            }
        }

        this.v[0] += a[0];
        this.v[1] += a[1];

        this.pos[0] += this.v[0]/100;
        this.pos[1] += this.v[1]/100;
    }

    draw(){
        fill(this.red,this.green,this.blue);
        circle(this.pos[0],this.pos[1],this.r);
    }
}

var Earth = new Planet([100, 300], 12, [0, -10000], 2*10**24, 0, 0, 255);
var Sun = new Planet([400, 300], 70, [0, 0], 6*10**30, 255, 255, 0)
var planets = [Earth, Sun];

function setup(){
    createCanvas(800, 600);   
}

function draw(){
    background(0);
    for (var planet of planets){
        planet.update();
        planet.draw();
    }
}