var lienzo = document.getElementById("lienzo");
var pluma = lienzo.getContext("2d");
var forma = [[0, 0, 0, 0, 0, 0, 0], [0, 0, -1, -1, 0, 0, 0], [0, 0, -1, -1, -1, -1, 0], [0, -1, -1, 0, -1, -1, 0], [0, -1, -1, -1, -1, 0, 0], [0, 0, 0, -1, -1, 0, 0], [0, 0, 0, 0, 0, 0, 0]];
var llaves = [-1, -1, -1, 5, -1, 4, -1, -1, -1, -1];
var frecuencias = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 5, 5, 6, 6, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9];
var alf = 'ABCDEFGHIJ';
var fsumas = [];
var csumas = [];
var selected = [];
var puzzle = [];
var clues = 7;
var resuelto = false;
var niveles = document.getElementById("puzzles");
var nlist = niveles.textContent.split(";");
var levels = [];
var mostrar_clave = 10;
var barra = document.getElementById("bar");
var nivel_actual = parseInt(barra.innerText.split(" ")[1])-4;
// constantes
var square_size = 40;
var grid_size = 45;
var ksquare_size = 28;
var kgrid_size = 35;
var font_puzzle = '30px Arial';
var font_sums = '12px Arial';
var font_key = '20px Arial';


function min(n1, n2){
	if (n1<n2){
		return n1
	}
	return n2
}

function azar(lista){
	var r = parseInt(Math.random()*lista.length);
	return lista[r];
}

function permuta(lista){
	for (var kk=0; kk < 3*lista.length; kk++){
		var ii = parseInt(Math.random()*lista.length);
		var jj = parseInt(Math.random()*lista.length);
		var aux = lista[ii];
		lista[ii] = lista[jj];
		lista[jj] = aux;
	}
	return lista;
}

function copiar(plantilla){
	matr = [];
	for (var ii=0; ii<plantilla.length; ii++){
		matr[ii] = [];
		for (var jj=0; jj<plantilla[0].length; jj++){
			matr[ii][jj] = plantilla[ii][jj];
		}
	}
	return matr;
}

function generar(plantilla){
	var solucion = [];
	for (var ii = 0; ii < plantilla.length; ii++){
		solucion[ii] = [];
		for (var jj=0; jj<plantilla[0].length; jj++){
			if (plantilla[ii][jj]==0){
				solucion[ii][jj] = 0;
			} else {
				check = true;
				while (check){
					solucion[ii][jj] = azar(frecuencias);
					for (var kk=0; kk < 2; kk++){
						var xx = ii;
						var yy = jj;
						while (solucion[xx][yy]!=0 && check){
							xx = xx - (kk==0);
							yy = yy - (kk==1);
							if (solucion[ii][jj]==solucion[xx][yy]){
								check = false;
								break;
							}
						}
					}
					check = !check;
				} 
			}
		}
	}
	var keys = permuta([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]);
	var filas = [];
	var columnas = [];
	for (var ii=0; ii < plantilla.length; ii++){
		var check1 = false;
		var check2 = false;
		var suma1 = 0;
		var suma2 = 0;
		for (var jj=0; jj < plantilla[0].length; jj++){
			if (solucion[ii][jj]==0 && check1){
				filas[filas.length] = suma1.toString();
				suma1 = 0;
			}
			if (solucion[jj][ii]==0 && check2){
				columnas[columnas.length] = suma2.toString();
				suma2 = 0;
			}
			suma2 = suma2 + solucion[jj][ii];
			suma1 = suma1 + solucion[ii][jj];
			check1 = solucion[ii][jj]!=0;
			check2 = solucion[jj][ii]!=0;
		}
		if (check1){
			filas[filas.length] = suma1.toString();
		}
		if (check2){
			columnas[columnas.length] = suma2.toString();
		}
	}
	for (var ii=0; ii < solucion.length; ii++){
		for (var jj=0; jj < solucion.length; jj++){
			if (solucion[ii][jj]!=0){
				solucion[ii][jj] = alf[keys[solucion[ii][jj]]];
			}
		}
	}
	for (var ii=0; ii < filas.length; ii++){
		tt = "";
		for (var jj=0; jj<filas[ii].length; jj++){
			tt = tt + alf[keys[parseInt(filas[ii][jj])]];
		}
		filas[ii] = tt;
	}
	for (var ii=0; ii < columnas.length; ii++){
		tt = "";
		for (var jj=0; jj<columnas[ii].length; jj++){
			tt = tt + alf[keys[parseInt(columnas[ii][jj])]];
		}
		columnas[ii] = tt;
	}
	var ccc = 0;
	var pistas = copiar(plantilla);
	while (ccc<clues){
		var rx = parseInt(Math.random()*plantilla.length);
		var ry = parseInt(Math.random()*plantilla[0].length);
		if (pistas[rx][ry] == -1){
			pistas[rx][ry] = solucion[rx][ry];
			ccc++;
		}
	}
	return [pistas, filas, columnas];
}

function descifrar(texto, clave){
	res = "";
	for (var ii=0; ii<texto.length; ii++){
		ind = -1;
		for (var jj=0; jj<10; jj++){
			if (alf[jj]==texto[ii]){
				ind = jj;
				break;
			}
		}
		if (ind == -1){
			res = res + texto[ii];
		} else {
			ind = clave[ind];
			if (ind == -1){
				res = res + texto[ii];
			} else {
				res = res + ind.toString();
			}
		}
	}
	return res;
}

function dibujar(puzzle, filas, columnas, clave){
	pluma.textAlign = 'center';
	pluma.font = font_puzzle;
	for (var ii=0; ii < puzzle.length; ii++){
		for (var jj=0; jj < puzzle[0].length; jj++){
			var valor = puzzle[ii][jj];
			if (valor!=0){
				pluma.fillStyle = 'black';
				pluma.fillRect(grid_size*ii, grid_size*jj, square_size, square_size);
				pluma.stroke()
				if (valor != -1){
					pluma.fillStyle = 'white';
					if (resuelto){
						pluma.fillStyle = 'rgb(20, 250, 100)';
					}
					pluma.fillText(descifrar(valor.toString(), clave), grid_size*ii + parseInt(square_size/2), grid_size*jj + parseInt((31*square_size)/40));
				}
			}
		}
	}
	pluma.fillStyle = 'black';
	pluma.font = font_sums;
	var ind1 = 0;
	var ind2 = 0;
	for (var ii=0; ii < puzzle.length; ii++){
		var check1 = false;
		var check2 = false;
		for (var jj=0; jj < puzzle[0].length; jj++){
			if (puzzle[ii][jj]==0 && check1!=false){
				pluma.fillText(descifrar(filas[ind1], clave), grid_size*ii + 20, grid_size*jj + 7);
				ind1++;
			}
			if (puzzle[ii][jj]!=0 && check1==false){
				pluma.fillText(descifrar(filas[ind1], clave), grid_size*ii + 20, grid_size*jj - 4);
			}
			if (puzzle[jj][ii]==0 && check2!=false){
				pluma.fillText(descifrar(columnas[ind2], clave), grid_size*jj + 5, grid_size*ii + 23);
				ind2++;
			}
			if (puzzle[jj][ii]!=0 && check2==false){
				pluma.fillText(descifrar(columnas[ind2], clave), grid_size*jj - 9, grid_size*ii + 23);
			}
			check1 = puzzle[ii][jj]!=0;
			check2 = puzzle[jj][ii]!=0;
		}
	}
	if (nivel_actual == -3){
		const1 = 400
		const2 = 100
		pluma.fillStyle = 'black';
		pluma.fillRect(const1, const2, square_size, square_size);
		pluma.stroke();
		pluma.fillRect(const1 + grid_size, const2, square_size, square_size);
		pluma.stroke();
		pluma.fillRect(const1 + 2*grid_size, const2, square_size, square_size);
		pluma.stroke();
		pluma.font = font_sums;
		pluma.fillText("14", const1 + 3*grid_size + 3, const2 + 23);
		pluma.fillText("14", const1 - 9, const2 + 23);
		pluma.font = "20px Arial";
		pluma.fillText("3+7+4=14", const1 + 1.5*grid_size, const2 + 2*grid_size);
		pluma.fillStyle = 'rgb(20, 250, 100)';
		pluma.font = font_puzzle;
		pluma.fillText("3", const1 + parseInt(square_size/2), const2 + parseInt((31*square_size)/40));
		pluma.fillText("7", const1 + grid_size + parseInt(square_size/2), const2 + parseInt((31*square_size)/40));
		pluma.fillText("4", const1 + 2*grid_size + parseInt(square_size/2), const2 + parseInt((31*square_size)/40));
	}
	if (nivel_actual == -2){
		const1 = 400
		const2 = 100
		pluma.fillStyle = 'black';
		for (var ii = 0; ii < 5; ii++){
			pluma.fillRect(const1 + ii*grid_size, const2, square_size, square_size);
			pluma.stroke();
		}
		pluma.font = font_sums;
		pluma.fillText("23", const1 + 5*grid_size + 3, const2 + 23);
		pluma.fillText("23", const1 - 9, const2 + 23);
		pluma.fillStyle = 'red';
		pluma.font = font_puzzle;
		pluma.fillText("6", const1 + 4*grid_size + parseInt(square_size/2), const2 + parseInt((31*square_size)/40));
		pluma.fillText("6", const1 + grid_size + parseInt(square_size/2), const2 + parseInt((31*square_size)/40));
		pluma.fillStyle = 'white';
		pluma.fillText("2", const1 + parseInt(square_size/2), const2 + parseInt((31*square_size)/40));
		pluma.fillText("8", const1 + 2*grid_size + parseInt(square_size/2), const2 + parseInt((31*square_size)/40));
		pluma.fillText("1", const1 + 3*grid_size + parseInt(square_size/2), const2 + parseInt((31*square_size)/40));
	}
}

function dibujar_clave(){
	pluma.textAlign = 'center';
	pluma.font = font_key;
	for (var ii=0; ii<min(mostrar_clave, 10); ii++){
		pluma.fillStyle = 'black';
		pluma.fillText(alf[ii] + '=', grid_size*puzzle.length + 25, kgrid_size*ii + 74);
		pluma.fillRect(grid_size*puzzle.length + 40, 53 + kgrid_size*ii, ksquare_size, ksquare_size);
		pluma.stroke();
	}
	pluma.fillStyle = 'white';
	for (var ii=0; ii<min(mostrar_clave, 10); ii++){
		if (llaves[ii] != -1){
			pluma.fillText(llaves[ii].toString(), grid_size*puzzle.length + 53, kgrid_size*ii + 74);
		}
	}
}

function actualizar(){
	pluma.fillStyle = 'white';
	pluma.fillRect(0, 0, pluma.canvas.width, pluma.canvas.height);
	dibujar(puzzle, fsumas, csumas, llaves);
	dibujar_clave();
	if (selected!=[]){
		pluma.strokeStyle = 'rgb(5, 200, 100)';
		if (selected[0]=='puzzle'){
			pluma.beginPath();
			pluma.moveTo(grid_size*selected[1] - 1, grid_size*selected[2]);
			pluma.lineTo(grid_size*selected[1] + square_size, grid_size*selected[2]);
			pluma.lineTo(grid_size*selected[1] + square_size, grid_size*selected[2] + square_size);
			pluma.lineTo(grid_size*selected[1], grid_size*selected[2] + square_size);
			pluma.lineTo(grid_size*selected[1], grid_size*selected[2]);
			pluma.stroke();
		}
		if (selected[0]=='clave'){
			pluma.beginPath();
			pluma.moveTo(grid_size*puzzle.length + square_size-1 , 53 + kgrid_size*selected[1]);
			pluma.lineTo(grid_size*puzzle.length + square_size + ksquare_size, 53 + kgrid_size*selected[1]);
			pluma.lineTo(grid_size*puzzle.length + square_size + ksquare_size, 53 + kgrid_size*selected[1] + ksquare_size);
			pluma.lineTo(grid_size*puzzle.length + square_size, 53 + kgrid_size*selected[1] + ksquare_size);
			pluma.lineTo(grid_size*puzzle.length + square_size, 53 + kgrid_size*selected[1]);
			pluma.stroke();
			//pluma.fillRect(45*puzzle.length + 40, 53 + 35*selected[1], 28, 28);
		}
	}
}

function next_level(){
	nivel_actual ++;
	barra.innerHTML = "Nivel " + (4+nivel_actual) + "<input value=\"Reset\" style = \"font-size: 20px\" onclick=\"comenzar()\" type=\"button\">";
	comenzar();
}

function poner_archivo(texto){
	var lista = texto.split("\n");
	puzzle = [];
	llaves = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1];
	selected = [];
	tope = 0;
	for (var ii = 1; ii<lista.length; ii++){
		puzzle[ii-1] = [];
		check = false;
		for (var jj = 0; jj<lista[1].length; jj++){
			if (lista[ii][jj] == "#"){
				if (check == true){
					check = false;
					tope++;
				}
				puzzle[ii-1][jj] = 0;
			} else {
				check = true;
				puzzle[ii-1][jj] = lista[ii][jj];
			}
			if (lista[ii][jj] == " "){
				puzzle[ii-1][jj] = -1;
			}
		}
	}
	var nlista = lista[0].split(",");
	csumas = [];
	fsumas = [];
	for (var ii = 0; ii<tope; ii++){
		fsumas[ii] = nlista[ii];
	}
	for (var jj = tope; jj<nlista.length; jj++){
		csumas[csumas.length] = nlista[jj];
	}
	alf = "";
	for (var ii = 0; ii < 26; ii++){
		letra = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[ii];
		found = false;
		for (var jj = 0; jj < csumas.length; jj ++){
			if (csumas[jj].indexOf(letra) != -1){
				found = true;
				break;
			}
		}
		for (var jj = 0; jj < fsumas.length; jj ++){
			if (fsumas[jj].indexOf(letra) != -1 || found){
				found = true;
				break;
			}
		}
		for (var jj = 0; jj < puzzle.length && found == false; jj++){
			for (var kk = 0; kk < puzzle[0].length; kk++){
				if (puzzle[jj][kk] == letra){
					found = true;
					break;
				}
			}
		}
		if (found){
			alf = alf + letra;
		}
	}
	for (ii = alf.length; ii < 10; ii ++){
		alf = alf + "*-+!?#&%@$"[ii];
	}
	actualizar();
}

lienzo.addEventListener("click", function (e){
	var x;
	var y;
	if (e.pageX || e.pageY) {
		x = e.pageX;
		y = e.pageY;
	} else {
		x = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
		y = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
	}
	x -= lienzo.offsetLeft;
	y -= lienzo.offsetTop;
	//console.log(x, y);
	xx = parseInt(x/45);
	yy = parseInt(y/45);
	if (xx<puzzle.length && yy < puzzle.length){
		if (x - 45*xx < 40 && y - 45*yy < 40){
			if (puzzle[xx][yy] > 0 && puzzle[xx][yy] < 10 || puzzle[xx][yy]== -1){
				selected = ['puzzle', xx, yy];
				//console.log('selected puzzle');
			}
		}
	}
	if (x > 45*puzzle.length + 40 && x < 45*puzzle.length + 68){
		yyy = parseInt((y - 53)/35);
		if (yyy>=0 && yyy<min(mostrar_clave, 10)){
			if (y - 53 - 35*yyy < 28){
				selected = ['clave', yyy]
				//console.log('selected clave');
			}
		}
	}
	actualizar()
	actualizar()
}, false);

window.addEventListener("keydown", function(event) {
	if (event.keyCode > 47 && event.keyCode < 58) {
		if (selected[0]=='puzzle'){
			if (event.keyCode > 48){
				puzzle[selected[1]][selected[2]] = event.keyCode - 48;
			}
		}
		if (selected[0]=='clave'){
			llaves[selected[1]] = event.keyCode - 48;
		}
	}
	if (event.keyCode == 8 || event.keyCode == 32){
		if (selected[0]=='puzzle'){
			puzzle[selected[1]][selected[2]] = -1;
		}
		if (selected[0]=='clave'){
			llaves[selected[1]] = -1;
		}
	}
	actualizar()
	for (var ii = 0; ii < 10; ii++){
		if (llaves[ii] == -1){
			return false;
		}
	}
	ind1 = 0;
	ind2 = 0;
	for (var ii = 0; ii < puzzle.length; ii++){
		suma1 = 0;
		suma2 = 0;
		for (var jj=0; jj < puzzle[0].length; jj++){
			if (puzzle[ii][jj] == -1 || puzzle[jj][ii] == -1){
				return false;
			}
			if (puzzle[ii][jj]==0 && suma1>0){
				if (parseInt(descifrar(fsumas[ind1], llaves)) != suma1){
					return false;
				}
				suma1 = 0
				ind1++;
			}
			if (puzzle[ii][jj]!=0){
				suma1 = suma1 + parseInt(descifrar("" + puzzle[ii][jj], llaves))
			}
			if (puzzle[jj][ii]==0 && suma2 > 0){
				if (parseInt(descifrar(csumas[ind2], llaves)) != suma2){
					return false;
				}
				suma2 = 0
				ind2++;
			}
			if (puzzle[jj][ii]!=0){
				suma2 = suma2 + parseInt(descifrar("" + puzzle[jj][ii], llaves))
			}
		}
	}
	lis1 = [];
	lis2 = [];
	for (var ii = 0; ii < puzzle.length; ii++){
		for (var jj = 0; jj < puzzle[0].length; jj++){
			if (puzzle[ii][jj] == 0){
				lis1 = [];
			} else {
				if (puzzle[ii][jj] > 0 && puzzle[ii][jj] < 10){
					if (lis1.indexOf(puzzle[ii][jj]) != -1){
						return false;
					}
					lis1[lis1.length] = puzzle[ii][jj];
				}
			}
			if (puzzle[jj][ii] == 0){
				lis2 = [];
			} else {
				if (puzzle[jj][ii] > 0 && puzzle[jj][ii] < 10){
					if (lis2.indexOf(puzzle[jj][ii]) != -1){
						return false;
					}
					lis2[lis2.length] = puzzle[jj][ii];
				}
			}
		}
	}
	if (resuelto == false){
		if (nivel_actual == levels.length - 4){
			barra.innerHTML = barra.innerHTML + "  Has ganado!";
		} else {
			barra.innerHTML = barra.innerHTML + "<input value=\"Next level\" style = \"font-size: 20px\" onclick=\"next_level()\" type=\"button\">";
		}
	}
	resuelto = true;
	actualizar();
});

function comenzar(){
	pluma.canvas.height = window.innerHeight - 70;
	pluma.canvas.width = window.innerWidth - 40;
	first = 0;
	if (levels.length == 0){
		for (ii = 0; ii<nlist.length-1; ii++){
			if (nlist[ii][0] == "#" && nlist[ii+1][0] != "#"){
				levels[levels.length] = nlist[first];
				for (jj = first+1; jj <= ii; jj++){
					levels[levels.length-1] = levels[levels.length-1] + "\n" + nlist[jj];
				}
				first = ii+1;
			}
		}
	}
	clues = 10;//document.getElementById('an').value;
	llaves = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1];
	var kakuro = generar(forma);
	puzzle = kakuro[0];
	fsumas = kakuro[1];
	csumas = kakuro[2];
	poner_archivo(levels[3+nivel_actual]);
	if (nivel_actual == -3){
		mostrar_clave = 0;
		llaves = [0,1,2,3,4,5,6,7,8,9];
	}
	if (nivel_actual == -2){
		mostrar_clave = 0;
		llaves = [1,2,3,4,5,6,7,8,9,0];
	}
	if (nivel_actual == -1){
		mostrar_clave = 3;
		llaves = [-1, -1, -1, 1,3,4,5,6,8,9,0]
	}
	if (nivel_actual == 0){
		mostrar_clave = 10;
	}
	resuelto = false;
	actualizar();
}

comenzar();
