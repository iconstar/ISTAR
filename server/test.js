var str = "hx8cfb20aae3e75e6dbfe016a73b38a6b31f3ed101,1551184289705"

var list = str.split(",");
console.log("list: "+list);

var address = list[0];
var time = list[1];

console.log("address: "+address);
console.log("time: "+time);