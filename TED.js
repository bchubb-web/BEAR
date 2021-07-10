const {exec} = require("child_process");
var SerialPort = require('serialport');
try{
    var port = new SerialPort("COM4", {baudRate:9600});
}
catch(err){
    console.log("ARDUINO NOT FOUND");
    console.log("connect arduino board to allow for serial communication with The Bear")
}
const bodyParser = require('body-parser');
const express = require("express");
const app = express();

const pug = require('pug');

const MongoClient = require("mongodb").MongoClient;
const dbUrl = "mongodb://localhost:27017";

const path = require("path");
const file = require("fs");

//MODULES USED

app.use('/public/styles',express.static(__dirname+'/styles'));
app.use('/public/js',express.static(__dirname+'/js'));
app.use('/public/images',express.static(__dirname+'/images'));
app.use('/public/files',express.static(__dirname+'/../documentation'))
app.use(bodyParser.urlencoded({extended: true}));

//INIT EXPRESS FOLDERS

var data = {}
var status = 'Running';
var speech = 'Hello World';

function turnLeft(port){
    //SENDS SERIAL DATA TO ARDUINO FOR A LEFT TURN
    port.write('6',function(err){
        if(err)throw err;});
}

function turnRight(port){
    //SENDS SERIAL DATA TO ARDUINO FOR A RIGHT TURN
    port.write('9',function(err){
        if(err)throw err;});
}

function findFriend(MongoClient, url, name){
        //FUTURE FUNCTION TO FIND A FRIEND IN THE BEARS DATABASE
    MongoClient.connect(url,function(err,db){
        //connect to mongo
        if(err) throw err;
        var dbo = db.db("BEAR");//find the correct db
        dbo.collection("Bear_Friends").find({},{ projection:{name: name}//select the record within the friends collection that matches the name parameter given
        }).toArray(function(err,result){
            if(err) throw err;//    <<TODO>>    handle errors to return false, meaning the name given isnt found in the database
            console.log(result);
            db.close();//close connection to the db
        });
    });
}

function addFriend(MongoClient,url, name, age, gender){
    MongoClient.connect(url,function(err,db){
        //connect to mongo
        if(err){return "Db connect failed"};
        var dbo = db.db("BEAR");//find correct database
        var friend = {
            name: name,
            age: age,
            gender: gender
        };//enter the given information into an object
        dbo.collection("Bear_Friends").insertOne(friend,function(err,res){//insert into the friends collection
            if (err) {return "add friend failed"};
            console.log(name +" is now my friend!");
            db.close();
            return name+" is now my friend";
        });
    });
}

function returnFriends(MongoClient,url){
    MongoClient.connect(url, function(err,db){
    if(err){console.log("AHHHH")};
    var dbo = db.db("BEAR");
    dbo.collection("Bear_Friends").find({}).toArray(function(err,result){
        if (err){console.log("SHID")};
        var friends = []
        for(var i = 0;i<result.length;i++){
            friends.push("<p>"+result[i].name+"</p>");
        }
        db.close();
        return friends;
    });


});
}


//    SET
app.set('views',path.join(__dirname+'/views'));
app.set('view engine','pug');
app.set('title', 'BEAR');


//    GET 

app.get('/',(req,res) => {
    //send head of page
    res.render('index',{
        friends: returnFriends(MongoClient,dbUrl)
    });
});

app.get('/index',(req,res)=>{
    res.sendFile()
});

app.get('/face',(req,res)=>{
    //page that shows most recent co-ordinates of a face
    res.send(data);
});


app.get('/friends',(req,res)=>{
    res.sendFile(path.join(__dirname+"/index.html"));
});

//    POST

app.post('/face',(req,res)=>{
    console.log(req.body);
    data = req.body;
    var x = parseInt(data.x);
    var y = parseInt(data.y);
    var w = parseInt(data.w);
    var h = parseInt(data.h);
    if (x > 320){
        turnRight(port);
	    console.log("right");
	}
    if (x+w < 320){
        turnLeft(port);
	    console.log("left");
    }
    res.sendStatus(200)
});

app.post('/speak',(req,res)=>{
     speech = req.body.text;
});

app.post('/friend',(req,res)=>{
    var data = req.body;
    var age = data.age;
    var name = data.name;
    var gender = data.gender;
    status = addFriend(MongoClient,dbUrl,name,age,gender);
    res.sendStatus(200);
});



app.listen(3000,console.log('TED active'));
