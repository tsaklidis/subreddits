import asyncio

from main import Actions
from db_operations import DB
from helpers import log, confirm


async def main():
    database = DB()
    to_rollback = database.get_pending_rollbacks()

    if len(to_rollback) == 0:
        log('No pending rollbacks found.')
        return

    comments = [r for r in to_rollback if r['is_comment']]
    submissions = [r for r in to_rollback if not r['is_comment']]
    log(f'Found {len(to_rollback)} pending rollbacks '
        f'({len(comments)} comments, {len(submissions)} submissions)')

    if not confirm('Restore original content on Reddit?'):
        log('Rollback cancelled.')
        return

    account = Actions('old')
    await account.init_reddit()

    success = 0
    for i, item in enumerate(to_rollback, 1):
        item_id = item['id']
        kind = 'comment' if item['is_comment'] else 'submission'
        try:
            if item['is_comment']:
                obj = await account.get_comment(id=item_id)
            else:
                obj = await account.get_submission(id=item_id)

            await obj.edit(item['value'])
            database.delete_record(item_id)
            success += 1
            log(f'[{i}/{len(to_rollback)}] Restored {kind} {item_id}')
        except Exception as e:
            log(f'[{i}/{len(to_rollback)}] Failed {kind} {item_id}: {e}', 'error')

    await account.close_reddit()
    log(f'Rollback finished: {success}/{len(to_rollback)} restored.')


if __name__ == "__main__":
    asyncio.run(main())
