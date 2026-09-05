from fastapi import APIRouter
from database import SessionDep
from app.schemas import NoteCreate
from app.models import NoteOrm

router = APIRouter(prefix='/notes', tags=['Notes'])

@router.post('/')
async def create_note(session: SessionDep, note: NoteCreate):
    new_note = NoteOrm(title = note.title, content = note.content)

    session.add(new_note)
    session.commit()
    return {'msg': f'Задача {note.title} успешно добавлена!'}