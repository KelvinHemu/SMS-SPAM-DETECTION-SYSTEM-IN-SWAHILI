"""
Message Labeler
Adds Swahili warning labels to messages based on spam analysis results
"""

from api.models import DecisionOutcome
from core.logging import get_logger

logger = get_logger()

# Swahili label mappings
SWAHILI_LABELS = {
    DecisionOutcome.CLEAN: "",  # No label for clean messages
    DecisionOutcome.CONTENT_WARNING: "⚠️ Tahadhari: Epuka Matapeli",  # Warning: Avoid Fraud/Scams
    DecisionOutcome.SENDER_WARNING: "⚠️ Tahadhari: Epuka Matapeli",   # Warning: Avoid Fraud/Scams
    DecisionOutcome.BLOCKED: "🚫 Imezuiliwa: SPAM"  # Blocked: SPAM
}

# English translations for reference
LABEL_TRANSLATIONS = {
    DecisionOutcome.CLEAN: "Clean",
    DecisionOutcome.CONTENT_WARNING: "Warning: Avoid Fraud/Scams", 
    DecisionOutcome.SENDER_WARNING: "Warning: Avoid Fraud/Scams",
    DecisionOutcome.BLOCKED: "Blocked: SPAM"
}


def add_swahili_label(message_text: str, decision: DecisionOutcome) -> str:
    """
    Add appropriate Swahili label to message based on decision outcome
    
    Args:
        message_text: Original message text
        decision: Analysis decision outcome
        
    Returns:
        Message with appropriate Swahili label prepended
    """
    try:
        label = SWAHILI_LABELS.get(decision, "")
        
        if label:
            # Add label at the top with separator
            labeled_message = f"{label}\n\n{message_text}"
            logger.debug(f"Added label '{label}' to message")
        else:
            # Clean messages get no label
            labeled_message = message_text
            logger.debug("No label added - message is clean")
        
        return labeled_message
        
    except Exception as e:
        logger.error(f"Error adding label to message: {str(e)}")
        # Return original message on error
        return message_text


def get_label_info(decision: DecisionOutcome) -> dict:
    """
    Get label information for a decision outcome
    
    Args:
        decision: Analysis decision outcome
        
    Returns:
        Dictionary with label details
    """
    return {
        "swahili_label": SWAHILI_LABELS.get(decision, ""),
        "english_translation": LABEL_TRANSLATIONS.get(decision, "Unknown"),
        "has_label": bool(SWAHILI_LABELS.get(decision, "")),
        "decision": decision.value
    }


def should_block_message(decision: DecisionOutcome) -> bool:
    """
    Determine if message should be blocked from delivery
    
    Args:
        decision: Analysis decision outcome
        
    Returns:
        True if message should be blocked, False otherwise
    """
    return decision == DecisionOutcome.BLOCKED


# Available label styles for different use cases
def get_compact_label(decision: DecisionOutcome) -> str:
    """Get compact version of label for SMS/space-constrained scenarios"""
    compact_labels = {
        DecisionOutcome.CLEAN: "",
        DecisionOutcome.CONTENT_WARNING: "⚠️ Epuka Matapeli",
        DecisionOutcome.SENDER_WARNING: "⚠️ Epuka Matapeli", 
        DecisionOutcome.BLOCKED: "🚫 SPAM"
    }
    return compact_labels.get(decision, "")


def get_formal_label(decision: DecisionOutcome) -> str:
    """Get formal version of label for official communications"""
    formal_labels = {
        DecisionOutcome.CLEAN: "",
        DecisionOutcome.CONTENT_WARNING: "Tahadhari: Ujumbe huu unaweza kuwa ni ulaghai. Epuka kutoa maelezo ya kibinafsi au fedha.",
        DecisionOutcome.SENDER_WARNING: "Tahadhari: Ujumbe huu unaweza kuwa ni ulaghai. Epuka kutoa maelezo ya kibinafsi au fedha.",
        DecisionOutcome.BLOCKED: "Ujumbe huu umezuiliwa kwa sababu ni SPAM. Usijibu au usiingiliane na ujumbe huu."
    }
    return formal_labels.get(decision, "") 