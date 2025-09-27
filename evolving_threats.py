"""
Evolving Financial Threats System
=================================

Advanced threat system where financial viruses can evolve, adapt, and develop
resistance to antibodies. This creates a dynamic arms race between threats
and defenses, similar to biological virus evolution.
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


class EvolutionPressure(Enum):
    """Types of evolutionary pressure on threats"""
    ANTIBODY_RESISTANCE = "antibody_resistance"
    DETECTION_EVASION = "detection_evasion"
    CAMOUFLAGE = "camouflage"
    VIRULENCE = "virulence"
    TRANSMISSION = "transmission"


@dataclass
class GeneticMutation:
    """A genetic mutation in a threat"""
    mutation_id: str
    mutation_type: str
    target_gene: str
    effect_strength: float
    timestamp: datetime
    success_rate: float = 0.0


@dataclass
class ResistanceGene:
    """Gene that provides resistance to specific antibodies"""
    gene_id: str
    antibody_signature: str
    resistance_strength: float
    acquisition_date: datetime
    effectiveness: float
    energy_cost: float  # Resistance comes at a cost


@dataclass
class CamouflageGene:
    """Gene that helps threats blend in with normal behavior"""
    gene_id: str
    camouflage_type: str
    mimicry_pattern: Dict[str, Any]
    detection_evasion: float
    stability: float


class EvolvingThreat:
    """
    An evolving financial threat that can adapt and develop resistance
    
    Features:
    - Genetic mutations in response to pressure
    - Resistance to specific antibodies
    - Camouflage techniques
    - Virulence adaptation
    - Horizontal gene transfer between threats
    """
    
    def __init__(self, base_pathogen: FinancialPathogen):
        self.threat_id = str(uuid.uuid4())
        self.base_pathogen = base_pathogen
        self.generation = 1
        self.parent_id = None
        self.children_ids: List[str] = []
        
        # Genetic components
        self.resistance_genes: Dict[str, ResistanceGene] = {}
        self.camouflage_genes: Dict[str, CamouflageGene] = {}
        self.mutations: List[GeneticMutation] = []
        
        # Evolution parameters
        self.mutation_rate = 0.05
        self.fitness_score = 1.0
        self.energy_level = 100.0
        self.adaptation_memory: Dict[str, float] = {}
        
        # Behavioral traits
        self.stealth_level = 0.0
        self.virulence = base_pathogen.threat_level.value / 4.0
        self.transmission_rate = 0.1
        self.detection_evasion = 0.0
        
        # Evolution history
        self.blocked_by_antibodies: List[str] = []
        self.successful_attacks: List[str] = []
        self.evolution_events: List[Dict[str, Any]] = []
        
        logger.info(f"Created evolving threat {self.threat_id} from {base_pathogen.anomaly_type.value}")
    
    async def encounter_antibody(self, antibody: Antibody, outcome: bool) -> Dict[str, Any]:
        """Process encounter with an antibody and potentially evolve"""
        encounter_data = {
            "antibody_id": antibody.id,
            "antibody_signature": antibody.pathogen_signature,
            "outcome": outcome,
            "timestamp": datetime.now(),
            "pre_evolution_fitness": self.fitness_score
        }
        
        if not outcome:  # Antibody was successful (threat was blocked)
            self.blocked_by_antibodies.append(antibody.id)
            
            # Apply evolutionary pressure
            pressure_strength = antibody.effectiveness_score
            await self._apply_evolutionary_pressure(
                EvolutionPressure.ANTIBODY_RESISTANCE,
                pressure_strength,
                antibody
            )
            
            # Reduce fitness temporarily
            self.fitness_score *= 0.9
            
        else:  # Threat was successful
            self.successful_attacks.append(antibody.id)
            self.fitness_score *= 1.05
        
        encounter_data["post_evolution_fitness"] = self.fitness_score
        self.evolution_events.append(encounter_data)
        
        return encounter_data
    
    async def _apply_evolutionary_pressure(self, pressure_type: EvolutionPressure, 
                                         strength: float, context: Any = None):
        """Apply evolutionary pressure and potentially trigger mutations"""
        
        # Calculate mutation probability
        mutation_prob = self.mutation_rate * strength
        
        if np.random.random() < mutation_prob:
            await self._mutate(pressure_type, strength, context)
    
    async def _mutate(self, pressure_type: EvolutionPressure, strength: float, context: Any = None):
        """Perform genetic mutation in response to pressure"""
        
        mutation_id = str(uuid.uuid4())
        
        if pressure_type == EvolutionPressure.ANTIBODY_RESISTANCE:
            await self._develop_antibody_resistance(mutation_id, context, strength)
            
        elif pressure_type == EvolutionPressure.DETECTION_EVASION:
            await self._develop_detection_evasion(mutation_id, strength)
            
        elif pressure_type == EvolutionPressure.CAMOUFLAGE:
            await self._develop_camouflage(mutation_id, strength)
            
        elif pressure_type == EvolutionPressure.VIRULENCE:
            await self._mutate_virulence(mutation_id, strength)
            
        elif pressure_type == EvolutionPressure.TRANSMISSION:
            await self._mutate_transmission(mutation_id, strength)
        
        # Record mutation
        mutation = GeneticMutation(
            mutation_id=mutation_id,
            mutation_type=pressure_type.value,
            target_gene="various",
            effect_strength=strength,
            timestamp=datetime.now()
        )
        
        self.mutations.append(mutation)
        self.generation += 1
        
        # Consume energy for mutation
        self.energy_level -= strength * 10
        
        logger.info(f"Threat {self.threat_id} mutated: {pressure_type.value} (strength: {strength:.2f})")
    
    async def _develop_antibody_resistance(self, mutation_id: str, antibody: Antibody, strength: float):
        """Develop resistance to a specific antibody"""
        if not antibody:
            return
        
        resistance_gene = ResistanceGene(
            gene_id=mutation_id,
            antibody_signature=antibody.pathogen_signature,
            resistance_strength=min(strength, 0.9),  # Max 90% resistance
            acquisition_date=datetime.now(),
            effectiveness=0.1,  # Starts low, improves with use
            energy_cost=strength * 5  # Resistance is expensive
        )
        
        self.resistance_genes[antibody.pathogen_signature] = resistance_gene
        
        # Update adaptation memory
        self.adaptation_memory[antibody.pathogen_signature] = strength
    
    async def _develop_detection_evasion(self, mutation_id: str, strength: float):
        """Develop better detection evasion capabilities"""
        self.detection_evasion = min(self.detection_evasion + strength * 0.1, 0.8)
        self.stealth_level = min(self.stealth_level + strength * 0.05, 0.9)
        
        # Reduce attack signature visibility
        self.base_pathogen.confidence_score *= (1 - strength * 0.1)
    
    async def _develop_camouflage(self, mutation_id: str, strength: float):
        """Develop camouflage to blend in with normal behavior"""
        camouflage_types = [
            "amount_mimicry",
            "timing_mimicry", 
            "location_mimicry",
            "merchant_mimicry",
            "behavioral_mimicry"
        ]
        
        camouflage_type = np.random.choice(camouflage_types)
        
        # Create mimicry pattern based on successful normal transactions
        mimicry_pattern = await self._generate_mimicry_pattern(camouflage_type)
        
        camouflage_gene = CamouflageGene(
            gene_id=mutation_id,
            camouflage_type=camouflage_type,
            mimicry_pattern=mimicry_pattern,
            detection_evasion=strength * 0.2,
            stability=0.5
        )
        
        self.camouflage_genes[camouflage_type] = camouflage_gene
    
    async def _generate_mimicry_pattern(self, camouflage_type: str) -> Dict[str, Any]:
        """Generate a mimicry pattern for camouflage"""
        patterns = {
            "amount_mimicry": {
                "target_amounts": [50, 100, 200, 500],
                "variance": 0.1,
                "round_numbers": True
            },
            "timing_mimicry": {
                "preferred_hours": [9, 12, 15, 18],
                "avoid_hours": [2, 3, 4, 5],
                "business_days_only": True
            },
            "location_mimicry": {
                "common_locations": ["New York", "Los Angeles", "Chicago"],
                "avoid_suspicious": True
            },
            "merchant_mimicry": {
                "legitimate_merchants": ["Amazon", "Walmart", "Target", "Starbucks"],
                "avoid_cash_advance": True
            },
            "behavioral_mimicry": {
                "transaction_spacing": "30-120 minutes",
                "daily_limit": 5,
                "weekly_pattern": "consistent"
            }
        }
        
        return patterns.get(camouflage_type, {})
    
    async def _mutate_virulence(self, mutation_id: str, strength: float):
        """Mutate virulence (damage potential)"""
        # Virulence can increase or decrease
        direction = 1 if np.random.random() > 0.3 else -1
        virulence_change = direction * strength * 0.1
        
        self.virulence = max(0.1, min(self.virulence + virulence_change, 1.0))
        
        # Update base pathogen threat level
        if self.virulence > 0.8:
            self.base_pathogen.threat_level = ThreatLevel.CRITICAL
        elif self.virulence > 0.6:
            self.base_pathogen.threat_level = ThreatLevel.HIGH
        elif self.virulence > 0.4:
            self.base_pathogen.threat_level = ThreatLevel.MEDIUM
        else:
            self.base_pathogen.threat_level = ThreatLevel.LOW
    
    async def _mutate_transmission(self, mutation_id: str, strength: float):
        """Mutate transmission rate (spread capability)"""
        self.transmission_rate = min(self.transmission_rate + strength * 0.05, 0.5)
    
    async def calculate_resistance(self, antibody: Antibody) -> float:
        """Calculate resistance level to a specific antibody"""
        if antibody.pathogen_signature not in self.resistance_genes:
            return 0.0
        
        resistance_gene = self.resistance_genes[antibody.pathogen_signature]
        
        # Base resistance
        resistance = resistance_gene.resistance_strength
        
        # Improve with experience
        resistance *= (1 + resistance_gene.effectiveness)
        
        # Decay over time if not used
        days_since_acquisition = (datetime.now() - resistance_gene.acquisition_date).days
        if days_since_acquisition > 30:
            decay_factor = 0.99 ** (days_since_acquisition - 30)
            resistance *= decay_factor
        
        return min(resistance, 0.95)  # Max 95% resistance
    
    async def apply_camouflage(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply camouflage to make the threat look more normal"""
        camouflaged_data = transaction_data.copy()
        
        for camouflage_type, gene in self.camouflage_genes.items():
            pattern = gene.mimicry_pattern
            evasion_strength = gene.detection_evasion
            
            if camouflage_type == "amount_mimicry" and "amount" in camouflaged_data:
                target_amounts = pattern.get("target_amounts", [])
                if target_amounts:
                    # Shift amount towards a common value
                    target = np.random.choice(target_amounts)
                    current = camouflaged_data["amount"]
                    camouflaged_data["amount"] = current + (target - current) * evasion_strength
            
            elif camouflage_type == "timing_mimicry" and "timestamp" in camouflaged_data:
                preferred_hours = pattern.get("preferred_hours", [])
                if preferred_hours:
                    # Adjust timing towards preferred hours
                    current_hour = camouflaged_data["timestamp"].hour
                    target_hour = min(preferred_hours, key=lambda x: abs(x - current_hour))
                    # This would require more complex timestamp manipulation
            
            elif camouflage_type == "location_mimicry" and "location" in camouflaged_data:
                common_locations = pattern.get("common_locations", [])
                if common_locations and np.random.random() < evasion_strength:
                    camouflaged_data["location"] = np.random.choice(common_locations)
            
            elif camouflage_type == "merchant_mimicry" and "merchant" in camouflaged_data:
                legitimate_merchants = pattern.get("legitimate_merchants", [])
                if legitimate_merchants and np.random.random() < evasion_strength:
                    camouflaged_data["merchant"] = np.random.choice(legitimate_merchants)
        
        return camouflaged_data
    
    async def reproduce(self, partner: Optional['EvolvingThreat'] = None) -> 'EvolvingThreat':
        """Create offspring threat through reproduction"""
        
        # Create child pathogen
        child_pathogen = FinancialPathogen(
            id=str(uuid.uuid4()),
            anomaly_type=self.base_pathogen.anomaly_type,
            threat_level=self.base_pathogen.threat_level,
            confidence_score=self.base_pathogen.confidence_score,
            affected_transactions=[],
            detection_timestamp=datetime.now(),
            source_pattern=self.base_pathogen.source_pattern.copy(),
            risk_factors=self.base_pathogen.risk_factors.copy()
        )
        
        # Create child threat
        child = EvolvingThreat(child_pathogen)
        child.parent_id = self.threat_id
        child.generation = self.generation + 1
        
        # Inherit traits
        child.mutation_rate = self.mutation_rate * np.random.uniform(0.8, 1.2)
        child.fitness_score = self.fitness_score * 0.9  # Slight fitness cost for reproduction
        child.stealth_level = self.stealth_level * np.random.uniform(0.9, 1.1)
        child.virulence = self.virulence * np.random.uniform(0.9, 1.1)
        child.detection_evasion = self.detection_evasion * np.random.uniform(0.9, 1.1)
        
        # Inherit some resistance genes (with mutations)
        for signature, gene in self.resistance_genes.items():
            if np.random.random() < 0.7:  # 70% inheritance chance
                inherited_gene = ResistanceGene(
                    gene_id=str(uuid.uuid4()),
                    antibody_signature=signature,
                    resistance_strength=gene.resistance_strength * np.random.uniform(0.8, 1.2),
                    acquisition_date=datetime.now(),
                    effectiveness=gene.effectiveness * 0.5,  # Reduced effectiveness initially
                    energy_cost=gene.energy_cost
                )
                child.resistance_genes[signature] = inherited_gene
        
        # Inherit some camouflage genes
        for camo_type, gene in self.camouflage_genes.items():
            if np.random.random() < 0.6:  # 60% inheritance chance
                inherited_gene = CamouflageGene(
                    gene_id=str(uuid.uuid4()),
                    camouflage_type=camo_type,
                    mimicry_pattern=gene.mimicry_pattern.copy(),
                    detection_evasion=gene.detection_evasion * np.random.uniform(0.8, 1.2),
                    stability=gene.stability * 0.9
                )
                child.camouflage_genes[camo_type] = inherited_gene
        
        # Sexual reproduction with partner
        if partner:
            await self._sexual_reproduction(child, partner)
        
        # Add to children list
        self.children_ids.append(child.threat_id)
        
        # Consume energy for reproduction
        self.energy_level -= 30
        
        logger.info(f"Threat {self.threat_id} reproduced, created child {child.threat_id}")
        
        return child
    
    async def _sexual_reproduction(self, child: 'EvolvingThreat', partner: 'EvolvingThreat'):
        """Perform sexual reproduction with genetic recombination"""
        
        # Combine resistance genes from both parents
        all_resistance_genes = {**self.resistance_genes, **partner.resistance_genes}
        child.resistance_genes = {}
        
        for signature, gene in all_resistance_genes.items():
            if np.random.random() < 0.5:  # Random selection from parents
                child.resistance_genes[signature] = gene
        
        # Combine camouflage genes
        all_camouflage_genes = {**self.camouflage_genes, **partner.camouflage_genes}
        child.camouflage_genes = {}
        
        for camo_type, gene in all_camouflage_genes.items():
            if np.random.random() < 0.5:
                child.camouflage_genes[camo_type] = gene
        
        # Average traits
        child.virulence = (self.virulence + partner.virulence) / 2
        child.stealth_level = (self.stealth_level + partner.stealth_level) / 2
        child.detection_evasion = (self.detection_evasion + partner.detection_evasion) / 2
    
    async def horizontal_gene_transfer(self, donor: 'EvolvingThreat', gene_type: str):
        """Transfer genes horizontally from another threat"""
        
        if gene_type == "resistance" and donor.resistance_genes:
            # Transfer a random resistance gene
            signature = np.random.choice(list(donor.resistance_genes.keys()))
            donor_gene = donor.resistance_genes[signature]
            
            # Create transferred gene with reduced effectiveness
            transferred_gene = ResistanceGene(
                gene_id=str(uuid.uuid4()),
                antibody_signature=signature,
                resistance_strength=donor_gene.resistance_strength * 0.7,
                acquisition_date=datetime.now(),
                effectiveness=donor_gene.effectiveness * 0.3,
                energy_cost=donor_gene.energy_cost * 1.2
            )
            
            self.resistance_genes[signature] = transferred_gene
            
        elif gene_type == "camouflage" and donor.camouflage_genes:
            # Transfer a random camouflage gene
            camo_type = np.random.choice(list(donor.camouflage_genes.keys()))
            donor_gene = donor.camouflage_genes[camo_type]
            
            transferred_gene = CamouflageGene(
                gene_id=str(uuid.uuid4()),
                camouflage_type=camo_type,
                mimicry_pattern=donor_gene.mimicry_pattern.copy(),
                detection_evasion=donor_gene.detection_evasion * 0.8,
                stability=donor_gene.stability * 0.7
            )
            
            self.camouflage_genes[camo_type] = transferred_gene
        
        # Consume energy for gene transfer
        self.energy_level -= 15
        
        logger.info(f"Horizontal gene transfer: {donor.threat_id} -> {self.threat_id} ({gene_type})")
    
    def get_evolution_summary(self) -> Dict[str, Any]:
        """Get comprehensive evolution summary"""
        return {
            "threat_id": self.threat_id,
            "generation": self.generation,
            "parent_id": self.parent_id,
            "children_count": len(self.children_ids),
            "fitness_score": self.fitness_score,
            "energy_level": self.energy_level,
            "mutations_count": len(self.mutations),
            "resistance_genes": len(self.resistance_genes),
            "camouflage_genes": len(self.camouflage_genes),
            "stealth_level": self.stealth_level,
            "virulence": self.virulence,
            "detection_evasion": self.detection_evasion,
            "successful_attacks": len(self.successful_attacks),
            "blocked_attacks": len(self.blocked_by_antibodies),
            "evolution_events": len(self.evolution_events)
        }


class ThreatEcosystem:
    """Manages the ecosystem of evolving threats"""
    
    def __init__(self):
        self.threats: Dict[str, EvolvingThreat] = {}
        self.threat_families: Dict[str, List[str]] = defaultdict(list)
        self.ecosystem_pressure = 0.1
        self.generation_counter = 0
    
    async def introduce_threat(self, pathogen: FinancialPathogen) -> EvolvingThreat:
        """Introduce a new threat into the ecosystem"""
        threat = EvolvingThreat(pathogen)
        self.threats[threat.threat_id] = threat
        
        # Add to family
        family_key = pathogen.anomaly_type.value
        self.threat_families[family_key].append(threat.threat_id)
        
        logger.info(f"Introduced new threat {threat.threat_id} into ecosystem")
        return threat
    
    async def simulate_ecosystem_evolution(self, time_steps: int = 100):
        """Simulate ecosystem evolution over time"""
        
        for step in range(time_steps):
            # Apply environmental pressures
            await self._apply_environmental_pressure()
            
            # Reproduction cycle
            await self._reproduction_cycle()
            
            # Natural selection
            await self._natural_selection()
            
            # Horizontal gene transfer
            await self._horizontal_gene_transfer_events()
            
            self.generation_counter += 1
            
            if step % 10 == 0:
                logger.info(f"Ecosystem evolution step {step}, threats: {len(self.threats)}")
    
    async def _apply_environmental_pressure(self):
        """Apply environmental pressure to all threats"""
        for threat in self.threats.values():
            # Random environmental challenges
            if np.random.random() < 0.1:
                pressure_type = np.random.choice(list(EvolutionPressure))
                strength = np.random.uniform(0.1, 0.5)
                await threat._apply_evolutionary_pressure(pressure_type, strength)
    
    async def _reproduction_cycle(self):
        """Handle reproduction for fit threats"""
        reproducing_threats = [
            threat for threat in self.threats.values()
            if threat.fitness_score > 1.2 and threat.energy_level > 50
        ]
        
        for threat in reproducing_threats:
            if np.random.random() < threat.transmission_rate:
                # Find partner from same family
                family_key = threat.base_pathogen.anomaly_type.value
                family_members = [
                    self.threats[tid] for tid in self.threat_families[family_key]
                    if tid != threat.threat_id and tid in self.threats
                ]
                
                partner = np.random.choice(family_members) if family_members else None
                child = await threat.reproduce(partner)
                
                self.threats[child.threat_id] = child
                self.threat_families[family_key].append(child.threat_id)
    
    async def _natural_selection(self):
        """Remove unfit threats from the ecosystem"""
        threats_to_remove = []
        
        for threat_id, threat in self.threats.items():
            # Remove threats with very low fitness or energy
            if threat.fitness_score < 0.3 or threat.energy_level < 10:
                threats_to_remove.append(threat_id)
        
        for threat_id in threats_to_remove:
            threat = self.threats[threat_id]
            family_key = threat.base_pathogen.anomaly_type.value
            
            # Remove from family
            if threat_id in self.threat_families[family_key]:
                self.threat_families[family_key].remove(threat_id)
            
            # Remove from ecosystem
            del self.threats[threat_id]
            logger.info(f"Natural selection removed threat {threat_id}")
    
    async def _horizontal_gene_transfer_events(self):
        """Simulate horizontal gene transfer between threats"""
        threat_list = list(self.threats.values())
        
        for _ in range(max(1, len(threat_list) // 10)):  # 10% of threats participate
            if len(threat_list) < 2:
                break
            
            donor, recipient = np.random.choice(threat_list, 2, replace=False)
            gene_type = np.random.choice(["resistance", "camouflage"])
            
            await recipient.horizontal_gene_transfer(donor, gene_type)
    
    def get_ecosystem_stats(self) -> Dict[str, Any]:
        """Get comprehensive ecosystem statistics"""
        if not self.threats:
            return {"total_threats": 0}
        
        fitness_scores = [t.fitness_score for t in self.threats.values()]
        generations = [t.generation for t in self.threats.values()]
        
        family_stats = {}
        for family, members in self.threat_families.items():
            active_members = [mid for mid in members if mid in self.threats]
            family_stats[family] = {
                "active_threats": len(active_members),
                "avg_fitness": np.mean([self.threats[mid].fitness_score for mid in active_members]) if active_members else 0
            }
        
        return {
            "total_threats": len(self.threats),
            "generation_counter": self.generation_counter,
            "avg_fitness": np.mean(fitness_scores),
            "max_fitness": max(fitness_scores),
            "min_fitness": min(fitness_scores),
            "avg_generation": np.mean(generations),
            "max_generation": max(generations),
            "family_stats": family_stats,
            "total_resistance_genes": sum(len(t.resistance_genes) for t in self.threats.values()),
            "total_camouflage_genes": sum(len(t.camouflage_genes) for t in self.threats.values())
        }


# Demo function
async def demo_evolving_threats():
    """Demonstrate the evolving threats system"""
    print("🦠 Evolving Financial Threats Demo")
    print("=" * 40)
    
    # Create ecosystem
    ecosystem = ThreatEcosystem()
    
    # Create initial threat
    from financial_immune_system import FinancialPathogen, AnomalyType, ThreatLevel
    
    base_pathogen = FinancialPathogen(
        id="initial_threat",
        anomaly_type=AnomalyType.VELOCITY_ANOMALY,
        threat_level=ThreatLevel.MEDIUM,
        confidence_score=0.8,
        affected_transactions=["tx1", "tx2"],
        detection_timestamp=datetime.now(),
        source_pattern={"velocity": "high"},
        risk_factors=["Multiple rapid transactions"]
    )
    
    threat = await ecosystem.introduce_threat(base_pathogen)
    print(f"Introduced initial threat: {threat.threat_id}")
    
    # Simulate antibody encounters
    from financial_immune_system import Antibody
    
    antibody = Antibody(
        id="test_antibody",
        name="Velocity Limiter",
        pathogen_signature="velocity_pattern_123",
        rule_logic={"type": "velocity_limit"},
        effectiveness_score=0.8,
        creation_timestamp=datetime.now(),
        last_updated=datetime.now(),
        activation_count=0,
        success_rate=0.0
    )
    
    print("\nSimulating antibody encounters...")
    for i in range(5):
        outcome = np.random.random() > 0.6  # 40% success rate for antibody
        encounter = await threat.encounter_antibody(antibody, not outcome)  # Invert for threat perspective
        print(f"Encounter {i+1}: {'Blocked' if not outcome else 'Successful'} - Fitness: {threat.fitness_score:.2f}")
    
    # Show evolution summary
    summary = threat.get_evolution_summary()
    print(f"\nThreat Evolution Summary:")
    print(f"Generation: {summary['generation']}")
    print(f"Fitness: {summary['fitness_score']:.2f}")
    print(f"Mutations: {summary['mutations_count']}")
    print(f"Resistance Genes: {summary['resistance_genes']}")
    print(f"Stealth Level: {summary['stealth_level']:.2f}")
    
    # Simulate ecosystem evolution
    print(f"\nSimulating ecosystem evolution...")
    await ecosystem.simulate_ecosystem_evolution(20)
    
    # Show final ecosystem stats
    stats = ecosystem.get_ecosystem_stats()
    print(f"\nEcosystem Statistics:")
    print(f"Total Threats: {stats['total_threats']}")
    print(f"Average Fitness: {stats['avg_fitness']:.2f}")
    print(f"Max Generation: {stats['max_generation']}")
    print(f"Total Resistance Genes: {stats['total_resistance_genes']}")
    
    print("\n🦠 Evolving Threats Demo Complete!")


if __name__ == "__main__":
    asyncio.run(demo_evolving_threats())
