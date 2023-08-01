import { TradeObject } from "./TradeObject.js";

document.getElementById("speakCommand").onclick = function giveCommand(){       
    eel.giveCommand()(call_Back)  
}  

document.getElementById("getLiveRate").onclick = function getLiveRate(){
    const ccy = document.getElementById("ccy").value;
    const ctr = document.getElementById("ctr").value;
    eel.getLiveRate(ccy +" "+ ctr)(call_Back_rate)  
}  

const submitElement = document.getElementById("submitTrade");
submitElement.addEventListener("click", submitTrade);

function submitTrade(){  
    const cmrName = document.getElementById("cmrName").value;
    const buySellIndicator = document.getElementById("buySellIndicator").value;    
    const ccy = document.getElementById("ccy").value;
    const ctr = document.getElementById("ctr").value;
    const allInRate = document.getElementById("allInRate").value;
    const isInverted = document.getElementById("isInverted").value == "on" ? true :  false;
    const valueDate = document.getElementById("valueDate").valueAsDate;
    const tobj = new TradeObject(cmrName , buySellIndicator, ccy, ctr, allInRate, isInverted, valueDate);
    console.log("object created is "+isInverted)
    eel.submitTrade(JSON.stringify(tobj))(submitTradeCallback)  
}  

// function submitValues(){
//     cmrName = document.getElementById("cmrName").value;
//     buySellIndicator = document.getElementById("buySellIndicator").value;    
//     ccy = document.getElementById("ccy").value;
//     ctr = document.getElementById("ctr").value;
//     allInRate = document.getElementById("allInRate").value;
//     isInverted = document.getElementById("isInverted").checked;
//     valueDate = document.getElementById("valueDate").valueAsDate;
//     tobj = new TradeObject(cmrName , buySellIndicator, ccy, ctr, allInRate, isInverted, valueDate);
//     console.log("object created is "+tobj)
//     eel.submitTrade(JSON.stringify(tobj))(submitTradeCallback) 
// }

function populateTradeDetails(tradeData){
    console.log("Inside populate")
    const jsonObj = JSON.parse(tradeData)    
    document.getElementById("cmrName").value = jsonObj.cmrName[0] 
    document.getElementById("buySellIndicator").value = jsonObj.buySellIndicator[0]
    
    document.getElementById("ccy").value = jsonObj.ccy[0]
    document.getElementById("ctr").value = jsonObj.ctr[0]
    document.getElementById("allInRate").value = jsonObj.allInRate[0]

    document.getElementById("isInverted").checked = jsonObj.isInverted[0] 
    document.getElementById("valueDate").valueAsDate = new Date();
}

function call_Back(output){  
    document.getElementById("speakCommand").value = output
    if(output != "Error"){
        eel.processCommand(output)        
    }
    displayMessage("CLICK HERE TO SPEAK");    
}

function submitTradeCallback(output){  
    displayResult(output)
    displayMessage("CLICK HERE TO SPEAK");    
}

function call_Back_rate(output){  
    displayResult(output)
    displayMessage("CLICK HERE TO SPEAK");    
}

eel.expose(displayMessage);
eel.expose(displayResult);
eel.expose(populateTradeDetails);
eel.expose(displayAllInRate);
eel.expose(getLiveRate);
eel.expose(submitTrade);

function displayMessage(message){
    console.log("Inside display message !!! ")
    document.getElementById("speakCommand").innerHTML = message
}

function displayResult(message){
    document.getElementById("result").innerHTML = message
}

function getLiveRate(){
    const ccy = document.getElementById("ccy").value
    const ctr = document.getElementById("ctr").value
    eel.getLiveRate(ccy+" "+ctr)
}

function displayAllInRate(message){
    document.getElementById("rateResult").innerHTML = message
}
