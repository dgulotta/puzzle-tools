window.onload = function () {
	document.getElementById("start").addEventListener("click",submit);
	document.getElementById("restart").addEventListener("click",reset);
	answerElt = document.getElementById("answers");
	answerElt.addEventListener("keypress",clueKeyPress);
	messageElt = document.getElementById("message");
	messageElt.addEventListener("keypress",messageKeyPress);
}

function BlankFiller(pattern)
{
	if(typeof(pattern)=="string") {
		pattern = pattern.split("");
	}
	this.pattern = pattern;
	this.answers = []
	this.pattern_to_answer = [];
	this.answer_to_pattern = [];
	var j=0;
	for(var i=0;i<pattern.length;i++) {
		if(pattern[i]=='\b') {
			this.pattern_to_answer.push(j);
			this.answer_to_pattern.push(i);
			this.answers.push('.');
			j+=1;
		}
		else {
			this.pattern_to_answer.push(null);
		}
	}
	this.text = function () {
		var ans = []
		for(var i=0; i<this.pattern.length; i++) {
			var j = this.pattern_to_answer[i];
			if(j==null) {
				ans.push(this.pattern[i]);
			}
			else {
				ans.push(this.answers[j]);
			}
		}
		return ans.join("")
	}
	this.set_message_char = function(index, ch) {
		var j = this.pattern_to_answer[index];
		if(j!=null) {
			this.set_answer_char(j,ch);
		}
		return j;
	}
	this.set_answer_char = function(index, ch) {
		this.answers[index]=ch;
	}
}

function setClue(index, ch)
{
	var i = clues.set_message_char(index,ch);
	if(i!=null) {
		var j = clue_to_message[i];
		if(j>=0) {
			msg.set_answer_char(j,ch);
			message_to_clue[j].forEach(function(k) { clues.set_answer_char(k,ch); });
		}
	}
}

function setMsg(index, ch)
{
	var j = msg.set_message_char(index,ch);
	if(j!=null) {
		message_to_clue[j].forEach(function(k) { clues.set_answer_char(k,ch);});
	}
}

function submit()
{
	document.getElementById("setup").setAttribute("style","display:none");
	document.getElementById("solve").removeAttribute("style");
	msg = new BlankFiller(document.getElementById("messagepattern").value.replace(/\./g,'\b'));
	setupClues();
	updateText();
}

function setupClues()
{
	var cluetext = document.getElementById("clues").value.split("\n");
	var cluepat = document.getElementById("cluepattern").value.split("\n");
	var clue_combined = []
	clue_to_message = []
	message_to_clue = []
	for(var i=0; i<cluetext.length || i<cluepat.length; i++) {
		if(i<cluetext.length&&cluetext[i]) {
			clue_combined.push(cluetext[i]);
			clue_combined.push(" ");
		}
		if(i<cluepat.length&&cluepat[i]) {
			var row = cluepat[i].split(/[^\d]+/);
			for(j=0;j<row.length;j++) {
				var n = row[j];
				if(n) {
					var d = parseInt(n)-1;
					if(d>=0) {
						while(message_to_clue.length<=d) {
							message_to_clue.push([]);
						}
						message_to_clue[d].push(clue_to_message.length);
					}
					clue_to_message.push(d);
					clue_combined.push("\b");
				}
			}
		}
		clue_combined.push("\n");
	}
	clues = new BlankFiller(clue_combined.join(""));
	var msgpat = document.getElementById("messagepattern").value.replace(/\./g,'\b');
	var s = message_to_clue.length;
	for(var i=0;i<msgpat.length;i++) {
		if(msgpat[i]=='\b') {
			s--;
		}
	}
	if(s>0) {
		msgpat+='\b'.repeat(s);
		for(;s>0;s--) {
			message_to_clue.push([]);
		}
	}
	msg = new BlankFiller(msgpat);
	clues.setAndPropagate = setClue;
	msg.setAndPropagate = setMsg;
}

function moveCursor(elt,n)
{
	var p = elt.selectionStart+n;
	elt.setSelectionRange(p,p);
}

function changeAndMoveCursor(elt,bf,dir,ch)
{
	var p = elt.selectionStart;
	if(dir<0) {
		if(p>0) {
			bf.setAndPropagate(p-1,ch);
			updateText();
			var q = (p<2)?0:bf.pattern.lastIndexOf('\b',p-2)+1;
			if(q<0) q=p-1;
			elt.setSelectionRange(q,q);
		}
	}
	else {
		if(p<elt.value.length) {
			bf.setAndPropagate(p,ch);
			updateText();
			var q = bf.pattern.indexOf('\b',p+1);
			if(q<0) q=p+1;
			elt.setSelectionRange(q,q);
		}
	}
}

function isValidInput(c)
{
	var cc = c.charCodeAt(0);
	return (cc==46)||(cc>=48&&cc<=57)||(cc>=65&&cc<=90)||(cc>=97&&cc<=122);
}

function keyEvent(e,elt,bf)
{
	var k = e.keyCode;
	var c = e.charCode?String.fromCharCode(e.charCode):null;
	if(k==46) c='.'; // delete
	if(c) {
		e.preventDefault();
		if(c==' ') c='.';
		if(isValidInput(c)) {
			changeAndMoveCursor(elt,bf,1,c);
		}
		return;
	}
	if(e.keyCode==8) { // backspace
		e.preventDefault();
		changeAndMoveCursor(elt,bf,-1,'.');
		return;
	}
	if(e.keyCode==13) { // enter
		e.preventDefault();
		return;
	}
}

function messageKeyPress(e)
{
	keyEvent(e,messageElt,msg);
}

function clueKeyPress(e)
{
	keyEvent(e,answerElt,clues);
}

function reset()
{
	document.getElementById("solve").setAttribute("style","display:none");
	document.getElementById("setup").removeAttribute("style");
}

function updateText()
{
	answerElt.value = clues.text();
	messageElt.value = msg.text();
}
