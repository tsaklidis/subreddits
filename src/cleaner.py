from main import Actions


import argparse
parser = argparse.ArgumentParser(description='Clean Reddit Account')

parser.add_argument('--confuse', '-c', action="store_true",
                    help="Confuse all comments or submissions")

parser.add_argument('--single_confuse', '-sc', action="store_true",
                    help="Confuse single comments or submissions")

parser.add_argument('--delete', '-d', action="store_true",
                    help="Delete comments or submissions")


if __name__ == "__main__":
    args = parser.parse_args()

    confuse = getattr(args, 'confuse')
    delete = getattr(args, 'delete')

    if confuse:
        print('[i] Will CONFUSE your activity.')
        print("[ATTENTION!] This can't be undone. Are you sure? (Y/N)")
        ans = input('[Ans]:')

        if ans.lower() == 'y':
            account = Actions('old')
            print('[Q] CONFUSE All data or for a single id? \nAll=A Single=S')
            bulk = input('[Ans]:')

            if bulk.lower() == 'a':
                print('[Q] What do you want to confuse?\nComments=C '
                      'Submissions=S')
                what = input('[Ans]:')

                if what.lower() == 'c':
                    account.confuser(comments=True)
                elif what.lower() == 's':
                    account.confuser(submission=True)
                else:
                    quit('Not known action provided, quiting...')

            if bulk.lower() == 's':
                print('[Q] What do you want to confuse?\nComments=C '
                      'Submissions=S')
                what = input('[Ans]:')

                print('[Q] Provide the id (grub it from the link)')
                id = input('[Ans]:')

                if what.lower() == 'c':
                    account.confuser(comments=True, id=id)
                elif what.lower() == 's':
                    account.confuser(submission=True, id=id)
                else:
                    quit('Not known action provided, quiting...')

    if delete:
        print('[i] This Will DELETE ALL of your activity. You will lose all '
              'the earned karma\n'
              '[HINT] Reddit keeps archive of deleted stuff, use confuse '
              'option (-c) for better results')
        print("[ATTENTION!] This can't be undone. Are you sure? (Y/N)")
        ans = input('[Ans]:')
        if ans.lower() == 'y':
            account = Actions('old')
            print('[Q] What to delete?\nComments=C Submissions=S')
            ans = input('[Ans]:')
            if ans.lower() == 'c':
                account.delete_activity(comments=True)
            if ans.lower() == 's':
                account.delete_activity(submission=True)
