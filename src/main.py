import argparse
import datetime
import json
import os
import praw
import time

from helpers import get_text, log
from db_operations import DB


parser = argparse.ArgumentParser(description='Backup Reddit Account')

parser.add_argument('--export', '-e', action="store_true",
                    help="Export Subreddits to a .json file")

parser.add_argument('--restore', '-r', action="store_true",
                    help="Restore subreddits from .json file")

parser.add_argument('--one', '-o', action="store_true",
                    help="Export and Import to new account with one run")


class Actions:

    def __init__(self, account, rollback=None):
        try:
            log('Asking permissions for your account(s)...')
            self.reddit = praw.Reddit(account)
            self.username = str(self.reddit.user.me())
            log('Permissions granted.\n')
            self.rollback = rollback
            if self.rollback:
                self.db = DB()
        except Exception as e:
            log(e, 'error')
            quit('\n\n[e] HINT:Did you create your own praw.ini file?')

    def get_subs(self):
        log('Getting subreddits from Reddit...')
        user_subs = self.reddit.user.subreddits(limit=None)

        return [sub.display_name for sub in user_subs]

    def export_subs(self, filename=None):
        subs = self.get_subs()

        log(f'Found total {len(subs)} subreddits, saving to a file...')
        if not filename:
            t = time.time()
            stamp = datetime.datetime.fromtimestamp(t).strftime('%Y%m%d_%H%M')
            filename = f'{self.username}_{stamp}.json'

        file = open(filename, 'w')
        subs = sorted(subs, key=str.lower)
        json.dump(subs, file, indent=4)
        file.close()
        log(f'Saved to: {filename}')

    def read_file(self, path):
        file = open(path, 'r')
        subs = json.load(file)
        file.close()
        return list(set(subs))

    def search_files(self):
        log('Searching available files...\n')
        struct = {}  # Extracted tree {'path':'filename'}
        found_files = []  # All files in dirs ['file1', 'file2', 'file_n']
        filtered_struct = []

        for root, dirs, files in os.walk(os.getcwd()):
            for file in files:
                struct[root] = file
                found_files.append(file)
                # If a useful file found, keep the path and the name
                if file.split('.')[-1] == 'json':
                    filtered_struct.append([root, file])

        for idx, this_file in enumerate(filtered_struct):
            print(f'[{idx}] {"/".join(this_file)}')

        if len(filtered_struct) > 0:
            while True:
                try:
                    selection = int(input('[In] Select available file from [0-{0}]:'.format(len(filtered_struct) - 1)))  # noqa
                    if selection > len(filtered_struct) - 1 or selection < 0:
                        log('Please select in range.', 'error')
                        continue
                    else:
                        break
                except ValueError:
                    log('Select a number.', 'error')
                    continue
            return '/'.join(filtered_struct[selection])
        else:
            return False

    def subscribe(self, sub, action):
        # With action True or False
        # Select subscribe or leave a subreddit
        try:
            if action:
                self.reddit.subreddit(sub).subscribe()
                log(f'Successfully joined {sub}')
            else:
                self.reddit.subreddit(sub).unsubscribe()
                log(f'Leaved {sub}')
        except Exception as e:
            log(e, 'error')

    def user_activity(self, submission=None, comments=None, count=None):
        data = []
        if submission:
            for s in self.reddit.redditor(self.username).submissions.new(limit=None):
                data.append(s)
        elif comments:
            for c in self.reddit.redditor(self.username).comments.new(limit=None):
                data.append(c)
        if count:
            return len(data)
        return data

    def get_submission(self, id):
        return self.reddit.submission(id=id)

    def get_comment(self, id):
        return self.reddit.comment(id=id)

    def confuser(self, submission=None, comments=None, id=None, size=10):
        # TODO: How long to confuse. Example 3 weeks or 1 hour
        if id:
            if submission:
                sub = self.get_submission(id=id)
                self.try_for_rollback(sub, sub=True)
                sub.edit(get_text(size))
                quit(f'[i] Submission with id {id} confused')

            elif comments:
                com = self.get_comment(id=id)
                self.try_for_rollback(com, sub=False)
                com.edit(get_text(size))
                quit(f'[i] Comment with id: {id} confused')

        if submission:
            log('This may take some time.\nLoading data...')
            data = self.user_activity(submission=True)
            log('Confusing submission text but NOT title...')
            for s in data:
                self.try_for_rollback(s, sub=True)
                self.reddit.submission(s).edit(get_text(size))

        elif comments:
            log('This may take some time.\nLoading data...')
            data = self.user_activity(comments=True)
            log('Confusing comments...')
            for c in data:
                self.try_for_rollback(c, sub=False)
                self.reddit.comment(c).edit(get_text(size))
        log(f'Confused {len(data)} items.')

    def delete_activity(self, submission=None, comments=None, id=None):
        if id:
            if submission:
                sub = self.get_submission(id=id)
                sub.delete()
                quit('[i] Submission deleted.')

            elif comments:
                com = self.get_comment(id=id)
                com.delete()
                quit('[i] Comment deleted')
        if submission:
            log('Deleting submissions...')
            data = self.user_activity(submission=True)
            for s in data:
                self.reddit.submission(s).delete()
        elif comments:
            log('Deleting comments...')
            data = self.user_activity(comments=True)
            for c in data:
                self.reddit.comment(c).delete()
        log(f'Removed {len(data)} items.')

    def try_for_rollback(self, obj, sub=False):
        '''
        Save the id and value of the submission to a local DB
        :param obj: Submission or Comment instance
        :param sub: If True submission is passed, if False comment is passed
        '''
        if not self.rollback:
            # Rollback not asked with -rlb ignore
            return

        value = obj.selftext if sub else obj.body
        data = {
            'id': obj.id,
            'value': value,
            'is_comment': int(not sub)
        }
        saved = self.db.insert(data)
        if saved:
            log('Available for rollback')
        else:
            log('Not saved for rollback, probably id already in DB',
                'error')


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
            log('No ".json" files found. Bye!')
            quit('[i] HINT: Use -e argument')

        subs = old.read_file(backup_file)

        print('#' * 50)
        log(f'Try to Subscribe in {len(subs)} subreddits? (Y/N)', 'question')
        ans = input('[Ans]:')
        if ans.lower() == 'y':
            new = Actions('new')
            existing_subs = new.get_subs()
            to_sub = set(subs) - set(existing_subs)

            for sub in list(to_sub):
                new.subscribe(sub, True)
            quit('[i] All done. Bye!')
        else:
            quit('OK, quiting with no worries.')
