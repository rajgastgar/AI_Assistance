class TradeObject {
    constructor(cmrName , buySellIndicator, ccy, ctr, allInRate, isInverted, valueDate, ccyAmount,ctrAmount,notes,typeOfTrade ) {
        this.cmrName = cmrName;
        this.buySellIndicator = buySellIndicator;
        this.isInverted = isInverted;
        this.ccy = ccy;
        this.ctr = ctr;
        this.allInRate = allInRate;
        this.valueDate = valueDate;
        this.ccyAmount = ccyAmount;
        this.ctrAmount = ctrAmount;
        this.notes = notes;
        this.typeOfTrade = typeOfTrade;
    }
}

export {TradeObject}
