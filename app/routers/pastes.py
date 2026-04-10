import redis
from fastapi import APIRouter

from app.utils import Base62

TTL = 60 * 3
router = APIRouter(prefix='/pastes', tags=['pastes'])
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
base_62 = Base62()
