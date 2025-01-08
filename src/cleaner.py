import asyncio
from main import Actions
from helpers import log

import argparse
parser = argparse.ArgumentParser(description='Clean Reddit Account')

parser.add_argument('--confuse', '-c', action="store_true",
                    help="Confuse all comments or submissions")

parser.add_argument('--single_confuse', '-sc', action="store_true",
                    help="Confuse single comments or submissions")

parser.add_argument('--delete', '-d', action="store_true",
                    help="Delete comments or submissions")

parser.add_argument('--activate_rollback', '-rlb', action="store_true",
                    help="Activate rollback with help of a local DB")


async def main():
    args = parser.parse_args()

    confuse = getattr(args, 'confuse')
    delete = getattr(args, 'delete')
    rlb = getattr(args, 'activate_rollback', False)

    if confuse:
        log('I am going to CONFUSE your activity.')
        print("[ATTENTION!] In most cases actions are not revertible. Proceed? (Y/N)")
        ans = input('[Ans]:')

        if ans.lower() == 'y':
            account = Actions('old', rlb)
            await account.init_reddit()
            log('CONFUSE All data or for a single id? \nAll=A Single=S', 'question')
            bulk = input('[Ans]:')

            if bulk.lower() == 'a':
                log('What do you want to confuse?\nComments=C Submissions=S, Both=B', 'question')
                what = input('[Ans]:')

                if what.lower() == 'c':
                    await account.confuser(comments=True)
                elif what.lower() == 's':
                    await account.confuser(submission=True)
                elif what.lower() == 'b':
                    await account.confuser(submission=True, comments=True)
                else:
                    quit('Not known action provided, quitting...')

            if bulk.lower() == 's':
                log('What do you want to confuse?\nComments=C Submissions=S', 'question')
                what = input('[Ans]:')

                log('Provide the id (grab it from the link)', 'question')
                id = input('[Ans]:')

                if what.lower() == 'c':
                    await account.confuser(comments=True, id=id)
                elif what.lower() == 's':
                    await account.confuser(submission=True, id=id)
                else:
                    quit('Not known action provided, quitting...')

    if delete:
        log('This Will DELETE ALL of your activity. You will lose all the earned karma\n'
            '[HINT] Reddit keeps an archive of deleted stuff, use confuse option (-c) for better results')
        print("[ATTENTION!] This can't be undone. Are you sure? (Y/N)")
        ans = input('[Ans]:')
        if ans.lower() == 'y':
            account = Actions('old', rlb)
            await account.init_reddit()
            log('What to delete?\nComments=C Submissions=S', 'question')
            ans = input('[Ans]:')

            if ans.lower() == 'c':
                await account.delete_activity(comments=True)
            elif ans.lower() == 's':
                await account.delete_activity(submission=True)

    log('All operations are completed', 'info')
    await account.close_reddit()


if __name__ == "__main__":
    asyncio.run(main())