from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.database import SessionDep
from app.schemas import CreateNote, ResponseNote, UpdateNote
from app.models import NoteOrm

router = APIRouter(prefix='/notes', tags=['Notes'])

@router.post('/', summary='Добавить заметку', response_model=ResponseNote)
async def create_note(session: SessionDep, note: CreateNote):
    
    new_note = NoteOrm(title = note.title, content = note.content)
    session.add(new_note)
    await session.commit()

    return new_note


@router.get('/get', summary='Получить заметки по имени', response_model=list[ResponseNote])
async def get_one_by_title(session: SessionDep, search: str):

    query = select(NoteOrm).where(NoteOrm.title.ilike(f'%{search}%'))
    result = await session.execute(query)
    note = result.scalars().all()

    if not note:
        raise HTTPException(status_code=404, detail='Заметка не найдена')

    return note


@router.get('/{note_id}', summary='Получить одну заметку по id', response_model=ResponseNote)
async def get_one_by_id(session: SessionDep, note_id: int):

    query = select(NoteOrm).where(NoteOrm.id == note_id)
    note = await session.execute(query)
    result = note.scalar_one_or_none()

    if result is None:
        raise HTTPException(status_code=404, detail='Заметка не найдена!')

    return result


@router.get('/', summary='Получить все заметки', response_model=list[ResponseNote])
async def get_all(session: SessionDep):

    query = select(NoteOrm)
    note = await session.execute(query)
    result = note.scalars().all()

    return result


@router.patch('/{note_id}', summary='Изменить заметку', response_model=ResponseNote)
async def edit_note(session: SessionDep, note_id: int, note: UpdateNote):

    query = select(NoteOrm).where(NoteOrm.id == note_id)
    result = await session.execute(query)
    db_notes = result.scalar_one_or_none()

    if db_notes is None:
        raise HTTPException(status_code=404, detail='Заметка не найдена!')

    if note.title is not None:
        db_notes.title = note.title
    if note.content is not None:
        db_notes.content = note.content

    await session.commit()
    await session.refresh(db_notes)
    return db_notes


@router.delete('/{note_id}', summary='Удалить заметку')
async def delete_note(session: SessionDep, note_id: int):

    query = select(NoteOrm).where(NoteOrm.id == note_id)
    result = await session.execute(query)
    note = result.scalar_one_or_none()

    if note is None:
        raise HTTPException(status_code=404, detail='Заметка не найдена!')

    await session.delete(note)
    await session.commit()

    return {'msg': f'Заметка {note.title} удалена!'}

