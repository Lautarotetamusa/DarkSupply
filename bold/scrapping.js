const XMLHttpRequest = require('xhr2');
const fs = require('fs');
const {MessageEmbed} = require('discord.js');

const api = "https://api.cxl8rgz-articulos1-p1-public.model-t.cc.commerce.ondemand.com"

const listUrl = api + "/rest/v2/boldb2cstore/products/search?fields="+
                "products(url,code,name,price(value),images(url),stock(FULL))" +
                "&query=:DEFAULT:allCategories:boldMarcas&currentPage=__PAGE__&pageSize=100&lang=es_CL&curr=CLP";


const detailUrl = api + "/rest/v2/boldb2cstore/products/__CODE__?fields=" +
                   "variantOptions(code, priceData(value), stock(stockLevel), url, variantOptionQualifiers(value))"+
                   "&lang=es_CL&curr=CLP"

function httpGetAsync(theUrl, callback){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4){
          if (xmlHttp.status == 200){
              callback(xmlHttp.responseText);
	        }
          else{
              console.log("HTTP error: ", xmlHttp.statusText);
	            console.log("request:    ", theUrl);
              callback("err");
	        }
        }
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous
    xmlHttp.setRequestHeader('User-Agent',"Googlebot");
    xmlHttp.send(null);
}

function findDiff(arr1, arr2){
    var diff = [];
    arr1.forEach(i => {
      var cont = 0;
      arr2.forEach(j => {
        if (i["name"] != j["name"])
          cont ++;
      });
      if (cont == arr2.length)
        diff.push(i);
    });

    return diff;
}

function writeInFile(filename, data){
  fs.writeFile(filename, JSON.stringify(data, null, " "), function(err) {
      if (err)
          console.log(err);
      else
        console.log("Write data in file");
  });
}

async function setVariants(arr){
  var file = {};

  for (var i = 0; i < arr.length; i++) {
    var uri = detailUrl.replace("__CODE__", arr[i].code);
    await getVariant(arr[i], uri, file).then(obj => {
      file = obj;
    });
    console.log("escribiendo variants: ", uri);
  }
  fs.writeFileSync('variants.json', JSON.stringify(file, null, " "), {encoding:'utf8', flag:'w'});
}

function getVariant(i, uri, obj){
  return new Promise((resolve, reject) =>
  httpGetAsync(uri, function(response){
    var variants = parseVariants(response);
    obj[i.code] = {
      variants: variants
    }
    resolve(obj);
  }));
}
function parseVariants(response){
  var variants = [];

  if (response != "err"){
    var jsonData = JSON.parse(response);
    var v = jsonData["variantOptions"];
    var file;

    if(typeof(v) != "undefined"){
      v.forEach(i => {
        variants.push({
          code  : i.code,
          stock : i.stock["stockLevel"],
          size  : i.variantOptionQualifiers[0]["value"],
          url   : "https://bold.cl".concat(i.url)
        });
      });
    }
  }

  return variants;
}
function parseProduct(rawData){

  var file = [];
  if (rawData != "err"){
    var jsonData = JSON.parse(rawData);
    var products = jsonData["products"];

    products.forEach(i => {
        file.push({
            name:  i.name,
            price: i.price['value'],
            code:  i.code,
            stock: i.stock['stockLevel'],
            image: api.concat(i.images[1]['url']),
            url:   "http://bold.cl".concat(i.url)
        });
    });
  }else{
    console.log("Error obtain data");
  }

  return file;
}

async function checkNewProducts(newData){
  var oldData = fs.readFileSync('data.json', {encoding:'utf8', flag:'r'});

  try {
    oldData = JSON.parse(oldData);
  } catch (e) {
    console.log("ERROR: el archivo data.json esta vacio...");
    oldData = newData;
  }

  let nuevo   = findDiff(newData, oldData);
  let borrado = findDiff(oldData, newData);

  if(nuevo.length > 0){
    console.log("PRODUCTOS NUEVOS: ");
    console.log("Old: ", oldData.length, " | New:", newData.length);

    console.log("NUEVO:", nuevo.length);
    writeInFile("nuevo.json", nuevo);
    writeInFile("olddata.json", oldData);
    writeInFile("borrado.json", borrado);
    //console.log(nuevo);

    if(newData.length > 0){
      writeInFile("data.json", newData);
    }

    await setVariants(nuevo);
    console.log("Se escribieron todas las variantes");
  }

  if(borrado.length > 0){
    console.log("PRODUCTOS BORRADOS: ");
    console.log("Old: ", oldData.length, " | New:", newData.length);

    console.log("BORRADO:", borrado.length);
    console.log(borrado);

    if(newData.length > 0){
        writeInFile("data.json", newData);
    }
  }

  return new Promise((resolve, reject) =>{
    resolve(nuevo);
  });
}

function getData(page){
  return new Promise((resolve, reject) =>{
    httpGetAsync(listUrl.replace("__PAGE__", page), function(response){
      var parseRes = parseProduct(response);
      resolve(parseRes);
    });
  });
}

module.exports = {getData, checkNewProducts};
