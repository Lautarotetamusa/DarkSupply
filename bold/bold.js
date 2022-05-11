const {getData, checkNewProducts} = require('./scrapping.js');
const {sleep} = require('../functions.js');
const fs = require('fs');

const {token, serverIDS, delay} = require('../config.json');

const {Client, Intents, MessageEmbed, GuildManager} = require('discord.js');
const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES] });

client.login(token);

client.on('ready', () => {
	console.log("BOT iniciado");
	getDiff();
});

async function getDiff(){

	var consulta = 1;
	while(true){
		var res;
	  var products = [];
	  var page;
	  var pageNumber = 0;
		var diference = [];
		var error = false;

		var time = new Date();
		console.log("consulta bold nro: ", consulta, "Time: ", time.toLocaleTimeString());
		do {
	    await getData(pageNumber).then(response => {
	      page = response;
	    });
	    pageNumber ++;
			if(page == [])
				error = true

			products = products.concat(page);
	  } while (page.length > 0);

		if (error == false){
			await checkNewProducts(products).then(diff => {
		    diference = diff;
		  });
		}

		if(diference.length > 0){
			diference.forEach(i => {
				var embed = createMessage(i);
				sendMessages(embed);
			});
		}

		consulta += 1;

		//await sleep(delay["bold"]);
	}
}
function sendMessages(embed){
	serverIDS.forEach(server => {
		if(server["avaible"]){
			var c = client.channels.cache.get(server["channels"]["bold"]);
			c.send({ embeds: [embed], files: ['../icon.png'] })
			console.log("mensaje enviado a: ", server["name"]);
		}
	});
}
function createMessage(product){
		var description = "";
		var rawData = fs.readFileSync('variants.json', {encoding:'utf8', flag:'r'});
		var data = JSON.parse(rawData);
		var detail_producto = data[product["code"]];
		var variants = detail_producto["variants"];

		variants.forEach( i => {
			description += "**"+ i["size"] +"**\t - [QTY: "+ i["stock"] +"]\n";
		});

		stock = product["stock"] ? product["stock"].toString() : "-";

		var embed = new MessageEmbed()
		.setColor('#C800FF')
		.setTitle(product["name"])
		.setURL(product["url"])
		.setDescription(description)
		.setThumbnail(product["image"])
		.addFields(
			{ name: 'Price', value: product["price"].toString() },
			{ name: 'Stock', value: stock },
			{ name: 'Code',  value: product["code"].toString() },
		)
		.setTimestamp()
		.setFooter({ text: 'Provider by darksupply', iconURL: 'attachment://icon.png' });

		return embed;
}
