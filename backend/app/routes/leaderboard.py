from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.deps import get_db

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("/")
def get_leaderboard(db: Session = Depends(get_db)):
    query = text("""
        SELECT 
            u.id AS student_id,
            u.email,
            COUNT(s.id) AS total_submissions,
            RANK() OVER (ORDER BY COUNT(s.id) DESC) AS rank
        FROM users u
        LEFT JOIN submissions s ON u.id = s.student_id
        WHERE u.role = 'student'
        GROUP BY u.id
        ORDER BY rank
    """)

    result = db.execute(query).fetchall()

    return [
        {
            "student_id": row.student_id,
            "email": row.email,
            "total_submissions": row.total_submissions,
            "rank": row.rank
        }
        for row in result
    ]