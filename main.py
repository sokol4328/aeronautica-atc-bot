from bot import AeroATCBot

def main():
    bot = AeroATCBot()
    file = open("token.txt", "r")
    token = file.read()
    bot.run(token)

if __name__ == "__main__":
    main()