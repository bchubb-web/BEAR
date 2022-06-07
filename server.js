//MODULES USED
const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
const {exec} = require("child_process");
const {SerialPort} = require('serialport');
try{
    var port = new SerialPort({path:"COM9",baudRate:9600});
}
catch(err){
    console.log("ARDUINO NOT FOUND");
    console.log("connect arduino board to allow for serial communication with The Bear")
    console.log(">-->"+err);
}
const bodyParser = require('body-parser');
const express = require("express");
const app = express();

const pug = require('pug');

const MongoClient = require("mongodb").MongoClient;
const dbUrl = "mongodb://127.0.0.1:27017/";

const path = require("path");
const file = require("fs");
const { CLIENT_RENEG_WINDOW } = require('tls');
const { setFlagsFromString } = require('v8');


//  INIT EXPRESS FOLDERS

app.use('/public/styles',express.static(__dirname+'/styles'));
app.use('/public/js',express.static(__dirname+'/js'));
app.use('/public/images',express.static(__dirname+'/images'));
app.use('/public/files',express.static(__dirname+'/../documentation'))
app.use(bodyParser.urlencoded({extended: true}));


//  VARIABLES

var data = {};
global.entry = "";
global.leave = "";

function turnLeft(port){
    console.log("LEFT");
    //SENDS SERIAL DATA TO ARDUINO FOR A LEFT TURN
    try{
        port.write('6');
    }
    catch(err){
        console.log("[error] - bear serial connection interupted")
        try{
            var port = new SerialPort({path:"COM9",baudRate:9600});
        }
        catch(err){
            console.log("ARDUINO NOT FOUND");
            console.log("connect arduino board to allow for serial communication with The Bear")
            console.log(">-->"+err);
        }
    }
}
function turnRight(port){
    console.log("RIGHT");
    //SENDS SERIAL DATA TO ARDUINO FOR A RIGHT TURN
    try{
        port.write('9');
    }
    catch(err){
        console.log("[error] - bear serial connection interupted")
        try{
            var port = new SerialPort({path:"COM9",baudRate:9600});
        }
        catch(err){
            console.log("ARDUINO NOT FOUND");
            console.log("connect arduino board to allow for serial communication with The Bear")
            console.log(">-->"+err);
        }
    }
}

function get_attending(MongoClient, url){
    var value = "";
    MongoClient.connect(url, function(err,db){//connect to db
        if(err){throw err};
        var dbo = db.db("Bear");
        var attend_query = {main: "THIS"};
        //select the settings document
        dbo.collection("Bear_Settings").find(attend_query,{projection:{attending_val:1}}).toArray(function(err,result){//find settings document
            if(err){throw err};
            console.log(result[0]["attending_val"]);
            value =  result[0]["attending_val"];//get attending value
        });
    });
    while(value == ""){
        console.log("waiting");
    }
    return value;
}

function update_attending(MongoClient, url, data){
    MongoClient.connect(url,function(err,db){//connect to db
        if(err){throw err}
        var dbo = db.db("Bear");
        var query = {main: "THIS"};
        //select the settings document
        var new_values = {$set: {attending_val: data}};
        //set the attending value to the new one specified by the input from the page
        dbo.collection("Bear_Settings").updateOne(query, new_values, function(err, res){
            if(err){throw err};
            console.log(`students will now be registered: ${data}`);
            reg_in = [];
        });
    });
}

function register(MongoClient, url, student, time){

    MongoClient.connect(url, function(err,db){
        if(err){return"DB CONNECT FAILED"};
        var dbo = db.db("Bear");
        var query = {PID: student};
        //connect to db, and create query for finding student
        console.log(query);
        dbo.collection("Bear_register").find(query,{projection:{_id:0}}).toArray(function(err,result){
            if(err){throw err};
            console.log(result[0]);
                var attend = result[0]["attending"];
                //query to find the settings document
                var attend_query = {main: "THIS"};
                dbo.collection("Bear_Settings").find(attend_query,{projection:{attending_val:1}}).toArray(function(err,settings){
                    if(err){throw err};
                    var register_val =  settings[0]["attending_val"];
                    if (attend != register_val){
                        //if the students atteending value is differnet from the settings value
                        var stuVal = { $set: {attending: register_val, last: time}}; // declare new values with iverted attending status
                        console.log(stuVal);
                        dbo.collection("Bear_register").updateOne(query, stuVal, function(err,res){
                            if(err){throw err};
                            console.log(student+" registered at: "+ time);
                        });
                        
                    }
                    
                });
            
        });
    });
}



//  SET

app.set('views',path.join(__dirname+'/views'));
app.set('view engine','pug');
app.set('title', 'BEAR');




//  GET 

app.get('/',(req,res) => {
    //send head of page
    MongoClient.connect(dbUrl,{useUnifiedTopology: true}, function(err,db){//connect to MONGO
        if (err) throw err;//if any errors then return them
        var dbo = db.db("Bear");//sepecify the database we want

        dbo.collection("Bear_Friends").find({}).toArray(function(err,result){//find collection and return all documents to an array
            if (err) throw err;
            var friends = [];
            for(var i = 0; i<result.length;i++)if(!friends.includes("> "+result[i]['name'])){ friends.push("> "+result[i]['name'])};
            db.close();
            res.render('index',{
                friends: friends
            });
        });
    });
});


app.get('/',(req,res) => {
    res.send()
    res.sendStatus(200);
});

app.get('/register', (req,res) => {
    var staff = [];
    var students = [];
    MongoClient.connect(dbUrl,{useUnifiedTopology:true}, function(err,db){//connect to db
        if(err)throw err;
        var dbo = db.db("Bear");
        dbo.collection("Bear_register").find({}).toArray(function(err,result){//get register documents
            if(err) throw err;
            for(var i=0;i<result.length;i++){//iterate through documents
                var pid = result[i].PID;
                if(pid.charAt(0) == "1"){
                    staff.push(result[i]);//add to staff list
                }
                else{
                    students.push(result[i]);//add to student list
                }
            }
                //console.log(result);
            res.render('register',{students: students,staff:staff});//render page
            db.close();
        });
    });
});


//  POST

app.post('/face',(req,res)=>{
    console.log(req.body);

    //get data from request
    data = req.body;
    var x = parseInt(data.x);
    var w = parseInt(data.w);
    var student = data.student;
    var hour = data.time;


    if (x > 320) {//turn right
        console.log(x);
        turnRight(port);
    }
    if (w < 320) {//turn left
        console.log(w)
        turnLeft(port);
    }
    if (x < 320 && w > 320){
        register(MongoClient,dbUrl,student, hour);//register student
    }
    res.sendStatus(200)
});

app.post('/ATTENTION', (req,res)=>{
    var request = req.body;
    var attention = request.BUTTON;
    update_attending(MongoClient,dbUrl, attention);
    return res.redirect("/");
});

app.post('/add_member', (req,res) =>{
    var body = req.body;
    var name = body.first+" "+body.last;
    var YOB = body.yob;
    var position = body.position;
    //generate pid
    //position bit, 0=student 1=staff
    //first and last letters of the first name
    //first and last letters of the last name
    //filler 0
    //last 2 digits of year of birth
    var PID = position + body.first.charAt(0) + body.first.charAt(body.first.length -1) + body.last.charAt(0) + body.last.charAt(body.last.length -1) + "0" +YOB.slice(-2);

    //insert data into db
    MongoClient.connect(dbUrl,{useUnifiedTopology: true}, function(err,db){
        if(err)throw err;
        var dbo = db.db("Bear");
        var reg_obj = {
            "name": name,
            "PID": PID,
            "attending": "NULL",
            "last": "NULL"
        };

        var friend_obj = {
            "name":name,
            "PID": PID,
            "position":position,
            "YOB": YOB
        };

        
        dbo.collection("Bear_register").insertOne(reg_obj, function(err, res) {
            if (err) throw err;
            console.log(reg_obj);
        });

        dbo.collection("Bear_Friends").insertOne(friend_obj, function(err, res) {
            if (err) throw err;
            console.log(friend_obj);
        });
    });
    res.redirect('/register')
});

app.post('/sens', (req,res) => {
    var sens = req.body.sens;
    MongoClient.connect(dbUrl,{useUnifiedTopology:true}, function(err,db){
        if(err)throw err;
        var dbo = db.db("Bear");
        dbo.collection("Bear_Settings").updateOne({main:"THIS"}, {$set: {sensitiviity:"sens"}},function(err,res){//update settings document
            if(err)throw err;
            console.log("updated");
        });
    });
    res.redirect('/');
});


//  INIT server on port 3000
app.listen(3000,console.log('BEAR active'));