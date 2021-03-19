class Broker:
    def __init__(self, name, money, stocks):
        self.name = name
        self.wallet = money
        self.start_wallet = money

        self.stocks = stocks
        self.start_stocks = stocks

    def update_variables(self, day, stock_value):
        self.last_stock_value = stock_value
        money = self.wallet + self.stocks * stock_value

    def buy_all(self, stock_value, day):
        while(self.wallet > stock_value):
            self.stocks += 1
            self.wallet -= stock_value
            self.wallet = round(self.wallet, 2)
        self.update_variables(day, stock_value)

    def buy_half(self, stock_value, day):
        for i in range(int(self.stocks / 2)):
            self.stocks += 1
            self.wallet -= stock_value
            self.wallet = round(self.wallet, 2)
        self.update_variables(day, stock_value)

    def sell_all(self, stock_value, day):
        while (self.stocks > 0):
            self.stocks -= 1
            self.wallet += stock_value
            self.wallet = round(self.wallet, 2)
        self.update_variables(day, stock_value)

    def sell_half(self, stock_value, day):
        for i in range(int(self.stocks / 2)):
            self.stocks -= 1
            self.wallet += stock_value
            self.wallet = round(self.wallet, 2)
        self.update_variables(day, stock_value)

    def status(self):
        sold_all_wallet = self.wallet
        stocks = self.stocks
        while (stocks > 0):
            stocks -= 1
            sold_all_wallet += self.last_stock_value
            sold_all_wallet = round(sold_all_wallet, 2)

        print()
        print('{0}:'.format(self.name))
        print(' Start    > Money = {0:.2f}, Stocks = {1}'.format(self.start_wallet, self.start_stocks))
        print(' Current  > Money = {0:.2f}, Stocks = {1}'.format(self.wallet, self.stocks))
        print(' Sold all > Money = {0:.2f}, Stocks = 0'.format(sold_all_wallet))
        print()
        print('Profit: {:.2f}'.format(sold_all_wallet - self.start_wallet))
        print('Effectiveness: {:.2f}%'.format((sold_all_wallet / self.start_wallet - 1) * 100))
        print()