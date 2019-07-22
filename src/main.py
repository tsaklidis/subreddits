import argparse
import datetime
import json
import os
import praw
import time


parser = argparse.ArgumentParser(description='Backup Reddit Account')

parser.add_argument('--export', '-e', action="store_true",
                    help="Export Subreddits to a .json file")

parser.add_argument('--restore', '-r', action="store_true",
                    help="Restore subreddits from .json file")

parser.add_argument('--one', '-o', action="store_true",
                    help="Export and Import to new account with one run")


class Actions:

    def __init__(self, account):
        try:
            print('[i] Asking permissions for ' + account + ' account...')
            self.reddit = praw.Reddit(account)
            self.username = str(self.reddit.user.me())
            print('[i] Permissions granted.\n')
        except Exception as e:
            print(e)
            quit('\n\n[e] HINT:Did you create your own praw.ini file?')

    def get_subs(self):
        subs = []
        print('[i] Getting subreddits from Reddit...')
        user_subs = self.reddit.user.subreddits(limit=None)

        for sub in user_subs:
            subs.append(sub.display_name)
        return subs

    def export_subs(self, filename=None):
        subs = self.get_subs()

        print('[i] Saving your subreddits to a file...')
        if not filename:
            t = time.time()
            stamp = datetime.datetime.fromtimestamp(
                t).strftime('%Y%m%d_%H%M')

            filename = '{0}_{1}.json'.format(self.username, stamp)

        file = open(filename, 'w')
        subs = sorted(subs, key=str.lower)
        json.dump(subs, file, indent=4)
        file.close()
        print('[i] Saved to: ' + filename)

    def read_file(self, path):
        file = open(path, 'r')
        subs = json.load(file)
        file.close()
        return list(set(subs))

    def search_files(self):
        print('[i] Searching available files...\n')
        struct = {}  # Extracted tree {'path':'filename'}
        found_files = []  # All files in dirs ['file1', 'file2', 'file_n']
        filterd_struct = []

        for root, dirs, files in os.walk(os.getcwd()):
            for file in files:
                struct[root] = file
                found_files.append(file)
                # If a useful file found, keep the path and the name
                if file.split('.')[-1] == 'json':
                    filterd_struct.append([root, file])

        for idx, this_file in enumerate(filterd_struct):
            print('[{0}] {1}'.format(idx, "/".join(this_file)))

        if len(filterd_struct) > 0:
            while True:
                try:
                    selection = int(input('[In] Select available file from [0-{0}]:'.format(len(filterd_struct) - 1)))  # noqa
                    if selection > len(filterd_struct) - 1 or selection < 0:
                        print('[e] Please select in range.')
                        continue
                    else:
                        break
                except ValueError:
                    print('[e] Select a nubmer.')
                    continue
            return '/'.join(filterd_struct[selection])
        else:
            return False

    def subscribe(self, sub, action):
        # With action True or False
        # Select subscribe or leave a subreddit
        try:
            if action:
                self.reddit.subreddit(sub).subscribe()
                print('[i] Successfully joined ' + sub)
            else:
                self.reddit.subreddit(sub).unsubscribe()
                print('[i] Leaved ' + sub)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    args = parser.parse_args()

    export_subs = getattr(args, 'export')
    restore = getattr(args, 'restore')
    one = getattr(args, 'one')

    if export_subs or restore or one:
        old = Actions('old')
    else:
        quit('[i] Use an argument for Export or Import.')

    if one:
        export_subs = restore = True

    if export_subs:
        old.export_subs()

    if restore:
        backup_file = old.search_files()
        if not backup_file:
            print('[i] No ".json" files found. Bye!')
            quit('[i] HINT: Use -e argument')

        subs = old.read_file(backup_file)

        print('#' * 50)
        print(
            '[Q]: Try to Subscribe in {0} subreddits? (Y/N)'.format(len(subs)))
        ans = input('[Ans]:')
        if ans == 'Y' or ans == 'y':
            new = Actions('new')
            existing_subs = new.get_subs()
            to_sub = set(subs) - set(existing_subs)

            for sub in list(to_sub):
                new.subscribe(sub, True)
            quit('[i] All done. Bye!')
        else:
            quit('OK, quiting with no worries.')
