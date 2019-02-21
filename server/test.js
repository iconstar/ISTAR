


// var obj = JSON.parse('{"content":{"path":"callie/circle","type":"file"},"video":{"videoId":"CvIr-2lMLs‌​k","endSeconds":"30","startSeconds":15}}');
// console.log(obj.content);
// var obj2 = obj.content;
var a = "{'player': 'Griffin', 'run': 306, 'power': 355, 'dribble': 390}"
console.log(a.replace(/\'/gi, "\""));
var b = a.replace(/\'/gi, "\"");

// var a = '{"player": "Griffin", "run": 306, "power": 355, "dribble": 390}'
// console.log("a: "+a);
console.log(typeof(b));
var obj = JSON.parse(b);
console.log(typeof(obj));
console.log(obj.player);
// var array = a.split(',');
// console.log("fkakfdhk"+ a.split[',']);

// console.log(array.length);

// var property = String(array).split(":");

// console.log(property);
// for(var i=0; i<array.length; i++) {
//     console.log(array[i]);
// }
// console.log(typeof(array));

// console.log(array);

// var beforeStr = "02-123-4567";
// var afterStr = beforeStr.split('-');

// console.log("fkakfdhk"+ beforeStr);
// console.log("adfadf"+afterStr);