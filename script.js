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

function dibujar(matriz, filas, columnas, clave){
	pluma.textAlign = 'center';
	pluma.font = '30px Arial';
	for (var ii=0; ii < matriz.length; ii++){
		for (var jj=0; jj < matriz[0].length; jj++){
			var valor = matriz[ii][jj];
			if (valor!=0){
				pluma.fillStyle = 'black';
				pluma.fillRect(45*ii, 45*jj, 40, 40);
				pluma.stroke()
				if (valor != -1){
					pluma.fillStyle = 'white';
					pluma.fillText(descifrar(valor.toString(), clave), 45*ii + 20, 45*jj + 31);
				}
			}
		}
	}
	pluma.fillStyle = 'black';
	pluma.font = '10px Arial';
	var ind1 = 0;
	var ind2 = 0;
	for (var ii=0; ii < matriz.length; ii++){
		var check1 = false;
		var check2 = false;
		for (var jj=0; jj < matriz[0].length; jj++){
			if (matriz[ii][jj]==0 && check1!=false){
				pluma.fillText(descifrar(filas[ind1], clave), 45*ii + 20, 45*jj + 7);
				ind1++;
			}
			if (matriz[ii][jj]!=0 && check1==false){
				pluma.fillText(descifrar(filas[ind1], clave), 45*ii + 20, 45*jj - 4);
			}
			if (matriz[jj][ii]==0 && check2!=false){
				pluma.fillText(descifrar(columnas[ind2], clave), 45*jj + 3, 45*ii + 23);
				ind2++;
			}
			if (matriz[jj][ii]!=0 && check2==false){
				pluma.fillText(descifrar(columnas[ind2], clave), 45*jj - 9, 45*ii + 23);
			}
			check1 = matriz[ii][jj]!=0;
			check2 = matriz[jj][ii]!=0;
		}
	}
}

function dibujar_clave(){
	pluma.textAlign = 'center';
	pluma.font = '20px Arial';
	for (var ii=0; ii<10; ii++){
		pluma.fillStyle = 'black';
		pluma.fillText(alf[ii] + '=', 45*puzzle.length + 25, 35*ii + 74);
		pluma.fillRect(45*puzzle.length + 40, 53 + 35*ii, 28, 28);
		pluma.stroke();
	}
	pluma.fillStyle = 'white';
	for (var ii=0; ii<10; ii++){
		if (llaves[ii] != -1){
			pluma.fillText(llaves[ii].toString(), 45*puzzle.length + 53, 35*ii + 74);
		}
	}
}

function actualizar(){
	pluma.fillStyle = 'white';
	pluma.fillRect(0, 0, 600, 600);
	dibujar(puzzle, fsumas, csumas, llaves);
	dibujar_clave();
	if (selected!=[]){
		pluma.fillStyle = 'rgb(5, 200, 100)';
		if (selected[0]=='puzzle'){
			pluma.beginPath();
			pluma.moveTo(45*selected[1], 45*selected[2]);
			pluma.lineTo(45*selected[1] + 40, 45*selected[2]);
			pluma.lineTo(45*selected[1] + 40, 45*selected[2] + 40);
			pluma.lineTo(45*selected[1], 45*selected[2] + 40);
			pluma.lineTo(45*selected[1], 45*selected[2]);
			pluma.stroke()
		}
		if (selected[0]=='clave'){
			pluma.beginPath();
			pluma.moveTo(45*puzzle.length + 40, 53 + 35*selected[1]);
			pluma.lineTo(45*puzzle.length + 40 + 28, 53 + 35*selected[1]);
			pluma.lineTo(45*puzzle.length + 40 + 28, 53 + 35*selected[1] + 28);
			pluma.lineTo(45*puzzle.length + 40, 53 + 35*selected[1] + 28);
			pluma.lineTo(45*puzzle.length + 40, 53 + 35*selected[1]);
			pluma.stroke();
			//pluma.fillRect(45*puzzle.length + 40, 53 + 35*selected[1], 28, 28);
		}
	}
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
	console.log(x, y);
	xx = parseInt(x/45);
	yy = parseInt(y/45);
	if (xx<puzzle.length && yy < puzzle.length){
		if (x - 45*xx < 40 && y - 45*yy < 40){
			if (puzzle[xx][yy] > 0 && puzzle[xx][yy] < 10 || puzzle[xx][yy]== -1){
				selected = ['puzzle', xx, yy];
				console.log('selected puzzle');
			}
		}
	}
	if (x > 45*puzzle.length + 40 && x < 45*puzzle.length + 68){
		yyy = parseInt((y - 53)/35);
		if (yyy>=0 && yyy<10){
			if (y - 53 - 35*yyy < 28){
				selected = ['clave', yyy]
				console.log('selected clave');
			}
		}
	}
	actualizar()
}, false);

window.addEventListener("keydown", function(event) {
	if (event.keyCode > 47 && event.keyCode < 58) {
		if (selected[0]=='puzzle'){
			puzzle[selected[1]][selected[2]] = event.keyCode - 48;
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
});

function comenzar(){
	llaves = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1];
	var kakuro = generar(forma);
	puzzle = kakuro[0];
	fsumas = kakuro[1];
	csumas = kakuro[2];
	actualizar();
}

comenzar();
