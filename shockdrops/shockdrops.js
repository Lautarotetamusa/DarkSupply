const {sleep, parseJson, runScraper} = require('../functions.js');
const {token, serverIDS, delay} = require('../config.json');
const {messageATC} = require('../embeds.js');
const commands = require('./commands.js')

const fs = require('fs');

const {Client, Intents} = require('discord.js');
const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES] });

client.login(token);

client.on('ready', () => {
	console.log("BOT Skus iniciado");
	main();
});

async function main(){
		var i = 1;

		while(true){
			// SKUs en la lista
			time = new Date();
			console.log("Consulta SKUs nro:", i, "Time: ", time.toLocaleTimeString());

			res = await runScraper(["./restock.py", "restock"]);
			newProducts = parseJson(res);

			if (newProducts.length > 0){
				console.log("nuevos: ", newProducts);
				newProducts.forEach(shoe => {
					if(shoe['ERROR']){
						console.log('ERROR');
					}else{
						const embed = messageATC(shoe);
						var c = client.channels.cache.get(serverIDS[1]["channels"]["skus"]);
						c.send({ embeds: [embed], files: ['../icon.png'] });
						var c = client.channels.cache.get(serverIDS[1]["channels"]["skus-consola"]);
						c.send({ embeds: [embed], files: ['../icon.png'] });
					}
				});
			}

			await sleep(delay["skus"]);
			i++;
		}
}

client.on('message', msg => {
	if(msg.content[0] != "!") return;
	var args = msg.content.split(' ');

	var isAdmin = (msg.member != null) && (msg.member.permissionsIn(msg.channel).has("ADMINISTRATOR"));

	if(isAdmin){
		try {
			const data = fs.readFileSync('monitored-skus.json', 'utf8');
			list_skus = JSON.parse(data);
		} catch (e) {
			list_skus = [];
		}

		command = args[0].toLowerCase().substr(1);
		try {
			commands[command](args, msg, list_skus, client);
		} catch (e) {
			console.log("se ingreso otro comando");
		}
	}else
		msg.reply("Debes ser admistrador para utilizar comandos");

});
