import util.chaninfo
def main(bot, cmdtext):
	print(util.chaninfo.get_users(bot.current_server(),bot.current_target()))
	print(bot.current_target())