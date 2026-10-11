import asyncio
import argparse

from main import Actions
from helpers import log, confirm, choose

parser = argparse.ArgumentParser(description='Clean Reddit Account')

parser.add_argument('--confuse', '-c', action="store_true",
                    help="Confuse all comments or submissions")

parser.add_argument('--delete', '-d', action="store_true",
                    help="Delete comments or submissions")

parser.add_argument('--activate_rollback', '-rlb', action="store_true",
                    help="Save originals to a local DB for rollback")


async def run_confuse(account):
    scope = choose('All data or a single item?',
                   {'A': 'all', 'S': 'single'})

    if scope == 'all':
        what = choose('What do you want to confuse?',
                      {'C': 'comments', 'S': 'submissions', 'B': 'both'})

        if what == 'comments':
            count = await account.user_activity(comments=True, count=True)
            log(f'Found {count} comments for u/{account.username}')
            if count == 0:
                log('Nothing to confuse.')
                return
            if not confirm(f'Confuse all {count} comments?'):
                return
            await account.confuser(comments=True)

        elif what == 'submissions':
            count = await account.user_activity(submission=True, count=True)
            log(f'Found {count} submissions for u/{account.username}')
            if count == 0:
                log('Nothing to confuse.')
                return
            if not confirm(f'Confuse all {count} submissions?'):
                return
            await account.confuser(submission=True)

        elif what == 'both':
            c_count = await account.user_activity(comments=True, count=True)
            s_count = await account.user_activity(submission=True, count=True)
            log(f'Found {c_count} comments and {s_count} submissions for u/{account.username}')
            if c_count == 0 and s_count == 0:
                log('Nothing to confuse.')
                return
            if not confirm(f'Confuse all {c_count} comments and {s_count} submissions?'):
                return
            await account.confuser(submission=True, comments=True)
        else:
            quit('Unknown option, quitting.')

    elif scope == 'single':
        what = choose('What type of item?',
                      {'C': 'comment', 'S': 'submission'})

        log('Enter the item id (from the Reddit URL)', 'question')
        item_id = input('    > ').strip()
        if not item_id:
            quit('No id provided, quitting.')

        if what == 'comment':
            await account.confuser(comments=True, id=item_id)
        elif what == 'submission':
            await account.confuser(submission=True, id=item_id)
        else:
            quit('Unknown option, quitting.')


async def run_delete(account):
    what = choose('What do you want to delete?',
                  {'C': 'comments', 'S': 'submissions'})

    if what == 'comments':
        count = await account.user_activity(comments=True, count=True)
        log(f'Found {count} comments for u/{account.username}')
        if count == 0:
            log('Nothing to delete.')
            return
        log('Reddit keeps an archive of deleted content. Consider using confuse (-c) first.', 'warn')
        if not confirm(f'Permanently delete all {count} comments? This cannot be undone'):
            return
        await account.delete_activity(comments=True)

    elif what == 'submissions':
        count = await account.user_activity(submission=True, count=True)
        log(f'Found {count} submissions for u/{account.username}')
        if count == 0:
            log('Nothing to delete.')
            return
        log('Reddit keeps an archive of deleted content. Consider using confuse (-c) first.', 'warn')
        if not confirm(f'Permanently delete all {count} submissions? This cannot be undone'):
            return
        await account.delete_activity(submission=True)
    else:
        quit('Unknown option, quitting.')


async def main():
    args = parser.parse_args()

    confuse = args.confuse
    delete = args.delete
    rlb = args.activate_rollback

    if not confuse and not delete:
        parser.print_help()
        return

    account = Actions('old', rlb if confuse else None)
    await account.init_reddit()

    if rlb and confuse:
        log('Rollback enabled - originals will be saved to local DB')

    if confuse:
        await run_confuse(account)

    if delete:
        await run_delete(account)

    log('All operations completed.')
    await account.close_reddit()


if __name__ == "__main__":
    asyncio.run(main())
