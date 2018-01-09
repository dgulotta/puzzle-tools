var bits_to_char = "   W J#  YU T    RQ P   O        ML K   I       H                FE D   C       B               A                                ZX V           S               N                               G                                                               ";
var pts = [[90,50],[78,22],[50,10],[22,22],[10,50],[22,78],[50,90],[78,78]];
var boxes = [];

function getChar(bits, num_mode)
{
	var ch = bits_to_char[bits];
	if (num_mode) {
		if (ch == "J") {
			num_mode = false;
			ch = "\u03b1";
		}
		else if (ch == "K") { ch = "0" }
		else {
			n = ch.charCodeAt(0);
			if (n >= 65 && n <= 73) {
				ch = String.fromCharCode(n-16);
			}
			else { ch = " "; }
		}
	}
	else {
		if (ch == "#") { num_mode = true; }
	}
	return [ch, num_mode];
}

function isSpecial(ch) {
	return ch == "#" || ch == "\u03b1";
}

function clearChildren(elt) {
	while(elt.lastChild) {
		elt.removeChild(lastChild);
	}
}

function addText(elt, text) {
	elt.innerText = text;
}

function updateChar(box, num_mode) {
	var ch;
	[ch, num_mode] = getChar(box.bits, num_mode);
	addText(box.letter, ch);
	var cls = isSpecial(ch) ? "lspecial" : "lnormal";
	box.letter.setAttribute("class","letter "+cls);
	return num_mode;
}

function drawBack(box) {
	var ctx = box.canvas.getContext("2d");
	ctx.clearRect(0,0,100,100);
	ctx.beginPath();
	for (var coord of pts) {
		ctx.moveTo(50,50);
		ctx.lineTo(coord[0],coord[1]);
		ctx.strokeStyle="gray";
		ctx.lineWidth=3;
	}
	ctx.stroke();
}

function drawSem(box) {
	var ctx = box.canvas.getContext("2d");
	ctx.beginPath();
	for(var i = 0; i<8; i++) {
		if(box.bits & (1<<i)) {
			ctx.moveTo(50,50);
			ctx.lineTo(pts[i][0],pts[i][1]);
		}
	}
	ctx.strokeStyle="red";
	ctx.lineWidth=5;
	ctx.stroke();
}

function redrawBox(box) {
	drawBack(box);
	drawSem(box);
}

function computeLetters() {
	var num_mode = false;
	for(var box of boxes) {
		num_mode = updateChar(box, num_mode);
	}
}

function checkCreateNew(box) {
	if (box.bits && box === boxes[boxes.length-1]) createBox();
}

function clickBox(box, ev) {
	var dx = ev.offsetX - 50;
	var dy = ev.offsetY - 50;
	var r = dx * dx + dy * dy;
	if (r<25||r>2025)
		return;
	var ang = Math.atan2(-dy,dx)*4/Math.PI;
	var angr = Math.round(ang);
	if (Math.abs(ang-angr)>.3)
		return;
	if (angr<0)
		angr+=8;
	box.bits = box.bits ^ (1 << angr);
	redrawBox(box);
	checkCreateNew(box);
	computeLetters();
}

function SemaphoreBox() {
	this.div = document.createElement("div");
	this.div.setAttribute("class", "box");
	this.letter = document.createElement("div");
	this.letter.setAttribute("class", "letter lnormal");
	this.canvas = document.createElement("canvas");
	this.canvas.setAttribute("width", "100");
	this.canvas.setAttribute("height", "100");
	this.bits = 0;
	this.div.appendChild(this.letter);
	this.div.appendChild(this.canvas);
	var box = this;
	this.canvas.addEventListener("click", ev => clickBox(box, ev));
}

function createBox() {
	var box = new SemaphoreBox();
	document.getElementById("main").appendChild(box.div);
	redrawBox(box);
	boxes.push(box);
}

window.onload = function() {
	createBox();
}
