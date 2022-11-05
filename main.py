import curses
import datetime as dt
import humanize
import psutil

stdscr = curses.initscr()

curses.noecho()

curses.curs_set(False)

curses.start_color()

curses.use_default_colors()

curses.init_pair(1, curses.COLOR_GREEN, -1)

curses.init_pair(2, curses.COLOR_YELLOW, -1)

curses.init_pair(3, curses.COLOR_RED, -1)

stdscr.nodelay(1)

stdscr.keypad(1)

def get_percentage_bar(percent, columns):
    percent_length = len(str(percent))
    bar = ''
    columns_for_bar = columns
    columns_for_bar -= 6
    columns_for_bar -= percent_length
    y = round((percent/100)*columns_for_bar)
    for x in range(columns_for_bar):
        if not y == 0:
            bar += '|'
            y -= 1
        else:
            bar += ' '
    return bar

def get_uptime():
    f = open('/proc/uptime', 'r')
    uptime = round(float(f.read().split(' ')[0]))
    f.close()
    return uptime

try:
    while True:
        cpu_percents = psutil.cpu_percent(percpu=True)
        uptime = get_uptime()
        load_average = psutil.getloadavg()
        rows_for_cpu_percents = curses.LINES-9
        columns = curses.COLS
        amount_of_cores = len(cpu_percents)
        space_between_bars = round(rows_for_cpu_percents/amount_of_cores)
        y = 1
        for core in cpu_percents:
            stdscr.addstr(y, 0, ' [')
            if core >= 50 and core < 75:
                stdscr.addstr(y, 2, get_percentage_bar(core, columns), curses.color_pair(2))
            elif core >= 75:
                stdscr.addstr(y, 2, get_percentage_bar(core, columns), curses.color_pair(3))
            else:
                stdscr.addstr(y, 2, get_percentage_bar(core, columns), curses.color_pair(1))
            columns_pos = columns
            columns_pos -= 4
            columns_pos -= len(str(core))
            stdscr.addstr(y, columns_pos, '] {}% '.format(core))
            
            y += space_between_bars
        stdscr.addstr(y, 1, 'Load Average: {} {} {}'.format(load_average[0], load_average[1], load_average[2]))
        y += 1
        stdscr.addstr(y, 1, 'System Uptime: {}'.format(humanize.precisedelta(dt.timedelta(seconds=uptime))))
        stdscr.refresh()
        stdscr.getch()
        stdscr.timeout(1000)
except Exception as e:
    exception = e

curses.nocbreak()
curses.echo()
curses.curs_set(True)
curses.endwin()

if not exception == False:
    raise exception
