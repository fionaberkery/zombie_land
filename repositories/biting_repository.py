from db.run_sql import run_sql
from models.biting import Biting
import repositories.human_repository as human_repo
import repositories.zombie_repository as zombie_repo

def save(bite):
    sql = "INSERT INTO bitings (zombie_id, human_id) VALUES (%s, %s) RETURNING id"
    values = [bite.zombie.id, bite.human.id]
    results = run_sql(sql, values)
    id = results[0]['id']
    bite.id = id


def select_all():
    bites = []
    sql = "SELECT * FROM bitings"
    results = run_sql(sql)
    for result in results:
        human = human_repo.select(result["human_id"])
        zombie = zombie_repo.select(result["zombie_id"])
        bite = Biting(human, zombie, result['id'])
        bites.append(bite)
    return bites


def select(id):
    sql = "SELECT * FROM bitings WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)[0]
    bite = Biting(result["zombie_id"], result["human_id"], result["id"])
    return bite


def delete_all():
    sql = "DELETE FROM bitings"
    run_sql(sql)


def delete(id):
    sql = "DELETE FROM bitings WHERE id = %s"
    values = [id]
    run_sql(sql, values)


def update(bite):
    sql = "UPDATE bitings SET (human_id, zombie_id) = (%s, %s) WHERE id = %s"
    values = [bite.human.id, bite.zombie.id, bite.id]
    run_sql(sql, values)
