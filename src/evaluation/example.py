from evaluate import evaluate_technical_answer

# Sample question data
sample_question = {
    "question_text": "How would you implement dynamic batching with Nvidia Triton server for a video analytics system? What are the main challenges involved in this implementation?",
    "category": "Technical",
    "difficulty": "Medium",
    "context": "Dynamic batching is crucial for handling high-throughput data efficiently. This question assesses the ability to integrate advanced technologies like NVIDIA Triton into a real-time system and understand the associated challenges.",
    "expected_points": [
        "Integration of TensorRT with Kubernetes",
        "Understanding of dynamic batching mechanisms",
        "Challenges in managing high throughput without performance degradation"
    ]
}

# Sample answers with different quality levels
sample_answers = {
    "excellent_answer": """
To implement dynamic batching with NVIDIA Triton for video analytics, I would follow these steps:

1. Integration with Kubernetes:
   - Deploy Triton server as a Kubernetes service
   - Use TensorRT for optimized inference
   - Implement horizontal scaling based on load
   - Set up proper resource allocation and monitoring

2. Dynamic Batching Implementation:
   - Configure Triton's dynamic batcher with appropriate parameters
   - Set max batch size based on GPU memory and latency requirements
   - Implement request queuing with timeout mechanisms
   - Use sequence batching for temporal video analysis

3. Performance Optimization:
   - Implement request prioritization
   - Use GPU memory pooling
   - Optimize batch sizes based on workload patterns
   - Monitor and adjust batch parameters dynamically

4. Challenges and Solutions:
   - Latency vs Throughput Trade-off:
     * Implement adaptive batching
     * Use request prioritization
     * Set appropriate timeout values
   
   - Resource Management:
     * Dynamic GPU memory allocation
     * Efficient request queuing
     * Load balancing across instances
   
   - Monitoring and Scaling:
     * Real-time performance metrics
     * Automated scaling based on load
     * Health checks and failover mechanisms
""",
    
    "good_answer": """
For implementing dynamic batching with NVIDIA Triton in video analytics:

1. Basic Setup:
   - Deploy Triton server
   - Configure basic batching parameters
   - Set up Kubernetes deployment

2. Batching Configuration:
   - Set max batch size
   - Configure timeout values
   - Implement basic queuing

3. Challenges:
   - Managing latency
   - Resource allocation
   - Scaling issues
""",
    
    "poor_answer": """
I would use Triton server for video analytics. It's good for batching.
Set up some parameters and it should work.
The main challenge is making it fast.
"""
}

def run_evaluation_examples():
    print("=== Evaluating Excellent Answer ===")
    excellent_result = evaluate_technical_answer(sample_question, sample_answers["excellent_answer"])
    print("\nEvaluation Results:")
    print(f"Traditional Score: {excellent_result['score']} ({excellent_result['score_value']})")
    print("\nTraditional Feedback:")
    print(excellent_result['feedback'])
    print("\nLLM Evaluation:")
    print(f"Score: {excellent_result['llm_score']}")
    print(f"Technical Depth: {excellent_result['llm_technical_depth']}")
    print(f"Clarity: {excellent_result['llm_clarity']}")
    print(f"Completeness: {excellent_result['llm_completeness']}")
    print("\nStrengths:")
    for strength in excellent_result['llm_strengths']:
        print(f"- {strength}")
    print("\nAreas for Improvement:")
    for area in excellent_result['llm_areas_for_improvement']:
        print(f"- {area}")
    
    print("\n=== Evaluating Good Answer ===")
    good_result = evaluate_technical_answer(sample_question, sample_answers["good_answer"])
    print("\nEvaluation Results:")
    print(f"Traditional Score: {good_result['score']} ({good_result['score_value']})")
    print("\nTraditional Feedback:")
    print(good_result['feedback'])
    print("\nLLM Evaluation:")
    print(f"Score: {good_result['llm_score']}")
    print(f"Technical Depth: {good_result['llm_technical_depth']}")
    print(f"Clarity: {good_result['llm_clarity']}")
    print(f"Completeness: {good_result['llm_completeness']}")
    
    print("\n=== Evaluating Poor Answer ===")
    poor_result = evaluate_technical_answer(sample_question, sample_answers["poor_answer"])
    print("\nEvaluation Results:")
    print(f"Traditional Score: {poor_result['score']} ({poor_result['score_value']})")
    print("\nTraditional Feedback:")
    print(poor_result['feedback'])
    print("\nLLM Evaluation:")
    print(f"Score: {poor_result['llm_score']}")
    print(f"Technical Depth: {poor_result['llm_technical_depth']}")
    print(f"Clarity: {poor_result['llm_clarity']}")
    print(f"Completeness: {poor_result['llm_completeness']}")

if __name__ == "__main__":
    run_evaluation_examples() 