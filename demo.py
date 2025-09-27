#!/usr/bin/env python3
"""
Financial Immune System - Interactive Demo
==========================================

An interactive demonstration of the Financial Immune System's capabilities.
Run this script to see the system in action with various threat scenarios.
"""

import asyncio
import time
from datetime import datetime
import numpy as np
from typing import List

from immune_system_app import FinancialImmuneSystem, create_sample_transaction
from financial_immune_system import AnomalyType, ThreatLevel


class InteractiveDemo:
    """Interactive demonstration of the Financial Immune System"""
    
    def __init__(self):
        self.immune_system = None
        self.demo_users = [
            "alice_2024",
            "bob_merchant", 
            "charlie_traveler",
            "diana_investor",
            "eve_student"
        ]
    
    async def initialize_system(self):
        """Initialize the immune system for demo"""
        print("🦠 Initializing Financial Immune System...")
        print("=" * 60)
        
        self.immune_system = FinancialImmuneSystem()
        await self.immune_system.start_system()
        
        print("✅ System initialized successfully!")
        print("🛡️  All immune components are active and ready")
        print()
        
        # Show initial system status
        await self.show_system_status()
    
    async def show_system_status(self):
        """Display current system status"""
        status = await self.immune_system.get_system_status()
        
        print("📊 SYSTEM STATUS")
        print("-" * 30)
        print(f"System Health: {status['system_info']['status'].upper()}")
        print(f"Uptime: {status['system_info']['uptime_seconds']:.0f} seconds")
        print(f"Transactions Processed: {status['performance_metrics']['transactions_processed']}")
        print(f"Threats Detected: {status['performance_metrics']['threats_detected']}")
        print(f"Active Antibodies: {status['active_antibodies_count']}")
        print(f"Network Health: {status['network_status']['network_health']:.1%}")
        print()
    
    async def demo_normal_transactions(self):
        """Demonstrate normal transaction processing"""
        print("💳 DEMO: Normal Transaction Processing")
        print("-" * 40)
        print("Processing typical user transactions...")
        print()
        
        # Process several normal transactions
        for i in range(5):
            user = np.random.choice(self.demo_users)
            transaction = await create_sample_transaction(
                user_id=user,
                amount=np.random.uniform(25, 500),
                location=np.random.choice(["New York", "Los Angeles", "Chicago"]),
                merchant=np.random.choice(["Starbucks", "Amazon", "Walmart", "Target"])
            )
            
            result = await self.immune_system.process_transaction(transaction)
            
            status_emoji = {
                'approved': '✅',
                'approved_with_conditions': '⚠️',
                'flagged': '🚩',
                'blocked': '🚫'
            }.get(result['status'], '❓')
            
            print(f"{status_emoji} {user}: ${transaction.amount:.2f} at {transaction.merchant} - {result['status']}")
            
            if result['threats_detected'] > 0:
                print(f"   └─ {result['threats_detected']} threat(s) detected, risk score: {result['risk_score']:.1f}")
            
            await asyncio.sleep(0.5)  # Small delay for readability
        
        print()
        await self.show_system_status()
    
    async def demo_velocity_attack(self):
        """Demonstrate velocity attack detection"""
        print("🚨 DEMO: Velocity Attack Detection")
        print("-" * 40)
        print("Simulating rapid-fire transaction attack...")
        print()
        
        attacker_user = "suspicious_user_001"
        
        for i in range(15):
            transaction = await create_sample_transaction(
                user_id=attacker_user,
                amount=np.random.uniform(10, 100),
                location="New York",
                merchant=np.random.choice(["QuickMart", "FastFood", "GasPump"])
            )
            
            result = await self.immune_system.process_transaction(transaction)
            
            print(f"Transaction {i+1:2d}: ${transaction.amount:6.2f} - {result['status']}", end="")
            
            if result['threats_detected'] > 0:
                print(f" 🚨 THREAT DETECTED! Risk: {result['risk_score']:.1f}")
                print("   └─ Velocity anomaly detected - implementing countermeasures")
                
                # Show generated antibodies
                if result['actions_taken']:
                    for action in result['actions_taken']:
                        print(f"   └─ Action: {action['response_type']}")
                
                break
            else:
                print(" ✅ Normal")
            
            await asyncio.sleep(0.2)
        
        print()
        await self.show_system_status()
    
    async def demo_geographic_anomaly(self):
        """Demonstrate geographic anomaly detection"""
        print("🌍 DEMO: Geographic Anomaly Detection")
        print("-" * 40)
        print("Simulating transactions from unusual locations...")
        print()
        
        # Establish normal pattern for user
        regular_user = "charlie_traveler"
        
        print("Establishing normal pattern...")
        for i in range(3):
            transaction = await create_sample_transaction(
                user_id=regular_user,
                amount=np.random.uniform(50, 200),
                location="San Francisco",
                merchant=np.random.choice(["Local Cafe", "Grocery Store", "Gas Station"])
            )
            
            result = await self.immune_system.process_transaction(transaction)
            print(f"✅ Normal transaction: ${transaction.amount:.2f} in {transaction.location}")
            await asyncio.sleep(0.3)
        
        print("\nNow simulating suspicious geographic activity...")
        
        # Suspicious transactions from different locations
        suspicious_locations = ["Tokyo", "London", "Sydney", "Mumbai"]
        
        for location in suspicious_locations:
            transaction = await create_sample_transaction(
                user_id=regular_user,
                amount=np.random.uniform(1000, 5000),
                location=location,
                merchant="Unknown Merchant"
            )
            
            result = await self.immune_system.process_transaction(transaction)
            
            if result['threats_detected'] > 0:
                print(f"🚨 GEOGRAPHIC ANOMALY: ${transaction.amount:.2f} in {location}")
                print(f"   └─ Risk score: {result['risk_score']:.1f}, Status: {result['status']}")
                
                for action in result['actions_taken']:
                    print(f"   └─ Response: {action['response_type']}")
                break
            else:
                print(f"✅ Transaction approved: ${transaction.amount:.2f} in {location}")
            
            await asyncio.sleep(0.5)
        
        print()
        await self.show_system_status()
    
    async def demo_amount_anomaly(self):
        """Demonstrate large amount anomaly detection"""
        print("💰 DEMO: Amount Anomaly Detection")
        print("-" * 40)
        print("Simulating unusually large transaction...")
        print()
        
        # Establish spending pattern
        normal_user = "diana_investor"
        
        print("Establishing normal spending pattern...")
        normal_amounts = [45.67, 123.45, 78.90, 234.56, 89.12]
        
        for amount in normal_amounts:
            transaction = await create_sample_transaction(
                user_id=normal_user,
                amount=amount,
                location="Boston",
                merchant=np.random.choice(["Coffee Shop", "Bookstore", "Restaurant"])
            )
            
            result = await self.immune_system.process_transaction(transaction)
            print(f"✅ Normal: ${amount:.2f} - {result['status']}")
            await asyncio.sleep(0.2)
        
        print("\nNow processing unusually large transaction...")
        
        # Large anomalous transaction
        large_transaction = await create_sample_transaction(
            user_id=normal_user,
            amount=75000.00,  # Much larger than normal
            location="Boston",
            merchant="Luxury Car Dealer"
        )
        
        result = await self.immune_system.process_transaction(large_transaction)
        
        if result['threats_detected'] > 0:
            print(f"🚨 AMOUNT ANOMALY DETECTED!")
            print(f"   └─ Amount: ${large_transaction.amount:,.2f}")
            print(f"   └─ Risk score: {result['risk_score']:.1f}")
            print(f"   └─ Status: {result['status']}")
            
            for action in result['actions_taken']:
                print(f"   └─ Action: {action['response_type']}")
                if 'details' in action:
                    for key, value in action['details'].items():
                        print(f"      • {key}: {value}")
        else:
            print(f"✅ Large transaction approved: ${large_transaction.amount:,.2f}")
        
        print()
        await self.show_system_status()
    
    async def demo_account_takeover(self):
        """Demonstrate account takeover detection"""
        print("🔒 DEMO: Account Takeover Detection")
        print("-" * 40)
        print("Simulating account takeover scenario...")
        print()
        
        victim_user = "alice_2024"
        
        # Normal pattern
        print("Normal user behavior:")
        transaction = await create_sample_transaction(
            user_id=victim_user,
            amount=85.50,
            location="Seattle",
            merchant="Regular Store"
        )
        
        result = await self.immune_system.process_transaction(transaction)
        print(f"✅ Normal: ${transaction.amount:.2f} in {transaction.location}")
        
        await asyncio.sleep(0.5)
        
        print("\nSuspicious takeover activity detected:")
        
        # Rapid diverse transactions (takeover pattern)
        takeover_locations = ["Miami", "Las Vegas", "Phoenix", "Denver"]
        takeover_merchants = ["Cash Advance", "Pawn Shop", "Casino", "ATM Withdrawal"]
        
        for i, (location, merchant) in enumerate(zip(takeover_locations, takeover_merchants)):
            transaction = await create_sample_transaction(
                user_id=victim_user,
                amount=np.random.uniform(500, 2000),
                location=location,
                merchant=merchant
            )
            
            result = await self.immune_system.process_transaction(transaction)
            
            print(f"Transaction {i+1}: ${transaction.amount:.2f} in {location} at {merchant}")
            
            if result['threats_detected'] > 0:
                print(f"🚨 ACCOUNT TAKEOVER DETECTED!")
                print(f"   └─ Multiple diverse locations and merchants")
                print(f"   └─ Risk score: {result['risk_score']:.1f}")
                print(f"   └─ Status: {result['status']}")
                
                for action in result['actions_taken']:
                    print(f"   └─ Response: {action['response_type']}")
                break
            
            await asyncio.sleep(0.3)
        
        print()
        await self.show_system_status()
    
    async def demo_adaptive_learning(self):
        """Demonstrate adaptive learning capabilities"""
        print("🧠 DEMO: Adaptive Learning & Memory")
        print("-" * 40)
        print("Demonstrating how the system learns and adapts...")
        print()
        
        # Show current antibodies
        print(f"Current active antibodies: {len(self.immune_system.active_antibodies)}")
        
        if self.immune_system.active_antibodies:
            print("Active antibody types:")
            for antibody_id, antibody in list(self.immune_system.active_antibodies.items())[:3]:
                print(f"  • {antibody.name} (Effectiveness: {antibody.effectiveness_score:.2%})")
        
        print()
        
        # Show immune memory
        memory_count = len(self.immune_system.immune_memory.memory_store)
        print(f"Immune memory entries: {memory_count}")
        
        if memory_count > 0:
            print("System has learned from previous encounters and will:")
            print("  • Recognize similar threat patterns faster")
            print("  • Apply appropriate countermeasures automatically")
            print("  • Adapt antibody sensitivity based on performance")
            print("  • Share immunity across the entire network")
        
        print()
    
    async def demo_network_immunity(self):
        """Demonstrate network-wide immunity distribution"""
        print("🕸️ DEMO: Network-wide Immunity Distribution")
        print("-" * 40)
        print("Showing how immunity spreads across the network...")
        print()
        
        # Show network status
        network_status = await self.immune_system.distribution_network.get_network_status()
        
        print(f"Network nodes: {network_status['total_nodes']}")
        print(f"Healthy nodes: {network_status['healthy_nodes']}")
        print(f"Network health: {network_status['network_health']:.1%}")
        print(f"Total antibodies distributed: {network_status['total_antibodies']}")
        
        print("\nRegistered network nodes:")
        for node_id, node_info in self.immune_system.distribution_network.network_nodes.items():
            status_emoji = "🟢" if node_info['health_status'] == 'healthy' else "🔴"
            print(f"  {status_emoji} {node_id} ({node_info['info']['type']})")
        
        print("\nWhen a threat is detected:")
        print("  1. 🔍 Local detection engine identifies the threat")
        print("  2. 💉 Antibody is generated for the specific threat pattern")
        print("  3. 📡 Antibody is distributed to all network nodes")
        print("  4. 🛡️ All nodes gain immunity to this threat type")
        print("  5. 🧠 System learns and adapts for future encounters")
        
        print()
    
    async def show_final_report(self):
        """Show final system report"""
        print("📋 FINAL SYSTEM REPORT")
        print("=" * 60)
        
        # Generate comprehensive threat report
        threat_report = await self.immune_system.generate_threat_report(hours=1)
        
        print(f"Total threats detected: {threat_report['total_threats']}")
        print()
        
        if threat_report['threat_by_type']:
            print("Threats by type:")
            for threat_type, count in threat_report['threat_by_type'].items():
                print(f"  • {threat_type}: {count}")
            print()
        
        if threat_report['threat_by_level']:
            print("Threats by severity:")
            for level, count in threat_report['threat_by_level'].items():
                print(f"  • {level}: {count}")
            print()
        
        if threat_report['top_risk_factors']:
            print("Top risk factors:")
            for factor, count in list(threat_report['top_risk_factors'].items())[:5]:
                print(f"  • {factor}: {count}")
            print()
        
        # Final system status
        await self.show_system_status()
        
        print("🎉 Demo completed successfully!")
        print("The Financial Immune System is now protecting your network.")
        print()
        print("Next steps:")
        print("  • Run 'streamlit run dashboard.py' for the web interface")
        print("  • Integrate with your existing transaction processing")
        print("  • Customize detection algorithms for your specific needs")
        print("  • Monitor system performance and adapt as needed")
    
    async def run_full_demo(self):
        """Run the complete interactive demo"""
        print("🦠 FINANCIAL IMMUNE SYSTEM - INTERACTIVE DEMO")
        print("=" * 60)
        print("This demo will showcase the system's capabilities through")
        print("various fraud detection scenarios inspired by biological immunity.")
        print()
        
        input("Press Enter to start the demo...")
        print()
        
        # Initialize system
        await self.initialize_system()
        
        # Run demo scenarios
        demos = [
            ("Normal Transactions", self.demo_normal_transactions),
            ("Velocity Attack", self.demo_velocity_attack),
            ("Geographic Anomaly", self.demo_geographic_anomaly),
            ("Amount Anomaly", self.demo_amount_anomaly),
            ("Account Takeover", self.demo_account_takeover),
            ("Adaptive Learning", self.demo_adaptive_learning),
            ("Network Immunity", self.demo_network_immunity),
        ]
        
        for demo_name, demo_func in demos:
            print(f"\n🔬 Starting demo: {demo_name}")
            input("Press Enter to continue...")
            await demo_func()
            time.sleep(1)
        
        # Final report
        await self.show_final_report()


async def main():
    """Main demo function"""
    demo = InteractiveDemo()
    await demo.run_full_demo()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user. Thank you for trying Financial Immune System!")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("Please check the system requirements and try again.")
