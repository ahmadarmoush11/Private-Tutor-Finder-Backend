from fastapi import APIRouter, Depends, status

from app.features.auth.dependencies import require_admin
from app.features.subjects.dependencies import SubjectServiceDep
from app.features.subjects.schemas import SubjectCreate, SubjectOut, SubjectUpdate


router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.get("", response_model=list[SubjectOut])
def get_subjects(service: SubjectServiceDep):
    return service.get_all()


@router.get("/{subject_id}", response_model=SubjectOut)
def get_subject(subject_id: int, service: SubjectServiceDep):
    return service.get_by_id(subject_id)


@router.post(
    "",
    response_model=SubjectOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
def create_subject(data: SubjectCreate, service: SubjectServiceDep):
    return service.create(data)


@router.patch(
    "/{subject_id}",
    response_model=SubjectOut,
    dependencies=[Depends(require_admin)],
)
def update_subject(subject_id: int, data: SubjectUpdate, service: SubjectServiceDep):
    return service.update(subject_id, data)


@router.delete(
    "/{subject_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_subject(subject_id: int, service: SubjectServiceDep):
    service.delete(subject_id)
