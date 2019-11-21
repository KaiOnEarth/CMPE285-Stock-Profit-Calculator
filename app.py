from flask import Flask
from flask import render_template
from flask import request
import requests
import time

app = Flask (__name__)


@app.route('/', methods=['GET', 'POST'])
def cal():
    if request.method == 'GET' :
        return render_template ('index.html')
    elif request.method == 'POST' :

        allotment = request.form['allotment']
        final = request.form['final']
        sell_commission = request.form['sell_commission']
        initial = request.form['initial']
        buy_commission = request.form['buy_commission']
        tax_rate = request.form['tax_rate']

        proceeds = int(allotment) * float (final)
        print_proceeds = "$%.2f" % proceeds

        cost = int (allotment) * float(initial) + float(buy_commission) + float(sell_commission) + 0.01 \
               * float(tax_rate) * (
                           float(proceeds) - float(buy_commission) - float(sell_commission) - int(allotment) *
                           float(initial))
        print_cost = "$%.2f" % cost

        print_initial = "$" + initial
        initial_total = int(allotment) * float(initial)
        print_initial_total = "$%.2f" % float(initial_total)
        print_buy_commission = "$%.2f" % float(buy_commission)
        print_sell_commission = "$%.2f" % float(sell_commission)
        print_tax = tax_rate + "%"
        capital_gain = float(proceeds) - float(buy_commission) - float(sell_commission) - int(allotment) * \
                       float(initial)
        print_capital_gain = "$" + "%.2f" % capital_gain
        tax_on_capital_gain = 0.01 * float(tax_rate) * float(capital_gain)
        print_tax_on_capital_gain = "$" + "%.2f" % tax_on_capital_gain

        net_profit = proceeds - cost
        print_net_profit = "$" + "%.2f" % net_profit

        return_on_investment = net_profit / cost * 100
        print_return_on_investment = "%.2f" % return_on_investment + "%"

        break_even_price = (int(allotment) * float(initial) + float(buy_commission) + float(sell_commission)) / \
                           int(allotment)
        print_break_even_price = "$" + "%.2f" % break_even_price

        return render_template('result.html', proceeds=print_proceeds, cost=print_cost, allotment=allotment,
                                initial=print_initial, initial_total=print_initial_total,
                                buy_commission=print_buy_commission, sell_commission=print_sell_commission,
                                tax=print_tax, capital_gain=print_capital_gain,
                                tax_on_capital_gain=print_tax_on_capital_gain, net_profit=print_net_profit,
                                return_on_investment=print_return_on_investment,
                                break_even_price=print_break_even_price)


@app.route ("/stocks", methods=['GET', 'POST'])
def stock_info():
    if request.method == 'POST':
        stock_symbol = request.form['stock_symbol']
        try:
            now = time.strftime("%a %b %d %H:%M:%S %Z %Y")
            result = requests.get(
                'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=' + stock_symbol + '&apikey'
                                                                                                   '=VMX0ZIDD6F24V7R3')
            # grab data
            data = result.json()
            symbol = data['Global Quote']['01. symbol']
            price = data['Global Quote']['05. price']
            change = float(data['Global Quote']['09. change'])
            change_per = data['Global Quote']['10. change percent']

            stock_name = requests.get(
                'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=' + stock_symbol + '&apikey'
                                                                                                      '=VMX0ZIDD6F'
                                                                                                      '24V7R3')
            name = stock_name.json()['bestMatches'][0]['2. name']
            temp_data = {
                'symbol': symbol,
                'price': price,
                'change': change,
                'change_per': change_per,
                'stock_name': stock_name,
                'name': name,
                'time': now
            }
            return render_template('stockResult.html', temp_data=temp_data)
        except:
            try:
                requests.get('http://www.google.com')
                return render_template('stockResult.html', error={'error': 'Invalid Symbol, Please try again'})
            except:
                return render_template('stockResult.html', error={'error': 'Network connection lost. Please try again '
                                                                           'later'})
    return render_template('stockInfo.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)