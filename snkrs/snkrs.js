const {runScraper, sleep, parseJson} = require('../functions.js');
const {token, serverIDS, delay} = require('../config.json');
const {sendMessages} = require('../embeds.js');

const fs = require('fs');
const {Client, Intents, MessageEmbed, GuildManager} = require('discord.js');
const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES] });

client.login(token);

client.on('ready', () => {
	console.log("BOT snkrs iniciado");
	main();
});

async function main(){
	var i = 1;
	while(true){
		var time = new Date();
		console.log("Consulta snkrs nro:", i, "Time: ", time.toLocaleTimeString());

		res = await runScraper(["./scrapper.py"]);
		newProducts = parseJson(res);

		if (newProducts.length > 0){
			console.log("Nuevos productos: ", newProducts);

			newProducts.forEach(shoe => {
				if(shoe['ERROR'])
					console.log('ERROR');
				else
					sendMessages(client, shoe, "snkrs");
			});
		}

		await sleep(delay["snkrs"]);
		i = i+1;
	}
}
