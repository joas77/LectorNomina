class Payment:
    """
    Payment class
    """

    def __init__(self,date, perceptions:dict=None, deductions:dict=None):
        self._date = date
        self.perceptions = perceptions
        self.deductions = deductions

    def __str__(self):
        ret = f"""
        Date:   {self.date}
        Total Perceptions:  ${self.total_perceptions():,.2f}
        Total Deductions:   ${self.total_deductions():,.2f}
        ------------------------
        Total:  ${self.total():,.2f}"""
        # format(self.date, 
        #             self.total_perceptions(),
        #             self.total_deductions(),
        #             self.total())
        
        return ret

    def total(self):
        return self.total_perceptions() - self.total_deductions()

    def total_perceptions(self):
        return sum(self.perceptions.values())

    def total_deductions(self):
        return sum(self.deductions.values())

    @property
    def date(self):
        return self._date