#!/usr/bin/env python
from ib_insync import *
import click
import logging
import pandas as pd
import math
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


@click.command()
@click.argument('symbol')
def main(symbol):
    # util.logToConsole(logging.DEBUG)

    s = symbol.upper()
    click.echo("reqSecDefOptParams {}".format(s))

    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=3, readonly=True)

    contract = Stock(s, 'SMART', 'USD')

    ib.qualifyContracts(contract)
    click.echo(contract)

    ib.reqMarketDataType(4)

    [ticker] = ib.reqTickers(contract)

    value = ticker.marketPrice()
    click.echo("Market Prioce {}: {}".format(s, value))

    chains = ib.reqSecDefOptParams(
        contract.symbol, '', contract.secType, contract.conId)

    click.echo(util.df(chains))

    chain = next(c for c in chains if c.exchange == 'SMART')

    strikes = [strike for strike in chain.strikes
               if value - 1.5 < strike < value + 1.5]
    expirations = sorted(exp for exp in chain.expirations)[:1]
    #rights = ['P', 'C']
    rights = ['P']

    contracts = [Option('INTC', expiration, strike, right, 'SMART', tradingClass='INTC')
                 for right in rights
                 for expiration in expirations
                 for strike in strikes]

    contracts = ib.qualifyContracts(*contracts)
    click.echo(len(contracts))

    tickers = ib.reqTickers(*contracts)

    print(tickers)


if __name__ == "__main__":
    main()