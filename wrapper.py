#!/usr/bin/env python


import os
import sys
import subprocess


def line_handler(line):
    #line:running for 100 turns
    #line:                  ant_count c_turns climb? cutoff food r_turn ranking_bots s_alive s_hills score  w_turn winning
    #line:turn    0 stats:   [1,1,0]     0    [0,0]    -     12    0        None      [0,1]   [1,1]  [0,1]   0     None
    #line:score 0 3
    #line:status crashed survived
    #line:playerturns 0 0
    #line:waiting 0.25 seconds for bots to process end turn
    if line.strip().startswith('running'):
        return ('game', 'running', line.strip())
    if line.strip().startswith('ant'):
        return ('game', 'description', line.strip())
    elif line.strip().startswith('turn'):
        return ('game', 'turn', line.strip())
    elif line.strip().startswith('score'):
        return ('game', 'score', line.strip())
    elif line.strip().startswith('status'):
        return ('game', 'status', line.strip())
    elif line.strip().startswith('playerturns'):
        return ('game', 'playerturns', line.strip())
    elif line.strip().startswith('waiting'):
        return ('game', 'waiting', line.strip())
    elif line.strip().startswith('bot='):
        return ('bot',
                '{}'.format(line[len('bot='):].split(':', 1)[0] if len(line.split(':', 1)) == 2 else 'noname'),
                line.split(':', 1)[1].strip())

    else:
        return ('unknown', '', line.rstrip('\n'))


def main():
    FNULL = open('/dev/null', 'w')
    p = subprocess.Popen(
            ['./playgame.py',
            '--player_seed=42',
            '--end_wait=0.25',
            '--verbose',
            '-e',
            '--log_dir=game_logs',
            '--turns=100',
            '--map_file=maps/example/tutorial1.map',
            'python3 ../mybot/bot.py',
            'python sample_bots/python/HunterBot.py',
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd='./tools/',
            bufsize=1)

    while p.poll() is None:
        for line in iter(p.stdout.readline, b''):
            logger, name, msg = line_handler(line)
            if logger == 'game':
                print('{logger}: {msg}'.format(logger=logger, msg=line.strip()))
            else:
                print('unknown: {msg}'.format(msg=line.strip()))

    try:
        p.wait()
    except OSError:
        # can't kill a dead proc
        pass

    for line in iter(p.stdout.readline, b''):
        logger, name, msg = line_handler(line)
        if logger == 'game':
            print('{logger}: {msg}'.format(logger=logger, msg=line.strip()))
        else:
            print('unknown: {msg}'.format(msg=line.strip()))

    print('')
    for line in iter(p.stderr.readline, b''):
        logger, name, msg = line_handler(line)
        if logger == 'game':
            print('{logger}: {msg}'.format(logger=logger, msg=line.strip()))
        elif logger == 'bot':
            print('{logger}: {bot} >> {msg}'.format(logger=logger, bot=name, msg=msg))
        else:
            print('unknown: {msg}'.format(msg=msg))


    if p.stdin:
        p.stdin.close()
    if p.stdout:
        p.stdout.close()
    if p.stderr:
        p.stderr.close()


if __name__ == '__main__':
    main()

