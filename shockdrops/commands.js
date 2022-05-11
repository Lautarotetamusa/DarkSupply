const {parseJson, runScraper} = require('../functions.js');
const {token, serverIDS, delay} = require('../config.json');
const {messageATC} = require('../embeds.js');

async function addsku(args, msg, list_skus, client){
	console.log("addsku command");

	var agregar = [];
	for (var i = 1; i < args.length; i++) {
		if(typeof(args[i]) != "undefined"){
			if (list_skus.includes(args[i])){
				msg.reply('El SKU '+ args[i] +' ya se encuentra en la lista de monitoreo');
			}else{
				agregar.push(args[i]);
			}
		}else{
			msg.reply("Debes ingresar un SKU valido");
		}
	}

	await runScraper(["./restock.py", "add"].concat(agregar));
	msg.reply("SKUs agregados");
}

async function removesku(args, msg, list_skus, client){
	console.log("removesku command");

	var eliminar = [];
	for (var i = 1; i < args.length; i++) {
		if(typeof(args[i]) != "undefined"){
			if (list_skus.includes(args[i])){
				eliminar.push(args[i])
			}else{
				msg.reply('El SKU '+ args[i] +' NO se encuentra en la lista de monitoreo');
			}
		}else{
			msg.reply("Debes ingresar un SKU valido");
		}
	}

	await runScraper(["./restock.py", "remove"].concat(eliminar));
	msg.reply('Los SKU fueron retirados de la lista de monitoreo');
}

async function checksku(args, msg, list_skus, client){
	console.log("checksku command");

	var consultar = [];
	for (var i = 1; i < args.length; i++) {
		consultar.push(args[i]);
	}

	res = await runScraper(["./restock.py", "check"].concat(consultar));
	product = parseJson(res);

	if(product.length > 0){
		product.forEach(i => {
			const embed = messageATC(i);
			var c = client.channels.cache.get(serverIDS[1]["channels"]["skus-consola"]);
			c.send({ embeds: [embed], files: ['../icon.png'] });
		});
	}else{
		msg.reply("Nigun skus se encuentra disponible")
	}
}

function listsku(args, msg, list_skus){
	console.log("listsku command");
	var msgList = "";
	if(list_skus.length > 0){
		list_skus.forEach(i => {
			msgList += i+"\n";
		});
		msg.reply(msgList);
	}else{
		msg.reply("Actualmente no se esta monitoreando ningun par");
	}
}

module.exports = {addsku, removesku, checksku, listsku}
