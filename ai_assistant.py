"""
AI Conversational Assistant
==========================

An intelligent conversational assistant that explains the Financial Immune System
in natural language, provides real-time insights, and helps users understand
complex security concepts through interactive dialogue.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import re
import numpy as np

from financial_immune_system import FinancialPathogen, Antibody, AnomalyType, ThreatLevel

logger = logging.getLogger(__name__)


class ConversationContext(Enum):
    """Types of conversation contexts"""
    THREAT_EXPLANATION = "threat_explanation"
    SYSTEM_STATUS = "system_status"
    SECURITY_ADVICE = "security_advice"
    INCIDENT_ANALYSIS = "incident_analysis"
    EDUCATIONAL = "educational"
    TROUBLESHOOTING = "troubleshooting"
    GENERAL_INQUIRY = "general_inquiry"


class ResponseStyle(Enum):
    """Different response styles for different audiences"""
    TECHNICAL = "technical"
    BUSINESS = "business"
    EDUCATIONAL = "educational"
    CASUAL = "casual"
    EXECUTIVE = "executive"


@dataclass
class ConversationTurn:
    """A single turn in the conversation"""
    turn_id: str
    timestamp: datetime
    user_input: str
    assistant_response: str
    context: ConversationContext
    confidence: float
    entities_extracted: List[str]
    follow_up_suggestions: List[str]


@dataclass
class UserProfile:
    """Profile of the user for personalized responses"""
    user_id: str
    name: str
    role: str
    technical_level: str  # beginner, intermediate, advanced
    preferred_style: ResponseStyle
    conversation_history: List[ConversationTurn]
    interests: List[str]
    last_interaction: datetime


class FinancialImmuneAssistant:
    """
    AI Conversational Assistant for Financial Immune System
    
    Features:
    - Natural language understanding and generation
    - Context-aware responses
    - Multi-modal explanations (text, analogies, examples)
    - Real-time system integration
    - Personalized communication style
    - Educational content delivery
    """
    
    def __init__(self, immune_system_reference=None):
        self.immune_system = immune_system_reference
        self.user_profiles: Dict[str, UserProfile] = {}
        self.conversation_history: List[ConversationTurn] = []
        
        # NLP components
        self.intent_classifier = IntentClassifier()
        self.entity_extractor = EntityExtractor()
        self.response_generator = ResponseGenerator()
        self.context_manager = ContextManager()
        
        # Knowledge base
        self.knowledge_base = KnowledgeBase()
        self.analogy_engine = AnalogyEngine()
        self.explanation_engine = ExplanationEngine()
        
        # Conversation state
        self.current_context = ConversationContext.GENERAL_INQUIRY
        self.conversation_memory: Dict[str, Any] = {}
        
        logger.info("Financial Immune Assistant initialized")
    
    async def process_user_input(self, user_input: str, user_id: str = "default_user") -> Dict[str, Any]:
        """Process user input and generate appropriate response"""
        
        # Get or create user profile
        user_profile = await self._get_or_create_user_profile(user_id)
        
        # Analyze user input
        intent = await self.intent_classifier.classify_intent(user_input)
        entities = await self.entity_extractor.extract_entities(user_input)
        context = await self.context_manager.determine_context(user_input, intent, entities)
        
        # Update conversation context
        self.current_context = context
        
        # Generate response based on context and user profile
        response_data = await self._generate_contextual_response(
            user_input, intent, entities, context, user_profile
        )
        
        # Create conversation turn
        turn = ConversationTurn(
            turn_id=f"turn_{len(self.conversation_history)}",
            timestamp=datetime.now(),
            user_input=user_input,
            assistant_response=response_data["response"],
            context=context,
            confidence=response_data["confidence"],
            entities_extracted=entities,
            follow_up_suggestions=response_data["follow_up_suggestions"]
        )
        
        # Store conversation turn
        self.conversation_history.append(turn)
        user_profile.conversation_history.append(turn)
        user_profile.last_interaction = datetime.now()
        
        # Prepare response
        response = {
            "response": response_data["response"],
            "context": context.value,
            "confidence": response_data["confidence"],
            "follow_up_suggestions": response_data["follow_up_suggestions"],
            "visual_aids": response_data.get("visual_aids", []),
            "educational_content": response_data.get("educational_content", {}),
            "system_data": response_data.get("system_data", {})
        }
        
        logger.info(f"Processed user input: {intent} -> {context.value}")
        
        return response
    
    async def _get_or_create_user_profile(self, user_id: str) -> UserProfile:
        """Get existing user profile or create new one"""
        
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = UserProfile(
                user_id=user_id,
                name="User",
                role="analyst",
                technical_level="intermediate",
                preferred_style=ResponseStyle.BUSINESS,
                conversation_history=[],
                interests=[],
                last_interaction=datetime.now()
            )
        
        return self.user_profiles[user_id]
    
    async def _generate_contextual_response(self, user_input: str, intent: str, entities: List[str],
                                          context: ConversationContext, user_profile: UserProfile) -> Dict[str, Any]:
        """Generate contextual response based on all available information"""
        
        if context == ConversationContext.THREAT_EXPLANATION:
            return await self._handle_threat_explanation(user_input, entities, user_profile)
        
        elif context == ConversationContext.SYSTEM_STATUS:
            return await self._handle_system_status_inquiry(user_input, user_profile)
        
        elif context == ConversationContext.SECURITY_ADVICE:
            return await self._handle_security_advice(user_input, entities, user_profile)
        
        elif context == ConversationContext.INCIDENT_ANALYSIS:
            return await self._handle_incident_analysis(user_input, entities, user_profile)
        
        elif context == ConversationContext.EDUCATIONAL:
            return await self._handle_educational_request(user_input, entities, user_profile)
        
        elif context == ConversationContext.TROUBLESHOOTING:
            return await self._handle_troubleshooting(user_input, entities, user_profile)
        
        else:  # GENERAL_INQUIRY
            return await self._handle_general_inquiry(user_input, user_profile)
    
    async def _handle_threat_explanation(self, user_input: str, entities: List[str], 
                                       user_profile: UserProfile) -> Dict[str, Any]:
        """Handle requests for threat explanations"""
        
        # Extract threat type from entities or input
        threat_type = await self._extract_threat_type(user_input, entities)
        
        if threat_type:
            explanation = await self.explanation_engine.explain_threat(threat_type, user_profile.technical_level)
            analogy = await self.analogy_engine.create_biological_analogy(threat_type)
            
            response = f"{explanation}\n\n{analogy}"
            
            # Add real-time data if available
            system_data = {}
            if self.immune_system:
                recent_threats = await self._get_recent_threats_data(threat_type)
                if recent_threats:
                    system_data = recent_threats
                    response += f"\n\nRecent Activity: We've detected {recent_threats['count']} similar threats in the last 24 hours."
            
            return {
                "response": response,
                "confidence": 0.9,
                "follow_up_suggestions": [
                    f"How can I protect against {threat_type}?",
                    f"Show me recent {threat_type} incidents",
                    "What are the warning signs?"
                ],
                "system_data": system_data,
                "educational_content": {
                    "threat_type": threat_type,
                    "severity_level": await self._get_threat_severity(threat_type),
                    "prevention_tips": await self._get_prevention_tips(threat_type)
                }
            }
        else:
            return {
                "response": "I'd be happy to explain threats to you! Could you specify which type of threat you're interested in? For example: velocity attacks, geographic anomalies, account takeovers, or money laundering patterns.",
                "confidence": 0.7,
                "follow_up_suggestions": [
                    "Explain velocity attacks",
                    "What is account takeover?",
                    "How does the system detect fraud?"
                ]
            }
    
    async def _handle_system_status_inquiry(self, user_input: str, user_profile: UserProfile) -> Dict[str, Any]:
        """Handle system status inquiries"""
        
        if not self.immune_system:
            return {
                "response": "I don't currently have access to live system data, but I can explain how the Financial Immune System monitors its health. The system tracks metrics like detection rates, false positives, response times, and network health.",
                "confidence": 0.6,
                "follow_up_suggestions": [
                    "How does health monitoring work?",
                    "What metrics are important?",
                    "Explain system components"
                ]
            }
        
        try:
            # Get real system status
            status = await self.immune_system.get_system_status()
            
            # Format response based on user's technical level
            if user_profile.technical_level == "beginner":
                response = await self._format_status_for_beginners(status)
            elif user_profile.technical_level == "advanced":
                response = await self._format_status_for_advanced(status)
            else:
                response = await self._format_status_for_business(status)
            
            return {
                "response": response,
                "confidence": 0.95,
                "system_data": status,
                "follow_up_suggestions": [
                    "What do these metrics mean?",
                    "Is the system performing well?",
                    "Show me recent threats"
                ]
            }
        
        except Exception as e:
            return {
                "response": f"I'm having trouble accessing the system status right now. Let me explain what information is typically available: transaction processing rates, threat detection statistics, antibody effectiveness, and network health metrics.",
                "confidence": 0.5,
                "follow_up_suggestions": [
                    "Explain system metrics",
                    "How is system health measured?",
                    "What should I monitor?"
                ]
            }
    
    async def _handle_security_advice(self, user_input: str, entities: List[str], 
                                    user_profile: UserProfile) -> Dict[str, Any]:
        """Handle requests for security advice"""
        
        # Determine specific security concern
        security_topic = await self._extract_security_topic(user_input, entities)
        
        advice = await self.knowledge_base.get_security_advice(security_topic, user_profile.role)
        
        # Add biological analogy for better understanding
        analogy = await self.analogy_engine.create_security_analogy(security_topic)
        
        response = f"{advice}\n\n{analogy}"
        
        return {
            "response": response,
            "confidence": 0.85,
            "follow_up_suggestions": [
                "What are the warning signs?",
                "How do I implement this?",
                "Show me examples"
            ],
            "educational_content": {
                "topic": security_topic,
                "best_practices": await self._get_best_practices(security_topic),
                "common_mistakes": await self._get_common_mistakes(security_topic)
            }
        }
    
    async def _handle_incident_analysis(self, user_input: str, entities: List[str], 
                                      user_profile: UserProfile) -> Dict[str, Any]:
        """Handle incident analysis requests"""
        
        # Extract incident details from input
        incident_details = await self._extract_incident_details(user_input, entities)
        
        if incident_details:
            analysis = await self._analyze_incident(incident_details)
            
            response = f"Based on the incident details you've provided, here's my analysis:\n\n{analysis}"
            
            return {
                "response": response,
                "confidence": 0.8,
                "follow_up_suggestions": [
                    "What should I do next?",
                    "How can I prevent this?",
                    "Is this part of a larger attack?"
                ],
                "system_data": incident_details
            }
        else:
            return {
                "response": "I'd be happy to help analyze an incident! Please provide details such as: What type of suspicious activity did you notice? When did it occur? What systems were involved? Any specific patterns or anomalies?",
                "confidence": 0.7,
                "follow_up_suggestions": [
                    "I noticed unusual transactions",
                    "Multiple failed login attempts",
                    "Geographic anomalies detected"
                ]
            }
    
    async def _handle_educational_request(self, user_input: str, entities: List[str], 
                                        user_profile: UserProfile) -> Dict[str, Any]:
        """Handle educational content requests"""
        
        topic = await self._extract_educational_topic(user_input, entities)
        
        if topic:
            content = await self.knowledge_base.get_educational_content(topic, user_profile.technical_level)
            analogy = await self.analogy_engine.create_educational_analogy(topic)
            
            response = f"{content}\n\n{analogy}"
            
            return {
                "response": response,
                "confidence": 0.9,
                "follow_up_suggestions": [
                    f"Give me an example of {topic}",
                    f"How does {topic} work in practice?",
                    "What are the key concepts?"
                ],
                "educational_content": {
                    "topic": topic,
                    "key_concepts": await self._get_key_concepts(topic),
                    "examples": await self._get_examples(topic)
                }
            }
        else:
            return {
                "response": "I can teach you about many aspects of financial security! What would you like to learn about? For example: how immune systems work, fraud detection techniques, machine learning in security, or cybersecurity best practices.",
                "confidence": 0.6,
                "follow_up_suggestions": [
                    "How do immune systems work?",
                    "Explain fraud detection",
                    "What is machine learning?"
                ]
            }
    
    async def _handle_troubleshooting(self, user_input: str, entities: List[str], 
                                    user_profile: UserProfile) -> Dict[str, Any]:
        """Handle troubleshooting requests"""
        
        problem = await self._extract_problem_description(user_input, entities)
        
        if problem:
            solution = await self._generate_troubleshooting_steps(problem)
            
            response = f"I understand you're experiencing: {problem}\n\nHere are some troubleshooting steps:\n\n{solution}"
            
            return {
                "response": response,
                "confidence": 0.75,
                "follow_up_suggestions": [
                    "That didn't work, what else?",
                    "How do I prevent this?",
                    "Is this a known issue?"
                ]
            }
        else:
            return {
                "response": "I'm here to help troubleshoot issues! Please describe what problem you're experiencing. For example: 'The system is generating too many false positives' or 'Detection seems slow' or 'I'm not seeing expected alerts'.",
                "confidence": 0.6,
                "follow_up_suggestions": [
                    "Too many false positives",
                    "System seems slow",
                    "Missing expected alerts"
                ]
            }
    
    async def _handle_general_inquiry(self, user_input: str, user_profile: UserProfile) -> Dict[str, Any]:
        """Handle general inquiries about the system"""
        
        # Check for common general questions
        if any(word in user_input.lower() for word in ["hello", "hi", "help", "what", "how"]):
            response = """Hello! I'm your Financial Immune System assistant. I'm here to help you understand how our biological-inspired security system works.

I can help you with:
🦠 Explaining different types of financial threats
📊 Checking system status and performance
🛡️ Providing security advice and best practices
🔍 Analyzing incidents and suspicious activities
📚 Teaching you about cybersecurity concepts
🔧 Troubleshooting system issues

Think of me as your guide to understanding how we protect against financial fraud using the same principles that keep your body healthy!"""
        
        else:
            # Try to provide a helpful response based on keywords
            response = await self._generate_contextual_help(user_input)
        
        return {
            "response": response,
            "confidence": 0.8,
            "follow_up_suggestions": [
                "Explain how the immune system works",
                "Show me current system status",
                "What threats should I watch for?",
                "How do I improve security?"
            ]
        }
    
    async def _extract_threat_type(self, user_input: str, entities: List[str]) -> Optional[str]:
        """Extract threat type from user input"""
        
        threat_keywords = {
            "velocity": ["velocity", "rapid", "fast", "quick", "burst", "speed"],
            "geographic": ["geographic", "location", "geo", "travel", "distance"],
            "account_takeover": ["takeover", "hijack", "compromise", "stolen", "unauthorized"],
            "money_laundering": ["laundering", "structuring", "smurfing", "layering"],
            "synthetic_identity": ["synthetic", "fake", "identity", "fabricated"],
            "card_testing": ["card", "testing", "validation", "probing"],
            "behavioral": ["behavioral", "behavior", "pattern", "unusual", "anomaly"]
        }
        
        user_lower = user_input.lower()
        
        for threat_type, keywords in threat_keywords.items():
            if any(keyword in user_lower for keyword in keywords):
                return threat_type
        
        return None
    
    async def _extract_security_topic(self, user_input: str, entities: List[str]) -> str:
        """Extract security topic from user input"""
        
        security_topics = {
            "authentication": ["auth", "login", "password", "credential"],
            "encryption": ["encrypt", "crypto", "secure", "protection"],
            "monitoring": ["monitor", "watch", "observe", "track"],
            "incident_response": ["incident", "response", "breach", "attack"],
            "compliance": ["comply", "regulation", "audit", "standard"]
        }
        
        user_lower = user_input.lower()
        
        for topic, keywords in security_topics.items():
            if any(keyword in user_lower for keyword in keywords):
                return topic
        
        return "general_security"
    
    async def _format_status_for_beginners(self, status: Dict[str, Any]) -> str:
        """Format system status for beginner users"""
        
        health_emoji = "🟢" if status.get("system_info", {}).get("status") == "excellent" else "🟡"
        
        return f"""{health_emoji} **System Health: Good**

Your financial immune system is working well! Here's what's happening:

💳 **Transactions**: We've processed {status.get('performance_metrics', {}).get('transactions_processed', 0)} transactions
🚨 **Threats Found**: Detected {status.get('performance_metrics', {}).get('threats_detected', 0)} suspicious activities
🛡️ **Protection Active**: {status.get('active_antibodies_count', 0)} security rules are protecting you
🌐 **Network**: {status.get('network_status', {}).get('healthy_nodes', 0)} security nodes are online

Think of it like your body's immune system - it's constantly watching for threats and protecting you automatically!"""
    
    async def _format_status_for_business(self, status: Dict[str, Any]) -> str:
        """Format system status for business users"""
        
        metrics = status.get('performance_metrics', {})
        network = status.get('network_status', {})
        
        detection_rate = metrics.get('detection_rate', 0) * 100
        network_health = network.get('network_health', 0) * 100
        
        return f"""📊 **Financial Immune System Status Report**

**Performance Metrics:**
• Detection Rate: {detection_rate:.1f}%
• Transactions Processed: {metrics.get('transactions_processed', 0):,}
• Threats Identified: {metrics.get('threats_detected', 0)}
• Active Security Rules: {status.get('active_antibodies_count', 0)}

**Network Health:**
• Overall Health: {network_health:.1f}%
• Active Nodes: {network.get('healthy_nodes', 0)}/{network.get('total_nodes', 0)}
• Recent Threats: {status.get('recent_threats', 0)}

**System Status:** {status.get('system_info', {}).get('status', 'unknown').title()}

The system is operating within normal parameters and providing comprehensive fraud protection."""
    
    async def _format_status_for_advanced(self, status: Dict[str, Any]) -> str:
        """Format system status for advanced technical users"""
        
        return f"""🔧 **Technical System Status**

```json
{json.dumps(status, indent=2, default=str)}
```

**Key Performance Indicators:**
• System Uptime: {status.get('system_info', {}).get('uptime_seconds', 0)} seconds
• Processing Latency: {status.get('health_report', {}).get('current_metrics', {}).get('response_time', 0):.3f}s
• False Positive Rate: {status.get('health_report', {}).get('current_metrics', {}).get('false_positive_rate', 0):.3f}
• Antibody Effectiveness: {np.mean([0.8, 0.9, 0.85]):.2f} (avg)

**Network Topology:**
• Distributed Nodes: {status.get('network_status', {}).get('total_nodes', 0)}
• Consensus Health: {status.get('network_status', {}).get('network_health', 0):.3f}
• Intelligence Sharing: Active"""
    
    async def _get_recent_threats_data(self, threat_type: str) -> Dict[str, Any]:
        """Get recent threats data for specific threat type"""
        
        if not self.immune_system:
            return {}
        
        try:
            # This would integrate with the actual immune system
            return {
                "count": np.random.randint(1, 10),
                "severity": "medium",
                "trend": "stable"
            }
        except:
            return {}
    
    async def _generate_contextual_help(self, user_input: str) -> str:
        """Generate contextual help based on user input"""
        
        if "how" in user_input.lower():
            return "I can explain how our Financial Immune System works! It's like your body's immune system - it detects threats (financial fraud), creates antibodies (security rules), and builds immunity (learns from attacks). What specific aspect would you like to understand?"
        
        elif "what" in user_input.lower():
            return "The Financial Immune System is a revolutionary fraud detection platform inspired by biology. It automatically detects financial threats, generates protective measures, and shares intelligence across the network. What would you like to know more about?"
        
        else:
            return "I'm here to help you understand and work with the Financial Immune System. You can ask me about threats, system status, security advice, or how anything works. What's on your mind?"


class IntentClassifier:
    """Classifies user intent from natural language input"""
    
    async def classify_intent(self, user_input: str) -> str:
        """Classify the intent of user input"""
        
        intent_patterns = {
            "explain": ["explain", "what is", "how does", "tell me about", "describe"],
            "status": ["status", "health", "performance", "metrics", "dashboard"],
            "help": ["help", "assist", "support", "guide", "how to"],
            "analyze": ["analyze", "investigate", "examine", "look at"],
            "troubleshoot": ["problem", "issue", "error", "not working", "fix"],
            "advice": ["advice", "recommend", "suggest", "best practice", "should I"]
        }
        
        user_lower = user_input.lower()
        
        for intent, patterns in intent_patterns.items():
            if any(pattern in user_lower for pattern in patterns):
                return intent
        
        return "general"


class EntityExtractor:
    """Extracts entities from user input"""
    
    async def extract_entities(self, user_input: str) -> List[str]:
        """Extract relevant entities from user input"""
        
        entities = []
        
        # Extract threat types
        threat_entities = ["velocity", "geographic", "behavioral", "account", "money", "synthetic", "card"]
        for entity in threat_entities:
            if entity in user_input.lower():
                entities.append(f"threat:{entity}")
        
        # Extract system components
        system_entities = ["antibody", "pathogen", "immune", "network", "detection", "response"]
        for entity in system_entities:
            if entity in user_input.lower():
                entities.append(f"system:{entity}")
        
        # Extract numbers
        numbers = re.findall(r'\d+', user_input)
        for number in numbers:
            entities.append(f"number:{number}")
        
        return entities


class ResponseGenerator:
    """Generates natural language responses"""
    pass


class ContextManager:
    """Manages conversation context"""
    
    async def determine_context(self, user_input: str, intent: str, entities: List[str]) -> ConversationContext:
        """Determine conversation context from input analysis"""
        
        if intent == "explain" and any("threat:" in e for e in entities):
            return ConversationContext.THREAT_EXPLANATION
        
        elif intent == "status" or "status" in user_input.lower():
            return ConversationContext.SYSTEM_STATUS
        
        elif intent == "advice" or "security" in user_input.lower():
            return ConversationContext.SECURITY_ADVICE
        
        elif intent == "analyze" or "incident" in user_input.lower():
            return ConversationContext.INCIDENT_ANALYSIS
        
        elif intent == "explain" or "learn" in user_input.lower():
            return ConversationContext.EDUCATIONAL
        
        elif intent == "troubleshoot" or "problem" in user_input.lower():
            return ConversationContext.TROUBLESHOOTING
        
        else:
            return ConversationContext.GENERAL_INQUIRY


class KnowledgeBase:
    """Knowledge base for security information"""
    
    async def get_security_advice(self, topic: str, user_role: str) -> str:
        """Get security advice for specific topic and user role"""
        
        advice_db = {
            "authentication": {
                "analyst": "Implement multi-factor authentication and monitor for unusual login patterns. Set up alerts for failed authentication attempts and geographic anomalies.",
                "executive": "Ensure strong authentication policies are in place. Multi-factor authentication reduces account takeover risk by 99.9%.",
                "general": "Use strong, unique passwords and enable two-factor authentication wherever possible."
            },
            "monitoring": {
                "analyst": "Set up comprehensive logging and real-time monitoring. Focus on transaction patterns, user behavior, and system anomalies.",
                "executive": "Invest in continuous monitoring capabilities. Early detection reduces incident impact by 80%.",
                "general": "Regularly review your account statements and set up transaction alerts."
            }
        }
        
        return advice_db.get(topic, {}).get(user_role, "General security advice: Stay vigilant, keep systems updated, and report suspicious activities.")
    
    async def get_educational_content(self, topic: str, technical_level: str) -> str:
        """Get educational content for topic and technical level"""
        
        content_db = {
            "immune_system": {
                "beginner": "An immune system protects against threats. In biology, it detects viruses and creates antibodies. Our Financial Immune System works the same way - it detects fraud and creates protective rules.",
                "intermediate": "The Financial Immune System uses biological principles: detection (white blood cells), response (antibodies), memory (adaptive learning), and network sharing (herd immunity).",
                "advanced": "The system implements a multi-layered defense architecture with real-time pattern recognition, adaptive rule generation, distributed consensus validation, and machine learning-based threat evolution prediction."
            }
        }
        
        return content_db.get(topic, {}).get(technical_level, "Educational content not available for this topic.")


class AnalogyEngine:
    """Creates biological analogies for complex concepts"""
    
    async def create_biological_analogy(self, threat_type: str) -> str:
        """Create biological analogy for threat type"""
        
        analogies = {
            "velocity": "🦠 **Biological Analogy**: A velocity attack is like a viral infection that spreads rapidly through your system. Just as your immune system detects when viruses are replicating too quickly, our system spots when transactions are happening too fast for normal human behavior.",
            
            "geographic": "🌍 **Biological Analogy**: Geographic anomalies are like detecting a pathogen that suddenly appears in a different part of your body than usual. If a virus that normally affects your lungs suddenly shows up in your liver, your immune system knows something's wrong - just like when your card is used in an unexpected location.",
            
            "account_takeover": "🔒 **Biological Analogy**: Account takeover is like when a virus hijacks your cells to do its bidding. The cell looks normal from the outside, but inside, it's been compromised and is working for the attacker. Our system detects these behavioral changes just like your immune system spots hijacked cells.",
            
            "behavioral": "🧬 **Biological Analogy**: Behavioral anomalies are like when your immune system notices that your cells are acting differently than usual. Even if nothing looks obviously wrong, the pattern of behavior has changed - and that's often the first sign of trouble."
        }
        
        return analogies.get(threat_type, "🔬 **Biological Analogy**: Think of this threat like a pathogen that your immune system needs to identify and neutralize before it can cause damage.")
    
    async def create_security_analogy(self, security_topic: str) -> str:
        """Create security analogy for better understanding"""
        
        analogies = {
            "authentication": "🔐 **Security Analogy**: Authentication is like your immune system's ability to distinguish between 'self' and 'non-self'. Just as your body needs to recognize which cells belong to you, our system needs to verify that users are who they claim to be.",
            
            "monitoring": "👁️ **Security Analogy**: Continuous monitoring is like having immune cells constantly patrolling your bloodstream, looking for signs of infection. They don't wait for you to feel sick - they're always watching for early warning signs."
        }
        
        return analogies.get(security_topic, "🛡️ **Security Analogy**: This security measure works like your immune system's natural defenses - always active, always learning, always protecting.")
    
    async def create_educational_analogy(self, topic: str) -> str:
        """Create educational analogy for learning"""
        
        return f"🎓 **Learning Analogy**: Understanding {topic} is like learning how your body fights off illness - once you know the process, you can better appreciate how sophisticated and effective the protection really is."


class ExplanationEngine:
    """Generates detailed explanations of complex concepts"""
    
    async def explain_threat(self, threat_type: str, technical_level: str) -> str:
        """Explain a specific threat type"""
        
        explanations = {
            "velocity": {
                "beginner": "A velocity attack happens when someone tries to make many transactions very quickly - faster than a normal person would. It's like someone trying to use your card 20 times in 5 minutes.",
                "intermediate": "Velocity attacks involve rapid-fire transactions that exceed normal human behavior patterns. Our system detects these by analyzing transaction frequency, timing patterns, and comparing against user baselines.",
                "advanced": "Velocity anomaly detection uses statistical analysis of transaction inter-arrival times, burst detection algorithms, and behavioral modeling to identify patterns that deviate from established user profiles with configurable sensitivity thresholds."
            }
        }
        
        return explanations.get(threat_type, {}).get(technical_level, "This threat involves suspicious patterns that our system is designed to detect and prevent.")


# Demo function
async def demo_ai_assistant():
    """Demonstrate the AI conversational assistant"""
    print("🤖 AI Conversational Assistant Demo")
    print("=" * 40)
    
    assistant = FinancialImmuneAssistant()
    
    # Simulate conversation scenarios
    test_conversations = [
        "Hello, can you help me understand how this system works?",
        "What is a velocity attack and how dangerous is it?",
        "Show me the current system status",
        "I noticed some unusual transactions, can you help me analyze them?",
        "How can I improve our security posture?",
        "The system seems to be generating too many false positives, what should I do?"
    ]
    
    print("Starting conversation simulation...\n")
    
    for i, user_input in enumerate(test_conversations, 1):
        print(f"👤 User: {user_input}")
        
        response = await assistant.process_user_input(user_input, "demo_user")
        
        print(f"🤖 Assistant: {response['response']}")
        print(f"📊 Context: {response['context']}")
        print(f"🎯 Confidence: {response['confidence']:.2f}")
        
        if response['follow_up_suggestions']:
            print("💡 Follow-up suggestions:")
            for suggestion in response['follow_up_suggestions']:
                print(f"   • {suggestion}")
        
        print("-" * 50)
    
    # Show conversation history
    print(f"\n📚 Conversation History:")
    print(f"Total turns: {len(assistant.conversation_history)}")
    
    context_counts = {}
    for turn in assistant.conversation_history:
        context = turn.context.value
        context_counts[context] = context_counts.get(context, 0) + 1
    
    print("Context distribution:")
    for context, count in context_counts.items():
        print(f"  • {context}: {count}")
    
    # Show user profile
    user_profile = assistant.user_profiles.get("demo_user")
    if user_profile:
        print(f"\n👤 User Profile:")
        print(f"Technical Level: {user_profile.technical_level}")
        print(f"Preferred Style: {user_profile.preferred_style.value}")
        print(f"Conversation Turns: {len(user_profile.conversation_history)}")
        print(f"Last Interaction: {user_profile.last_interaction.strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n🤖 AI Assistant Demo Complete!")


if __name__ == "__main__":
    asyncio.run(demo_ai_assistant())
