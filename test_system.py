#!/usr/bin/env python3
"""
Financial Immune System - Test Suite
====================================

Basic test suite to verify system functionality.
"""

import asyncio
import unittest
from datetime import datetime
import numpy as np

from financial_immune_system import (
    Transaction, FinancialPathogen, Antibody, ThreatLevel, AnomalyType,
    WhiteBloodCell, AntibodyFactory, ImmuneMemorySystem, 
    ImmunityDistributionNetwork, SystemHealthMonitor
)
from immune_system_app import FinancialImmuneSystem, create_sample_transaction


class TestFinancialImmuneSystem(unittest.TestCase):
    """Test cases for the Financial Immune System"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.immune_system = None
    
    async def async_setUp(self):
        """Async setup for tests"""
        self.immune_system = FinancialImmuneSystem()
        await self.immune_system.start_system()
    
    def test_transaction_creation(self):
        """Test transaction creation"""
        async def run_test():
            transaction = await create_sample_transaction(
                user_id="test_user",
                amount=100.0,
                location="Test City",
                merchant="Test Merchant"
            )
            
            self.assertEqual(transaction.user_id, "test_user")
            self.assertEqual(transaction.amount, 100.0)
            self.assertEqual(transaction.location, "Test City")
            self.assertEqual(transaction.merchant, "Test Merchant")
            self.assertIsInstance(transaction.timestamp, datetime)
        
        asyncio.run(run_test())
    
    def test_white_blood_cell_detection(self):
        """Test white blood cell detection capabilities"""
        async def run_test():
            wbc = WhiteBloodCell()
            
            # Test normal transaction
            normal_transaction = await create_sample_transaction(
                user_id="normal_user",
                amount=50.0
            )
            
            pathogens = await wbc.scan_transaction(normal_transaction)
            # First transaction should not trigger anomalies
            self.assertEqual(len(pathogens), 0)
            
            # Test large amount anomaly
            large_transaction = await create_sample_transaction(
                user_id="normal_user",
                amount=50000.0  # Very large amount
            )
            
            pathogens = await wbc.scan_transaction(large_transaction)
            # Should detect pattern anomaly
            self.assertGreater(len(pathogens), 0)
        
        asyncio.run(run_test())
    
    def test_antibody_generation(self):
        """Test antibody generation"""
        async def run_test():
            factory = AntibodyFactory()
            
            # Create a test pathogen
            pathogen = FinancialPathogen(
                id="test_pathogen",
                anomaly_type=AnomalyType.VELOCITY_ANOMALY,
                threat_level=ThreatLevel.HIGH,
                confidence_score=0.9,
                affected_transactions=["tx1", "tx2"],
                detection_timestamp=datetime.now(),
                source_pattern={'test': 'pattern'},
                risk_factors=["High velocity"]
            )
            
            antibody = await factory.generate_antibody(pathogen)
            
            self.assertIsInstance(antibody, Antibody)
            self.assertEqual(antibody.rule_logic['type'], 'velocity_limit')
            self.assertGreater(antibody.effectiveness_score, 0)
        
        asyncio.run(run_test())
    
    def test_immune_memory(self):
        """Test immune memory system"""
        async def run_test():
            memory = ImmuneMemorySystem()
            
            # Create test pathogen and antibody
            pathogen = FinancialPathogen(
                id="test_pathogen",
                anomaly_type=AnomalyType.VELOCITY_ANOMALY,
                threat_level=ThreatLevel.HIGH,
                confidence_score=0.9,
                affected_transactions=["tx1"],
                detection_timestamp=datetime.now(),
                source_pattern={'test': 'pattern'},
                risk_factors=["Test"]
            )
            
            antibody = Antibody(
                id="test_antibody",
                name="Test Antibody",
                pathogen_signature="test_sig",
                rule_logic={'type': 'test'},
                effectiveness_score=0.8,
                creation_timestamp=datetime.now(),
                last_updated=datetime.now(),
                activation_count=0,
                success_rate=0.0
            )
            
            # Store encounter
            await memory.store_encounter(pathogen, antibody, True)
            
            # Check memory
            immunity_strength = await memory.get_immunity_strength("test_sig", AnomalyType.VELOCITY_ANOMALY)
            self.assertGreater(immunity_strength, 0.5)
        
        asyncio.run(run_test())
    
    def test_distribution_network(self):
        """Test immunity distribution network"""
        async def run_test():
            network = ImmunityDistributionNetwork()
            
            # Register a node
            await network.register_node("test_node", {"type": "test", "location": "test"})
            
            # Check node registration
            self.assertIn("test_node", network.network_nodes)
            
            # Test antibody distribution
            antibody = Antibody(
                id="test_antibody",
                name="Test Antibody",
                pathogen_signature="test_sig",
                rule_logic={'type': 'test'},
                effectiveness_score=0.8,
                creation_timestamp=datetime.now(),
                last_updated=datetime.now(),
                activation_count=0,
                success_rate=0.0
            )
            
            await network.distribute_antibody(antibody)
            
            # Check distribution
            self.assertIn(antibody.id, network.antibody_registry)
        
        asyncio.run(run_test())
    
    def test_system_integration(self):
        """Test full system integration"""
        async def run_test():
            await self.async_setUp()
            
            # Process a normal transaction
            transaction = await create_sample_transaction(
                user_id="integration_test_user",
                amount=100.0
            )
            
            result = await self.immune_system.process_transaction(transaction)
            
            # Check result structure
            self.assertIn('transaction_id', result)
            self.assertIn('status', result)
            self.assertIn('threats_detected', result)
            self.assertIn('processing_time', result)
            
            # Should be approved for normal transaction
            self.assertEqual(result['status'], 'approved')
            
            # Test system status
            status = await self.immune_system.get_system_status()
            self.assertIn('system_info', status)
            self.assertIn('performance_metrics', status)
            self.assertEqual(status['performance_metrics']['transactions_processed'], 1)
        
        asyncio.run(run_test())
    
    def test_velocity_attack_detection(self):
        """Test velocity attack detection"""
        async def run_test():
            await self.async_setUp()
            
            user_id = "velocity_test_user"
            
            # Generate multiple rapid transactions
            for i in range(12):
                transaction = await create_sample_transaction(
                    user_id=user_id,
                    amount=50.0
                )
                
                result = await self.immune_system.process_transaction(transaction)
                
                # Should detect velocity anomaly after several transactions
                if result['threats_detected'] > 0:
                    self.assertGreater(result['risk_score'], 0)
                    self.assertIn(result['status'], ['flagged', 'blocked', 'approved_with_conditions'])
                    break
            else:
                self.fail("Velocity attack not detected")
        
        asyncio.run(run_test())


class TestSystemComponents(unittest.TestCase):
    """Test individual system components"""
    
    def test_threat_levels(self):
        """Test threat level enumeration"""
        self.assertEqual(ThreatLevel.LOW.value, 1)
        self.assertEqual(ThreatLevel.MEDIUM.value, 2)
        self.assertEqual(ThreatLevel.HIGH.value, 3)
        self.assertEqual(ThreatLevel.CRITICAL.value, 4)
    
    def test_anomaly_types(self):
        """Test anomaly type enumeration"""
        self.assertIn(AnomalyType.VELOCITY_ANOMALY, AnomalyType)
        self.assertIn(AnomalyType.GEOGRAPHIC_ANOMALY, AnomalyType)
        self.assertIn(AnomalyType.UNUSUAL_TRANSACTION_PATTERN, AnomalyType)
    
    def test_health_monitor(self):
        """Test system health monitor"""
        async def run_test():
            monitor = SystemHealthMonitor()
            
            # Update metrics
            test_metrics = {
                'detection_rate': 0.85,
                'false_positive_rate': 0.08,
                'response_time': 2.5
            }
            
            await monitor.update_metrics(test_metrics)
            
            # Check metrics storage
            self.assertEqual(monitor.health_metrics['detection_rate'], 0.85)
            
            # Generate health report
            report = await monitor.get_health_report()
            self.assertIn('current_metrics', report)
            self.assertIn('system_status', report)
        
        asyncio.run(run_test())


def run_basic_functionality_test():
    """Run a basic functionality test"""
    print("🧪 Running Basic Functionality Test...")
    print("-" * 40)
    
    async def test():
        # Initialize system
        immune_system = FinancialImmuneSystem()
        await immune_system.start_system()
        
        print("✅ System initialization successful")
        
        # Process test transaction
        transaction = await create_sample_transaction()
        result = await immune_system.process_transaction(transaction)
        
        print(f"✅ Transaction processing successful: {result['status']}")
        
        # Check system status
        status = await immune_system.get_system_status()
        print(f"✅ System status check successful: {status['system_info']['status']}")
        
        print("🎉 All basic functionality tests passed!")
        
        return True
    
    try:
        return asyncio.run(test())
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False


def main():
    """Main test function"""
    print("🦠 Financial Immune System - Test Suite")
    print("=" * 50)
    
    # Run basic functionality test first
    if not run_basic_functionality_test():
        print("❌ Basic functionality test failed. Skipping unit tests.")
        return
    
    print("\n🔬 Running Unit Tests...")
    print("-" * 30)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestFinancialImmuneSystem))
    suite.addTests(loader.loadTestsFromTestCase(TestSystemComponents))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n📊 Test Summary")
    print("-" * 20)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed. Check output above for details.")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Tests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        exit(1)
