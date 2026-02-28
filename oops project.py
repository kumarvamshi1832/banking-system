import sqlite3 as sql

class Bank:

    def __init__(self):
        self.con = sql.connect("banks")
        self.cur = self.con.cursor()

    def menu(self):
       #print("\n1)Create Account")
         #print("2)Deposit Amount")
        #print("3)Withdraw Amount")
        #print("4)Transfer")
       # print("5)Balance Enquiry")
        #print("6)Transaction history")
       # print("7)Delete Account Details")
       # print("8)Exit")
       menu = ["1)Create Account", "2)Deposit Amount", "3)Withdraw Amount", "4)Transfer", "5)Balance Enquiry",
               "6)Transaction history", "7)Delete Account Details", "8)exit"]
       for i in menu:
           print(i)

    # ---------------- CREATE ACCOUNT ----------------
    def create_account(self):
        print("\nCreate Account")
        q1 = "insert into cus values(?,?,?,?,?)"

        cid = int(input("Enter customer id: "))
        cacc = int(input("Enter customer account: "))
        cname = input("Enter customer name: ")
        pwd = input("Enter customer password: ")
        amount = int(input("Enter amount: "))

        length = len(pwd)

        if 8 <= length <= 14:
            l = u = d = s = 0
            for i in pwd:
                if i.islower():
                    l += 1
                elif i.isupper():
                    u += 1
                elif i.isdigit():
                    d += 1
                else:
                    s += 1

            if l >= 1 and u >= 1 and d >= 1 and s >= 1:
                self.cur.execute(q1, (cid, cacc, cname, pwd, amount))

                t = "insert into transactions(cacc, ttype, amount) values(?,?,?)"
                self.cur.execute(t, (cacc, "deposit", amount))

                self.con.commit()
                print("Account Created Successfully")
            else:
                print("Password must contain uppercase, lowercase, digit & special character")
        else:
            print("Password must be between 8 and 14 characters")

    # ---------------- DEPOSIT ----------------
    def deposit(self):
        print("\nDeposit Amount")
        cacc = int(input("Enter account: "))
        pwd = input("Enter password: ")

        q = "select * from cus where cacc=? and password=?"
        self.cur.execute(q, (cacc, pwd))
        data = self.cur.fetchone()

        if data:
            amount = int(input("Enter amount: "))
            self.cur.execute("update cus set amount=amount + ? where cacc=?", (amount, cacc))

            t = "insert into transactions(cacc, ttype, amount) values(?,?,?)"
            self.cur.execute(t, (cacc, "deposit", amount))

            self.con.commit()
            print("Amount Deposited Successfully")
        else:
            print("Invalid account or password")

    # ---------------- WITHDRAW ----------------
    def withdraw(self):
        print("\nWithdraw Amount")
        cacc = int(input("Enter account: "))
        pwd = input("Enter password: ")

        q = "select * from cus where cacc=? and password=?"
        self.cur.execute(q, (cacc, pwd))
        data = self.cur.fetchone()

        if data:
            balance = data[4]
            amount = int(input("Enter amount: "))

            if amount <= balance:
                self.cur.execute("update cus set amount=amount - ? where cacc=?", (amount, cacc))

                t = "insert into transactions(cacc, ttype, amount) values(?,?,?)"
                self.cur.execute(t, (cacc, "withdraw", amount))

                self.con.commit()
                print("Amount Withdrawn Successfully")
            else:
                print("Insufficient Funds")
        else:
            print("Invalid account or password")

    # ---------------- TRANSFER ----------------
    def transfer(self):
        print("\nTransfer Amount")
        cacc = int(input("Enter sender account: "))
        pwd = input("Enter sender password: ")

        q = "select * from cus where cacc=? and password=?"
        self.cur.execute(q, (cacc, pwd))
        sender = self.cur.fetchone()

        if sender:
            balance = sender[4]
            amount = int(input("Enter amount: "))

            if amount <= balance:
                acc = int(input("Enter receiver account: "))

                if cacc != acc:
                    self.cur.execute("select * from cus where cacc=?", (acc,))
                    receiver = self.cur.fetchone()

                    if receiver:
                        # Deduct from sender
                        self.cur.execute("update cus set amount=amount - ? where cacc=?", (amount, cacc))
                        # Add to receiver
                        self.cur.execute("update cus set amount=amount + ? where cacc=?", (amount, acc))

                        t = "insert into transactions(cacc, ttype, amount) values(?,?,?)"
                        self.cur.execute(t, (cacc, "transfer", amount))
                        self.cur.execute(t, (acc, "received", amount))

                        self.con.commit()
                        print("Transaction Completed Successfully")
                    else:
                        print("Receiver account not found")
                else:
                    print("Sender and receiver cannot be same")
            else:
                print("Insufficient Funds")
        else:
            print("Invalid account or password")

    # ---------------- BALANCE ----------------
    def balance(self):
        print("\nBalance Enquiry")
        cacc = int(input("Enter account: "))
        pwd = input("Enter password: ")

        q = "select * from cus where cacc=? and password=?"
        self.cur.execute(q, (cacc, pwd))
        data = self.cur.fetchone()

        if data:
            print("Your Current Balance is:", data[4])
        else:
            print("Invalid account or password")

    # ---------------- HISTORY ----------------
    def history(self):
        print("\nTransaction History")
        cacc = int(input("Enter account: "))

        self.cur.execute("select * from transactions where cacc=?", (cacc,))
        data = self.cur.fetchall()

        if data:
            for row in data:
                print(f"Type: {row[2]} | Amount: {row[3]}")
        else:
            print("No transactions found")

    # ---------------- DELETE ----------------
    def delete(self):
        print("\nDelete Account")
        cacc = int(input("Enter account: "))
        pwd = input("Enter password: ")

        self.cur.execute("delete from cus where cacc=? and password=?", (cacc, pwd))
        self.con.commit()
        print("Account Deleted Successfully")

    def close(self):
        self.con.close()


# ---------------- MAIN PROGRAM ----------------

b = Bank()
ch = "y"

while ch.lower() == "y":
    b.menu()
    choice = int(input("Enter your choice: "))

    if choice == 1:
        b.create_account()
    elif choice == 2:
        b.deposit()
    elif choice == 3:
        b.withdraw()
    elif choice == 4:
        b.transfer()
    elif choice == 5:
        b.balance()
    elif choice == 6:
        b.history()
    elif choice == 7:
        b.delete()
    elif choice == 8:
        break
    else:
        print("Invalid Choice")

    ch = input("Do you want to continue? (y/n): ")

b.close()