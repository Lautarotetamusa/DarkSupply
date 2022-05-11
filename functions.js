var spawn = require('child_process').spawn;

async function consult(mode, sendMessage){
	res = await runScraper(["./scraper.py", mode]);
	newProducts = parseJson(res);

	if (newProducts.length > 0){
		console.log("nuevos: ", newProducts);
		newProducts.forEach(shoe => {
			if(shoe['ERROR']){
				console.log('ERROR');
			}else{
				sendMessage(shoe);
			}
		});
	}
}
function runScraper(mode) {
    return new Promise((resolve, reject) => {
        var command = spawn('python3',mode);
        var result = ''
        command.stdout.on('data', function(data) {
             result += data.toString()
        })
        command.on('close', function(code) {
				  	command.kill();
						console.log(result);
            resolve(result);
        })
        command.on('error', function(err) { reject(err) })
    })
}
function parseJson(data){
	products = []
	try {
		products = JSON.parse(data);
		if (products["ERROR"]){
			console.log("ERROR in scraper.py");
			console.log(products["ERROR"], products["Exception"]);
		}
	} catch (e) {
		console.log('error in python scraper', data);
		products = [];
	}
	return products;
}
function sleep(ms){
	return new Promise((resolve) => {
		setTimeout(resolve, ms*1000);
	});
}

module.exports = {runScraper, sleep, consult, parseJson}
