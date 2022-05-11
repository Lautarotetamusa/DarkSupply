const {MessageEmbed} = require('discord.js');
const {serverIDS} = require('./config.json');

function createEmbed(product, monitor){
	var description = "";
	var variants = product["variants"];

	variants.forEach( i => {
    if(i["stock"] <= 0){
		   description += i["size"]+" - [QTY: 0]\n";
     }
    else {
      description += "[**"+i["size"] +"**]("+i["cartUrl"]+")";
			description += "  -  **[QTY: "+ i["stock"] +"]**\n";
    }
	});
	description += ""

	var embed = new MessageEmbed()
  .setURL(product["url"])
	.setColor('#E800FF')
	.setTitle(product["name"])
	.setDescription(description)
	.setThumbnail(product["img"])
	.addFields(
		{ name: 'Price',       value: product["price"].toString(), inline: true },
		{ name: 'ID',          value: product["id"].toString(),    inline: true },
	)
	.setTimestamp()
	.setFooter({ text: 'Provider by darksupply', iconURL: 'attachment://icon.png' });

	if(monitor == 'snkrs'){
		embed.setAuthor({name: 'SNKRS', iconURL:'https://nikeclprod.vteximg.com.br/arquivos/favicon.png?v=637671335585370000'});
		embed.addFields(
			{ name: 'Stock',       value: product["stock"].toString(), inline: true },
			{ name: 'Release Date',value: product["releaseDate"].toString(),    inline: false },
		);
	}else if(monitor == 'nike'){
		embed.setAuthor({name: 'nike.cl', iconURL:'https://nikeclprod.vteximg.com.br/arquivos/favicon.png?v=637671335585370000'})
	}

	return embed;
}

function messageATC(product){

	var description = "[** ATC Link **]("+product["cartUrl"]+")";

	var embed = new MessageEmbed()
	.setAuthor({name: 'nike.cl', iconURL:'https://nikeclprod.vteximg.com.br/arquivos/favicon.png?v=637671335585370000'})
	.setColor('#1a1e1e')
	.setTitle('SHOCKDROP')
	.setThumbnail(product["img"])
	.setDescription(description)
	.addFields(
		{ name: 'Name',   	value: product["name"].toString() },
		{ name: 'Price',   	value: product["price"].toString(), inline:true},
		{ name: 'Sku',   		value: product["sku"].toString(), 	inline:true },
		{ name: 'Size',  		value: product["size"].toString(),  inline:true },
	)
	.setTimestamp()
	.setFooter({ text: 'Provider by darksupply', iconURL: 'attachment://icon.png' });

	return embed;
}

function sendMessages(client, shoe, monitor){
	embed = createEmbed(shoe, monitor);

	serverIDS.forEach(server => {
		if(server["avaible"]){
			var c = client.channels.cache.get(server["channels"][monitor]);
			c.send({ embeds: [embed], files: ['../icon.png'] })
			console.log("mensaje enviado a: ", server["name"]);
		}
	});
}

module.exports = {sendMessages, createEmbed, messageATC}
