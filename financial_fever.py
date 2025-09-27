"""
Financial Fever System
=====================

Implements a system-wide fever response to massive coordinated attacks.
Like biological fever, this raises the "temperature" of the entire system,
increasing sensitivity and activating emergency protocols.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np
from collections import defaultdict, deque
import uuid

from financial_immune_system import FinancialPathogen, Antibody, ThreatLevel

logger = logging.getLogger(__name__)


class FeverLevel(Enum):
    """System fever levels"""
    NORMAL = 98.6
    MILD_FEVER = 100.4
    MODERATE_FEVER = 102.2
    HIGH_FEVER = 104.0
    CRITICAL_FEVER = 106.0


class FeverTrigger(Enum):
    """Events that can trigger fever response"""
    COORDINATED_ATTACK = "coordinated_attack"
    MASSIVE_VELOCITY = "massive_velocity"
    GEOGRAPHIC_SPREAD = "geographic_spread"
    NEW_THREAT_VARIANT = "new_threat_variant"
    ANTIBODY_RESISTANCE = "antibody_resistance"
    SYSTEM_COMPROMISE = "system_compromise"


@dataclass
class FeverEvent:
    """An event that contributes to system fever"""
    event_id: str
    trigger_type: FeverTrigger
    severity: float
    timestamp: datetime
    source_data: Dict[str, Any]
    temperature_contribution: float
    duration_minutes: int = 60


@dataclass
class EmergencyProtocol:
    """Emergency protocol activated during fever"""
    protocol_id: str
    name: str
    activation_temperature: float
    actions: List[str]
    effectiveness: float
    energy_cost: float
    cooldown_minutes: int = 30


class FinancialFever:
    """
    Financial Fever System - System-wide immune response
    
    Features:
    - Temperature monitoring based on threat density
    - Escalating response protocols
    - Enhanced sensitivity during fever
    - Emergency countermeasures
    - Coordinated network response
    """
    
    def __init__(self):
        self.current_temperature = FeverLevel.NORMAL.value
        self.baseline_temperature = FeverLevel.NORMAL.value
        self.fever_events: deque = deque(maxlen=1000)
        self.active_protocols: Dict[str, EmergencyProtocol] = {}
        
        # Fever parameters
        self.temperature_decay_rate = 0.1  # Temperature drops per minute
        self.sensitivity_multiplier = 1.0
        self.response_threshold_modifier = 1.0
        self.energy_consumption_rate = 1.0
        
        # Tracking
        self.fever_history: List[Dict[str, Any]] = []
        self.protocol_activations: List[Dict[str, Any]] = []
        self.system_stress_level = 0.0
        
        # Initialize emergency protocols
        self._initialize_emergency_protocols()
        
        logger.info("Financial Fever System initialized")
    
    def _initialize_emergency_protocols(self):
        """Initialize emergency response protocols"""
        protocols = [
            EmergencyProtocol(
                protocol_id="enhanced_scanning",
                name="Enhanced Transaction Scanning",
                activation_temperature=100.0,
                actions=[
                    "increase_detection_sensitivity",
                    "reduce_confidence_thresholds",
                    "activate_additional_scanners"
                ],
                effectiveness=0.8,
                energy_cost=1.5
            ),
            EmergencyProtocol(
                protocol_id="velocity_lockdown",
                name="Velocity Lockdown Protocol",
                activation_temperature=101.0,
                actions=[
                    "reduce_transaction_limits",
                    "increase_cooling_periods",
                    "mandatory_step_up_auth"
                ],
                effectiveness=0.9,
                energy_cost=2.0
            ),
            EmergencyProtocol(
                protocol_id="geographic_quarantine",
                name="Geographic Quarantine",
                activation_temperature=102.0,
                actions=[
                    "restrict_new_locations",
                    "enhanced_geo_verification",
                    "location_based_blocking"
                ],
                effectiveness=0.85,
                energy_cost=2.5
            ),
            EmergencyProtocol(
                protocol_id="network_isolation",
                name="Network Node Isolation",
                activation_temperature=103.0,
                actions=[
                    "isolate_compromised_nodes",
                    "reroute_traffic",
                    "emergency_authentication"
                ],
                effectiveness=0.95,
                energy_cost=3.0
            ),
            EmergencyProtocol(
                protocol_id="system_shutdown",
                name="Emergency System Shutdown",
                activation_temperature=105.0,
                actions=[
                    "halt_new_transactions",
                    "freeze_suspicious_accounts",
                    "activate_manual_review"
                ],
                effectiveness=0.99,
                energy_cost=5.0,
                cooldown_minutes=120
            )
        ]
        
        for protocol in protocols:
            self.active_protocols[protocol.protocol_id] = protocol
    
    async def register_fever_event(self, trigger_type: FeverTrigger, severity: float, 
                                 source_data: Dict[str, Any]) -> FeverEvent:
        """Register an event that contributes to system fever"""
        
        # Calculate temperature contribution
        base_contribution = severity * 2.0  # Base fever contribution
        
        # Amplify based on recent events
        recent_events = [
            event for event in self.fever_events
            if (datetime.now() - event.timestamp).total_seconds() < 3600  # Last hour
        ]
        
        amplification = 1.0 + (len(recent_events) * 0.1)  # 10% per recent event
        temperature_contribution = base_contribution * amplification
        
        # Create fever event
        fever_event = FeverEvent(
            event_id=str(uuid.uuid4()),
            trigger_type=trigger_type,
            severity=severity,
            timestamp=datetime.now(),
            source_data=source_data,
            temperature_contribution=temperature_contribution,
            duration_minutes=max(30, int(severity * 60))  # Duration based on severity
        )
        
        self.fever_events.append(fever_event)
        
        # Update system temperature
        await self._update_temperature()
        
        logger.warning(f"Fever event registered: {trigger_type.value} (severity: {severity:.2f}, temp: +{temperature_contribution:.1f}°F)")
        
        return fever_event
    
    async def _update_temperature(self):
        """Update system temperature based on active fever events"""
        current_time = datetime.now()
        active_contribution = 0.0
        
        # Calculate contribution from active events
        for event in self.fever_events:
            # Check if event is still active
            elapsed_minutes = (current_time - event.timestamp).total_seconds() / 60
            
            if elapsed_minutes < event.duration_minutes:
                # Apply decay over time
                decay_factor = 1.0 - (elapsed_minutes / event.duration_minutes) * 0.5
                active_contribution += event.temperature_contribution * decay_factor
        
        # Update temperature
        target_temperature = self.baseline_temperature + active_contribution
        
        # Smooth temperature changes
        temperature_diff = target_temperature - self.current_temperature
        self.current_temperature += temperature_diff * 0.3  # 30% adjustment per update
        
        # Update system parameters based on temperature
        await self._update_system_parameters()
        
        # Check for protocol activation/deactivation
        await self._manage_emergency_protocols()
        
        # Record fever history
        if len(self.fever_history) == 0 or abs(self.current_temperature - self.fever_history[-1]["temperature"]) > 0.5:
            self.fever_history.append({
                "timestamp": current_time.isoformat(),
                "temperature": self.current_temperature,
                "active_events": len([e for e in self.fever_events if (current_time - e.timestamp).total_seconds() < e.duration_minutes * 60]),
                "fever_level": self._get_fever_level().name
            })
    
    def _get_fever_level(self) -> FeverLevel:
        """Determine current fever level"""
        temp = self.current_temperature
        
        if temp >= FeverLevel.CRITICAL_FEVER.value:
            return FeverLevel.CRITICAL_FEVER
        elif temp >= FeverLevel.HIGH_FEVER.value:
            return FeverLevel.HIGH_FEVER
        elif temp >= FeverLevel.MODERATE_FEVER.value:
            return FeverLevel.MODERATE_FEVER
        elif temp >= FeverLevel.MILD_FEVER.value:
            return FeverLevel.MILD_FEVER
        else:
            return FeverLevel.NORMAL
    
    async def _update_system_parameters(self):
        """Update system parameters based on current temperature"""
        fever_level = self._get_fever_level()
        temp_above_normal = self.current_temperature - self.baseline_temperature
        
        # Increase sensitivity during fever
        if fever_level == FeverLevel.NORMAL:
            self.sensitivity_multiplier = 1.0
            self.response_threshold_modifier = 1.0
            self.energy_consumption_rate = 1.0
        elif fever_level == FeverLevel.MILD_FEVER:
            self.sensitivity_multiplier = 1.2
            self.response_threshold_modifier = 0.9
            self.energy_consumption_rate = 1.1
        elif fever_level == FeverLevel.MODERATE_FEVER:
            self.sensitivity_multiplier = 1.5
            self.response_threshold_modifier = 0.8
            self.energy_consumption_rate = 1.3
        elif fever_level == FeverLevel.HIGH_FEVER:
            self.sensitivity_multiplier = 2.0
            self.response_threshold_modifier = 0.6
            self.energy_consumption_rate = 1.6
        elif fever_level == FeverLevel.CRITICAL_FEVER:
            self.sensitivity_multiplier = 3.0
            self.response_threshold_modifier = 0.4
            self.energy_consumption_rate = 2.0
        
        # Update system stress level
        self.system_stress_level = min(temp_above_normal / 10.0, 1.0)
    
    async def _manage_emergency_protocols(self):
        """Activate or deactivate emergency protocols based on temperature"""
        current_time = datetime.now()
        
        for protocol_id, protocol in self.active_protocols.items():
            should_be_active = self.current_temperature >= protocol.activation_temperature
            is_currently_active = any(
                activation["protocol_id"] == protocol_id and activation["status"] == "active"
                for activation in self.protocol_activations
                if (current_time - datetime.fromisoformat(activation["timestamp"])).total_seconds() < protocol.cooldown_minutes * 60
            )
            
            if should_be_active and not is_currently_active:
                await self._activate_protocol(protocol)
            elif not should_be_active and is_currently_active:
                await self._deactivate_protocol(protocol)
    
    async def _activate_protocol(self, protocol: EmergencyProtocol):
        """Activate an emergency protocol"""
        activation_record = {
            "protocol_id": protocol.protocol_id,
            "protocol_name": protocol.name,
            "timestamp": datetime.now().isoformat(),
            "temperature": self.current_temperature,
            "status": "active",
            "actions": protocol.actions.copy()
        }
        
        self.protocol_activations.append(activation_record)
        
        logger.critical(f"EMERGENCY PROTOCOL ACTIVATED: {protocol.name} (Temp: {self.current_temperature:.1f}°F)")
        
        # Execute protocol actions
        for action in protocol.actions:
            await self._execute_protocol_action(action, protocol)
    
    async def _deactivate_protocol(self, protocol: EmergencyProtocol):
        """Deactivate an emergency protocol"""
        # Find and update the most recent activation
        for activation in reversed(self.protocol_activations):
            if activation["protocol_id"] == protocol.protocol_id and activation["status"] == "active":
                activation["status"] = "deactivated"
                activation["deactivation_timestamp"] = datetime.now().isoformat()
                activation["deactivation_temperature"] = self.current_temperature
                break
        
        logger.info(f"Emergency protocol deactivated: {protocol.name} (Temp: {self.current_temperature:.1f}°F)")
    
    async def _execute_protocol_action(self, action: str, protocol: EmergencyProtocol):
        """Execute a specific protocol action"""
        
        if action == "increase_detection_sensitivity":
            # This would integrate with the main detection system
            logger.info("Increased detection sensitivity")
            
        elif action == "reduce_confidence_thresholds":
            # Lower thresholds for flagging transactions
            logger.info("Reduced confidence thresholds")
            
        elif action == "reduce_transaction_limits":
            # Implement stricter velocity limits
            logger.info("Reduced transaction velocity limits")
            
        elif action == "mandatory_step_up_auth":
            # Require additional authentication
            logger.info("Activated mandatory step-up authentication")
            
        elif action == "restrict_new_locations":
            # Block transactions from new geographic locations
            logger.info("Restricted transactions from new locations")
            
        elif action == "isolate_compromised_nodes":
            # Isolate potentially compromised network nodes
            logger.info("Isolated potentially compromised nodes")
            
        elif action == "halt_new_transactions":
            # Emergency stop for new transactions
            logger.critical("EMERGENCY: Halted new transaction processing")
            
        elif action == "freeze_suspicious_accounts":
            # Freeze accounts showing suspicious activity
            logger.critical("EMERGENCY: Froze suspicious accounts")
        
        # Consume energy for action
        # This would integrate with the main system's energy management
    
    async def apply_fever_modifiers(self, detection_result: Dict[str, Any]) -> Dict[str, Any]:
        """Apply fever-based modifiers to detection results"""
        modified_result = detection_result.copy()
        
        # Increase sensitivity during fever
        if "confidence_score" in modified_result:
            original_confidence = modified_result["confidence_score"]
            modified_confidence = min(original_confidence * self.sensitivity_multiplier, 1.0)
            modified_result["confidence_score"] = modified_confidence
            modified_result["fever_amplification"] = self.sensitivity_multiplier
        
        # Lower response thresholds
        if "risk_score" in modified_result:
            original_risk = modified_result["risk_score"]
            modified_risk = original_risk * self.sensitivity_multiplier
            modified_result["risk_score"] = modified_risk
        
        # Add fever context
        modified_result["system_temperature"] = self.current_temperature
        modified_result["fever_level"] = self._get_fever_level().name
        modified_result["system_stress"] = self.system_stress_level
        
        return modified_result
    
    async def check_coordinated_attack(self, recent_threats: List[FinancialPathogen]) -> bool:
        """Check if recent threats indicate a coordinated attack"""
        if len(recent_threats) < 5:
            return False
        
        # Analyze temporal clustering
        timestamps = [threat.detection_timestamp for threat in recent_threats]
        time_spans = [(timestamps[i+1] - timestamps[i]).total_seconds() for i in range(len(timestamps)-1)]
        avg_time_span = np.mean(time_spans)
        
        # Check for rapid succession (coordinated timing)
        if avg_time_span < 300:  # Less than 5 minutes between threats
            # Check for diversity in attack vectors
            attack_types = set(threat.anomaly_type for threat in recent_threats)
            
            if len(attack_types) >= 3:  # Multiple attack types
                # Register coordinated attack event
                await self.register_fever_event(
                    FeverTrigger.COORDINATED_ATTACK,
                    severity=min(len(recent_threats) / 10.0, 1.0),
                    source_data={
                        "threat_count": len(recent_threats),
                        "attack_types": [at.value for at in attack_types],
                        "avg_time_span": avg_time_span,
                        "time_window": "last_hour"
                    }
                )
                return True
        
        return False
    
    async def monitor_antibody_resistance(self, resistance_events: List[Dict[str, Any]]):
        """Monitor for widespread antibody resistance"""
        if len(resistance_events) < 3:
            return
        
        # Check for multiple antibodies being resisted
        resisted_antibodies = set(event.get("antibody_id") for event in resistance_events)
        
        if len(resisted_antibodies) >= 3:
            await self.register_fever_event(
                FeverTrigger.ANTIBODY_RESISTANCE,
                severity=len(resisted_antibodies) / 10.0,
                source_data={
                    "resisted_antibodies": len(resisted_antibodies),
                    "resistance_events": len(resistance_events),
                    "time_window": "recent"
                }
            )
    
    async def detect_new_threat_variant(self, threat_signatures: List[str]):
        """Detect emergence of new threat variants"""
        # This would analyze threat signatures for novel patterns
        # Simplified implementation
        
        unique_signatures = set(threat_signatures)
        if len(unique_signatures) > len(threat_signatures) * 0.8:  # High diversity
            await self.register_fever_event(
                FeverTrigger.NEW_THREAT_VARIANT,
                severity=0.7,
                source_data={
                    "total_signatures": len(threat_signatures),
                    "unique_signatures": len(unique_signatures),
                    "diversity_ratio": len(unique_signatures) / len(threat_signatures)
                }
            )
    
    def get_fever_status(self) -> Dict[str, Any]:
        """Get comprehensive fever system status"""
        current_time = datetime.now()
        
        # Count active events
        active_events = [
            event for event in self.fever_events
            if (current_time - event.timestamp).total_seconds() < event.duration_minutes * 60
        ]
        
        # Count active protocols
        active_protocols = [
            activation for activation in self.protocol_activations
            if activation["status"] == "active" and 
            (current_time - datetime.fromisoformat(activation["timestamp"])).total_seconds() < 3600
        ]
        
        return {
            "current_temperature": self.current_temperature,
            "fever_level": self._get_fever_level().name,
            "baseline_temperature": self.baseline_temperature,
            "temperature_above_normal": self.current_temperature - self.baseline_temperature,
            "system_stress_level": self.system_stress_level,
            "sensitivity_multiplier": self.sensitivity_multiplier,
            "response_threshold_modifier": self.response_threshold_modifier,
            "energy_consumption_rate": self.energy_consumption_rate,
            "active_fever_events": len(active_events),
            "total_fever_events": len(self.fever_events),
            "active_protocols": len(active_protocols),
            "protocol_names": [p["protocol_name"] for p in active_protocols],
            "fever_history_points": len(self.fever_history)
        }
    
    async def cool_down_system(self, cooling_factor: float = 0.5):
        """Manually cool down the system (emergency intervention)"""
        original_temp = self.current_temperature
        self.current_temperature = self.baseline_temperature + (self.current_temperature - self.baseline_temperature) * cooling_factor
        
        await self._update_system_parameters()
        await self._manage_emergency_protocols()
        
        logger.info(f"Manual system cooldown: {original_temp:.1f}°F -> {self.current_temperature:.1f}°F")


# Demo function
async def demo_financial_fever():
    """Demonstrate the financial fever system"""
    print("🌡️ Financial Fever System Demo")
    print("=" * 40)
    
    fever_system = FinancialFever()
    
    print(f"Initial system temperature: {fever_system.current_temperature:.1f}°F")
    print(f"Fever level: {fever_system._get_fever_level().name}")
    
    # Simulate escalating attack scenario
    print("\nSimulating coordinated attack scenario...")
    
    # Register multiple fever events
    events = [
        (FeverTrigger.MASSIVE_VELOCITY, 0.6, {"attack_type": "velocity_burst"}),
        (FeverTrigger.GEOGRAPHIC_SPREAD, 0.4, {"locations": ["NY", "LA", "Chicago"]}),
        (FeverTrigger.COORDINATED_ATTACK, 0.8, {"attack_vectors": 5}),
        (FeverTrigger.ANTIBODY_RESISTANCE, 0.5, {"resistant_antibodies": 3}),
        (FeverTrigger.NEW_THREAT_VARIANT, 0.7, {"variant_signatures": 12})
    ]
    
    for trigger, severity, data in events:
        await fever_system.register_fever_event(trigger, severity, data)
        status = fever_system.get_fever_status()
        
        print(f"Event: {trigger.value}")
        print(f"  Temperature: {status['current_temperature']:.1f}°F")
        print(f"  Fever Level: {status['fever_level']}")
        print(f"  Active Protocols: {status['active_protocols']}")
        if status['protocol_names']:
            print(f"  Protocols: {', '.join(status['protocol_names'])}")
        print()
        
        # Small delay to simulate time progression
        await asyncio.sleep(0.1)
    
    # Show final status
    final_status = fever_system.get_fever_status()
    print("Final Fever System Status:")
    print(f"Temperature: {final_status['current_temperature']:.1f}°F")
    print(f"Fever Level: {final_status['fever_level']}")
    print(f"System Stress: {final_status['system_stress_level']:.2f}")
    print(f"Sensitivity Multiplier: {final_status['sensitivity_multiplier']:.1f}x")
    print(f"Active Events: {final_status['active_fever_events']}")
    print(f"Active Protocols: {final_status['active_protocols']}")
    
    # Demonstrate fever modifiers
    print("\nTesting fever modifiers on detection result...")
    sample_detection = {
        "confidence_score": 0.6,
        "risk_score": 3.0,
        "threat_detected": True
    }
    
    modified_detection = await fever_system.apply_fever_modifiers(sample_detection)
    print(f"Original confidence: {sample_detection['confidence_score']:.2f}")
    print(f"Fever-modified confidence: {modified_detection['confidence_score']:.2f}")
    print(f"Amplification factor: {modified_detection['fever_amplification']:.1f}x")
    
    # Demonstrate cooldown
    print("\nApplying emergency cooldown...")
    await fever_system.cool_down_system(0.3)
    
    cooldown_status = fever_system.get_fever_status()
    print(f"Post-cooldown temperature: {cooldown_status['current_temperature']:.1f}°F")
    print(f"Post-cooldown fever level: {cooldown_status['fever_level']}")
    
    print("\n🌡️ Financial Fever Demo Complete!")


if __name__ == "__main__":
    asyncio.run(demo_financial_fever())
