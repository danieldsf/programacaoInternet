const vetor = ['static/irineu1.jpg', 'static/num_sei.jpg', 'static/nunca_nem_vi.jpg'];
let cont = 0, objeto = document.getElementById("irineu");
//INIT:
objeto.src = vetor[0];

function irineu(){
	if(cont == 2)
		cont = -1
	cont++;
	objeto.src = vetor[cont];
}
