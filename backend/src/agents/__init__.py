"""
Malla de Agentes Especializados de Lifextreme Perú
Conectados a Qdrant Vector DB y motor local de IA Ollama nomic-embed-text.
"""
from .medical_acclimatization_agent import MedicalAcclimatizationAgent
from .duffle_bag_optimizer_agent import DuffleBagOptimizerAgent
from .tailor_made_private_agent import TailorMadePrivateAgent
from .field_sentinel_safety_agent import FieldSentinelSafetyAgent
from .reputation_quality_agent import ReputationQualityAgent
from .router import router

__all__ = [
    "MedicalAcclimatizationAgent",
    "DuffleBagOptimizerAgent",
    "TailorMadePrivateAgent",
    "FieldSentinelSafetyAgent",
    "ReputationQualityAgent",
    "router"
]
