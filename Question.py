class Question:
    def askBool(self, question):
        while True:
            rawAnswer = input(question + " [Y/N]: ").lower()
            if(rawAnswer == "y" or rawAnswer == "yes"):
                return True
            elif (rawAnswer == "n" or rawAnswer == "no"):
                return False
            else:
                print("You must provide [Y/N] answer!")
    def askInt(self, question, limit=None):
        while True:
            rawAnswer = input(question + ": ")
            try:
                if (limit == None):
                    return int(rawAnswer)
                elif (int(rawAnswer) < limit and int(rawAnswer) >= 0):
                    return int(rawAnswer)
                else:
                    print("Invalid answer!")
            except:
                print("You must provide a valid integer!")