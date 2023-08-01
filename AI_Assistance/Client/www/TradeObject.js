class TradeObject {
    constructor(cmrName , buySellIndicator, ccy, ctr, allInRate, isInverted, valueDate) {
        this.cmrName = cmrName;
        this.buySellIndicator = buySellIndicator;
        this.isInverted = isInverted;
        this.ccy = ccy;
        this.ctr = ctr;
        this.allInRate = allInRate;
        this.valueDate = valueDate;
    }
}

export {TradeObject}
