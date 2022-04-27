# ts4_viz
### how to run
```bash
pip install git+https://github.com/DarkSquirrelComes/ts4_viz.git
python3 -m ts4_viz ./path_to_ts4_log.json
```
Script re-generates .gv file after each command.

Type `?` inside the CLI for help

Json log generator is no supported in ts4 for now, you can install ts4 from my fork (https://github.com/DarkSquirrelComes/TestSuite4/tree/ts4-0.5.0-alpha) or wait for PR's merge.

Just call `ts4.dump_json_data()` after ts4 scenario to generate log.
