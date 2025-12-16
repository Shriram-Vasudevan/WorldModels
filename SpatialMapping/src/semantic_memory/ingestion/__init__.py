"""Ingestion pipeline for photos and descriptions."""

from semantic_memory.ingestion.observation import Observation
from semantic_memory.ingestion.photo_processor import PhotoProcessor

__all__ = ["Observation", "PhotoProcessor"]
