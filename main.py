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

def add_spaces(data, columns):
    spaces_needed = columns-len(data)
    for column in range(spaces_needed):
        data += ' '
    return data

try:
    while True:
        cpu_percents = psutil.cpu_percent(percpu=True)
        uptime = get_uptime()
        load_average = psutil.getloadavg()
        rows_for_cpu_percents = curses.LINES-9
        columns = curses.COLS
        amount_of_cores = len(cpu_percents)
        space_between_bars = round(rows_for_cpu_percents/amount_of_cores)
        stdscr.addstr(1, 1, 'CPU Usage:')
        y = 3
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
        stdscr.addstr(y, 1, 'Memory Usage:')
        y += 2
        stdscr.addstr(y, 0, ' [')
        usage = psutil.virtual_memory()[2]
        usage_gb = round(psutil.virtual_memory()[3]/1000000000, 1)
        if usage >= 50 and usage < 75:
            stdscr.addstr(y, 2, get_percentage_bar(usage, columns), curses.color_pair(2))
        elif usage >= 75:
            stdscr.addstr(y, 2, get_percentage_bar(usage, columns), curses.color_pair(3))
        else:
            stdscr.addstr(y, 2, get_percentage_bar(usage, columns), curses.color_pair(1))
        columns_pos = columns
        columns_pos -= 7
        columns_pos -= len(str(usage))
        columns_pos -= len(str(usage_gb))
        stdscr.addstr(y, columns_pos, '] {}% {}GB '.format(usage, usage_gb))
        y += 2
        stdscr.addstr(y, 1, add_spaces('Load Average: {} {} {}'.format(round(load_average[0], 2), round(load_average[1], 2), round(load_average[2], 2)), columns))
        y += 1
        stdscr.addstr(y, 1, add_spaces('System Uptime: {}'.format(humanize.precisedelta(dt.timedelta(seconds=uptime))), columns))
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
