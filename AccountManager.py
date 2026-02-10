class AccountManager:
    accountNumber = -1
    accountStatus = False
    accountType = "None"
    accountPlan = "None"

    def changePlan(self, newPlan):
        self.accountPlan = newPlan
    def changeStatus(self, newStatus):
        self.accountStatus = newStatus
    def deleteAccount(self):
        self.accountNumber = -1
        self.accountStatus = False
        self.accountType = "None"
        self.accountPlan = "None"
    def createAccount(self, accountNumber, accountType, accountPlan):
        self.accountNumber = accountNumber
        self.accountStatus = True
        self.accountType = accountType
        self.accountPlan = accountPlan