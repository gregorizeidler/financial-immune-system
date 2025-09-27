"""
Financial Forensics Laboratory
=============================

Advanced forensic analysis system for post-attack investigation and intelligence gathering.
Performs detailed analysis of attack patterns, attribution, and creates comprehensive
threat profiles for future prevention.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np
from collections import defaultdict, deque
import hashlib
import uuid
import re

from financial_immune_system import FinancialPathogen, Transaction, AnomalyType, ThreatLevel

logger = logging.getLogger(__name__)


class EvidenceType(Enum):
    """Types of forensic evidence"""
    TRANSACTION_PATTERN = "transaction_pattern"
    BEHAVIORAL_SIGNATURE = "behavioral_signature"
    NETWORK_TRACE = "network_trace"
    TEMPORAL_CORRELATION = "temporal_correlation"
    GEOGRAPHIC_FOOTPRINT = "geographic_footprint"
    DEVICE_FINGERPRINT = "device_fingerprint"
    SOCIAL_GRAPH = "social_graph"
    LINGUISTIC_ANALYSIS = "linguistic_analysis"


class AttackPhase(Enum):
    """Phases of an attack lifecycle"""
    RECONNAISSANCE = "reconnaissance"
    INITIAL_ACCESS = "initial_access"
    PERSISTENCE = "persistence"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    LATERAL_MOVEMENT = "lateral_movement"
    COLLECTION = "collection"
    EXFILTRATION = "exfiltration"
    IMPACT = "impact"


class AttributionConfidence(Enum):
    """Confidence levels for threat attribution"""
    LOW = 0.3
    MEDIUM = 0.6
    HIGH = 0.8
    VERY_HIGH = 0.95


@dataclass
class ForensicEvidence:
    """A piece of forensic evidence"""
    evidence_id: str
    evidence_type: EvidenceType
    source_transaction_id: str
    timestamp: datetime
    data: Dict[str, Any]
    confidence: float
    chain_of_custody: List[str]
    analysis_notes: str


@dataclass
class AttackVector:
    """Detailed analysis of an attack vector"""
    vector_id: str
    attack_type: str
    entry_point: str
    techniques_used: List[str]
    tools_identified: List[str]
    timeline: List[Dict[str, Any]]
    success_indicators: List[str]
    failure_indicators: List[str]
    sophistication_level: float


@dataclass
class ThreatActor:
    """Profile of a threat actor"""
    actor_id: str
    aliases: List[str]
    attribution_confidence: AttributionConfidence
    known_techniques: List[str]
    target_preferences: List[str]
    geographic_origin: Optional[str]
    motivation: str
    sophistication_level: float
    activity_timeline: List[Dict[str, Any]]
    associated_campaigns: List[str]


@dataclass
class AttackCampaign:
    """Analysis of a coordinated attack campaign"""
    campaign_id: str
    campaign_name: str
    start_date: datetime
    end_date: Optional[datetime]
    threat_actor: Optional[str]
    attack_vectors: List[str]
    targets: List[str]
    geographic_scope: List[str]
    estimated_damage: float
    indicators_of_compromise: List[str]
    mitigation_recommendations: List[str]


class ForensicAnalyzer:
    """Core forensic analysis engine"""
    
    def __init__(self):
        self.evidence_database: Dict[str, ForensicEvidence] = {}
        self.attack_vectors: Dict[str, AttackVector] = {}
        self.threat_actors: Dict[str, ThreatActor] = {}
        self.attack_campaigns: Dict[str, AttackCampaign] = {}
        
        # Analysis engines
        self.pattern_analyzer = PatternAnalyzer()
        self.behavioral_analyzer = BehavioralAnalyzer()
        self.network_analyzer = NetworkAnalyzer()
        self.temporal_analyzer = TemporalAnalyzer()
        self.attribution_engine = AttributionEngine()
        
        logger.info("Forensic Analyzer initialized")
    
    async def initiate_investigation(self, incident_data: Dict[str, Any]) -> str:
        """Initiate a new forensic investigation"""
        
        investigation_id = str(uuid.uuid4())
        
        # Create investigation record
        investigation = {
            "investigation_id": investigation_id,
            "incident_type": incident_data.get("incident_type", "unknown"),
            "start_time": datetime.now(),
            "status": "active",
            "priority": incident_data.get("priority", "medium"),
            "assigned_analysts": ["forensic_ai_1", "pattern_analyst_2"],
            "evidence_collected": [],
            "findings": [],
            "timeline": [],
            "recommendations": []
        }
        
        # Begin evidence collection
        await self._collect_initial_evidence(investigation_id, incident_data)
        
        logger.info(f"Initiated forensic investigation: {investigation_id}")
        
        return investigation_id
    
    async def _collect_initial_evidence(self, investigation_id: str, incident_data: Dict[str, Any]):
        """Collect initial evidence for investigation"""
        
        # Extract transactions involved in incident
        transactions = incident_data.get("transactions", [])
        
        for transaction_data in transactions:
            # Collect transaction pattern evidence
            pattern_evidence = await self._analyze_transaction_pattern(transaction_data)
            if pattern_evidence:
                self.evidence_database[pattern_evidence.evidence_id] = pattern_evidence
            
            # Collect behavioral evidence
            behavioral_evidence = await self._analyze_behavioral_signature(transaction_data)
            if behavioral_evidence:
                self.evidence_database[behavioral_evidence.evidence_id] = behavioral_evidence
            
            # Collect temporal evidence
            temporal_evidence = await self._analyze_temporal_patterns(transaction_data)
            if temporal_evidence:
                self.evidence_database[temporal_evidence.evidence_id] = temporal_evidence
    
    async def _analyze_transaction_pattern(self, transaction_data: Dict[str, Any]) -> Optional[ForensicEvidence]:
        """Analyze transaction patterns for forensic evidence"""
        
        # Extract pattern features
        pattern_features = {
            "amount_pattern": self._extract_amount_pattern(transaction_data),
            "frequency_pattern": self._extract_frequency_pattern(transaction_data),
            "merchant_pattern": self._extract_merchant_pattern(transaction_data),
            "location_pattern": self._extract_location_pattern(transaction_data)
        }
        
        # Calculate pattern uniqueness
        pattern_hash = hashlib.sha256(json.dumps(pattern_features, sort_keys=True).encode()).hexdigest()
        uniqueness_score = await self._calculate_pattern_uniqueness(pattern_hash)
        
        if uniqueness_score > 0.7:  # Significant pattern
            evidence = ForensicEvidence(
                evidence_id=str(uuid.uuid4()),
                evidence_type=EvidenceType.TRANSACTION_PATTERN,
                source_transaction_id=transaction_data.get("id", "unknown"),
                timestamp=datetime.now(),
                data={
                    "pattern_features": pattern_features,
                    "pattern_hash": pattern_hash,
                    "uniqueness_score": uniqueness_score
                },
                confidence=uniqueness_score,
                chain_of_custody=["forensic_analyzer"],
                analysis_notes=f"Unique transaction pattern identified (score: {uniqueness_score:.2f})"
            )
            
            return evidence
        
        return None
    
    def _extract_amount_pattern(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract amount-related patterns"""
        amount = transaction_data.get("amount", 0)
        
        return {
            "amount": amount,
            "is_round_number": amount == int(amount),
            "decimal_places": len(str(amount).split('.')[-1]) if '.' in str(amount) else 0,
            "amount_range": self._categorize_amount(amount),
            "suspicious_amount": self._is_suspicious_amount(amount)
        }
    
    def _categorize_amount(self, amount: float) -> str:
        """Categorize transaction amount"""
        if amount < 10:
            return "micro"
        elif amount < 100:
            return "small"
        elif amount < 1000:
            return "medium"
        elif amount < 10000:
            return "large"
        else:
            return "huge"
    
    def _is_suspicious_amount(self, amount: float) -> bool:
        """Check if amount is suspicious (e.g., structuring)"""
        # Common structuring amounts
        structuring_amounts = [9000, 9500, 9900, 9999]
        return any(abs(amount - sa) < 100 for sa in structuring_amounts)
    
    def _extract_frequency_pattern(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract frequency-related patterns"""
        timestamp = transaction_data.get("timestamp", datetime.now())
        
        return {
            "hour_of_day": timestamp.hour,
            "day_of_week": timestamp.weekday(),
            "is_weekend": timestamp.weekday() >= 5,
            "is_business_hours": 9 <= timestamp.hour <= 17,
            "is_night_time": timestamp.hour < 6 or timestamp.hour > 22
        }
    
    def _extract_merchant_pattern(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract merchant-related patterns"""
        merchant = transaction_data.get("merchant", "").lower()
        
        return {
            "merchant": merchant,
            "merchant_category": self._categorize_merchant(merchant),
            "is_online": "online" in merchant or "web" in merchant,
            "is_cash_equivalent": any(term in merchant for term in ["atm", "cash", "advance"]),
            "merchant_risk_level": self._assess_merchant_risk(merchant)
        }
    
    def _categorize_merchant(self, merchant: str) -> str:
        """Categorize merchant type"""
        categories = {
            "retail": ["store", "shop", "mall", "target", "walmart"],
            "food": ["restaurant", "cafe", "food", "pizza"],
            "gas": ["gas", "fuel", "shell", "exxon"],
            "online": ["amazon", "ebay", "paypal", "online"],
            "entertainment": ["movie", "theater", "game"],
            "travel": ["hotel", "airline", "uber"],
            "financial": ["bank", "atm", "cash", "loan"]
        }
        
        for category, keywords in categories.items():
            if any(keyword in merchant for keyword in keywords):
                return category
        
        return "other"
    
    def _assess_merchant_risk(self, merchant: str) -> str:
        """Assess merchant risk level"""
        high_risk_indicators = ["cash", "advance", "pawn", "check", "loan", "unknown"]
        medium_risk_indicators = ["online", "digital", "crypto", "gaming"]
        
        if any(indicator in merchant for indicator in high_risk_indicators):
            return "high"
        elif any(indicator in merchant for indicator in medium_risk_indicators):
            return "medium"
        else:
            return "low"
    
    def _extract_location_pattern(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract location-related patterns"""
        location = transaction_data.get("location", "").lower()
        
        return {
            "location": location,
            "is_international": self._is_international_location(location),
            "risk_jurisdiction": self._assess_jurisdiction_risk(location),
            "location_type": self._categorize_location_type(location)
        }
    
    def _is_international_location(self, location: str) -> bool:
        """Check if location is international"""
        international_indicators = ["international", "foreign", "overseas"]
        return any(indicator in location for indicator in international_indicators)
    
    def _assess_jurisdiction_risk(self, location: str) -> str:
        """Assess jurisdiction risk level"""
        high_risk_jurisdictions = ["unknown", "offshore", "anonymous"]
        
        if any(jurisdiction in location for jurisdiction in high_risk_jurisdictions):
            return "high"
        else:
            return "low"
    
    def _categorize_location_type(self, location: str) -> str:
        """Categorize location type"""
        if "online" in location or "virtual" in location:
            return "virtual"
        elif "atm" in location:
            return "atm"
        elif "store" in location or "shop" in location:
            return "retail"
        else:
            return "physical"
    
    async def _calculate_pattern_uniqueness(self, pattern_hash: str) -> float:
        """Calculate how unique a pattern is"""
        # In a real implementation, this would compare against a database of known patterns
        # For demo purposes, we'll simulate uniqueness based on hash
        
        # Convert hash to numeric value for simulation
        hash_numeric = int(pattern_hash[:8], 16) / 0xFFFFFFFF
        
        # Simulate uniqueness (higher values are more unique)
        uniqueness = 0.3 + (hash_numeric * 0.7)
        
        return uniqueness
    
    async def _analyze_behavioral_signature(self, transaction_data: Dict[str, Any]) -> Optional[ForensicEvidence]:
        """Analyze behavioral signatures"""
        
        behavioral_features = {
            "user_id": transaction_data.get("user_id"),
            "device_fingerprint": self._extract_device_fingerprint(transaction_data),
            "interaction_pattern": self._extract_interaction_pattern(transaction_data),
            "timing_signature": self._extract_timing_signature(transaction_data)
        }
        
        # Calculate behavioral anomaly score
        anomaly_score = await self._calculate_behavioral_anomaly(behavioral_features)
        
        if anomaly_score > 0.6:
            evidence = ForensicEvidence(
                evidence_id=str(uuid.uuid4()),
                evidence_type=EvidenceType.BEHAVIORAL_SIGNATURE,
                source_transaction_id=transaction_data.get("id", "unknown"),
                timestamp=datetime.now(),
                data={
                    "behavioral_features": behavioral_features,
                    "anomaly_score": anomaly_score
                },
                confidence=anomaly_score,
                chain_of_custody=["behavioral_analyzer"],
                analysis_notes=f"Behavioral anomaly detected (score: {anomaly_score:.2f})"
            )
            
            return evidence
        
        return None
    
    def _extract_device_fingerprint(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract device fingerprint information"""
        metadata = transaction_data.get("metadata", {})
        
        return {
            "user_agent": metadata.get("user_agent", "unknown"),
            "ip_address": metadata.get("ip_address", "unknown"),
            "device_type": metadata.get("device_type", "unknown"),
            "browser": metadata.get("browser", "unknown"),
            "os": metadata.get("os", "unknown")
        }
    
    def _extract_interaction_pattern(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract user interaction patterns"""
        return {
            "session_duration": transaction_data.get("session_duration", 0),
            "clicks_before_transaction": transaction_data.get("clicks", 0),
            "form_fill_time": transaction_data.get("form_fill_time", 0),
            "authentication_method": transaction_data.get("auth_method", "unknown")
        }
    
    def _extract_timing_signature(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract timing-related behavioral signatures"""
        timestamp = transaction_data.get("timestamp", datetime.now())
        
        return {
            "transaction_time": timestamp.isoformat(),
            "time_since_last_login": transaction_data.get("time_since_login", 0),
            "typing_speed": transaction_data.get("typing_speed", 0),
            "mouse_movement_pattern": transaction_data.get("mouse_pattern", "normal")
        }
    
    async def _calculate_behavioral_anomaly(self, behavioral_features: Dict[str, Any]) -> float:
        """Calculate behavioral anomaly score"""
        anomaly_indicators = 0
        total_indicators = 0
        
        # Check device fingerprint anomalies
        device_fp = behavioral_features.get("device_fingerprint", {})
        if device_fp.get("user_agent") == "unknown":
            anomaly_indicators += 1
        total_indicators += 1
        
        # Check interaction pattern anomalies
        interaction = behavioral_features.get("interaction_pattern", {})
        if interaction.get("session_duration", 0) < 10:  # Very short session
            anomaly_indicators += 1
        total_indicators += 1
        
        # Check timing signature anomalies
        timing = behavioral_features.get("timing_signature", {})
        if timing.get("typing_speed", 0) > 200:  # Unusually fast typing
            anomaly_indicators += 1
        total_indicators += 1
        
        return anomaly_indicators / total_indicators if total_indicators > 0 else 0.0
    
    async def _analyze_temporal_patterns(self, transaction_data: Dict[str, Any]) -> Optional[ForensicEvidence]:
        """Analyze temporal patterns for forensic evidence"""
        
        timestamp = transaction_data.get("timestamp", datetime.now())
        
        temporal_features = {
            "timestamp": timestamp.isoformat(),
            "hour_of_day": timestamp.hour,
            "day_of_week": timestamp.weekday(),
            "is_holiday": self._is_holiday(timestamp),
            "time_zone_analysis": self._analyze_timezone_patterns(transaction_data)
        }
        
        # Check for temporal anomalies
        anomaly_score = await self._detect_temporal_anomalies(temporal_features)
        
        if anomaly_score > 0.5:
            evidence = ForensicEvidence(
                evidence_id=str(uuid.uuid4()),
                evidence_type=EvidenceType.TEMPORAL_CORRELATION,
                source_transaction_id=transaction_data.get("id", "unknown"),
                timestamp=datetime.now(),
                data={
                    "temporal_features": temporal_features,
                    "anomaly_score": anomaly_score
                },
                confidence=anomaly_score,
                chain_of_custody=["temporal_analyzer"],
                analysis_notes=f"Temporal anomaly detected (score: {anomaly_score:.2f})"
            )
            
            return evidence
        
        return None
    
    def _is_holiday(self, timestamp: datetime) -> bool:
        """Check if timestamp falls on a holiday"""
        # Simplified holiday detection
        holidays = [
            (1, 1),   # New Year's Day
            (7, 4),   # Independence Day
            (12, 25), # Christmas
        ]
        
        return (timestamp.month, timestamp.day) in holidays
    
    def _analyze_timezone_patterns(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze timezone-related patterns"""
        return {
            "reported_timezone": transaction_data.get("timezone", "unknown"),
            "ip_timezone": transaction_data.get("ip_timezone", "unknown"),
            "timezone_mismatch": transaction_data.get("timezone") != transaction_data.get("ip_timezone")
        }
    
    async def _detect_temporal_anomalies(self, temporal_features: Dict[str, Any]) -> float:
        """Detect temporal anomalies"""
        anomaly_score = 0.0
        
        # Check for unusual hours
        hour = temporal_features.get("hour_of_day", 12)
        if hour < 6 or hour > 22:  # Late night/early morning
            anomaly_score += 0.3
        
        # Check for holiday activity
        if temporal_features.get("is_holiday", False):
            anomaly_score += 0.2
        
        # Check for timezone mismatches
        tz_analysis = temporal_features.get("time_zone_analysis", {})
        if tz_analysis.get("timezone_mismatch", False):
            anomaly_score += 0.4
        
        return min(anomaly_score, 1.0)
    
    async def perform_attack_reconstruction(self, evidence_ids: List[str]) -> Dict[str, Any]:
        """Reconstruct attack timeline and methodology"""
        
        # Gather all evidence
        evidence_pieces = [self.evidence_database[eid] for eid in evidence_ids if eid in self.evidence_database]
        
        if not evidence_pieces:
            return {"error": "No evidence found"}
        
        # Sort evidence by timestamp
        evidence_pieces.sort(key=lambda e: e.timestamp)
        
        # Reconstruct attack timeline
        timeline = []
        for evidence in evidence_pieces:
            timeline.append({
                "timestamp": evidence.timestamp.isoformat(),
                "evidence_type": evidence.evidence_type.value,
                "description": evidence.analysis_notes,
                "confidence": evidence.confidence
            })
        
        # Identify attack phases
        attack_phases = await self._identify_attack_phases(evidence_pieces)
        
        # Determine attack sophistication
        sophistication_level = await self._assess_attack_sophistication(evidence_pieces)
        
        # Generate attack vector profile
        attack_vector = AttackVector(
            vector_id=str(uuid.uuid4()),
            attack_type=self._classify_attack_type(evidence_pieces),
            entry_point=self._identify_entry_point(evidence_pieces),
            techniques_used=self._extract_techniques_used(evidence_pieces),
            tools_identified=self._identify_tools_used(evidence_pieces),
            timeline=timeline,
            success_indicators=self._identify_success_indicators(evidence_pieces),
            failure_indicators=self._identify_failure_indicators(evidence_pieces),
            sophistication_level=sophistication_level
        )
        
        self.attack_vectors[attack_vector.vector_id] = attack_vector
        
        reconstruction = {
            "attack_vector_id": attack_vector.vector_id,
            "attack_type": attack_vector.attack_type,
            "timeline": timeline,
            "attack_phases": attack_phases,
            "sophistication_level": sophistication_level,
            "techniques_used": attack_vector.techniques_used,
            "tools_identified": attack_vector.tools_identified,
            "confidence_score": np.mean([e.confidence for e in evidence_pieces])
        }
        
        logger.info(f"Attack reconstruction completed: {attack_vector.vector_id}")
        
        return reconstruction
    
    async def _identify_attack_phases(self, evidence_pieces: List[ForensicEvidence]) -> List[str]:
        """Identify phases of the attack"""
        phases = []
        
        # Analyze evidence types to infer phases
        evidence_types = [e.evidence_type for e in evidence_pieces]
        
        if EvidenceType.NETWORK_TRACE in evidence_types:
            phases.append(AttackPhase.RECONNAISSANCE.value)
        
        if EvidenceType.BEHAVIORAL_SIGNATURE in evidence_types:
            phases.append(AttackPhase.INITIAL_ACCESS.value)
        
        if EvidenceType.TRANSACTION_PATTERN in evidence_types:
            phases.append(AttackPhase.COLLECTION.value)
        
        if len(evidence_pieces) > 5:  # Multiple evidence pieces suggest persistence
            phases.append(AttackPhase.PERSISTENCE.value)
        
        return phases
    
    async def _assess_attack_sophistication(self, evidence_pieces: List[ForensicEvidence]) -> float:
        """Assess the sophistication level of the attack"""
        sophistication_indicators = 0
        total_indicators = 0
        
        # Check for advanced techniques
        for evidence in evidence_pieces:
            data = evidence.data
            
            # Advanced evasion techniques
            if evidence.evidence_type == EvidenceType.BEHAVIORAL_SIGNATURE:
                behavioral_features = data.get("behavioral_features", {})
                device_fp = behavioral_features.get("device_fingerprint", {})
                
                if device_fp.get("user_agent") == "unknown":
                    sophistication_indicators += 1
                total_indicators += 1
            
            # Complex transaction patterns
            if evidence.evidence_type == EvidenceType.TRANSACTION_PATTERN:
                pattern_features = data.get("pattern_features", {})
                
                if pattern_features.get("amount_pattern", {}).get("suspicious_amount", False):
                    sophistication_indicators += 1
                total_indicators += 1
        
        # Base sophistication on evidence diversity
        evidence_type_diversity = len(set(e.evidence_type for e in evidence_pieces))
        diversity_score = min(evidence_type_diversity / 5.0, 1.0)
        
        # Combine indicators
        if total_indicators > 0:
            indicator_score = sophistication_indicators / total_indicators
            return (indicator_score + diversity_score) / 2.0
        else:
            return diversity_score
    
    def _classify_attack_type(self, evidence_pieces: List[ForensicEvidence]) -> str:
        """Classify the type of attack based on evidence"""
        evidence_types = [e.evidence_type for e in evidence_pieces]
        
        if EvidenceType.TRANSACTION_PATTERN in evidence_types and EvidenceType.BEHAVIORAL_SIGNATURE in evidence_types:
            return "account_takeover"
        elif EvidenceType.TRANSACTION_PATTERN in evidence_types:
            return "financial_fraud"
        elif EvidenceType.BEHAVIORAL_SIGNATURE in evidence_types:
            return "identity_theft"
        else:
            return "unknown"
    
    def _identify_entry_point(self, evidence_pieces: List[ForensicEvidence]) -> str:
        """Identify the attack entry point"""
        for evidence in evidence_pieces:
            if evidence.evidence_type == EvidenceType.BEHAVIORAL_SIGNATURE:
                behavioral_data = evidence.data.get("behavioral_features", {})
                device_fp = behavioral_data.get("device_fingerprint", {})
                
                if device_fp.get("device_type") == "mobile":
                    return "mobile_application"
                elif device_fp.get("browser") != "unknown":
                    return "web_application"
        
        return "unknown"
    
    def _extract_techniques_used(self, evidence_pieces: List[ForensicEvidence]) -> List[str]:
        """Extract attack techniques used"""
        techniques = []
        
        for evidence in evidence_pieces:
            if evidence.evidence_type == EvidenceType.TRANSACTION_PATTERN:
                pattern_data = evidence.data.get("pattern_features", {})
                
                if pattern_data.get("amount_pattern", {}).get("suspicious_amount", False):
                    techniques.append("structuring")
                
                if pattern_data.get("frequency_pattern", {}).get("is_night_time", False):
                    techniques.append("off_hours_activity")
            
            elif evidence.evidence_type == EvidenceType.BEHAVIORAL_SIGNATURE:
                behavioral_data = evidence.data.get("behavioral_features", {})
                device_fp = behavioral_data.get("device_fingerprint", {})
                
                if device_fp.get("user_agent") == "unknown":
                    techniques.append("user_agent_spoofing")
        
        return list(set(techniques))  # Remove duplicates
    
    def _identify_tools_used(self, evidence_pieces: List[ForensicEvidence]) -> List[str]:
        """Identify tools used in the attack"""
        tools = []
        
        for evidence in evidence_pieces:
            if evidence.evidence_type == EvidenceType.BEHAVIORAL_SIGNATURE:
                behavioral_data = evidence.data.get("behavioral_features", {})
                interaction = behavioral_data.get("interaction_pattern", {})
                
                if interaction.get("typing_speed", 0) > 200:
                    tools.append("automated_form_filler")
                
                if interaction.get("session_duration", 0) < 10:
                    tools.append("scripted_automation")
        
        return list(set(tools))
    
    def _identify_success_indicators(self, evidence_pieces: List[ForensicEvidence]) -> List[str]:
        """Identify indicators of attack success"""
        indicators = []
        
        # High confidence evidence suggests successful techniques
        high_confidence_evidence = [e for e in evidence_pieces if e.confidence > 0.8]
        
        if len(high_confidence_evidence) > 2:
            indicators.append("multiple_successful_techniques")
        
        # Check for transaction completion
        for evidence in evidence_pieces:
            if evidence.evidence_type == EvidenceType.TRANSACTION_PATTERN:
                indicators.append("transaction_completed")
                break
        
        return indicators
    
    def _identify_failure_indicators(self, evidence_pieces: List[ForensicEvidence]) -> List[str]:
        """Identify indicators of attack failure or detection"""
        indicators = []
        
        # Low confidence evidence might indicate failed attempts
        low_confidence_evidence = [e for e in evidence_pieces if e.confidence < 0.4]
        
        if len(low_confidence_evidence) > 1:
            indicators.append("multiple_failed_attempts")
        
        return indicators
    
    def get_investigation_summary(self, investigation_id: str) -> Dict[str, Any]:
        """Get comprehensive investigation summary"""
        # This would retrieve investigation data from a database
        # For demo purposes, we'll create a summary based on current evidence
        
        total_evidence = len(self.evidence_database)
        evidence_by_type = defaultdict(int)
        
        for evidence in self.evidence_database.values():
            evidence_by_type[evidence.evidence_type.value] += 1
        
        return {
            "investigation_id": investigation_id,
            "status": "active",
            "total_evidence_pieces": total_evidence,
            "evidence_by_type": dict(evidence_by_type),
            "attack_vectors_identified": len(self.attack_vectors),
            "threat_actors_identified": len(self.threat_actors),
            "campaigns_identified": len(self.attack_campaigns),
            "confidence_distribution": self._calculate_confidence_distribution(),
            "recommendations": self._generate_investigation_recommendations()
        }
    
    def _calculate_confidence_distribution(self) -> Dict[str, int]:
        """Calculate distribution of evidence confidence levels"""
        distribution = {"low": 0, "medium": 0, "high": 0}
        
        for evidence in self.evidence_database.values():
            if evidence.confidence < 0.4:
                distribution["low"] += 1
            elif evidence.confidence < 0.7:
                distribution["medium"] += 1
            else:
                distribution["high"] += 1
        
        return distribution
    
    def _generate_investigation_recommendations(self) -> List[str]:
        """Generate recommendations based on investigation findings"""
        recommendations = []
        
        if len(self.evidence_database) > 10:
            recommendations.append("Consider correlating evidence across multiple attack vectors")
        
        if len(self.attack_vectors) > 1:
            recommendations.append("Investigate potential coordinated campaign")
        
        high_confidence_evidence = [e for e in self.evidence_database.values() if e.confidence > 0.8]
        if len(high_confidence_evidence) > 3:
            recommendations.append("High-confidence evidence suggests active threat - implement immediate countermeasures")
        
        return recommendations


class PatternAnalyzer:
    """Specialized analyzer for pattern recognition"""
    pass


class BehavioralAnalyzer:
    """Specialized analyzer for behavioral analysis"""
    pass


class NetworkAnalyzer:
    """Specialized analyzer for network traces"""
    pass


class TemporalAnalyzer:
    """Specialized analyzer for temporal correlations"""
    pass


class AttributionEngine:
    """Engine for threat attribution analysis"""
    pass


# Demo function
async def demo_forensics_lab():
    """Demonstrate the forensics laboratory system"""
    print("🔬 Financial Forensics Laboratory Demo")
    print("=" * 40)
    
    forensic_analyzer = ForensicAnalyzer()
    
    # Create sample incident data
    incident_data = {
        "incident_type": "suspected_fraud",
        "priority": "high",
        "transactions": [
            {
                "id": "tx_001",
                "user_id": "user_123",
                "amount": 9500.0,  # Suspicious structuring amount
                "timestamp": datetime.now() - timedelta(hours=2),
                "location": "Unknown Location",
                "merchant": "Cash Advance Store",
                "metadata": {
                    "user_agent": "unknown",
                    "device_type": "mobile",
                    "session_duration": 5,
                    "typing_speed": 250
                }
            },
            {
                "id": "tx_002", 
                "user_id": "user_123",
                "amount": 9800.0,
                "timestamp": datetime.now() - timedelta(hours=1),
                "location": "Different City",
                "merchant": "Pawn Shop",
                "metadata": {
                    "user_agent": "unknown",
                    "device_type": "desktop",
                    "session_duration": 3,
                    "typing_speed": 300
                }
            }
        ]
    }
    
    # Initiate investigation
    investigation_id = await forensic_analyzer.initiate_investigation(incident_data)
    print(f"Investigation initiated: {investigation_id}")
    
    # Show collected evidence
    print(f"\nEvidence collected: {len(forensic_analyzer.evidence_database)} pieces")
    
    for evidence_id, evidence in forensic_analyzer.evidence_database.items():
        print(f"\nEvidence: {evidence_id[:8]}...")
        print(f"  Type: {evidence.evidence_type.value}")
        print(f"  Confidence: {evidence.confidence:.2f}")
        print(f"  Notes: {evidence.analysis_notes}")
    
    # Perform attack reconstruction
    evidence_ids = list(forensic_analyzer.evidence_database.keys())
    reconstruction = await forensic_analyzer.perform_attack_reconstruction(evidence_ids)
    
    print(f"\nAttack Reconstruction:")
    print(f"Attack Type: {reconstruction['attack_type']}")
    print(f"Sophistication Level: {reconstruction['sophistication_level']:.2f}")
    print(f"Techniques Used: {', '.join(reconstruction['techniques_used'])}")
    print(f"Tools Identified: {', '.join(reconstruction['tools_identified'])}")
    print(f"Confidence Score: {reconstruction['confidence_score']:.2f}")
    
    # Show timeline
    print(f"\nAttack Timeline:")
    for event in reconstruction['timeline']:
        timestamp = datetime.fromisoformat(event['timestamp']).strftime('%H:%M:%S')
        print(f"  {timestamp} - {event['evidence_type']}: {event['description']}")
    
    # Get investigation summary
    summary = forensic_analyzer.get_investigation_summary(investigation_id)
    
    print(f"\nInvestigation Summary:")
    print(f"Total Evidence: {summary['total_evidence_pieces']}")
    print(f"Evidence Types: {summary['evidence_by_type']}")
    print(f"Attack Vectors: {summary['attack_vectors_identified']}")
    print(f"Confidence Distribution: {summary['confidence_distribution']}")
    
    print(f"\nRecommendations:")
    for rec in summary['recommendations']:
        print(f"  • {rec}")
    
    print("\n🔬 Forensics Laboratory Demo Complete!")


if __name__ == "__main__":
    asyncio.run(demo_forensics_lab())
