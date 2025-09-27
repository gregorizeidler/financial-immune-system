"""
Financial DNA System
===================

Creates unique financial fingerprints for each user based on their behavioral patterns.
Like biological DNA, each user has a unique financial signature that helps identify
anomalies and potential account takeovers.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import numpy as np
from collections import defaultdict, deque
import hashlib

from financial_immune_system import Transaction

logger = logging.getLogger(__name__)


@dataclass
class FinancialGene:
    """A single financial gene representing a behavioral trait"""
    gene_name: str
    value: float
    confidence: float
    last_updated: datetime
    mutation_rate: float = 0.01


@dataclass
class DNASequence:
    """A sequence of financial genes that make up part of the DNA"""
    sequence_type: str
    genes: Dict[str, FinancialGene]
    stability_score: float
    creation_date: datetime


class FinancialDNA:
    """
    Financial DNA System - Creates unique behavioral fingerprints
    
    Each user's financial DNA consists of multiple sequences:
    - Spending Rhythm (circadian patterns)
    - Merchant Affinity (preferred store types)
    - Amount Distribution (statistical spending patterns)
    - Temporal Patterns (day/week/month cycles)
    - Geographic Preferences (location patterns)
    - Social Connections (transaction network)
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.dna_sequences: Dict[str, DNASequence] = {}
        self.dna_hash = ""
        self.last_evolution = datetime.now()
        self.evolution_count = 0
        self.stability_threshold = 0.8
        
        # Initialize DNA sequences
        self._initialize_dna_sequences()
    
    def _initialize_dna_sequences(self):
        """Initialize all DNA sequences with default values"""
        sequence_types = [
            "spending_rhythm",
            "merchant_affinity", 
            "amount_distribution",
            "temporal_patterns",
            "geographic_preferences",
            "social_connections",
            "risk_tolerance",
            "payment_methods"
        ]
        
        for seq_type in sequence_types:
            self.dna_sequences[seq_type] = DNASequence(
                sequence_type=seq_type,
                genes={},
                stability_score=0.0,
                creation_date=datetime.now()
            )
    
    async def analyze_transaction(self, transaction: Transaction) -> Dict[str, float]:
        """Analyze a transaction and update DNA accordingly"""
        analysis_results = {}
        
        # Analyze spending rhythm (hour of day patterns)
        rhythm_analysis = await self._analyze_spending_rhythm(transaction)
        analysis_results.update(rhythm_analysis)
        
        # Analyze merchant affinity
        merchant_analysis = await self._analyze_merchant_affinity(transaction)
        analysis_results.update(merchant_analysis)
        
        # Analyze amount patterns
        amount_analysis = await self._analyze_amount_distribution(transaction)
        analysis_results.update(amount_analysis)
        
        # Analyze temporal patterns
        temporal_analysis = await self._analyze_temporal_patterns(transaction)
        analysis_results.update(temporal_analysis)
        
        # Analyze geographic preferences
        geo_analysis = await self._analyze_geographic_preferences(transaction)
        analysis_results.update(geo_analysis)
        
        # Update DNA based on analysis
        await self._update_dna(analysis_results, transaction)
        
        return analysis_results
    
    async def _analyze_spending_rhythm(self, transaction: Transaction) -> Dict[str, float]:
        """Analyze circadian spending patterns"""
        hour = transaction.timestamp.hour
        day_of_week = transaction.timestamp.weekday()
        
        # Create rhythm genes
        rhythm_genes = {
            f"hour_{hour}": transaction.amount,
            f"day_{day_of_week}": transaction.amount,
            f"weekend_activity": 1.0 if day_of_week >= 5 else 0.0,
            f"business_hours": 1.0 if 9 <= hour <= 17 else 0.0
        }
        
        return {"spending_rhythm": rhythm_genes}
    
    async def _analyze_merchant_affinity(self, transaction: Transaction) -> Dict[str, float]:
        """Analyze merchant preferences and categories"""
        merchant = transaction.merchant.lower()
        
        # Categorize merchants (simplified)
        merchant_categories = {
            "food": ["restaurant", "cafe", "food", "pizza", "burger"],
            "retail": ["store", "shop", "mall", "target", "walmart"],
            "gas": ["gas", "fuel", "shell", "exxon"],
            "entertainment": ["movie", "theater", "game", "netflix"],
            "travel": ["hotel", "airline", "uber", "taxi"],
            "online": ["amazon", "ebay", "paypal", "online"]
        }
        
        merchant_genes = {}
        for category, keywords in merchant_categories.items():
            if any(keyword in merchant for keyword in keywords):
                merchant_genes[f"category_{category}"] = transaction.amount
                merchant_genes[f"frequency_{category}"] = 1.0
        
        merchant_genes[f"merchant_{hash(merchant) % 1000}"] = transaction.amount
        
        return {"merchant_affinity": merchant_genes}
    
    async def _analyze_amount_distribution(self, transaction: Transaction) -> Dict[str, float]:
        """Analyze statistical patterns in transaction amounts"""
        amount = transaction.amount
        
        # Amount range classification
        amount_genes = {
            "micro_transaction": 1.0 if amount < 10 else 0.0,
            "small_transaction": 1.0 if 10 <= amount < 100 else 0.0,
            "medium_transaction": 1.0 if 100 <= amount < 1000 else 0.0,
            "large_transaction": 1.0 if 1000 <= amount < 10000 else 0.0,
            "huge_transaction": 1.0 if amount >= 10000 else 0.0,
            "round_number": 1.0 if amount == int(amount) else 0.0,
            "amount_variance": amount
        }
        
        return {"amount_distribution": amount_genes}
    
    async def _analyze_temporal_patterns(self, transaction: Transaction) -> Dict[str, float]:
        """Analyze temporal spending patterns"""
        now = transaction.timestamp
        
        temporal_genes = {
            "month_of_year": now.month,
            "day_of_month": now.day,
            "quarter": (now.month - 1) // 3 + 1,
            "is_month_start": 1.0 if now.day <= 5 else 0.0,
            "is_month_end": 1.0 if now.day >= 25 else 0.0,
            "is_payday": 1.0 if now.day in [1, 15] else 0.0
        }
        
        return {"temporal_patterns": temporal_genes}
    
    async def _analyze_geographic_preferences(self, transaction: Transaction) -> Dict[str, float]:
        """Analyze geographic spending patterns"""
        location = transaction.location.lower()
        
        geo_genes = {
            f"location_{hash(location) % 100}": transaction.amount,
            "location_diversity": 1.0,  # Will be calculated over time
            "home_location_preference": 0.5  # Will be learned
        }
        
        return {"geographic_preferences": geo_genes}
    
    async def _update_dna(self, analysis_results: Dict[str, Any], transaction: Transaction):
        """Update DNA sequences based on analysis results"""
        for sequence_type, gene_data in analysis_results.items():
            if sequence_type not in self.dna_sequences:
                continue
            
            sequence = self.dna_sequences[sequence_type]
            
            for gene_name, value in gene_data.items():
                if gene_name in sequence.genes:
                    # Update existing gene
                    gene = sequence.genes[gene_name]
                    
                    # Weighted average with decay
                    decay_factor = 0.95
                    gene.value = (gene.value * decay_factor) + (value * (1 - decay_factor))
                    gene.confidence = min(gene.confidence + 0.01, 1.0)
                    gene.last_updated = datetime.now()
                else:
                    # Create new gene
                    sequence.genes[gene_name] = FinancialGene(
                        gene_name=gene_name,
                        value=value,
                        confidence=0.1,
                        last_updated=datetime.now()
                    )
            
            # Update sequence stability
            await self._update_sequence_stability(sequence)
        
        # Update overall DNA hash
        await self._update_dna_hash()
    
    async def _update_sequence_stability(self, sequence: DNASequence):
        """Calculate and update sequence stability score"""
        if not sequence.genes:
            sequence.stability_score = 0.0
            return
        
        # Calculate stability based on gene confidence and consistency
        total_confidence = sum(gene.confidence for gene in sequence.genes.values())
        avg_confidence = total_confidence / len(sequence.genes)
        
        # Factor in time since creation
        age_days = (datetime.now() - sequence.creation_date).days
        age_factor = min(age_days / 30.0, 1.0)  # Stabilizes over 30 days
        
        sequence.stability_score = avg_confidence * age_factor
    
    async def _update_dna_hash(self):
        """Update the overall DNA hash for quick comparisons"""
        dna_data = {}
        
        for seq_type, sequence in self.dna_sequences.items():
            seq_data = {}
            for gene_name, gene in sequence.genes.items():
                seq_data[gene_name] = {
                    "value": round(gene.value, 4),
                    "confidence": round(gene.confidence, 4)
                }
            dna_data[seq_type] = seq_data
        
        dna_string = json.dumps(dna_data, sort_keys=True)
        self.dna_hash = hashlib.sha256(dna_string.encode()).hexdigest()
    
    async def calculate_anomaly_score(self, transaction: Transaction) -> float:
        """Calculate how anomalous a transaction is based on DNA"""
        analysis = await self.analyze_transaction(transaction)
        total_anomaly = 0.0
        total_weight = 0.0
        
        for sequence_type, gene_data in analysis.items():
            if sequence_type not in self.dna_sequences:
                continue
            
            sequence = self.dna_sequences[sequence_type]
            sequence_anomaly = 0.0
            sequence_weight = sequence.stability_score
            
            for gene_name, observed_value in gene_data.items():
                if gene_name in sequence.genes:
                    expected_gene = sequence.genes[gene_name]
                    expected_value = expected_gene.value
                    confidence = expected_gene.confidence
                    
                    # Calculate deviation
                    if expected_value != 0:
                        deviation = abs(observed_value - expected_value) / abs(expected_value)
                    else:
                        deviation = 1.0 if observed_value != 0 else 0.0
                    
                    # Weight by confidence
                    gene_anomaly = deviation * confidence
                    sequence_anomaly += gene_anomaly
            
            # Average anomaly for this sequence
            if gene_data:
                sequence_anomaly /= len(gene_data)
            
            total_anomaly += sequence_anomaly * sequence_weight
            total_weight += sequence_weight
        
        # Return normalized anomaly score
        return total_anomaly / total_weight if total_weight > 0 else 0.5
    
    async def compare_dna(self, other_dna: 'FinancialDNA') -> float:
        """Compare this DNA with another user's DNA (for fraud detection)"""
        if not other_dna or not other_dna.dna_sequences:
            return 0.0
        
        similarity_scores = []
        
        for seq_type in self.dna_sequences.keys():
            if seq_type not in other_dna.dna_sequences:
                continue
            
            seq1 = self.dna_sequences[seq_type]
            seq2 = other_dna.dna_sequences[seq_type]
            
            # Compare gene values
            common_genes = set(seq1.genes.keys()) & set(seq2.genes.keys())
            if not common_genes:
                continue
            
            gene_similarities = []
            for gene_name in common_genes:
                gene1 = seq1.genes[gene_name]
                gene2 = seq2.genes[gene_name]
                
                # Calculate similarity (inverse of difference)
                if gene1.value == 0 and gene2.value == 0:
                    similarity = 1.0
                elif gene1.value == 0 or gene2.value == 0:
                    similarity = 0.0
                else:
                    diff = abs(gene1.value - gene2.value) / max(abs(gene1.value), abs(gene2.value))
                    similarity = 1.0 - diff
                
                # Weight by confidence
                weight = min(gene1.confidence, gene2.confidence)
                gene_similarities.append(similarity * weight)
            
            if gene_similarities:
                seq_similarity = np.mean(gene_similarities)
                similarity_scores.append(seq_similarity)
        
        return np.mean(similarity_scores) if similarity_scores else 0.0
    
    async def evolve_dna(self, environmental_pressure: float = 0.1):
        """Evolve DNA based on environmental pressures (new fraud patterns)"""
        self.evolution_count += 1
        self.last_evolution = datetime.now()
        
        for sequence in self.dna_sequences.values():
            for gene in sequence.genes.values():
                # Apply mutation based on environmental pressure
                if np.random.random() < gene.mutation_rate * environmental_pressure:
                    mutation_strength = np.random.normal(0, 0.1)
                    gene.value *= (1 + mutation_strength)
                    gene.confidence *= 0.95  # Reduce confidence after mutation
        
        await self._update_dna_hash()
        logger.info(f"DNA evolved for user {self.user_id} - Evolution #{self.evolution_count}")
    
    def get_dna_profile(self) -> Dict[str, Any]:
        """Get a comprehensive DNA profile for analysis"""
        profile = {
            "user_id": self.user_id,
            "dna_hash": self.dna_hash,
            "evolution_count": self.evolution_count,
            "last_evolution": self.last_evolution.isoformat(),
            "sequences": {}
        }
        
        for seq_type, sequence in self.dna_sequences.items():
            profile["sequences"][seq_type] = {
                "stability_score": sequence.stability_score,
                "gene_count": len(sequence.genes),
                "creation_date": sequence.creation_date.isoformat(),
                "top_genes": {}
            }
            
            # Include top 5 genes by confidence
            top_genes = sorted(
                sequence.genes.items(),
                key=lambda x: x[1].confidence,
                reverse=True
            )[:5]
            
            for gene_name, gene in top_genes:
                profile["sequences"][seq_type]["top_genes"][gene_name] = {
                    "value": gene.value,
                    "confidence": gene.confidence
                }
        
        return profile
    
    async def detect_identity_theft(self, recent_transactions: List[Transaction]) -> Dict[str, Any]:
        """Detect potential identity theft based on DNA changes"""
        if len(recent_transactions) < 5:
            return {"risk_score": 0.0, "indicators": []}
        
        # Analyze recent transactions
        recent_anomalies = []
        for transaction in recent_transactions:
            anomaly_score = await self.calculate_anomaly_score(transaction)
            recent_anomalies.append(anomaly_score)
        
        avg_anomaly = np.mean(recent_anomalies)
        max_anomaly = max(recent_anomalies)
        
        # Identity theft indicators
        indicators = []
        risk_score = 0.0
        
        if avg_anomaly > 0.7:
            indicators.append("Sustained high anomaly scores")
            risk_score += 0.3
        
        if max_anomaly > 0.9:
            indicators.append("Extremely anomalous transaction detected")
            risk_score += 0.4
        
        # Check for sudden DNA changes
        stability_scores = [seq.stability_score for seq in self.dna_sequences.values()]
        avg_stability = np.mean(stability_scores)
        
        if avg_stability < 0.5:
            indicators.append("DNA instability detected")
            risk_score += 0.3
        
        return {
            "risk_score": min(risk_score, 1.0),
            "indicators": indicators,
            "avg_anomaly": avg_anomaly,
            "max_anomaly": max_anomaly,
            "dna_stability": avg_stability
        }


class DNADatabase:
    """Database for storing and managing financial DNA profiles"""
    
    def __init__(self):
        self.dna_profiles: Dict[str, FinancialDNA] = {}
        self.similarity_cache: Dict[Tuple[str, str], float] = {}
    
    async def get_or_create_dna(self, user_id: str) -> FinancialDNA:
        """Get existing DNA or create new one for user"""
        if user_id not in self.dna_profiles:
            self.dna_profiles[user_id] = FinancialDNA(user_id)
            logger.info(f"Created new DNA profile for user {user_id}")
        
        return self.dna_profiles[user_id]
    
    async def find_similar_dna(self, target_dna: FinancialDNA, threshold: float = 0.8) -> List[Tuple[str, float]]:
        """Find DNA profiles similar to the target (for fraud detection)"""
        similar_profiles = []
        
        for user_id, dna_profile in self.dna_profiles.items():
            if user_id == target_dna.user_id:
                continue
            
            # Check cache first
            cache_key = (target_dna.user_id, user_id)
            if cache_key in self.similarity_cache:
                similarity = self.similarity_cache[cache_key]
            else:
                similarity = await target_dna.compare_dna(dna_profile)
                self.similarity_cache[cache_key] = similarity
            
            if similarity >= threshold:
                similar_profiles.append((user_id, similarity))
        
        # Sort by similarity
        similar_profiles.sort(key=lambda x: x[1], reverse=True)
        return similar_profiles
    
    async def detect_synthetic_identity(self, user_id: str) -> Dict[str, Any]:
        """Detect if a user might be using a synthetic identity"""
        if user_id not in self.dna_profiles:
            return {"risk_score": 0.5, "reason": "No DNA profile available"}
        
        user_dna = self.dna_profiles[user_id]
        
        # Check DNA maturity
        total_genes = sum(len(seq.genes) for seq in user_dna.dna_sequences.values())
        avg_stability = np.mean([seq.stability_score for seq in user_dna.dna_sequences.values()])
        
        risk_indicators = []
        risk_score = 0.0
        
        # Too few genes for account age
        if total_genes < 20:
            risk_indicators.append("Insufficient behavioral data")
            risk_score += 0.3
        
        # Low stability scores
        if avg_stability < 0.3:
            risk_indicators.append("Unstable behavioral patterns")
            risk_score += 0.2
        
        # Check for similar DNA (possible identity farming)
        similar_profiles = await self.find_similar_dna(user_dna, threshold=0.9)
        if len(similar_profiles) > 2:
            risk_indicators.append(f"DNA similar to {len(similar_profiles)} other users")
            risk_score += 0.4
        
        return {
            "risk_score": min(risk_score, 1.0),
            "indicators": risk_indicators,
            "total_genes": total_genes,
            "avg_stability": avg_stability,
            "similar_users": len(similar_profiles)
        }


# Example usage and testing
async def demo_financial_dna():
    """Demonstrate the Financial DNA system"""
    print("🧬 Financial DNA System Demo")
    print("=" * 40)
    
    # Create DNA database
    dna_db = DNADatabase()
    
    # Create sample user
    user_dna = await dna_db.get_or_create_dna("user_123")
    
    # Simulate transactions to build DNA
    from immune_system_app import create_sample_transaction
    
    print("Building DNA profile with sample transactions...")
    for i in range(20):
        transaction = await create_sample_transaction(
            user_id="user_123",
            amount=np.random.uniform(20, 500),
            location="New York" if i < 15 else "Los Angeles",  # Mostly NY, some LA
            merchant=np.random.choice(["Starbucks", "Amazon", "Walmart", "Target"])
        )
        
        await user_dna.analyze_transaction(transaction)
    
    # Show DNA profile
    profile = user_dna.get_dna_profile()
    print(f"\nDNA Profile for {profile['user_id']}:")
    print(f"DNA Hash: {profile['dna_hash'][:16]}...")
    print(f"Evolution Count: {profile['evolution_count']}")
    
    for seq_type, seq_data in profile['sequences'].items():
        print(f"\n{seq_type.title()}:")
        print(f"  Stability: {seq_data['stability_score']:.2f}")
        print(f"  Genes: {seq_data['gene_count']}")
    
    # Test anomaly detection
    print("\nTesting anomaly detection...")
    
    # Normal transaction
    normal_tx = await create_sample_transaction(
        user_id="user_123",
        amount=85.0,
        location="New York",
        merchant="Starbucks"
    )
    
    normal_anomaly = await user_dna.calculate_anomaly_score(normal_tx)
    print(f"Normal transaction anomaly score: {normal_anomaly:.3f}")
    
    # Anomalous transaction
    anomalous_tx = await create_sample_transaction(
        user_id="user_123",
        amount=5000.0,  # Much larger than usual
        location="Tokyo",  # Different location
        merchant="Unknown Store"  # New merchant
    )
    
    anomalous_score = await user_dna.calculate_anomaly_score(anomalous_tx)
    print(f"Anomalous transaction score: {anomalous_score:.3f}")
    
    print("\n🧬 DNA System Demo Complete!")


if __name__ == "__main__":
    asyncio.run(demo_financial_dna())
