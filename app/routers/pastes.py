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

    paste = session.exec(select(Pastes).where(col(Pastes.code) == code)).first()
    data = Pastes.model_validate(paste).model_dump(mode="json")
    remaining_ttl = int((paste.expiration_time - datetime.now(tz=timezone.utc)).total_seconds())
    if remaining_ttl < 0:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail='text gone')
    r.set(code, json.dumps(data), ex=remaining_ttl)
    return paste
