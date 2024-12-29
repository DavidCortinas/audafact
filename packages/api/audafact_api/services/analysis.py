from sqlalchemy.ext.asyncio import AsyncSession
from models.analysis import UserAnalysis
import logging

logger = logging.getLogger(__name__)

async def save_user_analysis(
    email: str, 
    analysis_id: str, 
    db: AsyncSession,
    partial_results: dict = None
) -> UserAnalysis:
    try:
        # Check if analysis already exists
        existing_analysis = await db.query(UserAnalysis).filter(
            UserAnalysis.analysis_id == analysis_id
        ).first()
        
        if existing_analysis:
            # Update existing analysis with email
            existing_analysis.email = email
            await db.commit()
            return existing_analysis
            
        # Create new analysis entry
        new_analysis = UserAnalysis(
            email=email,
            analysis_id=analysis_id,
            partial_results=partial_results
        )
        
        db.add(new_analysis)
        await db.commit()
        await db.refresh(new_analysis)
        
        logger.info(f"Saved analysis for email: {email}, analysis_id: {analysis_id}")
        return new_analysis
        
    except Exception as e:
        await db.rollback()
        logger.error(f"Error saving user analysis: {str(e)}")
        raise
