"""
Advanced AI Mentor Service using LangChain and Groq
This service provides intelligent coding assistance, personalized learning paths,
and comprehensive code analysis.
"""

import os
import json
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import BaseMemory

import chromadb
from chromadb.utils import embedding_functions
import pandas as pd
import numpy as np

class AdvancedAIMentor:
    """
    Advanced AI Mentor with context awareness, personalized learning, and code analysis
    """
    
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
            
        # Initialize Groq LLM with LangChain - minimal parameters
        try:
            self.llm = ChatGroq(
                api_key=self.groq_api_key,
                model="llama-3.1-8b-instant",  # Using currently available model
                temperature=0.1,  # Low temperature for more focused responses
                max_tokens=4096
            )
            print("✅ Groq LLM initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize Groq LLM: {e}")
            raise e
        
        # Initialize vector database for context storage
        try:
            self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
            self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
            
            # Initialize collections for different types of data
            self._init_vector_collections()
            print("✅ ChromaDB initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize ChromaDB: {e}")
            raise e
        
        # Initialize conversation memory
        try:
            from langchain.memory import ConversationBufferWindowMemory
            self.memory = ConversationBufferWindowMemory(
                k=10,  # Keep last 10 exchanges
                return_messages=True,
                memory_key="chat_history"
            )
            print("✅ Conversation memory initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize memory: {e}")
            self.memory = None
        
        # Load coding patterns and best practices
        self.coding_patterns = self._load_coding_patterns()
        print("✅ Advanced AI Mentor fully initialized")
        
    def _init_vector_collections(self):
        """Initialize vector database collections"""
        if not self.chroma_client:
            return
            
        try:
            # Collection for problem solutions and explanations
            self.solutions_collection = self.chroma_client.create_collection(
                name="coding_solutions",
                embedding_function=self.embedding_function,
                metadata={"description": "Collection of coding problem solutions and explanations"}
            )
        except Exception:
            try:
                self.solutions_collection = self.chroma_client.get_collection("coding_solutions")
            except Exception as e:
                print(f"Warning: Could not initialize solutions collection: {e}")
                self.solutions_collection = None
            
        try:
            # Collection for user conversation history
            self.conversations_collection = self.chroma_client.create_collection(
                name="user_conversations",
                embedding_function=self.embedding_function,
                metadata={"description": "User conversation history for personalization"}
            )
        except Exception:
            try:
                self.conversations_collection = self.chroma_client.get_collection("user_conversations")
            except Exception as e:
                print(f"Warning: Could not initialize conversations collection: {e}")
                self.conversations_collection = None

    def _load_coding_patterns(self) -> Dict[str, Any]:
        """Load common coding patterns and best practices"""
        return {
            "data_structures": {
                "arrays": {
                    "patterns": ["two_pointers", "sliding_window", "prefix_sum"],
                    "complexity": "O(n) time, O(1) space"
                },
                "strings": {
                    "patterns": ["char_frequency", "palindromes", "pattern_matching"],
                    "complexity": "O(n) time, O(1) space typically"
                },
                "trees": {
                    "patterns": ["dfs", "bfs", "traversals"],
                    "complexity": "O(n) time, O(h) space"
                },
                "graphs": {
                    "patterns": ["dijkstra", "union_find", "topological_sort"],
                    "complexity": "Varies by algorithm"
                }
            },
            "algorithms": {
                "sorting": ["merge_sort", "quick_sort", "heap_sort"],
                "searching": ["binary_search", "dfs", "bfs"],
                "dynamic_programming": ["memoization", "tabulation"],
                "greedy": ["activity_selection", "huffman_coding"]
            }
        }

    async def get_personalized_hint(
        self, 
        problem_description: str,
        user_code: str,
        language: str,
        user_id: str,
        hint_level: str = "gentle"
    ) -> Dict[str, Any]:
        """
        Get personalized hints based on user's coding history and current context
        """
        
        # Retrieve user's coding history for personalization
        user_context = await self._get_user_context(user_id)
        
        # Analyze the current code
        code_analysis = await self._analyze_code(user_code, language, problem_description)
        
        # Create context-aware prompt
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=f"""
            You are an expert coding mentor with deep knowledge of algorithms, data structures, 
            and programming best practices. Your goal is to provide personalized, educational hints 
            that guide the user toward the solution without giving it away directly.

            User Context:
            - Programming experience level: {user_context.get('experience_level', 'intermediate')}
            - Preferred learning style: {user_context.get('learning_style', 'step-by-step')}
            - Previous struggles: {user_context.get('common_mistakes', [])}
            - Strong areas: {user_context.get('strengths', [])}

            Current Problem Context:
            Problem: {problem_description}
            User's Current Code: {user_code}
            Language: {language}
            Hint Level: {hint_level} (gentle/direct/detailed)

            Code Analysis:
            {json.dumps(code_analysis, indent=2)}

            Provide a helpful hint that:
            1. Matches the user's experience level
            2. Addresses their specific code issues
            3. Guides them toward the optimal approach
            4. Includes relevant examples or analogies
            5. Suggests next steps based on their learning style
            
            Format your response as clear, actionable guidance.
            """),
            HumanMessage(content="I need a hint for this coding problem. Help me understand what I should focus on next.")
        ])
        
        # Create the chain
        chain = prompt | self.llm | StrOutputParser()
        
        # Get the hint from AI
        response = await chain.ainvoke({})
        
        # Store this interaction for future personalization
        await self._store_interaction(user_id, problem_description, user_code, response, "hint")
        
        # Generate follow-up questions
        follow_up_questions = await self._generate_follow_up_questions(problem_description, user_code, response)
        
        return {
            "hint": response,
            "confidence_score": await self._calculate_confidence_score(user_code, problem_description),
            "suggested_next_steps": await self._suggest_next_steps(code_analysis, user_context),
            "follow_up_questions": follow_up_questions,
            "learning_resources": await self._get_relevant_resources(code_analysis["identified_concepts"]),
            "estimated_completion_time": self._estimate_completion_time(code_analysis, user_context)
        }

    async def analyze_code_quality(
        self, 
        code: str, 
        language: str,
        problem_description: str
    ) -> Dict[str, Any]:
        """
        Comprehensive code quality analysis with specific recommendations
        """
        
        prompt = ChatPromptTemplate.from_template("""
        As a senior software engineer and code reviewer, analyze the following {language} code 
        for a coding problem. Provide a comprehensive review covering:

        Problem: {problem_description}
        Code: {code}

        Please analyze:
        1. **Correctness**: Does the code solve the problem correctly?
        2. **Time Complexity**: What's the current time complexity? Can it be improved?
        3. **Space Complexity**: What's the space usage? Any optimization opportunities?
        4. **Code Style**: Following language conventions and best practices?
        5. **Readability**: Clear variable names, comments, structure?
        6. **Edge Cases**: Are edge cases handled properly?
        7. **Optimization Opportunities**: Specific suggestions for improvement

        Format your response as a structured analysis with specific, actionable feedback.
        Include code snippets for suggested improvements where applicable.
        """)
        
        chain = prompt | self.llm | StrOutputParser()
        
        analysis = await chain.ainvoke({
            "language": language,
            "code": code,
            "problem_description": problem_description
        })
        
        # Extract metrics and recommendations
        return {
            "detailed_analysis": analysis,
            "complexity_analysis": await self._extract_complexity_analysis(analysis),
            "quality_score": await self._calculate_quality_score(code, language),
            "improvement_suggestions": await self._extract_improvements(analysis),
            "optimized_code_snippet": await self._generate_optimized_version(code, language, problem_description)
        }

    async def create_learning_path(
        self, 
        user_id: str,
        current_problem_id: str,
        user_strengths: List[str],
        user_weaknesses: List[str]
    ) -> Dict[str, Any]:
        """
        Create a personalized learning path based on user's current skills and goals
        """
        
        user_context = await self._get_user_context(user_id)
        
        prompt = ChatPromptTemplate.from_template("""
        Create a personalized learning path for a programmer with the following profile:

        Current Skills:
        - Strengths: {strengths}
        - Areas for Improvement: {weaknesses}
        - Experience Level: {experience_level}
        - Learning Style: {learning_style}

        Current Problem Context: {current_problem_id}

        Design a 4-week learning path that:
        1. Builds on their strengths
        2. Systematically addresses weaknesses
        3. Includes specific coding problems to practice
        4. Suggests relevant resources and tutorials
        5. Sets achievable milestones
        6. Adapts to their preferred learning style

        Structure the response with:
        - Week-by-week breakdown
        - Specific topics to focus on
        - Recommended problems (with difficulty progression)
        - Success metrics
        - Additional resources
        """)
        
        chain = prompt | self.llm | StrOutputParser()
        
        learning_path = await chain.ainvoke({
            "strengths": ", ".join(user_strengths),
            "weaknesses": ", ".join(user_weaknesses),
            "experience_level": user_context.get('experience_level', 'intermediate'),
            "learning_style": user_context.get('learning_style', 'hands-on'),
            "current_problem_id": current_problem_id
        })
        
        return {
            "learning_path": learning_path,
            "estimated_duration": "4 weeks",
            "difficulty_progression": await self._create_difficulty_progression(user_weaknesses),
            "checkpoint_problems": await self._recommend_checkpoint_problems(user_weaknesses),
            "success_metrics": await self._define_success_metrics(user_strengths, user_weaknesses)
        }

    async def explain_concept(
        self, 
        concept: str,
        user_level: str = "intermediate",
        include_examples: bool = True,
        programming_language: str = "python"
    ) -> Dict[str, Any]:
        """
        Explain programming concepts with examples and visualizations
        """
        
        prompt = ChatPromptTemplate.from_template("""
        Explain the concept of "{concept}" to a {user_level} level programmer.

        Your explanation should:
        1. Start with a clear, simple definition
        2. Explain WHY this concept is important
        3. Show HOW it works with practical examples
        4. Include {programming_language} code examples
        5. Discuss common use cases and applications
        6. Mention potential pitfalls or common mistakes
        7. Suggest related concepts to explore next

        Make the explanation engaging and educational, using analogies where helpful.
        Include complexity analysis where relevant.
        """)
        
        chain = prompt | self.llm | StrOutputParser()
        
        explanation = await chain.ainvoke({
            "concept": concept,
            "user_level": user_level,
            "programming_language": programming_language
        })
        
        return {
            "explanation": explanation,
            "related_concepts": await self._find_related_concepts(concept),
            "practice_problems": await self._suggest_practice_problems(concept),
            "visual_aids": await self._generate_visual_aids_description(concept),
            "real_world_applications": await self._find_real_world_applications(concept)
        }

    async def debug_code(
        self, 
        code: str,
        language: str,
        error_message: str,
        expected_behavior: str
    ) -> Dict[str, Any]:
        """
        Advanced debugging assistance with step-by-step guidance
        """
        
        prompt = ChatPromptTemplate.from_template("""
        Help debug this {language} code:

        Code:
        {code}

        Error Message: {error_message}
        Expected Behavior: {expected_behavior}

        Provide debugging assistance:
        1. **Root Cause Analysis**: What's causing the issue?
        2. **Step-by-Step Fix**: How to resolve it?
        3. **Prevention**: How to avoid similar issues?
        4. **Testing Strategy**: How to verify the fix?
        5. **Code Review**: Any other potential issues?

        Include corrected code snippets and explain your reasoning.
        """)
        
        chain = prompt | self.llm | StrOutputParser()
        
        debug_analysis = await chain.ainvoke({
            "language": language,
            "code": code,
            "error_message": error_message,
            "expected_behavior": expected_behavior
        })
        
        return {
            "debug_analysis": debug_analysis,
            "suggested_fixes": await self._extract_suggested_fixes(debug_analysis),
            "corrected_code": await self._generate_corrected_code(code, language, debug_analysis),
            "prevention_tips": await self._generate_prevention_tips(error_message, language),
            "testing_suggestions": await self._suggest_test_cases(expected_behavior)
        }

    # Helper methods

    async def _get_user_context(self, user_id: str) -> Dict[str, Any]:
        """Retrieve user context from conversation history"""
        try:
            results = self.conversations_collection.query(
                query_texts=[f"user_id:{user_id}"],
                n_results=10
            )
            
            # Analyze user patterns
            return {
                "experience_level": "intermediate",  # Default, should be determined from history
                "learning_style": "step-by-step",
                "common_mistakes": [],
                "strengths": ["problem-solving"],
                "interaction_count": len(results.get("documents", []))
            }
        except Exception:
            return {
                "experience_level": "intermediate",
                "learning_style": "step-by-step",
                "common_mistakes": [],
                "strengths": [],
                "interaction_count": 0
            }

    async def _analyze_code(self, code: str, language: str, problem: str) -> Dict[str, Any]:
        """Analyze code structure and identify key concepts using AI"""
        
        prompt = ChatPromptTemplate.from_template("""
        Analyze this {language} code for the problem: "{problem}"
        
        Code: {code}
        
        Provide analysis in the following JSON format:
        {{
            "identified_concepts": ["concept1", "concept2"],
            "data_structures_used": ["array", "hashmap"],
            "algorithms_used": ["two_pointers"],
            "complexity_estimate": {{"time": "O(n)", "space": "O(1)"}},
            "code_quality_issues": ["issue1", "issue2"],
            "missing_components": ["error_handling", "edge_cases"],
            "correctness_confidence": 0.8
        }}
        
        Be specific and accurate in your analysis.
        """)
        
        chain = prompt | self.llm | StrOutputParser()
        
        try:
            analysis_str = await chain.ainvoke({
                "language": language,
                "code": code,
                "problem": problem
            })
            
            # Try to parse JSON response, with fallback for malformed JSON
            try:
                return json.loads(analysis_str)
            except json.JSONDecodeError:
                # Extract key information from text response
                return {
                    "identified_concepts": self._extract_concepts_from_text(analysis_str),
                    "data_structures_used": self._extract_data_structures(code),
                    "algorithms_used": self._extract_algorithms(code),
                    "complexity_estimate": {"time": "O(n)", "space": "O(1)"},
                    "code_quality_issues": [],
                    "missing_components": [],
                    "correctness_confidence": 0.7,
                    "ai_analysis": analysis_str
                }
                
        except Exception as e:
            print(f"Error in AI code analysis: {e}")
            # Basic analysis as last resort
            return {
                "identified_concepts": self._extract_concepts_from_text(code),
                "data_structures_used": self._extract_data_structures(code),
                "algorithms_used": self._extract_algorithms(code),
                "complexity_estimate": {"time": "O(n)", "space": "O(1)"},
                "code_quality_issues": [],
                "missing_components": [],
                "correctness_confidence": 0.6
            }

    async def _store_interaction(
        self, 
        user_id: str, 
        problem: str, 
        code: str, 
        response: str, 
        interaction_type: str
    ):
        """Store user interaction for future personalization"""
        try:
            interaction_data = {
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "problem": problem,
                "code_snippet": code,
                "ai_response": response,
                "type": interaction_type
            }
            
            self.conversations_collection.add(
                documents=[json.dumps(interaction_data)],
                metadatas=[{"user_id": user_id, "type": interaction_type}],
                ids=[f"{user_id}_{datetime.now().timestamp()}"]
            )
        except Exception as e:
            print(f"Failed to store interaction: {e}")

    async def _calculate_confidence_score(self, code: str, problem: str) -> float:
        """Calculate confidence score for the current solution"""
        if not code.strip():
            return 0.0
        
        # Basic heuristics - in production, this would be more sophisticated
        score = 0.5  # Base score
        
        if "def " in code or "function " in code:
            score += 0.2
        if len(code.split('\n')) > 3:
            score += 0.1
        if any(keyword in code.lower() for keyword in ['for', 'while', 'if']):
            score += 0.1
        
        return min(score, 1.0)

    async def _suggest_next_steps(self, code_analysis: Dict, user_context: Dict) -> List[str]:
        """Suggest next steps based on code analysis"""
        steps = []
        
        if code_analysis.get('correctness_confidence', 0) < 0.7:
            steps.append("Focus on getting the basic logic correct first")
        
        if 'error_handling' in code_analysis.get('missing_components', []):
            steps.append("Add error handling for edge cases")
        
        if code_analysis.get('complexity_estimate', {}).get('time') in ['O(n²)', 'O(n³)']:
            steps.append("Consider optimizing the time complexity")
        
        return steps

    async def _generate_follow_up_questions(self, problem: str, code: str, hint: str) -> List[str]:
        """Generate relevant follow-up questions"""
        return [
            "What data structure would be most efficient for this problem?",
            "Can you identify any edge cases that need special handling?",
            "How would you test this solution with different inputs?"
        ]

    async def _get_relevant_resources(self, concepts: List[str]) -> List[Dict[str, str]]:
        """Get relevant learning resources for identified concepts"""
        resources = []
        for concept in concepts[:3]:  # Limit to top 3
            resources.append({
                "title": f"Understanding {concept.replace('_', ' ').title()}",
                "type": "tutorial",
                "url": f"https://example.com/learn/{concept}",
                "description": f"Comprehensive guide to {concept}"
            })
        return resources

    def _estimate_completion_time(self, code_analysis: Dict, user_context: Dict) -> str:
        """Estimate time to completion based on current progress"""
        confidence = code_analysis.get('correctness_confidence', 0.5)
        
        if confidence > 0.8:
            return "5-10 minutes"
        elif confidence > 0.5:
            return "15-30 minutes"
        else:
            return "30-60 minutes"

    # Additional helper methods would be implemented here...
    async def _extract_complexity_analysis(self, analysis: str) -> Dict[str, str]:
        """Extract complexity information from analysis"""
        return {"time": "O(n)", "space": "O(1)"}  # Simplified

    async def _calculate_quality_score(self, code: str, language: str) -> float:
        """Calculate overall code quality score"""
        return 0.75  # Simplified

    async def _extract_improvements(self, analysis: str) -> List[str]:
        """Extract improvement suggestions from analysis"""
        return ["Add comments", "Handle edge cases"]  # Simplified

    async def _generate_optimized_version(self, code: str, language: str, problem: str) -> str:
        """Generate optimized version of the code"""
        return f"# Optimized {language} solution would be generated here"

    async def _create_difficulty_progression(self, weaknesses: List[str]) -> List[str]:
        """Create difficulty progression for learning path"""
        return ["Easy", "Medium", "Hard"]

    async def _recommend_checkpoint_problems(self, weaknesses: List[str]) -> List[Dict]:
        """Recommend problems for checkpoints"""
        return [{"title": "Two Sum", "difficulty": "Easy", "concepts": ["arrays", "hashmaps"]}]

    async def _define_success_metrics(self, strengths: List[str], weaknesses: List[str]) -> Dict:
        """Define success metrics for learning path"""
        return {"problems_solved": 20, "accuracy_rate": 0.8, "avg_time_improvement": "30%"}

    async def _find_related_concepts(self, concept: str) -> List[str]:
        """Find related programming concepts"""
        return ["arrays", "sorting", "searching"]  # Simplified

    async def _suggest_practice_problems(self, concept: str) -> List[Dict]:
        """Suggest practice problems for concept"""
        return [{"title": "Array Sum", "difficulty": "Easy"}]

    async def _generate_visual_aids_description(self, concept: str) -> str:
        """Generate description of visual aids"""
        return f"Visual representation of {concept} would help understanding"

    async def _find_real_world_applications(self, concept: str) -> List[str]:
        """Find real-world applications of concept"""
        return [f"{concept} is used in database indexing", f"{concept} powers search algorithms"]

    async def _extract_suggested_fixes(self, debug_analysis: str) -> List[str]:
        """Extract suggested fixes from debug analysis"""
        return ["Check array bounds", "Initialize variables properly"]

    async def _generate_corrected_code(self, code: str, language: str, debug_analysis: str) -> str:
        """Generate corrected version of the code"""
        return f"# Corrected {language} code\n# Based on debug analysis"

    async def _generate_prevention_tips(self, error_message: str, language: str) -> List[str]:
        """Generate tips to prevent similar errors"""
        return ["Always validate input", "Use proper error handling"]

    async def _suggest_test_cases(self, expected_behavior: str) -> List[Dict]:
        """Suggest test cases based on expected behavior"""
        return [{"input": "[1,2,3]", "expected": "6", "description": "Basic case"}]

    def _extract_concepts_from_text(self, text: str) -> List[str]:
        """Extract programming concepts from text analysis"""
        concepts = []
        text_lower = text.lower()
        
        concept_keywords = {
            "arrays": ["array", "list", "index"],
            "hash_tables": ["hash", "map", "dict", "dictionary"],
            "trees": ["tree", "node", "binary", "bst"],
            "graphs": ["graph", "vertex", "edge", "dfs", "bfs"],
            "sorting": ["sort", "merge", "quick", "heap"],
            "searching": ["search", "binary search", "find"],
            "dynamic_programming": ["dp", "dynamic", "memo", "cache"],
            "greedy": ["greedy", "optimal", "local"],
            "two_pointers": ["two pointer", "left", "right", "pointer"],
            "sliding_window": ["window", "slide", "subarray"]
        }
        
        for concept, keywords in concept_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                concepts.append(concept)
        
        return concepts[:5]  # Limit to top 5 concepts

    def _extract_data_structures(self, code: str) -> List[str]:
        """Extract data structures used in code"""
        structures = []
        code_lower = code.lower()
        
        if any(keyword in code_lower for keyword in ['[]', 'array', 'list']):
            structures.append("array")
        if any(keyword in code_lower for keyword in ['{}', 'dict', 'map', 'hashmap']):
            structures.append("hashmap")
        if any(keyword in code_lower for keyword in ['set(', 'set']):
            structures.append("set")
        if any(keyword in code_lower for keyword in ['stack', 'append', 'pop']):
            structures.append("stack")
        if any(keyword in code_lower for keyword in ['queue', 'deque']):
            structures.append("queue")
        if 'class' in code_lower and 'node' in code_lower:
            structures.append("tree")
            
        return structures

    def _extract_algorithms(self, code: str) -> List[str]:
        """Extract algorithms used in code"""
        algorithms = []
        code_lower = code.lower()
        
        if 'for' in code_lower or 'while' in code_lower:
            algorithms.append("iteration")
        if 'sort' in code_lower:
            algorithms.append("sorting")
        if any(keyword in code_lower for keyword in ['left', 'right']) and 'pointer' in code_lower:
            algorithms.append("two_pointers")
        if 'recursive' in code_lower or code.count('def') > 1:
            algorithms.append("recursion")
        if 'memo' in code_lower or 'cache' in code_lower:
            algorithms.append("memoization")
            
        return algorithms
