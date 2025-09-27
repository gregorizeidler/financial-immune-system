"""
Collective Intelligence System (Hive Mind)
=========================================

A distributed neural network that shares threat intelligence across multiple
financial institutions, creating a collective defense system where knowledge
from one institution strengthens the entire network.
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

from financial_immune_system import FinancialPathogen, Antibody, AnomalyType, ThreatLevel

logger = logging.getLogger(__name__)


class IntelligenceType(Enum):
    """Types of shared intelligence"""
    THREAT_PATTERN = "threat_pattern"
    ATTACK_SIGNATURE = "attack_signature"
    BEHAVIORAL_ANOMALY = "behavioral_anomaly"
    GEOGRAPHIC_THREAT = "geographic_threat"
    TEMPORAL_PATTERN = "temporal_pattern"
    ANTIBODY_EFFECTIVENESS = "antibody_effectiveness"
    CAMPAIGN_INTELLIGENCE = "campaign_intelligence"


class SharingLevel(Enum):
    """Levels of intelligence sharing"""
    PUBLIC = "public"           # Fully anonymized, shareable with all
    CONSORTIUM = "consortium"   # Shared within trusted consortium
    BILATERAL = "bilateral"     # Shared between two institutions
    INTERNAL = "internal"       # Internal use only


class TrustLevel(Enum):
    """Trust levels for intelligence sources"""
    VERIFIED = 0.95
    HIGH = 0.8
    MEDIUM = 0.6
    LOW = 0.4
    UNVERIFIED = 0.2


@dataclass
class SharedIntelligence:
    """Intelligence shared across the network"""
    intelligence_id: str
    source_institution: str
    intelligence_type: IntelligenceType
    sharing_level: SharingLevel
    trust_score: float
    timestamp: datetime
    expiration_date: datetime
    data_hash: str
    anonymized_data: Dict[str, Any]
    validation_count: int = 0
    effectiveness_reports: List[Dict[str, Any]] = None


@dataclass
class InstitutionNode:
    """A participating institution in the collective intelligence network"""
    institution_id: str
    institution_name: str
    trust_rating: TrustLevel
    join_date: datetime
    intelligence_contributed: int
    intelligence_consumed: int
    validation_accuracy: float
    reputation_score: float
    specializations: List[str]
    geographic_coverage: List[str]


@dataclass
class ConsensusResult:
    """Result of consensus validation"""
    intelligence_id: str
    consensus_score: float
    participating_nodes: int
    validation_results: Dict[str, bool]
    final_trust_score: float
    recommended_action: str


class CollectiveIntelligence:
    """
    Collective Intelligence System - Hive Mind for Financial Security
    
    Features:
    - Distributed threat intelligence sharing
    - Consensus-based validation
    - Privacy-preserving anonymization
    - Reputation-based trust scoring
    - Real-time threat propagation
    - Collaborative learning
    """
    
    def __init__(self, institution_id: str):
        self.institution_id = institution_id
        self.network_nodes: Dict[str, InstitutionNode] = {}
        self.shared_intelligence: Dict[str, SharedIntelligence] = {}
        self.local_intelligence: Dict[str, Dict[str, Any]] = {}
        
        # Network components
        self.anonymizer = DataAnonymizer()
        self.consensus_engine = ConsensusEngine()
        self.trust_manager = TrustManager()
        self.neural_correlator = NeuralCorrelator()
        
        # Network statistics
        self.network_stats = {
            "total_nodes": 0,
            "active_intelligence": 0,
            "consensus_validations": 0,
            "threat_predictions": 0,
            "collaborative_discoveries": 0
        }
        
        logger.info(f"Collective Intelligence initialized for {institution_id}")
    
    async def join_network(self, institution_info: Dict[str, Any]) -> str:
        """Join the collective intelligence network"""
        
        node = InstitutionNode(
            institution_id=self.institution_id,
            institution_name=institution_info.get("name", "Unknown"),
            trust_rating=TrustLevel.MEDIUM,  # Start with medium trust
            join_date=datetime.now(),
            intelligence_contributed=0,
            intelligence_consumed=0,
            validation_accuracy=0.5,
            reputation_score=0.5,
            specializations=institution_info.get("specializations", []),
            geographic_coverage=institution_info.get("geographic_coverage", [])
        )
        
        self.network_nodes[self.institution_id] = node
        self.network_stats["total_nodes"] = len(self.network_nodes)
        
        # Announce joining to network
        await self._broadcast_network_event("node_joined", {
            "institution_id": self.institution_id,
            "specializations": node.specializations,
            "geographic_coverage": node.geographic_coverage
        })
        
        logger.info(f"Joined collective intelligence network: {self.institution_id}")
        
        return self.institution_id
    
    async def contribute_intelligence(self, threat_data: Dict[str, Any], 
                                   intelligence_type: IntelligenceType,
                                   sharing_level: SharingLevel = SharingLevel.CONSORTIUM) -> str:
        """Contribute threat intelligence to the collective"""
        
        # Anonymize sensitive data
        anonymized_data = await self.anonymizer.anonymize_threat_data(threat_data, sharing_level)
        
        # Create intelligence record
        intelligence = SharedIntelligence(
            intelligence_id=str(uuid.uuid4()),
            source_institution=self.institution_id,
            intelligence_type=intelligence_type,
            sharing_level=sharing_level,
            trust_score=self._calculate_initial_trust_score(),
            timestamp=datetime.now(),
            expiration_date=datetime.now() + timedelta(days=30),
            data_hash=hashlib.sha256(json.dumps(anonymized_data, sort_keys=True).encode()).hexdigest(),
            anonymized_data=anonymized_data,
            effectiveness_reports=[]
        )
        
        # Store locally and share with network
        self.shared_intelligence[intelligence.intelligence_id] = intelligence
        
        # Update contribution statistics
        if self.institution_id in self.network_nodes:
            self.network_nodes[self.institution_id].intelligence_contributed += 1
        
        # Broadcast to network for consensus validation
        await self._request_consensus_validation(intelligence)
        
        # Update network statistics
        self.network_stats["active_intelligence"] += 1
        
        logger.info(f"Contributed intelligence: {intelligence.intelligence_id} ({intelligence_type.value})")
        
        return intelligence.intelligence_id
    
    def _calculate_initial_trust_score(self) -> float:
        """Calculate initial trust score for contributed intelligence"""
        if self.institution_id not in self.network_nodes:
            return 0.5
        
        node = self.network_nodes[self.institution_id]
        
        # Base trust on institution's reputation
        base_trust = node.trust_rating.value
        
        # Adjust based on validation accuracy
        accuracy_bonus = (node.validation_accuracy - 0.5) * 0.2
        
        # Adjust based on contribution history
        contribution_ratio = node.intelligence_contributed / max(node.intelligence_consumed, 1)
        contribution_bonus = min(contribution_ratio * 0.1, 0.2)
        
        return min(base_trust + accuracy_bonus + contribution_bonus, 1.0)
    
    async def _request_consensus_validation(self, intelligence: SharedIntelligence):
        """Request consensus validation from network nodes"""
        
        # Select validators based on specialization and trust
        validators = await self._select_validators(intelligence)
        
        # Request validation from selected nodes
        validation_requests = []
        for validator_id in validators:
            validation_requests.append(
                self._request_validation_from_node(validator_id, intelligence)
            )
        
        # Wait for validation responses
        validation_results = await asyncio.gather(*validation_requests, return_exceptions=True)
        
        # Process consensus
        consensus = await self.consensus_engine.process_consensus(
            intelligence.intelligence_id,
            validation_results,
            validators
        )
        
        # Update intelligence trust score based on consensus
        intelligence.trust_score = consensus.final_trust_score
        intelligence.validation_count = consensus.participating_nodes
        
        # Update network statistics
        self.network_stats["consensus_validations"] += 1
        
        logger.info(f"Consensus validation completed: {intelligence.intelligence_id} (score: {consensus.final_trust_score:.2f})")
    
    async def _select_validators(self, intelligence: SharedIntelligence) -> List[str]:
        """Select appropriate validators for intelligence"""
        validators = []
        
        # Filter nodes based on sharing level
        eligible_nodes = []
        for node_id, node in self.network_nodes.items():
            if node_id == intelligence.source_institution:
                continue  # Don't validate own intelligence
            
            # Check sharing level permissions
            if intelligence.sharing_level in [SharingLevel.PUBLIC, SharingLevel.CONSORTIUM]:
                eligible_nodes.append(node_id)
        
        # Select validators based on specialization and trust
        for node_id in eligible_nodes:
            node = self.network_nodes[node_id]
            
            # Check if node has relevant specialization
            relevant_specializations = [
                "fraud_detection", "behavioral_analysis", "pattern_recognition",
                intelligence.intelligence_type.value
            ]
            
            if any(spec in node.specializations for spec in relevant_specializations):
                validators.append(node_id)
            
            # Limit to top 5 validators
            if len(validators) >= 5:
                break
        
        # If not enough specialized validators, add high-trust general validators
        if len(validators) < 3:
            general_validators = [
                node_id for node_id, node in self.network_nodes.items()
                if node_id not in validators and node.trust_rating.value > 0.6
            ]
            validators.extend(general_validators[:3-len(validators)])
        
        return validators
    
    async def _request_validation_from_node(self, validator_id: str, 
                                          intelligence: SharedIntelligence) -> Dict[str, Any]:
        """Request validation from a specific node"""
        
        # Simulate validation request (in real implementation, this would be a network call)
        await asyncio.sleep(0.1)  # Simulate network delay
        
        validator_node = self.network_nodes.get(validator_id)
        if not validator_node:
            return {"validator_id": validator_id, "validation": False, "confidence": 0.0}
        
        # Simulate validation logic based on validator's expertise
        validation_confidence = await self._simulate_validation_logic(validator_node, intelligence)
        
        validation_result = {
            "validator_id": validator_id,
            "validation": validation_confidence > 0.6,
            "confidence": validation_confidence,
            "timestamp": datetime.now().isoformat(),
            "validation_notes": f"Validated by {validator_node.institution_name}"
        }
        
        return validation_result
    
    async def _simulate_validation_logic(self, validator: InstitutionNode, 
                                       intelligence: SharedIntelligence) -> float:
        """Simulate validation logic for demonstration"""
        
        # Base validation confidence on validator's expertise
        base_confidence = validator.validation_accuracy
        
        # Boost confidence if validator has relevant specialization
        if intelligence.intelligence_type.value in validator.specializations:
            base_confidence += 0.2
        
        # Add some randomness to simulate real-world validation
        random_factor = np.random.uniform(-0.1, 0.1)
        
        return min(max(base_confidence + random_factor, 0.0), 1.0)
    
    async def query_collective_intelligence(self, query: Dict[str, Any]) -> List[SharedIntelligence]:
        """Query the collective intelligence database"""
        
        query_type = query.get("intelligence_type")
        geographic_filter = query.get("geographic_filter", [])
        min_trust_score = query.get("min_trust_score", 0.5)
        time_window_hours = query.get("time_window_hours", 24)
        
        # Filter intelligence based on query parameters
        results = []
        cutoff_time = datetime.now() - timedelta(hours=time_window_hours)
        
        for intelligence in self.shared_intelligence.values():
            # Check expiration
            if intelligence.expiration_date < datetime.now():
                continue
            
            # Check time window
            if intelligence.timestamp < cutoff_time:
                continue
            
            # Check trust score
            if intelligence.trust_score < min_trust_score:
                continue
            
            # Check intelligence type
            if query_type and intelligence.intelligence_type.value != query_type:
                continue
            
            # Check geographic relevance
            if geographic_filter:
                intel_geo = intelligence.anonymized_data.get("geographic_indicators", [])
                if not any(geo in intel_geo for geo in geographic_filter):
                    continue
            
            results.append(intelligence)
        
        # Sort by trust score and recency
        results.sort(key=lambda x: (x.trust_score, x.timestamp), reverse=True)
        
        # Update consumption statistics
        if self.institution_id in self.network_nodes:
            self.network_nodes[self.institution_id].intelligence_consumed += len(results)
        
        logger.info(f"Intelligence query returned {len(results)} results")
        
        return results[:10]  # Return top 10 results
    
    async def correlate_threats_across_network(self, local_threat: FinancialPathogen) -> Dict[str, Any]:
        """Correlate local threat with network intelligence"""
        
        # Create threat signature for correlation
        threat_signature = await self._create_threat_signature(local_threat)
        
        # Query network for similar threats
        query = {
            "intelligence_type": "threat_pattern",
            "min_trust_score": 0.6,
            "time_window_hours": 168  # 1 week
        }
        
        similar_intelligence = await self.query_collective_intelligence(query)
        
        # Correlate with neural network
        correlations = await self.neural_correlator.find_correlations(
            threat_signature, 
            similar_intelligence
        )
        
        # Generate correlation report
        correlation_report = {
            "local_threat_id": local_threat.id,
            "network_correlations": len(correlations),
            "correlation_strength": np.mean([c["strength"] for c in correlations]) if correlations else 0.0,
            "geographic_spread": self._analyze_geographic_spread(correlations),
            "temporal_pattern": self._analyze_temporal_pattern(correlations),
            "predicted_evolution": await self._predict_threat_evolution(correlations),
            "recommended_actions": self._generate_correlation_recommendations(correlations)
        }
        
        # Update network statistics
        self.network_stats["threat_predictions"] += 1
        
        logger.info(f"Threat correlation completed: {len(correlations)} correlations found")
        
        return correlation_report
    
    async def _create_threat_signature(self, threat: FinancialPathogen) -> Dict[str, Any]:
        """Create a signature for threat correlation"""
        return {
            "anomaly_type": threat.anomaly_type.value,
            "threat_level": threat.threat_level.value,
            "confidence_score": threat.confidence_score,
            "risk_factors": threat.risk_factors,
            "pattern_hash": hashlib.sha256(str(threat.source_pattern).encode()).hexdigest()
        }
    
    def _analyze_geographic_spread(self, correlations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze geographic spread of correlated threats"""
        geographic_data = []
        
        for correlation in correlations:
            intel_data = correlation.get("intelligence", {}).get("anonymized_data", {})
            geo_indicators = intel_data.get("geographic_indicators", [])
            geographic_data.extend(geo_indicators)
        
        unique_locations = list(set(geographic_data))
        
        return {
            "affected_regions": len(unique_locations),
            "regions": unique_locations[:10],  # Top 10 regions
            "spread_velocity": len(unique_locations) / max(len(correlations), 1)
        }
    
    def _analyze_temporal_pattern(self, correlations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze temporal patterns in correlated threats"""
        timestamps = []
        
        for correlation in correlations:
            intel = correlation.get("intelligence", {})
            if intel.get("timestamp"):
                timestamps.append(intel["timestamp"])
        
        if not timestamps:
            return {"pattern": "insufficient_data"}
        
        # Sort timestamps
        timestamps.sort()
        
        # Calculate time intervals
        intervals = []
        for i in range(1, len(timestamps)):
            interval = (timestamps[i] - timestamps[i-1]).total_seconds() / 3600  # Hours
            intervals.append(interval)
        
        if intervals:
            avg_interval = np.mean(intervals)
            pattern_type = "rapid" if avg_interval < 6 else "moderate" if avg_interval < 24 else "slow"
        else:
            avg_interval = 0
            pattern_type = "single_occurrence"
        
        return {
            "pattern": pattern_type,
            "average_interval_hours": avg_interval,
            "total_duration_hours": (timestamps[-1] - timestamps[0]).total_seconds() / 3600 if len(timestamps) > 1 else 0
        }
    
    async def _predict_threat_evolution(self, correlations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Predict how the threat might evolve based on network intelligence"""
        
        if not correlations:
            return {"prediction": "insufficient_data"}
        
        # Analyze evolution patterns from correlations
        evolution_indicators = []
        
        for correlation in correlations:
            intel_data = correlation.get("intelligence", {}).get("anonymized_data", {})
            
            # Look for evolution indicators
            if intel_data.get("sophistication_increase"):
                evolution_indicators.append("increasing_sophistication")
            
            if intel_data.get("new_techniques"):
                evolution_indicators.append("technique_diversification")
            
            if intel_data.get("geographic_expansion"):
                evolution_indicators.append("geographic_expansion")
        
        # Generate prediction
        if len(evolution_indicators) > len(correlations) * 0.5:
            prediction = "rapid_evolution_likely"
            confidence = 0.8
        elif len(evolution_indicators) > 0:
            prediction = "moderate_evolution_expected"
            confidence = 0.6
        else:
            prediction = "stable_pattern"
            confidence = 0.4
        
        return {
            "prediction": prediction,
            "confidence": confidence,
            "evolution_indicators": list(set(evolution_indicators)),
            "estimated_timeline": "1-2 weeks" if prediction == "rapid_evolution_likely" else "2-4 weeks"
        }
    
    def _generate_correlation_recommendations(self, correlations: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on threat correlations"""
        recommendations = []
        
        if len(correlations) > 5:
            recommendations.append("High correlation count suggests coordinated campaign - implement enhanced monitoring")
        
        if any(c["strength"] > 0.8 for c in correlations):
            recommendations.append("Strong correlations detected - consider immediate defensive measures")
        
        # Analyze correlation patterns for specific recommendations
        geographic_spread = self._analyze_geographic_spread(correlations)
        if geographic_spread["affected_regions"] > 3:
            recommendations.append("Multi-regional threat detected - coordinate with international partners")
        
        temporal_pattern = self._analyze_temporal_pattern(correlations)
        if temporal_pattern["pattern"] == "rapid":
            recommendations.append("Rapid threat progression - accelerate response timeline")
        
        if not recommendations:
            recommendations.append("Monitor threat development and share updates with network")
        
        return recommendations
    
    async def _broadcast_network_event(self, event_type: str, event_data: Dict[str, Any]):
        """Broadcast an event to the network"""
        # In a real implementation, this would send the event to all network nodes
        logger.info(f"Broadcasting network event: {event_type}")
    
    def get_network_status(self) -> Dict[str, Any]:
        """Get comprehensive network status"""
        
        # Calculate network health metrics
        active_nodes = len([n for n in self.network_nodes.values() if n.trust_rating.value > 0.4])
        avg_trust = np.mean([n.trust_rating.value for n in self.network_nodes.values()]) if self.network_nodes else 0
        
        # Calculate intelligence freshness
        recent_intelligence = len([
            i for i in self.shared_intelligence.values()
            if (datetime.now() - i.timestamp).total_seconds() < 86400  # Last 24 hours
        ])
        
        return {
            "network_stats": self.network_stats,
            "active_nodes": active_nodes,
            "total_nodes": len(self.network_nodes),
            "average_trust_level": avg_trust,
            "recent_intelligence": recent_intelligence,
            "total_intelligence": len(self.shared_intelligence),
            "network_health": min(active_nodes / max(len(self.network_nodes), 1), 1.0),
            "intelligence_freshness": recent_intelligence / max(len(self.shared_intelligence), 1)
        }


class DataAnonymizer:
    """Anonymizes sensitive data for sharing"""
    
    async def anonymize_threat_data(self, threat_data: Dict[str, Any], 
                                  sharing_level: SharingLevel) -> Dict[str, Any]:
        """Anonymize threat data based on sharing level"""
        
        anonymized = threat_data.copy()
        
        if sharing_level == SharingLevel.PUBLIC:
            # Heavy anonymization for public sharing
            anonymized = await self._heavy_anonymization(anonymized)
        elif sharing_level == SharingLevel.CONSORTIUM:
            # Moderate anonymization for consortium
            anonymized = await self._moderate_anonymization(anonymized)
        elif sharing_level == SharingLevel.BILATERAL:
            # Light anonymization for bilateral sharing
            anonymized = await self._light_anonymization(anonymized)
        
        return anonymized
    
    async def _heavy_anonymization(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Heavy anonymization for public sharing"""
        anonymized = {}
        
        # Only share high-level patterns
        if "anomaly_type" in data:
            anonymized["anomaly_type"] = data["anomaly_type"]
        
        if "threat_level" in data:
            anonymized["threat_level"] = data["threat_level"]
        
        # Generalize amounts
        if "amount" in data:
            amount = data["amount"]
            if amount < 100:
                anonymized["amount_range"] = "small"
            elif amount < 1000:
                anonymized["amount_range"] = "medium"
            else:
                anonymized["amount_range"] = "large"
        
        # Generalize geographic data
        if "location" in data:
            anonymized["geographic_region"] = "generalized"
        
        return anonymized
    
    async def _moderate_anonymization(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Moderate anonymization for consortium sharing"""
        anonymized = data.copy()
        
        # Remove direct identifiers
        sensitive_fields = ["user_id", "account_number", "card_number", "ssn"]
        for field in sensitive_fields:
            if field in anonymized:
                anonymized[field] = hashlib.sha256(str(anonymized[field]).encode()).hexdigest()[:16]
        
        # Generalize but preserve some detail
        if "amount" in anonymized:
            amount = anonymized["amount"]
            # Round to nearest 100
            anonymized["amount"] = round(amount / 100) * 100
        
        return anonymized
    
    async def _light_anonymization(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Light anonymization for bilateral sharing"""
        anonymized = data.copy()
        
        # Only hash direct personal identifiers
        if "user_id" in anonymized:
            anonymized["user_id"] = hashlib.sha256(str(anonymized["user_id"]).encode()).hexdigest()[:16]
        
        return anonymized


class ConsensusEngine:
    """Processes consensus validation from network nodes"""
    
    async def process_consensus(self, intelligence_id: str, validation_results: List[Dict[str, Any]], 
                              validators: List[str]) -> ConsensusResult:
        """Process consensus validation results"""
        
        valid_results = [r for r in validation_results if isinstance(r, dict) and "validation" in r]
        
        if not valid_results:
            return ConsensusResult(
                intelligence_id=intelligence_id,
                consensus_score=0.0,
                participating_nodes=0,
                validation_results={},
                final_trust_score=0.2,
                recommended_action="reject"
            )
        
        # Calculate consensus metrics
        positive_validations = sum(1 for r in valid_results if r["validation"])
        total_validations = len(valid_results)
        consensus_score = positive_validations / total_validations
        
        # Weight by validator confidence
        weighted_score = sum(r["confidence"] for r in valid_results if r["validation"]) / total_validations
        
        # Final trust score combines consensus and confidence
        final_trust_score = (consensus_score * 0.6) + (weighted_score * 0.4)
        
        # Determine recommended action
        if final_trust_score > 0.8:
            recommended_action = "accept_high_confidence"
        elif final_trust_score > 0.6:
            recommended_action = "accept_medium_confidence"
        elif final_trust_score > 0.4:
            recommended_action = "accept_low_confidence"
        else:
            recommended_action = "reject"
        
        validation_dict = {r["validator_id"]: r["validation"] for r in valid_results}
        
        return ConsensusResult(
            intelligence_id=intelligence_id,
            consensus_score=consensus_score,
            participating_nodes=len(valid_results),
            validation_results=validation_dict,
            final_trust_score=final_trust_score,
            recommended_action=recommended_action
        )


class TrustManager:
    """Manages trust scores and reputation"""
    pass


class NeuralCorrelator:
    """Neural network for finding threat correlations"""
    
    async def find_correlations(self, threat_signature: Dict[str, Any], 
                              intelligence_list: List[SharedIntelligence]) -> List[Dict[str, Any]]:
        """Find correlations between threat signature and network intelligence"""
        
        correlations = []
        
        for intelligence in intelligence_list:
            intel_data = intelligence.anonymized_data
            
            # Calculate correlation strength
            correlation_strength = await self._calculate_correlation_strength(threat_signature, intel_data)
            
            if correlation_strength > 0.5:  # Significant correlation
                correlations.append({
                    "intelligence": intelligence,
                    "strength": correlation_strength,
                    "correlation_factors": self._identify_correlation_factors(threat_signature, intel_data)
                })
        
        # Sort by correlation strength
        correlations.sort(key=lambda x: x["strength"], reverse=True)
        
        return correlations
    
    async def _calculate_correlation_strength(self, signature: Dict[str, Any], 
                                           intel_data: Dict[str, Any]) -> float:
        """Calculate correlation strength between signature and intelligence data"""
        
        correlation_factors = []
        
        # Check anomaly type match
        if signature.get("anomaly_type") == intel_data.get("anomaly_type"):
            correlation_factors.append(0.4)
        
        # Check threat level similarity
        sig_level = signature.get("threat_level", 0)
        intel_level = intel_data.get("threat_level", 0)
        if abs(sig_level - intel_level) <= 1:
            correlation_factors.append(0.3)
        
        # Check risk factor overlap
        sig_factors = set(signature.get("risk_factors", []))
        intel_factors = set(intel_data.get("risk_factors", []))
        factor_overlap = len(sig_factors & intel_factors) / max(len(sig_factors | intel_factors), 1)
        correlation_factors.append(factor_overlap * 0.3)
        
        return sum(correlation_factors)
    
    def _identify_correlation_factors(self, signature: Dict[str, Any], 
                                    intel_data: Dict[str, Any]) -> List[str]:
        """Identify specific factors that correlate"""
        factors = []
        
        if signature.get("anomaly_type") == intel_data.get("anomaly_type"):
            factors.append("matching_anomaly_type")
        
        if abs(signature.get("threat_level", 0) - intel_data.get("threat_level", 0)) <= 1:
            factors.append("similar_threat_level")
        
        sig_factors = set(signature.get("risk_factors", []))
        intel_factors = set(intel_data.get("risk_factors", []))
        if sig_factors & intel_factors:
            factors.append("overlapping_risk_factors")
        
        return factors


# Demo function
async def demo_collective_intelligence():
    """Demonstrate the collective intelligence system"""
    print("🧠 Collective Intelligence (Hive Mind) Demo")
    print("=" * 50)
    
    # Create multiple institutions
    institutions = [
        {"id": "bank_alpha", "name": "Alpha Bank", "specializations": ["fraud_detection", "behavioral_analysis"]},
        {"id": "fintech_beta", "name": "Beta FinTech", "specializations": ["pattern_recognition", "velocity_analysis"]},
        {"id": "credit_gamma", "name": "Gamma Credit", "specializations": ["identity_verification", "risk_assessment"]}
    ]
    
    # Initialize collective intelligence for each institution
    hive_minds = {}
    for inst in institutions:
        hive_mind = CollectiveIntelligence(inst["id"])
        await hive_mind.join_network(inst)
        hive_minds[inst["id"]] = hive_mind
        
        # Simulate other institutions in the network
        for other_inst in institutions:
            if other_inst["id"] != inst["id"]:
                other_node = InstitutionNode(
                    institution_id=other_inst["id"],
                    institution_name=other_inst["name"],
                    trust_rating=TrustLevel.HIGH,
                    join_date=datetime.now(),
                    intelligence_contributed=np.random.randint(10, 50),
                    intelligence_consumed=np.random.randint(5, 30),
                    validation_accuracy=np.random.uniform(0.7, 0.9),
                    reputation_score=np.random.uniform(0.6, 0.9),
                    specializations=other_inst["specializations"],
                    geographic_coverage=["US", "EU"]
                )
                hive_mind.network_nodes[other_inst["id"]] = other_node
    
    print(f"Network established with {len(institutions)} institutions")
    
    # Alpha Bank contributes threat intelligence
    alpha_hive = hive_minds["bank_alpha"]
    
    threat_data = {
        "anomaly_type": "velocity_anomaly",
        "threat_level": 3,
        "confidence_score": 0.85,
        "risk_factors": ["rapid_transactions", "multiple_cards", "geographic_spread"],
        "geographic_indicators": ["US_East", "US_West"],
        "amount_range": "medium",
        "temporal_pattern": "night_time_activity"
    }
    
    print(f"\nAlpha Bank contributing threat intelligence...")
    intel_id = await alpha_hive.contribute_intelligence(
        threat_data, 
        IntelligenceType.THREAT_PATTERN,
        SharingLevel.CONSORTIUM
    )
    
    print(f"Intelligence contributed: {intel_id}")
    
    # Beta FinTech queries the collective intelligence
    beta_hive = hive_minds["fintech_beta"]
    
    query = {
        "intelligence_type": "threat_pattern",
        "min_trust_score": 0.6,
        "time_window_hours": 24
    }
    
    print(f"\nBeta FinTech querying collective intelligence...")
    results = await beta_hive.query_collective_intelligence(query)
    
    print(f"Query returned {len(results)} intelligence items")
    for result in results:
        print(f"  - {result.intelligence_type.value} (trust: {result.trust_score:.2f})")
    
    # Simulate local threat for correlation
    from financial_immune_system import FinancialPathogen, AnomalyType, ThreatLevel
    
    local_threat = FinancialPathogen(
        id="local_threat_001",
        anomaly_type=AnomalyType.VELOCITY_ANOMALY,
        threat_level=ThreatLevel.HIGH,
        confidence_score=0.8,
        affected_transactions=["tx1", "tx2", "tx3"],
        detection_timestamp=datetime.now(),
        source_pattern={"velocity": "high", "pattern": "burst"},
        risk_factors=["rapid_transactions", "multiple_cards"]
    )
    
    print(f"\nCorrelating local threat with network intelligence...")
    correlation_report = await beta_hive.correlate_threats_across_network(local_threat)
    
    print(f"Correlation Report:")
    print(f"  Network Correlations: {correlation_report['network_correlations']}")
    print(f"  Correlation Strength: {correlation_report['correlation_strength']:.2f}")
    print(f"  Geographic Spread: {correlation_report['geographic_spread']['affected_regions']} regions")
    print(f"  Temporal Pattern: {correlation_report['temporal_pattern']['pattern']}")
    print(f"  Predicted Evolution: {correlation_report['predicted_evolution']['prediction']}")
    
    print(f"\nRecommended Actions:")
    for action in correlation_report['recommended_actions']:
        print(f"  • {action}")
    
    # Show network status
    network_status = alpha_hive.get_network_status()
    
    print(f"\nNetwork Status:")
    print(f"  Active Nodes: {network_status['active_nodes']}/{network_status['total_nodes']}")
    print(f"  Network Health: {network_status['network_health']:.1%}")
    print(f"  Average Trust Level: {network_status['average_trust_level']:.2f}")
    print(f"  Total Intelligence: {network_status['total_intelligence']}")
    print(f"  Recent Intelligence: {network_status['recent_intelligence']}")
    print(f"  Intelligence Freshness: {network_status['intelligence_freshness']:.1%}")
    
    print("\n🧠 Collective Intelligence Demo Complete!")


if __name__ == "__main__":
    asyncio.run(demo_collective_intelligence())
