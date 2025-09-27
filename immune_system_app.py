"""
Financial Immune System - Main Application
==========================================

The central orchestrator for the Financial Immune System that coordinates
all components: detection, response, memory, and distribution.
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import asdict
import uuid
import random

from financial_immune_system import (
    Transaction, FinancialPathogen, Antibody, ThreatLevel, AnomalyType,
    WhiteBloodCell, AntibodyFactory, ImmuneMemorySystem, 
    ImmunityDistributionNetwork, SystemHealthMonitor
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FinancialImmuneSystem:
    """
    Main Financial Immune System orchestrator
    
    Coordinates all immune system components to provide comprehensive
    financial fraud protection with adaptive learning capabilities.
    """
    
    def __init__(self):
        # Core immune system components
        self.white_blood_cells = WhiteBloodCell()
        self.antibody_factory = AntibodyFactory()
        self.immune_memory = ImmuneMemorySystem()
        self.distribution_network = ImmunityDistributionNetwork()
        self.health_monitor = SystemHealthMonitor()
        
        # System state
        self.active_antibodies: Dict[str, Antibody] = {}
        self.detected_pathogens: List[FinancialPathogen] = []
        self.system_metrics = {
            'transactions_processed': 0,
            'threats_detected': 0,
            'antibodies_generated': 0,
            'false_positives': 0,
            'true_positives': 0,
            'start_time': time.time()
        }
        
        # Configuration
        self.config = {
            'auto_generate_antibodies': True,
            'auto_distribute_antibodies': True,
            'memory_adaptation_enabled': True,
            'real_time_monitoring': True,
            'max_concurrent_scans': 100
        }
        
        logger.info("Financial Immune System initialized")
    
    async def start_system(self):
        """Start the immune system with all components"""
        logger.info("Starting Financial Immune System...")
        
        # Initialize health monitoring
        self.health_monitor.start_time = time.time()
        
        # Register initial network nodes (simulated)
        await self._initialize_network_nodes()
        
        # Start background tasks
        asyncio.create_task(self._periodic_health_check())
        asyncio.create_task(self._periodic_network_sync())
        asyncio.create_task(self._periodic_antibody_adaptation())
        
        logger.info("Financial Immune System is now active and protecting your financial network")
    
    async def process_transaction(self, transaction: Transaction) -> Dict[str, Any]:
        """
        Process a transaction through the immune system
        
        Returns:
            Dict containing processing results and any actions taken
        """
        start_time = time.time()
        
        try:
            # Update metrics
            self.system_metrics['transactions_processed'] += 1
            
            # Scan for pathogens (threats)
            detected_pathogens = await self.white_blood_cells.scan_transaction(transaction)
            
            results = {
                'transaction_id': transaction.id,
                'timestamp': datetime.now().isoformat(),
                'processing_time': 0,
                'threats_detected': len(detected_pathogens),
                'actions_taken': [],
                'risk_score': 0,
                'status': 'approved'
            }
            
            if detected_pathogens:
                await self._handle_detected_threats(transaction, detected_pathogens, results)
            
            # Calculate processing time
            results['processing_time'] = time.time() - start_time
            
            # Update system health metrics
            await self._update_system_metrics(results)
            
            return results
            
        except Exception as e:
            logger.error(f"Error processing transaction {transaction.id}: {e}")
            return {
                'transaction_id': transaction.id,
                'timestamp': datetime.now().isoformat(),
                'processing_time': time.time() - start_time,
                'error': str(e),
                'status': 'error'
            }
    
    async def _handle_detected_threats(self, transaction: Transaction, pathogens: List[FinancialPathogen], results: Dict[str, Any]):
        """Handle detected threats by generating and applying antibodies"""
        
        for pathogen in pathogens:
            self.detected_pathogens.append(pathogen)
            self.system_metrics['threats_detected'] += 1
            
            logger.warning(f"Threat detected: {pathogen.anomaly_type.value} - Level: {pathogen.threat_level.name}")
            
            # Check if we have existing immunity
            immunity_strength = await self.immune_memory.get_immunity_strength(
                pathogen.source_pattern.get('signature', ''), 
                pathogen.anomaly_type
            )
            
            # Generate antibody if needed
            antibody = None
            if self.config['auto_generate_antibodies'] and immunity_strength < 0.8:
                antibody = await self.antibody_factory.generate_antibody(pathogen)
                self.active_antibodies[antibody.id] = antibody
                self.system_metrics['antibodies_generated'] += 1
                
                # Distribute antibody across network
                if self.config['auto_distribute_antibodies']:
                    await self.distribution_network.distribute_antibody(antibody)
            
            # Apply immune response
            action_taken = await self._apply_immune_response(transaction, pathogen, antibody, immunity_strength)
            results['actions_taken'].append(action_taken)
            
            # Update risk score
            risk_contribution = pathogen.confidence_score * pathogen.threat_level.value
            results['risk_score'] += risk_contribution
        
        # Determine final status based on risk score and actions
        if results['risk_score'] > 8:
            results['status'] = 'blocked'
        elif results['risk_score'] > 5:
            results['status'] = 'flagged'
        elif results['actions_taken']:
            results['status'] = 'approved_with_conditions'
    
    async def _apply_immune_response(self, transaction: Transaction, pathogen: FinancialPathogen, 
                                   antibody: Optional[Antibody], immunity_strength: float) -> Dict[str, Any]:
        """Apply appropriate immune response based on threat and immunity"""
        
        action = {
            'pathogen_id': pathogen.id,
            'pathogen_type': pathogen.anomaly_type.value,
            'threat_level': pathogen.threat_level.name,
            'confidence': pathogen.confidence_score,
            'immunity_strength': immunity_strength,
            'response_type': 'none',
            'details': {}
        }
        
        # Determine response based on threat level and immunity
        if pathogen.threat_level == ThreatLevel.CRITICAL:
            action['response_type'] = 'block_transaction'
            action['details'] = {'reason': 'Critical threat detected', 'requires_manual_review': True}
            
        elif pathogen.threat_level == ThreatLevel.HIGH:
            if immunity_strength < 0.5:
                action['response_type'] = 'require_additional_authentication'
                action['details'] = {'auth_method': 'multi_factor', 'timeout_minutes': 15}
            else:
                action['response_type'] = 'flag_for_review'
                action['details'] = {'priority': 'high', 'auto_review_eligible': True}
                
        elif pathogen.threat_level == ThreatLevel.MEDIUM:
            if immunity_strength < 0.3:
                action['response_type'] = 'step_up_verification'
                action['details'] = {'verification_method': 'sms_otp', 'timeout_minutes': 10}
            else:
                action['response_type'] = 'monitor_closely'
                action['details'] = {'monitoring_duration_hours': 24}
                
        else:  # LOW threat level
            action['response_type'] = 'log_and_monitor'
            action['details'] = {'log_level': 'info', 'monitoring_duration_hours': 1}
        
        # Apply antibody-specific logic if available
        if antibody and antibody.rule_logic:
            await self._apply_antibody_logic(transaction, antibody, action)
        
        # Store encounter in immune memory
        if antibody:
            outcome = action['response_type'] not in ['block_transaction']  # Simplified outcome determination
            await self.immune_memory.store_encounter(pathogen, antibody, outcome)
        
        logger.info(f"Applied immune response: {action['response_type']} for {pathogen.anomaly_type.value}")
        
        return action
    
    async def _apply_antibody_logic(self, transaction: Transaction, antibody: Antibody, action: Dict[str, Any]):
        """Apply specific antibody rule logic"""
        rule_logic = antibody.rule_logic
        rule_type = rule_logic.get('type')
        
        if rule_type == 'velocity_limit':
            action['details']['velocity_limit'] = rule_logic.get('max_transactions_per_hour')
            action['details']['cooldown_minutes'] = rule_logic.get('cooldown_minutes')
            
        elif rule_type == 'amount_threshold':
            action['details']['deviation_threshold'] = rule_logic.get('max_deviation')
            
        elif rule_type == 'location_verification':
            action['details']['require_location_verification'] = True
            
        elif rule_type == 'behavioral_check':
            action['details']['new_merchant_threshold'] = rule_logic.get('new_merchant_threshold')
        
        # Update antibody activation count
        antibody.activation_count += 1
    
    async def _update_system_metrics(self, transaction_results: Dict[str, Any]):
        """Update system performance metrics"""
        
        # Update health metrics
        health_metrics = {
            'transactions_processed': self.system_metrics['transactions_processed'],
            'threats_detected': self.system_metrics['threats_detected'],
            'detection_rate': self.system_metrics['threats_detected'] / max(self.system_metrics['transactions_processed'], 1),
            'response_time': transaction_results.get('processing_time', 0),
            'active_antibodies': len(self.active_antibodies),
            'network_health': (await self.distribution_network.get_network_status()).get('network_health', 0)
        }
        
        # Calculate false positive rate (simplified)
        if transaction_results.get('status') == 'flagged':
            # In a real system, this would be determined by manual review outcomes
            health_metrics['false_positive_rate'] = self.system_metrics.get('false_positives', 0) / max(self.system_metrics['threats_detected'], 1)
        
        await self.health_monitor.update_metrics(health_metrics)
    
    async def _initialize_network_nodes(self):
        """Initialize network nodes for immunity distribution"""
        nodes = [
            {'id': 'payment_gateway_1', 'type': 'gateway', 'location': 'us_east'},
            {'id': 'payment_gateway_2', 'type': 'gateway', 'location': 'us_west'},
            {'id': 'mobile_app_backend', 'type': 'application', 'location': 'cloud'},
            {'id': 'web_platform', 'type': 'application', 'location': 'cloud'},
            {'id': 'atm_network', 'type': 'physical', 'location': 'distributed'},
            {'id': 'card_processing', 'type': 'processor', 'location': 'secure_datacenter'}
        ]
        
        for node_info in nodes:
            await self.distribution_network.register_node(node_info['id'], node_info)
    
    async def _periodic_health_check(self):
        """Periodic system health monitoring"""
        while True:
            try:
                await asyncio.sleep(60)  # Check every minute
                
                # Generate health report
                health_report = await self.health_monitor.get_health_report()
                
                # Log system status
                system_status = health_report.get('system_status', 'unknown')
                logger.info(f"System health check - Status: {system_status}")
                
                # Auto-adapt based on performance
                if system_status in ['poor', 'fair'] and self.config['memory_adaptation_enabled']:
                    await self._trigger_system_adaptation()
                    
            except Exception as e:
                logger.error(f"Error in health check: {e}")
    
    async def _periodic_network_sync(self):
        """Periodic network synchronization"""
        while True:
            try:
                await asyncio.sleep(300)  # Sync every 5 minutes
                await self.distribution_network.sync_network()
            except Exception as e:
                logger.error(f"Error in network sync: {e}")
    
    async def _periodic_antibody_adaptation(self):
        """Periodic antibody adaptation based on performance"""
        while True:
            try:
                await asyncio.sleep(1800)  # Adapt every 30 minutes
                
                for antibody_id, antibody in self.active_antibodies.items():
                    # Calculate performance metrics (simplified)
                    performance_data = {
                        'success_rate': min(antibody.activation_count / max(antibody.activation_count + 1, 1), 0.95),
                        'false_positive_rate': 0.1  # Would be calculated from real data
                    }
                    
                    # Adapt antibody
                    adapted_antibody = await self.immune_memory.adapt_antibody(antibody, performance_data)
                    self.active_antibodies[antibody_id] = adapted_antibody
                    
                    # Redistribute adapted antibody
                    if self.config['auto_distribute_antibodies']:
                        await self.distribution_network.distribute_antibody(adapted_antibody)
                        
            except Exception as e:
                logger.error(f"Error in antibody adaptation: {e}")
    
    async def _trigger_system_adaptation(self):
        """Trigger system-wide adaptation for poor performance"""
        logger.info("Triggering system adaptation due to poor performance")
        
        # Analyze recent threats
        recent_pathogens = [p for p in self.detected_pathogens 
                          if (datetime.now() - p.detection_timestamp).total_seconds() < 3600]
        
        # Generate new antibodies for frequent threat patterns
        threat_patterns = {}
        for pathogen in recent_pathogens:
            pattern_key = f"{pathogen.anomaly_type.value}_{pathogen.threat_level.value}"
            threat_patterns[pattern_key] = threat_patterns.get(pattern_key, 0) + 1
        
        # Create antibodies for most common patterns
        for pattern, count in threat_patterns.items():
            if count > 3:  # Pattern seen more than 3 times
                # Find a representative pathogen for this pattern
                representative_pathogen = next(
                    p for p in recent_pathogens 
                    if f"{p.anomaly_type.value}_{p.threat_level.value}" == pattern
                )
                
                # Generate and distribute new antibody
                new_antibody = await self.antibody_factory.generate_antibody(representative_pathogen)
                self.active_antibodies[new_antibody.id] = new_antibody
                await self.distribution_network.distribute_antibody(new_antibody)
                
                logger.info(f"Generated adaptive antibody for pattern: {pattern}")
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        health_report = await self.health_monitor.get_health_report()
        network_status = await self.distribution_network.get_network_status()
        
        return {
            'system_info': {
                'version': '2.0',
                'uptime_seconds': time.time() - self.system_metrics['start_time'],
                'status': health_report.get('system_status', 'unknown')
            },
            'performance_metrics': self.system_metrics,
            'health_report': health_report,
            'network_status': network_status,
            'active_components': {
                'white_blood_cells': 'active',
                'antibody_factory': 'active',
                'immune_memory': 'active',
                'distribution_network': 'active',
                'health_monitor': 'active'
            },
            'active_antibodies_count': len(self.active_antibodies),
            'recent_threats': len([p for p in self.detected_pathogens 
                                 if (datetime.now() - p.detection_timestamp).total_seconds() < 3600])
        }
    
    async def generate_threat_report(self, hours: int = 24) -> Dict[str, Any]:
        """Generate comprehensive threat analysis report"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_threats = [p for p in self.detected_pathogens if p.detection_timestamp > cutoff_time]
        
        # Analyze threat patterns
        threat_analysis = {
            'total_threats': len(recent_threats),
            'threat_by_type': {},
            'threat_by_level': {},
            'threat_timeline': [],
            'top_risk_factors': {},
            'immunity_effectiveness': {}
        }
        
        # Group by type and level
        for threat in recent_threats:
            threat_type = threat.anomaly_type.value
            threat_level = threat.threat_level.name
            
            threat_analysis['threat_by_type'][threat_type] = threat_analysis['threat_by_type'].get(threat_type, 0) + 1
            threat_analysis['threat_by_level'][threat_level] = threat_analysis['threat_by_level'].get(threat_level, 0) + 1
            
            # Collect risk factors
            for factor in threat.risk_factors:
                threat_analysis['top_risk_factors'][factor] = threat_analysis['top_risk_factors'].get(factor, 0) + 1
        
        # Sort risk factors by frequency
        threat_analysis['top_risk_factors'] = dict(
            sorted(threat_analysis['top_risk_factors'].items(), key=lambda x: x[1], reverse=True)[:10]
        )
        
        return threat_analysis
    
    async def shutdown(self):
        """Gracefully shutdown the immune system"""
        logger.info("Shutting down Financial Immune System...")
        
        # Save current state (in a real system, this would persist to database)
        system_state = {
            'active_antibodies': {aid: asdict(antibody) for aid, antibody in self.active_antibodies.items()},
            'system_metrics': self.system_metrics,
            'shutdown_time': datetime.now().isoformat()
        }
        
        # In a real implementation, save to persistent storage
        logger.info("System state saved. Financial Immune System shutdown complete.")


async def create_sample_transaction(
    user_id: str = None,
    amount: float = None,
    location: str = None,
    merchant: str = None,
    **kwargs
) -> Transaction:
    """
    Create a sample transaction for testing purposes
    
    Args:
        user_id: User identifier (optional, will generate random if not provided)
        amount: Transaction amount (optional, will generate random if not provided)
        location: Transaction location (optional, will use default if not provided)
        merchant: Merchant name (optional, will generate random if not provided)
        **kwargs: Additional transaction parameters
    
    Returns:
        Transaction: A sample transaction object
    """
    # Generate random values if not provided
    if user_id is None:
        user_id = f"user_{random.randint(1000, 9999)}"
    
    if amount is None:
        amount = round(random.uniform(10.0, 500.0), 2)
    
    if location is None:
        locations = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
        location = random.choice(locations)
    
    if merchant is None:
        merchants = ["Amazon", "Walmart", "Target", "Starbucks", "McDonald's", "Shell", "Uber"]
        merchant = random.choice(merchants)
    
    # Create transaction
    transaction = Transaction(
        id=str(uuid.uuid4()),
        user_id=user_id,
        amount=amount,
        timestamp=datetime.now(),
        location=location,
        merchant=merchant,
        transaction_type="purchase",
        card_number=f"****-****-****-{random.randint(1000, 9999)}",
        metadata={'channel': random.choice(['online', 'mobile', 'pos', 'atm'])},
        **kwargs
    )
    
    return transaction


async def run_demo():
    """Run a demonstration of the Financial Immune System"""
    print("🦠 Financial Immune System Demo Starting...")
    print("=" * 60)
    
    # Initialize the immune system
    immune_system = FinancialImmuneSystem()
    await immune_system.start_system()
    
    print("✅ Financial Immune System initialized and active")
    print()
    
    # Simulate normal transactions
    print("📊 Processing normal transactions...")
    normal_user = "user_12345"
    
    for i in range(5):
        transaction = await create_sample_transaction(
            user_id=normal_user,
            amount=np.random.uniform(20, 200),
            location="New York",
            merchant="Starbucks"
        )
        
        result = await immune_system.process_transaction(transaction)
        print(f"Transaction {i+1}: ${transaction.amount:.2f} - Status: {result['status']}")
    
    print()
    
    # Simulate suspicious transactions
    print("🚨 Simulating suspicious activities...")
    
    # Velocity attack
    print("Testing velocity anomaly...")
    for i in range(12):
        transaction = await create_sample_transaction(
            user_id=normal_user,
            amount=np.random.uniform(10, 50),
            location="New York"
        )
        result = await immune_system.process_transaction(transaction)
        if result['threats_detected'] > 0:
            print(f"⚠️  Velocity threat detected! Actions: {len(result['actions_taken'])}")
            break
    
    # Geographic anomaly
    print("Testing geographic anomaly...")
    transaction = await create_sample_transaction(
        user_id=normal_user,
        amount=1000,
        location="Tokyo",  # Unusual location
        merchant="Unknown Merchant"
    )
    result = await immune_system.process_transaction(transaction)
    if result['threats_detected'] > 0:
        print(f"⚠️  Geographic threat detected! Risk score: {result['risk_score']}")
    
    # Large amount anomaly
    print("Testing amount anomaly...")
    transaction = await create_sample_transaction(
        user_id=normal_user,
        amount=50000,  # Very large amount
        location="New York"
    )
    result = await immune_system.process_transaction(transaction)
    if result['threats_detected'] > 0:
        print(f"⚠️  Amount anomaly detected! Status: {result['status']}")
    
    print()
    
    # Show system status
    print("📈 System Status Report:")
    status = await immune_system.get_system_status()
    print(f"Transactions Processed: {status['performance_metrics']['transactions_processed']}")
    print(f"Threats Detected: {status['performance_metrics']['threats_detected']}")
    print(f"Active Antibodies: {status['active_antibodies_count']}")
    print(f"System Health: {status['system_info']['status']}")
    print(f"Network Health: {status['network_status']['network_health']:.2%}")
    
    print()
    
    # Generate threat report
    print("🔍 Threat Analysis Report:")
    threat_report = await immune_system.generate_threat_report(hours=1)
    print(f"Total Threats (last hour): {threat_report['total_threats']}")
    print("Threats by Type:")
    for threat_type, count in threat_report['threat_by_type'].items():
        print(f"  - {threat_type}: {count}")
    
    print("Top Risk Factors:")
    for factor, count in list(threat_report['top_risk_factors'].items())[:3]:
        print(f"  - {factor}: {count}")
    
    print()
    print("🛡️  Financial Immune System Demo Complete!")
    print("The system is now actively protecting against financial threats.")
    
    # Shutdown
    await immune_system.shutdown()


if __name__ == "__main__":
    import numpy as np
    
    # Configure logging for demo
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run the demo
    asyncio.run(run_demo())
