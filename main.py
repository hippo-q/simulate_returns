import csv
import datetime
import matplotlib.pyplot as plt


AVERAGE_DAYS = 50
AVERAGE_DAYS_SHORT = 20


# if current price > moving average price and then cross, long;
def calculate_average_price(prices: list, days: int):
    ma = []
    for i in range(days, len(prices)):
        ma.append((prices[i][0], sum([p[1] for p in prices[i-days:i]]) / days))
    return ma


def simulate(prices, ma_short, ma_long):
    rets = []
    total_return = 0
    total_return_rate = 1

    ma_short_ = ma_short[AVERAGE_DAYS:]
    ma_long_ = ma_long[AVERAGE_DAYS:]

    prices_ = prices[AVERAGE_DAYS:]
    state = "long" if ma_short_[0][1] > ma_long_[0][1] else "short"
    buy_price = prices_[0][1] if state == "long" else 0
    sell_price = prices_[0][1] if state == "short" else 0

    for i in range(len(ma_long_)):
        if state == "long" and ma_short_[i][1] <= ma_long_[i][1]:
            sell_price = prices_[i][1]
            rets.append(sell_price/buy_price)
            total_return_rate *= sell_price/buy_price
            total_return += 2 * prices_[i][1]
            state = "short"
        elif state == "short" and ma_short_[i][1] >= ma_long_[i][1]:
            buy_price = prices_[i][1]
            total_return_rate *= sell_price/buy_price
            rets.append(sell_price/buy_price)
            total_return -= 2 * prices_[i][1]
            state = "long"

    print(f"Total return {total_return}")
    print(f"Total return rate {total_return_rate}")
    return rets


if __name__ == '__main__':
    price_list = []
    with open("USD_JPY Historical Data.csv", "r", encoding='utf-8-sig') as data_csv:
        reader = csv.reader(data_csv, delimiter=',', quotechar='"')
        for line in reader:
            date_ = int(datetime.datetime.strptime(line[0], "%d/%m/%Y").timestamp())
            price_list.append((date_, float(line[1])))
        price_list.sort(key=lambda x: x[0])

    avg_prices = calculate_average_price(price_list, AVERAGE_DAYS)
    avg_prices_short = calculate_average_price(price_list, AVERAGE_DAYS_SHORT)

    rets = simulate(price_list, avg_prices_short, avg_prices)

    fig = plt.figure()
    plt.grid(True)
    plt.plot([datetime.datetime.fromtimestamp(p[0]).date() for p in price_list], [p[1] for p in price_list], label = "price")
    plt.plot([datetime.datetime.fromtimestamp(p[0]).date() for p in avg_prices], [p[1] for p in avg_prices], label = "average")
    plt.plot([datetime.datetime.fromtimestamp(p[0]).date() for p in avg_prices_short], [p[1] for p in avg_prices_short],
             label="average_short")

    plt.legend()
    plt.show()







