import matplotlib 
# necessary on mac, see https://stackoverflow.com/questions/57943180/matplotlib-crashes-in-plt-show-on-macos-with-tkagg-backend
matplotlib.use('Qt5Agg') 
from matplotlib import pyplot as plt
from datetime import datetime

class PayrollPlotter:
    def __init__(self, payments: list):
        self._payments = payments
        self._payments.sort(key= lambda x: x.date)

    def plot(self):
        """
        Deafult plot, payment vs time
        """
        y = [payment.total() for payment in self._payments]
        dates = [datetime.strptime(payment.date, "%Y-%m-%dT%H:%M:%S") for payment in self._payments]

        fig, ax = plt.subplots()
        ax.plot(dates, y, "o")
        ax.set(xlabel="fechas", ylabel="sueldo($)",
            title="Pagos")
        
        ax.grid()
        plt.show()