import json
from datetime import timedelta, datetime, timezone

import redis
from fastapi import APIRouter, HTTPException, status
from sqlmodel import select, col

from app.database import SessionDep
from app.models import PastesCreate, Pastes
from app.utils import Base62

router = APIRouter(prefix='/pastes', tags=['pastes'])
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
base_62 = Base62()


@router.post('/', response_model=PastesCreate)
def create_paste(paste: Pastes, session: SessionDep = None):
    session.add(paste)
    session.commit()
    session.refresh(paste)

    paste.code = base_62.encoder(paste.id)
    paste.expiration_time = paste.creation_time + timedelta(seconds=paste.ttl)
    data = Pastes.model_validate(paste).model_dump(mode="json")

    r.set(paste.code, json.dumps(data), ex=paste.ttl)

    session.add(paste)
    session.commit()
    session.refresh(paste)
    return paste


@router.get('/{code}', response_model=PastesCreate)
def get_paste(code: str, session: SessionDep = None):
    cache = r.get(code)
    if cache:
        print(f"Cache Hit!")
        return json.loads(cache)

    paste = session.exec(select(Pastes).where(col(Pastes.code) == code)).one()
    data = Pastes.model_validate(paste).model_dump(mode="json")

    remaining_ttl = (paste.expiration_time - datetime.now(tz=timezone.utc)).seconds
    r.set(code, json.dumps(data), ex=remaining_ttl)

    if not paste:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail='text gone')
    return paste


async def pastes_cleanup(session: SessionDep = None):
    current_time = datetime.now(tz=timezone.utc)
    query = select(Pastes).where(col(Pastes.expiration_time) < current_time)
    session.delete(query)
    session.commit()
