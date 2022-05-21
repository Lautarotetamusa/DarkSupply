const {parseJson, runScraper} = require('../functions.js');
const {token, serverIDS, delay} = require('../config.json');
const {messageATC} = require('../embeds.js');

// lpm

async function update(args, msg, txt, fun){
	var update = [];
	for (var i = 1; i < args.length; i++) {
		if(typeof(args[i]) != "undefined"){
				update.push(args[i])
		}else{
			msg.reply("Debes ingresar un SKU valido");
		}
	}

	await runScraper(["./scraper.py", fun].concat(update));
	msg.reply(txt);
}

function addsku(args, msg){
	console.log("addsku command");

	update(args, msg, 'SKUs agregados', 'add');
}

function removesku(args, msg){
	console.log("removesku command");

	update(args, msg, 'Los SKU fueron retirados de la lista de monitoreo', 'remove');
}

async function checksku(args, msg, client){
	console.log("checksku command");

	var consultar = [];
	for (var i = 1; i < args.length; i++) {
		consultar.push(args[i]);
	}

	res = await runScraper(["./scraper.py", "check"].concat(consultar));
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

async function listsku(args, msg){
	console.log("listsku command");

	res = await runScraper(["./scraper.py", "list"]);

	if(res.length > 0){
		msg.reply(res);
	}else{
		msg.reply("Actualmente no se esta monitoreando ningun par");
	}
}

module.exports = {addsku, removesku, checksku, listsku}
