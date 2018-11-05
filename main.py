import Processor
import datetime


def main():
    last_run = datetime.datetime.today() - datetime.timedelta(days=365)
    proc = Processor.Processor()
    proc.process_since_last(last_run=last_run, channel="6977")


if __name__ == "__main__":
    main()
