"""
Cloud-Based AI Summarizer Module
File: backend/cloud_summarizer.py
Description: AI-powered text summarization using cloud APIs
"""


class CloudAISummarizer:
    """AI-powered text summarization using cloud LLMs"""
    
    def __init__(self, llm_client):
        """
        Initialize Cloud AI Summarizer
        
        Args:
            llm_client: Instance of GroqClient, OpenAIClient, or HuggingFaceClient
        """
        self.llm = llm_client
    
    def _truncate_text(self, text, max_chars=12000):
        """
        Truncate text to fit within context window
        
        Args:
            text (str): Input text
            max_chars (int): Maximum characters
            
        Returns:
            str: Truncated text
        """
        if len(text) <= max_chars:
            return text
        
        # Truncate at sentence boundary if possible
        truncated = text[:max_chars]
        last_period = truncated.rfind('.')
        if last_period > max_chars * 0.8:  # If close to end
            return truncated[:last_period + 1]
        return truncated
    
    def summarize_extractive(self, text, model, length="medium"):
        """
        Extractive summarization - AI selects key sentences
        
        Args:
            text (str): Input text to summarize
            model (str): Model name to use
            length (str): Summary length (short/medium/long)
            
        Returns:
            str: Extractive summary
        """
        length_map = {
            "short": "7-8 key sentences",
            "medium": "10-12 key sentences",
            "long": "12-15 key sentences"
        }
        
        # Truncate text to fit context window
        text = self._truncate_text(text)
        
        prompt = f"""You are an expert at extractive text summarization. Your task is to create a summary by selecting and combining the most important sentences from the original text.

TEXT TO SUMMARIZE:
{text}

INSTRUCTIONS:
Select {length_map[length]} from the original text that capture the main ideas and essential information.

RULES:
1. Use ONLY sentences or phrases from the original text
2. Do NOT create new sentences or paraphrase
3. Select sentences that contain the most important information
4. Maintain the original order when possible
5. Ensure the summary flows naturally
6. Focus on key facts, findings, and conclusions

EXTRACTIVE SUMMARY:"""
        
        return self.llm.generate(model, prompt, max_tokens=1024)
    
    def summarize_abstractive(self, text, model, length="medium"):
        """
        Abstractive summarization - AI generates new summary
        
        Args:
            text (str): Input text to summarize
            model (str): Model name to use
            length (str): Summary length (short/medium/long)
            
        Returns:
            str: Abstractive summary
        """
        length_map = {
            "short": "7-8 sentences (approximately 70-80 words)",
            "medium": "10-12 sentences (approximately 120-150 words)",
            "long": "12-15 sentences (approximately 200-300 words)"
        }
        
        # Truncate text
        text = self._truncate_text(text)
        
        prompt = f"""You are an expert at abstractive text summarization. Your task is to read and understand the text, then create a new summary in your own words.

TEXT TO SUMMARIZE:
{text}

INSTRUCTIONS:
Write a {length_map[length]} summary in your own words.

RULES:
1. Read and understand the entire text
2. Identify the main ideas, key points, and important details
3. Write a NEW summary in your own words (do not copy sentences verbatim)
4. Ensure the summary is coherent and flows naturally
5. Preserve the meaning and critical information
6. Use clear, concise language
7. Focus on what matters most

ABSTRACTIVE SUMMARY:"""
        
        return self.llm.generate(model, prompt, max_tokens=1024, temperature=0.7)
    
    def summarize_bullet_points(self, text, model):
        """
        Create bullet-point summary
        
        Args:
            text (str): Input text to summarize
            model (str): Model name to use
            
        Returns:
            str: Bullet-point summary
        """
        text = self._truncate_text(text)
        
        prompt = f"""You are an expert at creating concise bullet-point summaries. Extract the key points from the following text.

TEXT TO SUMMARIZE:
{text}

INSTRUCTIONS:
1. Create 6-10 bullet points
2. Each point should be one clear, complete sentence
3. Focus on the most important information
4. Use parallel structure
5. Start each bullet with a dash (-)

BULLET-POINT SUMMARY:"""
        
        return self.llm.generate(model, prompt, max_tokens=1024)
    
    def summarize_with_questions(self, text, model):
        """
        Question-based analytical summary
        
        Args:
            text (str): Input text to summarize
            model (str): Model name to use
            
        Returns:
            str: Question-based summary
        """
        text = self._truncate_text(text)
        
        prompt = f"""Analyze the following text and create a summary by answering these key questions:

TEXT:
{text}

Create a summary that answers:
1. What is the main topic or thesis?
2. What are the key arguments or findings?
3. What evidence or examples are provided?
4. What are the conclusions or implications?
5. What are the limitations or future directions (if mentioned)?

Provide a cohesive summary addressing these questions in paragraph form:"""
        
        return self.llm.generate(model, prompt, max_tokens=1024)
    
    def get_key_insights(self, text, model):
        """
        Extract key insights and takeaways
        
        Args:
            text (str): Input text to summarize
            model (str): Model name to use
            
        Returns:
            str: Key insights summary
        """
        text = self._truncate_text(text)
        
        prompt = f"""You are an expert analyst. Read the following text and extract the most important insights and takeaways.

TEXT:
{text}

Provide:
1. TOP 3-5 KEY INSIGHTS (clearly numbered)
2. MAIN TAKEAWAYS (what should readers remember?)
3. PRACTICAL IMPLICATIONS (if applicable)

Format your response with clear headers and make it actionable:"""
        
        return self.llm.generate(model, prompt, max_tokens=1024)
    
    def custom_summarize(self, text, model, custom_prompt):
        """
        Custom summarization with user-provided prompt
        
        Args:
            text (str): Input text to summarize
            model (str): Model name to use
            custom_prompt (str): Custom instructions
            
        Returns:
            str: Custom summary
        """
        text = self._truncate_text(text)
        
        full_prompt = f"""TEXT TO SUMMARIZE:
{text}

INSTRUCTIONS:
{custom_prompt}

SUMMARY:"""
        
        return self.llm.generate(model, full_prompt, max_tokens=1024)
