from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.deps import get_db, get_current_user
from app import models
from sqlalchemy import func

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/dashboard")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Only admin allowed
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    total_students = db.query(models.User).filter(models.User.role == "student").count()
    total_courses = db.query(models.Course).count()
    total_enrollments = db.query(models.Enrollment).count()

    # Course-wise student count
    course_stats = (
        db.query(
            models.Course.title,
            func.count(models.Enrollment.id).label("student_count")
        )
        .outerjoin(models.Enrollment, models.Course.id == models.Enrollment.course_id)
        .group_by(models.Course.id)
        .all()
    )

    return {
        "total_students": total_students,
        "total_courses": total_courses,
        "total_enrollments": total_enrollments,
        "course_stats": [
            {
                "course": c.title,
                "students": c.student_count
            }
            for c in course_stats
        ]
    }