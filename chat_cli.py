import asyncio
from colorama import Fore, Style
import pyfiglet
from agent import chat


# --- Fancy header with ASCII art ---
def show_header():
    ascii_art = pyfiglet.figlet_format("HSC Bangla Bot")
    print(Fore.CYAN + ascii_art)
    print(
        Fore.YELLOW + "আপনার যেকোনো প্রশ্ন লিখুন। বাংলা প্রথম পত্রের যেকোনো সাহায্য পেতে পারেন!\n"
    )


# --- Chat loop ---
async def run_chat():
    show_header()
    print(Fore.GREEN + "➡️ টাইপ করুন 'exit' বের হওয়ার জন্য\n")

    history = []

    while True:
        user_input = input(Fore.LIGHTWHITE_EX + Style.BRIGHT + "🧑 আপনি: ")
        if user_input.lower().strip() in ["exit", "quit"]:
            print(Fore.MAGENTA + "🙏 ধন্যবাদ! আবার দেখা হবে।")
            break

        history.append({"role": "user", "content": user_input})

        try:
            response = await chat(history)
            history.append({"role": "assistant", "content": response})
            print(
                Fore.LIGHTBLUE_EX + Style.BRIGHT + "🤖 HSC Bot:",
                Fore.WHITE + response + "\n",
            )

        except Exception as e:
            print(Fore.RED + f"❌ কোনো সমস্যা হয়েছে: {e}")


# Entry point
if __name__ == "__main__":
    asyncio.run(run_chat())
