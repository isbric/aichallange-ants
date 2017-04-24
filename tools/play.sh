#!/usr/bin/env sh
./playgame.py --player_seed 42 --end_wait=0.25 --verbose -E --log_dir game_logs --turns 100 --map_file maps/example/tutorial1.map "$@" "python3 ../mybot/bot.py" "python sample_bots/python/HunterBot.py"
