from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

# Start the scheduler
sched = BlockingScheduler()


# Define the function that is to be executed
def my_job(text):
    print('text')

# The job will be executed on November 6th, 2009


# Store the job in a variable in case we want to cancel it
def run():
    args_date = ['2021', '7', '18', '21', '59']
    sched.add_job(my_job, 'date',
                  run_date=datetime(int(args_date[0]), int(args_date[1]), int(args_date[2]), int(args_date[3]),
                                    int(args_date[4]), 0), args=['text'])
    sched.start()

    print("aaa")

