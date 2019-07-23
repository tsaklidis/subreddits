from main import Actions


import argparse
parser = argparse.ArgumentParser(description='Clean Reddit Account')

parser.add_argument('--confuse', '-c', action="store_true",
                    help="Confuse comments or submissions")

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
        if ans == 'Y' or ans == 'y':
            account = Actions('old')
            print('[Q] What to confuse?\nComments=C Submissions=S')
            ans = input('[Ans]:')
            if ans == 'c' or ans == 'C':
                account.confuser(comments=True)
            if ans == 's' or ans == 'S':
                account.confuser(submission=True)

    if delete:
        print('[i] Will DELETE your activity.')
        print("[ATTENTION!] This can't be undone. Are you sure? (Y/N)")
        ans = input('[Ans]:')
        if ans == 'Y' or ans == 'y':
            account = Actions('old')
            print('[Q] What to delete?\nComments=C Submissions=S')
            ans = input('[Ans]:')
            if ans == 'c' or ans == 'C':
                account.delete_activity(comments=True)
            if ans == 's' or ans == 'S':
                account.delete_activity(submission=True)
