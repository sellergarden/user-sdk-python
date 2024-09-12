import argparse
import importlib
import time
from datetime import datetime

import schedule
from croniter import croniter

from sellergarden_sdk.decorators import registered_functions


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the main program in simulation mode."
    )
    parser.add_argument(
        "module", type=str, help="The module to import and run", default="sample_app"
    )
    return parser.parse_args()


def schedule_task(cron_expression, func):
    def job():
        func()
        next_run = croniter(cron_expression, datetime.now()).get_next(datetime)
        schedule.every().day.at(next_run.strftime("%H:%M")).do(job)

    next_run = croniter(cron_expression, datetime.now()).get_next(datetime)
    schedule.every().day.at(next_run.strftime("%H:%M")).do(job)


def main():
    args = parse_args()
    module_name = args.module
    my_app = importlib.import_module(module_name)

    # Schedule tasks
    for schedule_info in registered_functions["schedules"]:
        func_name = schedule_info["name"].__name__
        cron_expression = schedule_info["cron_expression"]

        if hasattr(my_app, func_name):
            func = getattr(my_app, func_name)
            schedule_task(cron_expression, func)

    # Run scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
