"""
Financial Immune System
=======================

A sophisticated fraud detection system inspired by the human immune system.
Detects financial anomalies like "viruses," generates "antibodies" (new rules),
and distributes immunity across the entire financial network.

Key Components:
- Pathogen Detection (Anomaly Detection Engine)
- Antibody Generation (Rule Creation System)
- Immune Memory (Learning & Adaptation)
- Immunity Distribution (Network-wide Protection)
- System Health Monitoring
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np
from collections import defaultdict, deque
import hashlib
import uuid


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ThreatLevel(Enum):
    """Threat severity levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class AnomalyType(Enum):
    """Types of financial anomalies (viruses)"""
    UNUSUAL_TRANSACTION_PATTERN = "unusual_transaction_pattern"
    VELOCITY_ANOMALY = "velocity_anomaly"
    GEOGRAPHIC_ANOMALY = "geographic_anomaly"
    BEHAVIORAL_DEVIATION = "behavioral_deviation"
    ACCOUNT_TAKEOVER = "account_takeover"
    MONEY_LAUNDERING = "money_laundering"
    SYNTHETIC_IDENTITY = "synthetic_identity"
    CARD_TESTING = "card_testing"


@dataclass
class Transaction:
    """Represents a financial transaction"""
    id: str
    user_id: str
    amount: float
    timestamp: datetime
    location: str
    merchant: str
    transaction_type: str = "purchase"
    card_number: str = ""
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}




@dataclass
class FinancialPathogen:
    """Represents a detected financial anomaly (virus)"""
    id: str
    anomaly_type: AnomalyType
    threat_level: ThreatLevel
    confidence_score: float
    affected_transactions: List[str]
    detection_timestamp: datetime
    source_pattern: Dict[str, Any]
    risk_factors: List[str]


@dataclass
class Antibody:
    """Security rule generated to combat specific threats"""
    id: str
    name: str
    pathogen_signature: str
    rule_logic: Dict[str, Any]
    effectiveness_score: float
    creation_timestamp: datetime
    last_updated: datetime
    activation_count: int
    success_rate: float


@dataclass
class ImmuneMemory:
    """Long-term memory of threats and responses"""
    pathogen_id: str
    antibody_id: str
    encounter_count: int
    last_encounter: datetime
    adaptation_history: List[Dict[str, Any]]
    immunity_strength: float


class WhiteBloodCell:
    """Anomaly detection engine - the system's white blood cells"""
    
    def __init__(self):
        self.detection_algorithms = {
            AnomalyType.UNUSUAL_TRANSACTION_PATTERN: self._detect_pattern_anomaly,
            AnomalyType.VELOCITY_ANOMALY: self._detect_velocity_anomaly,
            AnomalyType.GEOGRAPHIC_ANOMALY: self._detect_geographic_anomaly,
            AnomalyType.BEHAVIORAL_DEVIATION: self._detect_behavioral_anomaly,
            AnomalyType.ACCOUNT_TAKEOVER: self._detect_account_takeover,
            AnomalyType.MONEY_LAUNDERING: self._detect_money_laundering,
            AnomalyType.SYNTHETIC_IDENTITY: self._detect_synthetic_identity,
            AnomalyType.CARD_TESTING: self._detect_card_testing,
        }
        self.user_profiles = defaultdict(dict)
        self.transaction_history = defaultdict(deque)
    
    async def scan_transaction(self, transaction: Transaction) -> List[FinancialPathogen]:
        """Scan a transaction for potential threats"""
        detected_pathogens = []
        
        # Update user profile and history
        self._update_user_profile(transaction)
        
        # Run all detection algorithms
        for anomaly_type, detector in self.detection_algorithms.items():
            try:
                pathogen = await detector(transaction)
                if pathogen:
                    detected_pathogens.append(pathogen)
                    logger.info(f"Pathogen detected: {anomaly_type.value} - Threat Level: {pathogen.threat_level.name}")
            except Exception as e:
                logger.error(f"Error in {anomaly_type.value} detection: {e}")
        
        return detected_pathogens
    
    def _update_user_profile(self, transaction: Transaction):
        """Update user behavioral profile"""
        user_id = transaction.user_id
        profile = self.user_profiles[user_id]
        history = self.transaction_history[user_id]
        
        # Add transaction to history (keep last 100)
        history.append(transaction)
        if len(history) > 100:
            history.popleft()
        
        # Update profile statistics
        amounts = [t.amount for t in history]
        profile.update({
            'avg_amount': np.mean(amounts) if amounts else 0,
            'std_amount': np.std(amounts) if len(amounts) > 1 else 0,
            'transaction_count': len(history),
            'common_locations': self._get_common_locations(history),
            'common_merchants': self._get_common_merchants(history),
            'last_transaction_time': transaction.timestamp,
        })
    
    def _get_common_locations(self, history: deque) -> List[str]:
        """Get most common transaction locations"""
        locations = defaultdict(int)
        for t in history:
            locations[t.location] += 1
        return sorted(locations.keys(), key=locations.get, reverse=True)[:5]
    
    def _get_common_merchants(self, history: deque) -> List[str]:
        """Get most common merchants"""
        merchants = defaultdict(int)
        for t in history:
            merchants[t.merchant] += 1
        return sorted(merchants.keys(), key=merchants.get, reverse=True)[:5]
    
    async def _detect_pattern_anomaly(self, transaction: Transaction) -> Optional[FinancialPathogen]:
        """Detect unusual transaction patterns"""
        user_profile = self.user_profiles[transaction.user_id]
        
        if not user_profile.get('avg_amount'):
            return None
        
        # Check for amount anomaly
        z_score = abs(transaction.amount - user_profile['avg_amount']) / (user_profile['std_amount'] + 1e-6)
        
        if z_score > 3:  # 3 standard deviations
            confidence = min(z_score / 10, 0.95)
            threat_level = ThreatLevel.HIGH if z_score > 5 else ThreatLevel.MEDIUM
            
            return FinancialPathogen(
                id=str(uuid.uuid4()),
                anomaly_type=AnomalyType.UNUSUAL_TRANSACTION_PATTERN,
                threat_level=threat_level,
                confidence_score=confidence,
                affected_transactions=[transaction.id],
                detection_timestamp=datetime.now(),
                source_pattern={'z_score': z_score, 'amount': transaction.amount, 'avg_amount': user_profile['avg_amount']},
                risk_factors=[f"Amount {z_score:.2f} standard deviations from normal"]
            )
        
        return None
    
    async def _detect_velocity_anomaly(self, transaction: Transaction) -> Optional[FinancialPathogen]:
        """Detect transaction velocity anomalies"""
        history = self.transaction_history[transaction.user_id]
        
        if len(history) < 2:
            return None
        
        # Check transactions in last hour
        recent_transactions = [
            t for t in history 
            if (transaction.timestamp - t.timestamp).total_seconds() < 3600
        ]
        
        if len(recent_transactions) > 10:  # More than 10 transactions per hour
            confidence = min(len(recent_transactions) / 20, 0.95)
            threat_level = ThreatLevel.CRITICAL if len(recent_transactions) > 20 else ThreatLevel.HIGH
            
            return FinancialPathogen(
                id=str(uuid.uuid4()),
                anomaly_type=AnomalyType.VELOCITY_ANOMALY,
                threat_level=threat_level,
                confidence_score=confidence,
                affected_transactions=[t.id for t in recent_transactions],
                detection_timestamp=datetime.now(),
                source_pattern={'transaction_count': len(recent_transactions), 'time_window': '1_hour'},
                risk_factors=[f"{len(recent_transactions)} transactions in 1 hour"]
            )
        
        return None
    
    async def _detect_geographic_anomaly(self, transaction: Transaction) -> Optional[FinancialPathogen]:
        """Detect geographic anomalies"""
        user_profile = self.user_profiles[transaction.user_id]
        common_locations = user_profile.get('common_locations', [])
        
        if common_locations and transaction.location not in common_locations:
            # Check if it's a completely new location
            history = self.transaction_history[transaction.user_id]
            all_locations = {t.location for t in history}
            
            if transaction.location not in all_locations:
                confidence = 0.8
                threat_level = ThreatLevel.MEDIUM
                
                return FinancialPathogen(
                    id=str(uuid.uuid4()),
                    anomaly_type=AnomalyType.GEOGRAPHIC_ANOMALY,
                    threat_level=threat_level,
                    confidence_score=confidence,
                    affected_transactions=[transaction.id],
                    detection_timestamp=datetime.now(),
                    source_pattern={'new_location': transaction.location, 'common_locations': common_locations},
                    risk_factors=[f"Transaction from new location: {transaction.location}"]
                )
        
        return None
    
    async def _detect_behavioral_anomaly(self, transaction: Transaction) -> Optional[FinancialPathogen]:
        """Detect behavioral deviations"""
        user_profile = self.user_profiles[transaction.user_id]
        common_merchants = user_profile.get('common_merchants', [])
        
        # Check for unusual merchant
        if common_merchants and transaction.merchant not in common_merchants:
            history = self.transaction_history[transaction.user_id]
            all_merchants = {t.merchant for t in history}
            
            if transaction.merchant not in all_merchants and transaction.amount > user_profile.get('avg_amount', 0) * 2:
                confidence = 0.7
                threat_level = ThreatLevel.MEDIUM
                
                return FinancialPathogen(
                    id=str(uuid.uuid4()),
                    anomaly_type=AnomalyType.BEHAVIORAL_DEVIATION,
                    threat_level=threat_level,
                    confidence_score=confidence,
                    affected_transactions=[transaction.id],
                    detection_timestamp=datetime.now(),
                    source_pattern={'new_merchant': transaction.merchant, 'high_amount': transaction.amount},
                    risk_factors=[f"High amount transaction at new merchant: {transaction.merchant}"]
                )
        
        return None
    
    async def _detect_account_takeover(self, transaction: Transaction) -> Optional[FinancialPathogen]:
        """Detect potential account takeover"""
        history = self.transaction_history[transaction.user_id]
        
        if len(history) < 5:
            return None
        
        # Check for rapid succession of transactions with different patterns
        recent = list(history)[-5:]
        locations = {t.location for t in recent}
        merchants = {t.merchant for t in recent}
        
        if len(locations) > 3 and len(merchants) > 3:
            confidence = 0.85
            threat_level = ThreatLevel.HIGH
            
            return FinancialPathogen(
                id=str(uuid.uuid4()),
                anomaly_type=AnomalyType.ACCOUNT_TAKEOVER,
                threat_level=threat_level,
                confidence_score=confidence,
                affected_transactions=[t.id for t in recent],
                detection_timestamp=datetime.now(),
                source_pattern={'diverse_locations': list(locations), 'diverse_merchants': list(merchants)},
                risk_factors=["Multiple locations and merchants in short timeframe"]
            )
        
        return None
    
    async def _detect_money_laundering(self, transaction: Transaction) -> Optional[FinancialPathogen]:
        """Detect potential money laundering patterns"""
        history = self.transaction_history[transaction.user_id]
        
        # Look for structuring (amounts just under reporting thresholds)
        if 9000 <= transaction.amount <= 9999:
            confidence = 0.6
            threat_level = ThreatLevel.MEDIUM
            
            return FinancialPathogen(
                id=str(uuid.uuid4()),
                anomaly_type=AnomalyType.MONEY_LAUNDERING,
                threat_level=threat_level,
                confidence_score=confidence,
                affected_transactions=[transaction.id],
                detection_timestamp=datetime.now(),
                source_pattern={'structuring_amount': transaction.amount},
                risk_factors=["Amount suggests potential structuring"]
            )
        
        return None
    
    async def _detect_synthetic_identity(self, transaction: Transaction) -> Optional[FinancialPathogen]:
        """Detect synthetic identity fraud"""
        # Simplified detection based on new user with high-value transactions
        user_profile = self.user_profiles[transaction.user_id]
        
        if user_profile.get('transaction_count', 0) < 3 and transaction.amount > 5000:
            confidence = 0.7
            threat_level = ThreatLevel.HIGH
            
            return FinancialPathogen(
                id=str(uuid.uuid4()),
                anomaly_type=AnomalyType.SYNTHETIC_IDENTITY,
                threat_level=threat_level,
                confidence_score=confidence,
                affected_transactions=[transaction.id],
                detection_timestamp=datetime.now(),
                source_pattern={'new_user_high_amount': transaction.amount, 'transaction_count': user_profile.get('transaction_count', 0)},
                risk_factors=["New user with high-value transaction"]
            )
        
        return None
    
    async def _detect_card_testing(self, transaction: Transaction) -> Optional[FinancialPathogen]:
        """Detect card testing attacks"""
        history = self.transaction_history[transaction.user_id]
        
        # Look for multiple small transactions in short time
        recent_small = [
            t for t in history 
            if (datetime.now() - t.timestamp).total_seconds() < 600 and t.amount < 10
        ]
        
        if len(recent_small) > 5:
            confidence = 0.9
            threat_level = ThreatLevel.HIGH
            
            return FinancialPathogen(
                id=str(uuid.uuid4()),
                anomaly_type=AnomalyType.CARD_TESTING,
                threat_level=threat_level,
                confidence_score=confidence,
                affected_transactions=[t.id for t in recent_small],
                detection_timestamp=datetime.now(),
                source_pattern={'small_transaction_count': len(recent_small)},
                risk_factors=["Multiple small transactions in short timeframe"]
            )
        
        return None


class AntibodyFactory:
    """Generates antibodies (security rules) to combat detected threats"""
    
    def __init__(self):
        self.antibody_templates = {
            AnomalyType.UNUSUAL_TRANSACTION_PATTERN: self._create_pattern_antibody,
            AnomalyType.VELOCITY_ANOMALY: self._create_velocity_antibody,
            AnomalyType.GEOGRAPHIC_ANOMALY: self._create_geographic_antibody,
            AnomalyType.BEHAVIORAL_DEVIATION: self._create_behavioral_antibody,
            AnomalyType.ACCOUNT_TAKEOVER: self._create_takeover_antibody,
            AnomalyType.MONEY_LAUNDERING: self._create_laundering_antibody,
            AnomalyType.SYNTHETIC_IDENTITY: self._create_synthetic_antibody,
            AnomalyType.CARD_TESTING: self._create_testing_antibody,
        }
    
    async def generate_antibody(self, pathogen: FinancialPathogen) -> Antibody:
        """Generate an antibody for a specific pathogen"""
        generator = self.antibody_templates.get(pathogen.anomaly_type)
        if not generator:
            raise ValueError(f"No antibody template for {pathogen.anomaly_type}")
        
        antibody = await generator(pathogen)
        logger.info(f"Generated antibody: {antibody.name} for pathogen {pathogen.id}")
        return antibody
    
    async def _create_pattern_antibody(self, pathogen: FinancialPathogen) -> Antibody:
        """Create antibody for pattern anomalies"""
        rule_logic = {
            'type': 'amount_threshold',
            'max_deviation': 3.0,  # Standard deviations
            'action': 'flag_for_review',
            'confidence_threshold': 0.7
        }
        
        return Antibody(
            id=str(uuid.uuid4()),
            name=f"Pattern Guard - {pathogen.id[:8]}",
            pathogen_signature=self._generate_signature(pathogen),
            rule_logic=rule_logic,
            effectiveness_score=0.8,
            creation_timestamp=datetime.now(),
            last_updated=datetime.now(),
            activation_count=0,
            success_rate=0.0
        )
    
    async def _create_velocity_antibody(self, pathogen: FinancialPathogen) -> Antibody:
        """Create antibody for velocity anomalies"""
        rule_logic = {
            'type': 'velocity_limit',
            'max_transactions_per_hour': 8,
            'action': 'temporary_block',
            'cooldown_minutes': 60
        }
        
        return Antibody(
            id=str(uuid.uuid4()),
            name=f"Velocity Limiter - {pathogen.id[:8]}",
            pathogen_signature=self._generate_signature(pathogen),
            rule_logic=rule_logic,
            effectiveness_score=0.9,
            creation_timestamp=datetime.now(),
            last_updated=datetime.now(),
            activation_count=0,
            success_rate=0.0
        )
    
    async def _create_geographic_antibody(self, pathogen: FinancialPathogen) -> Antibody:
        """Create antibody for geographic anomalies"""
        rule_logic = {
            'type': 'location_verification',
            'require_additional_auth': True,
            'trusted_locations_only': False,
            'action': 'request_verification'
        }
        
        return Antibody(
            id=str(uuid.uuid4()),
            name=f"Geo Guard - {pathogen.id[:8]}",
            pathogen_signature=self._generate_signature(pathogen),
            rule_logic=rule_logic,
            effectiveness_score=0.75,
            creation_timestamp=datetime.now(),
            last_updated=datetime.now(),
            activation_count=0,
            success_rate=0.0
        )
    
    async def _create_behavioral_antibody(self, pathogen: FinancialPathogen) -> Antibody:
        """Create antibody for behavioral anomalies"""
        rule_logic = {
            'type': 'behavioral_check',
            'new_merchant_threshold': 1000,  # Amount threshold for new merchants
            'action': 'step_up_authentication',
            'verification_method': 'sms_otp'
        }
        
        return Antibody(
            id=str(uuid.uuid4()),
            name=f"Behavior Monitor - {pathogen.id[:8]}",
            pathogen_signature=self._generate_signature(pathogen),
            rule_logic=rule_logic,
            effectiveness_score=0.7,
            creation_timestamp=datetime.now(),
            last_updated=datetime.now(),
            activation_count=0,
            success_rate=0.0
        )
    
    async def _create_takeover_antibody(self, pathogen: FinancialPathogen) -> Antibody:
        """Create antibody for account takeover"""
        rule_logic = {
            'type': 'account_protection',
            'max_location_diversity': 2,
            'max_merchant_diversity': 3,
            'action': 'account_freeze',
            'require_identity_verification': True
        }
        
        return Antibody(
            id=str(uuid.uuid4()),
            name=f"Account Shield - {pathogen.id[:8]}",
            pathogen_signature=self._generate_signature(pathogen),
            rule_logic=rule_logic,
            effectiveness_score=0.95,
            creation_timestamp=datetime.now(),
            last_updated=datetime.now(),
            activation_count=0,
            success_rate=0.0
        )
    
    async def _create_laundering_antibody(self, pathogen: FinancialPathogen) -> Antibody:
        """Create antibody for money laundering"""
        rule_logic = {
            'type': 'aml_monitoring',
            'structuring_threshold': 9500,
            'action': 'regulatory_report',
            'enhanced_monitoring': True
        }
        
        return Antibody(
            id=str(uuid.uuid4()),
            name=f"AML Guard - {pathogen.id[:8]}",
            pathogen_signature=self._generate_signature(pathogen),
            rule_logic=rule_logic,
            effectiveness_score=0.85,
            creation_timestamp=datetime.now(),
            last_updated=datetime.now(),
            activation_count=0,
            success_rate=0.0
        )
    
    async def _create_synthetic_antibody(self, pathogen: FinancialPathogen) -> Antibody:
        """Create antibody for synthetic identity"""
        rule_logic = {
            'type': 'identity_verification',
            'new_user_threshold': 2000,
            'action': 'enhanced_kyc',
            'verification_documents': ['id', 'address_proof', 'income_verification']
        }
        
        return Antibody(
            id=str(uuid.uuid4()),
            name=f"Identity Verifier - {pathogen.id[:8]}",
            pathogen_signature=self._generate_signature(pathogen),
            rule_logic=rule_logic,
            effectiveness_score=0.9,
            creation_timestamp=datetime.now(),
            last_updated=datetime.now(),
            activation_count=0,
            success_rate=0.0
        )
    
    async def _create_testing_antibody(self, pathogen: FinancialPathogen) -> Antibody:
        """Create antibody for card testing"""
        rule_logic = {
            'type': 'card_protection',
            'max_small_transactions': 3,
            'small_amount_threshold': 10,
            'action': 'card_temporary_block',
            'block_duration_minutes': 30
        }
        
        return Antibody(
            id=str(uuid.uuid4()),
            name=f"Card Protector - {pathogen.id[:8]}",
            pathogen_signature=self._generate_signature(pathogen),
            rule_logic=rule_logic,
            effectiveness_score=0.95,
            creation_timestamp=datetime.now(),
            last_updated=datetime.now(),
            activation_count=0,
            success_rate=0.0
        )
    
    def _generate_signature(self, pathogen: FinancialPathogen) -> str:
        """Generate a unique signature for the pathogen"""
        signature_data = {
            'anomaly_type': pathogen.anomaly_type.value,
            'threat_level': pathogen.threat_level.value,
            'source_pattern': pathogen.source_pattern
        }
        signature_str = json.dumps(signature_data, sort_keys=True)
        return hashlib.sha256(signature_str.encode()).hexdigest()


class ImmuneMemorySystem:
    """Manages long-term memory of threats and adaptive responses"""
    
    def __init__(self):
        self.memory_store: Dict[str, ImmuneMemory] = {}
        self.pathogen_history: Dict[str, List[FinancialPathogen]] = defaultdict(list)
        self.antibody_performance: Dict[str, Dict[str, float]] = defaultdict(dict)
    
    async def store_encounter(self, pathogen: FinancialPathogen, antibody: Antibody, outcome: bool):
        """Store an encounter between pathogen and antibody"""
        memory_key = f"{pathogen.anomaly_type.value}_{antibody.pathogen_signature}"
        
        if memory_key in self.memory_store:
            memory = self.memory_store[memory_key]
            memory.encounter_count += 1
            memory.last_encounter = datetime.now()
        else:
            memory = ImmuneMemory(
                pathogen_id=pathogen.id,
                antibody_id=antibody.id,
                encounter_count=1,
                last_encounter=datetime.now(),
                adaptation_history=[],
                immunity_strength=0.5
            )
            self.memory_store[memory_key] = memory
        
        # Update immunity strength based on outcome
        if outcome:
            memory.immunity_strength = min(memory.immunity_strength + 0.1, 1.0)
        else:
            memory.immunity_strength = max(memory.immunity_strength - 0.05, 0.1)
        
        # Store adaptation history
        memory.adaptation_history.append({
            'timestamp': datetime.now().isoformat(),
            'outcome': outcome,
            'immunity_strength': memory.immunity_strength
        })
        
        # Keep only last 100 adaptations
        if len(memory.adaptation_history) > 100:
            memory.adaptation_history = memory.adaptation_history[-100:]
        
        logger.info(f"Stored immune memory: {memory_key} - Strength: {memory.immunity_strength:.2f}")
    
    async def get_immunity_strength(self, pathogen_signature: str, anomaly_type: AnomalyType) -> float:
        """Get current immunity strength for a pathogen type"""
        memory_key = f"{anomaly_type.value}_{pathogen_signature}"
        memory = self.memory_store.get(memory_key)
        return memory.immunity_strength if memory else 0.0
    
    async def adapt_antibody(self, antibody: Antibody, performance_data: Dict[str, float]) -> Antibody:
        """Adapt an antibody based on performance data"""
        # Update effectiveness score based on recent performance
        success_rate = performance_data.get('success_rate', 0.5)
        false_positive_rate = performance_data.get('false_positive_rate', 0.1)
        
        # Calculate new effectiveness score
        new_effectiveness = (success_rate * 0.8) + ((1 - false_positive_rate) * 0.2)
        antibody.effectiveness_score = (antibody.effectiveness_score * 0.7) + (new_effectiveness * 0.3)
        
        # Adapt rule logic based on performance
        if false_positive_rate > 0.2:  # Too many false positives
            await self._reduce_sensitivity(antibody)
        elif success_rate < 0.6:  # Not catching enough threats
            await self._increase_sensitivity(antibody)
        
        antibody.last_updated = datetime.now()
        logger.info(f"Adapted antibody {antibody.name} - New effectiveness: {antibody.effectiveness_score:.2f}")
        
        return antibody
    
    async def _reduce_sensitivity(self, antibody: Antibody):
        """Reduce antibody sensitivity to reduce false positives"""
        rule_logic = antibody.rule_logic
        
        if rule_logic.get('type') == 'amount_threshold':
            rule_logic['max_deviation'] = min(rule_logic.get('max_deviation', 3) + 0.5, 5.0)
        elif rule_logic.get('type') == 'velocity_limit':
            rule_logic['max_transactions_per_hour'] = min(rule_logic.get('max_transactions_per_hour', 10) + 2, 20)
        elif rule_logic.get('type') == 'behavioral_check':
            rule_logic['new_merchant_threshold'] = rule_logic.get('new_merchant_threshold', 1000) * 1.2
    
    async def _increase_sensitivity(self, antibody: Antibody):
        """Increase antibody sensitivity to catch more threats"""
        rule_logic = antibody.rule_logic
        
        if rule_logic.get('type') == 'amount_threshold':
            rule_logic['max_deviation'] = max(rule_logic.get('max_deviation', 3) - 0.2, 1.5)
        elif rule_logic.get('type') == 'velocity_limit':
            rule_logic['max_transactions_per_hour'] = max(rule_logic.get('max_transactions_per_hour', 10) - 1, 3)
        elif rule_logic.get('type') == 'behavioral_check':
            rule_logic['new_merchant_threshold'] = rule_logic.get('new_merchant_threshold', 1000) * 0.8


class ImmunityDistributionNetwork:
    """Distributes immunity (antibodies) across the entire system network"""
    
    def __init__(self):
        self.network_nodes: Dict[str, Dict[str, Any]] = {}
        self.antibody_registry: Dict[str, Antibody] = {}
        self.distribution_log: List[Dict[str, Any]] = []
    
    async def register_node(self, node_id: str, node_info: Dict[str, Any]):
        """Register a new node in the network"""
        self.network_nodes[node_id] = {
            'info': node_info,
            'antibodies': {},
            'last_sync': datetime.now(),
            'health_status': 'healthy'
        }
        logger.info(f"Registered network node: {node_id}")
    
    async def distribute_antibody(self, antibody: Antibody, target_nodes: Optional[List[str]] = None):
        """Distribute an antibody to network nodes"""
        self.antibody_registry[antibody.id] = antibody
        
        nodes_to_update = target_nodes or list(self.network_nodes.keys())
        
        distribution_record = {
            'antibody_id': antibody.id,
            'antibody_name': antibody.name,
            'target_nodes': nodes_to_update,
            'distribution_time': datetime.now().isoformat(),
            'success_count': 0,
            'failure_count': 0
        }
        
        for node_id in nodes_to_update:
            try:
                await self._deploy_to_node(node_id, antibody)
                distribution_record['success_count'] += 1
                logger.info(f"Deployed antibody {antibody.name} to node {node_id}")
            except Exception as e:
                distribution_record['failure_count'] += 1
                logger.error(f"Failed to deploy antibody to node {node_id}: {e}")
        
        self.distribution_log.append(distribution_record)
        
        # Keep only last 1000 distribution records
        if len(self.distribution_log) > 1000:
            self.distribution_log = self.distribution_log[-1000:]
    
    async def _deploy_to_node(self, node_id: str, antibody: Antibody):
        """Deploy antibody to a specific node"""
        if node_id not in self.network_nodes:
            raise ValueError(f"Node {node_id} not registered")
        
        node = self.network_nodes[node_id]
        node['antibodies'][antibody.id] = {
            'antibody': antibody,
            'deployment_time': datetime.now(),
            'activation_count': 0,
            'last_activation': None
        }
        node['last_sync'] = datetime.now()
    
    async def sync_network(self):
        """Synchronize antibodies across all network nodes"""
        logger.info("Starting network synchronization...")
        
        for node_id, node in self.network_nodes.items():
            try:
                # Check for missing antibodies
                missing_antibodies = set(self.antibody_registry.keys()) - set(node['antibodies'].keys())
                
                for antibody_id in missing_antibodies:
                    antibody = self.antibody_registry[antibody_id]
                    await self._deploy_to_node(node_id, antibody)
                
                node['health_status'] = 'healthy'
                logger.info(f"Synced node {node_id} - Added {len(missing_antibodies)} antibodies")
                
            except Exception as e:
                node['health_status'] = 'error'
                logger.error(f"Failed to sync node {node_id}: {e}")
        
        logger.info("Network synchronization completed")
    
    async def get_network_status(self) -> Dict[str, Any]:
        """Get current network status"""
        healthy_nodes = sum(1 for node in self.network_nodes.values() if node['health_status'] == 'healthy')
        total_nodes = len(self.network_nodes)
        
        return {
            'total_nodes': total_nodes,
            'healthy_nodes': healthy_nodes,
            'total_antibodies': len(self.antibody_registry),
            'recent_distributions': len([d for d in self.distribution_log if 
                                       (datetime.now() - datetime.fromisoformat(d['distribution_time'])).total_seconds() < 3600]),
            'network_health': healthy_nodes / total_nodes if total_nodes > 0 else 0
        }


class SystemHealthMonitor:
    """Monitors overall system health and immune system performance"""
    
    def __init__(self):
        self.health_metrics: Dict[str, Any] = {}
        self.performance_history: List[Dict[str, Any]] = []
        self.alert_thresholds = {
            'detection_rate': 0.8,
            'false_positive_rate': 0.1,
            'response_time': 5.0,  # seconds
            'network_health': 0.9
        }
    
    async def update_metrics(self, metrics: Dict[str, Any]):
        """Update system health metrics"""
        self.health_metrics.update({
            **metrics,
            'last_updated': datetime.now().isoformat(),
            'system_uptime': time.time() - getattr(self, 'start_time', time.time())
        })
        
        # Add to performance history
        self.performance_history.append({
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics.copy()
        })
        
        # Keep only last 1000 records
        if len(self.performance_history) > 1000:
            self.performance_history = self.performance_history[-1000:]
        
        # Check for alerts
        await self._check_alerts()
    
    async def _check_alerts(self):
        """Check if any metrics exceed alert thresholds"""
        alerts = []
        
        for metric, threshold in self.alert_thresholds.items():
            current_value = self.health_metrics.get(metric, 0)
            
            if metric in ['detection_rate', 'network_health'] and current_value < threshold:
                alerts.append(f"{metric} below threshold: {current_value:.2f} < {threshold}")
            elif metric in ['false_positive_rate', 'response_time'] and current_value > threshold:
                alerts.append(f"{metric} above threshold: {current_value:.2f} > {threshold}")
        
        if alerts:
            logger.warning(f"System health alerts: {'; '.join(alerts)}")
    
    async def get_health_report(self) -> Dict[str, Any]:
        """Generate comprehensive health report"""
        recent_performance = self.performance_history[-24:] if len(self.performance_history) >= 24 else self.performance_history
        
        avg_metrics = {}
        if recent_performance:
            for metric in ['detection_rate', 'false_positive_rate', 'response_time']:
                values = [p['metrics'].get(metric, 0) for p in recent_performance if metric in p['metrics']]
                avg_metrics[f'avg_{metric}'] = np.mean(values) if values else 0
        
        return {
            'current_metrics': self.health_metrics,
            'average_metrics': avg_metrics,
            'performance_trend': self._calculate_trend(),
            'system_status': self._get_system_status(),
            'recommendations': self._generate_recommendations()
        }
    
    def _calculate_trend(self) -> str:
        """Calculate performance trend"""
        if len(self.performance_history) < 10:
            return "insufficient_data"
        
        recent = self.performance_history[-5:]
        older = self.performance_history[-10:-5]
        
        recent_avg = np.mean([p['metrics'].get('detection_rate', 0) for p in recent])
        older_avg = np.mean([p['metrics'].get('detection_rate', 0) for p in older])
        
        if recent_avg > older_avg * 1.05:
            return "improving"
        elif recent_avg < older_avg * 0.95:
            return "declining"
        else:
            return "stable"
    
    def _get_system_status(self) -> str:
        """Get overall system status"""
        detection_rate = self.health_metrics.get('detection_rate', 0)
        false_positive_rate = self.health_metrics.get('false_positive_rate', 1)
        network_health = self.health_metrics.get('network_health', 0)
        
        if detection_rate > 0.9 and false_positive_rate < 0.05 and network_health > 0.95:
            return "excellent"
        elif detection_rate > 0.8 and false_positive_rate < 0.1 and network_health > 0.9:
            return "good"
        elif detection_rate > 0.6 and false_positive_rate < 0.2 and network_health > 0.8:
            return "fair"
        else:
            return "poor"
    
    def _generate_recommendations(self) -> List[str]:
        """Generate system improvement recommendations"""
        recommendations = []
        
        detection_rate = self.health_metrics.get('detection_rate', 0)
        false_positive_rate = self.health_metrics.get('false_positive_rate', 1)
        response_time = self.health_metrics.get('response_time', 10)
        
        if detection_rate < 0.8:
            recommendations.append("Consider tuning detection algorithms for better sensitivity")
        
        if false_positive_rate > 0.15:
            recommendations.append("Reduce false positives by adjusting antibody sensitivity")
        
        if response_time > 3:
            recommendations.append("Optimize system performance to reduce response time")
        
        if not recommendations:
            recommendations.append("System performing well - continue monitoring")
        
        return recommendations


if __name__ == "__main__":
    # This will be implemented in the main application file
    pass
