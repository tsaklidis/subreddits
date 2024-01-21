import argparse

from main import Actions
from db_operations import DB
from helpers import log

parser = argparse.ArgumentParser(description='Rollback after confusion run')

parser.add_argument('--do-it', '-do-it', action="store_true",
                    help="Send the changes to Reddit, default is dry run")


if __name__ == "__main__":
    account = Actions('old')
    database = DB()
    to_rollback = database.get_pending_rollbacks()
    success_rolls = 0

    log(f'Found {len(to_rollback)} pending rollbacks')
    log(f'Try to send them back online (Y/N)?')
    ans = input('[Ans]:')
    if ans.lower() == 'y':
        for item in to_rollback:
            # We need to get the correct object, comment or submission
            item_id = item.get('id')
            if item.get('is_comment'):
                obj = account.get_comment(id=item_id)
            else:
                obj = account.get_submission(id=item_id)
            try:
                # Try to edit the object by id, it may fail for varius
                # reasons eg: Item is deleted
                obj.edit(item.get('value'))

                # Rollback sent back online, no reason to keep it in DB. Delete
                database.delete_record(item_id)
                success_rolls += 1
            except Exception as e:
                log('Could not rollback, Comment/Submission not found',
                    'error')
        log(f'Rollback finished! Completed {success_rolls}/{len(to_rollback)}')
        quit('Bye!')
    else:
        log('Rollback cancelled.')
        quit('Bye!')