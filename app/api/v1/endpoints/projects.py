from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.dependency import get_db
from app.core.di import registry
from app.models.project import Project
from app.api.v1.schemas.project import ProjectCreate, ProjectResponse, ProjectSelectByUser
from app.modules.projects.manager import ProjectManager

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectResponse, status_code=201)
async def create_project(
    body: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    manager: ProjectManager = Depends(registry.get(ProjectManager)),
):
    project = Project(
        project_name=body.project_name,
        user_id=body.user_id,
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    await manager.create(body.project_name, body.user_id)
    return project


@router.post("/select", response_model=List[ProjectResponse])
async def get_projects_by_user(body: ProjectSelectByUser, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).where(Project.user_id == body.user_id))
    return result.scalars().all()


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    manager: ProjectManager = Depends(registry.get(ProjectManager)),
):
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    await db.delete(project)
    await db.commit()
    await manager.delete(project_id)
