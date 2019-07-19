import argparse
import datetime
import json
import os
import praw
import time


parser = argparse.ArgumentParser(description='Reddit actions')

parser.add_argument('--export', '-e', action="store_true",
                    help="Export Subreddits")

parser.add_argument('--subscribe', '-s', action="store_true",
                    help="Subscribe to saved Subreddits")

parser.add_argument('--load', '-l', action="store_true",
                    help="File to load subreddits")


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
        print('[i] Getting subs from Reddit...')
        for sub in self.reddit.user.subreddits():
            subs.append(sub.display_name)
        return subs

    def export_subs(self, filename=None):
        print('[i] Saving your subreddits...')
        subs = self.get_subs()

        if not filename:
            t = time.time()
            stamp = datetime.datetime.fromtimestamp(
                t).strftime('%Y%m%d_%H:%M')

            filename = '{0}_{1}.json'.format(self.username, stamp)

        file = open(filename, 'w')
        subs = sorted(self.get_subs(), key=str.lower)
        json.dump(subs, file, indent=4)
        file.close()
        print('[i] Subreddits saved to: ' + filename)

    def read_file(self, path):
        file = open(path, 'r')
        subs = json.load(file)
        file.close()
        return list(set(subs))

    def search_files(self):
        print('[i] Searching available files...\n')
        # Search in extracted folders
        struct = {}  # Extracted tree {'path':'filename'}
        found_files = []  # All files in dirs ['file1', 'file2', 'file_n']

        # Only needed files with their path
        # [['path', 'file'], ['same_path', 'other_file']]
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

    def subscribe(self, sub):
        try:
            self.reddit.subreddit(sub).subscribe()
            print('[i] Successfully joined ' + sub)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    args = parser.parse_args()

    export_subs = getattr(args, 'export')
    subscribe = getattr(args, 'subscribe')
    load = getattr(args, 'load')

    old = Actions('old')

    if export_subs:
        old.export_subs()

    if load:
        backup_file = old.search_files()
        if not backup_file:
            quit('[i] No ".json" files found. Bye!')

        subs = old.read_file(backup_file)

        print('#######################################')
        print('[Q]: Subscribe to {0} subreddits? (Y/N)'.format(len(subs)))
        ans = input('[Ans]:')
        if ans == 'Y':
            new = Actions('new')
            existing_subs = new.get_subs()
            for sub in subs:
                if sub in existing_subs:
                    print('[i] You have already joined ' + sub + ' skiping...')
                else:
                    new.subscribe(sub)

            quit('[i] All done. Bye!')
        else:
            quit('OK, quiting with no worries.')