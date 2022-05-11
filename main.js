const {token, serverIDS} = require('./config.json');

const {Client, Intents, MessageEmbed, GuildManager} = require('discord.js');
const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES] });

const spawn = require("child_process").spawn;
const execSync = require("child_process").execSync;
var exec = require('child_process').exec,
    child;

/*const monitores = {
  "nike":  require('./nike/nike.js'),
  "snkrs": require('./snkrs/snkrs.js'),
  "bold":  require('./bold/bold.js').main,
};*/


const monitores = ["snkrs", "nike", "bold", "shockdrops"];

client.login(token);
client.on('ready', () => {
	console.log("BOT iniciado");
});

client.on('message', msg => {
	if(msg.content[0] == "!"){
		var args = msg.content.split(' ');

		var isAdmin = (msg.member != null) && (msg.member.permissionsIn(msg.channel).has("ADMINISTRATOR"));

    monitor = args[1];
    command = args[0].toLowerCase().substr(1);

		if(isAdmin){
      switch (command) {
        case  "stop":
          stop(monitor, msg);
          break;
        case  "start":
          start(monitor, msg);
          break;
      }
    }else{
        msg.reply("debes ser adminstrador para usar este comando")
    }

    switch (command) {
      case  "status":
        //is_running(monitor, msg);
        var embed = statusEmbed();
        var c = client.channels.cache.get(serverIDS[1]["channels"]["skus-consola"]);
        c.send({ embeds: [embed], files: ['./icon.png'] });
        break;
    }
  }
});

function stop(monitor, msg){
  child = exec('pgrep -f '+monitor+'.js',
    function (error, stdout, stderr) {
      console.log(stdout);
      if(stdout){
          child = exec('pkill -f '+monitor+'.js', function(){
            msg.reply('Monitor apagado');
          });
      }else{
          msg.reply('El monitor '+monitor+'ya está apagado');
      }
  });
}

function start(monitor, msg){
  child = exec('pgrep -f '+monitor+'.js',
    function (error, stdout, stderr) {
      if(stdout){
          msg.reply('El monitor '+ monitor+' ya está encendido');
      }else{
        child = exec('./run.sh '+monitor)
        msg.reply('Monitor encendido');
      }
  });
}

function is_running(monitor, msg) {
    child = exec('pgrep -f '+monitor+'.js',
      function (error, stdout, stderr) {
        console.log(stdout);
        if(stdout){
            msg.reply('El monitor está encendido');
        }else{
            msg.reply('El monitor '+monitor+' está apagado');
        }
    });
}

function statusEmbed(){
  var description = "";
  monitores.forEach(i => {
    var stdout = ""

    try {
      stdout = execSync('pgrep -f '+i+'.js').toString();
    } catch (e) {
      stdout = e.stdout.toString();
    }
    if(stdout != ""){
      description += "✅ " + i + "\n";
    }else{
      description += "🔴 " + i + "\n";
    }
  });
  console.log("description", description);


  var embed = new MessageEmbed()
	.setColor('#E800FF')
	.setTitle("status")
	.setDescription(description)
	.setTimestamp()
	.setFooter({ text: 'Provider by darksupply', iconURL: 'attachment://icon.png' });

	return embed;
}
