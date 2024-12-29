from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from services.analysis import save_user_analysis

router = APIRouter()

@router.post("/analysis/email")
async def save_user_email(
    email: str,
    analysis_id: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        # Save email and analysis association
        analysis = await save_user_analysis(email, analysis_id, db)
        
        # Return payment options/link
        return {
            "status": "success",
            "analysis_id": str(analysis.id),
            "next_step": "payment",
            "payment_url": generate_payment_url(str(analysis.id))
        }
    except Exception as e:
        logger.error(f"Error processing email save: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error saving analysis: {str(e)}"
        )
