import itertools, math
import settings

def main(bot, cmdtext):
	args = cmdtext.split(' ')
	if len(args) < 3:
		bot.reply_safe('Not enough arguments.')
		return
	try:
		x_min, x_max = [float(x) for x in args[1:3]]
		if x_min == x_max:
			bot.reply_safe('Your domain needs to have positive measure.')
			return
		expr = args[0].replace('.','').replace('[','').replace(']','').replace('pi',str(settings.const_pi)).replace('e',str(settings.const_e))
		n = settings.integral_steps
		if len(args) > 3:
			n = int(args[3])
		width = (x_max-x_min)*1.0/n
		area = sum([eval(expr)*width for x in itertools.islice(itertools.count(x_min,width),(x_max-x_min)/width)])

		bot.reply_safe('With '+str(n)+' rectangles, the area = '+str(area)+'.')
	except Exception, e:
		bot.reply_safe('You did something wrong.')
		print(e)