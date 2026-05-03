"""
Groq Client Module (Cloud-Based LLM)
File: backend/groq_client.py
Description: Handles all Groq API communication for cloud deployment
"""

import os
from groq import Groq
import streamlit as st


class GroqClient:
    """Client for Groq API communication (Cloud-based)"""
    
    def __init__(self, api_key=None):
        """
        Initialize Groq client
        
        Args:
            api_key (str): Optional API key for Groq (if not provided, will try to get from secrets/env)
        """
        # Try to get API key from different sources
        if api_key is None:
            # Try Streamlit secrets first (for cloud deployment)
            try:
                api_key = st.secrets["GROQ_API_KEY"]
            except:
                # Try environment variable
                api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            raise ValueError(
                "Groq API key not found. Please set GROQ_API_KEY in "
                "Streamlit secrets or environment variables."
            )
        
        self.client = Groq(api_key=api_key)
        self.available_models = [
            "llama-3.3-70b-versatile",                   # Best all-rounder for summarization
            "llama-3.1-8b-instant",                      # Fast & lightweight
            "openai/gpt-oss-120b",                       # Most powerful, 120B params
            "openai/gpt-oss-20b",                        # Fast, very cost-efficient
            "meta-llama/llama-4-scout-17b-16e-instruct", # Llama 4, latest Meta model
        ]
    
    def check_connection(self):
        """
        Check if Groq API is accessible

        Returns:
            bool: True if connected, False otherwise
        """
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            st.error(f"Groq API connection error: {str(e)}")
            return False
    
    def list_models(self):
        """
        Get list of available models
        
        Returns:
            list: List of model names
        """
        return self.available_models
    
    def generate(self, model, prompt, max_tokens=800, temperature=0.2):
        """
        Generate text using Groq model
        
        Args:
            model (str): Model name to use
            prompt (str): Input prompt
            max_tokens (int): Maximum tokens to generate
            temperature (float): Sampling temperature (0-0.5)
            
        Returns:
            str: Generated text or None if failed
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": 
                                    " You are a high-precision document summarization model,"
                                    "Your task is to summarize PDF content strictly based on the provided text only."
                                    "Mandatory rules (must not be violated):"
                                    "1. Use only the information explicitly present in the document."
                                    "2. Do not infer, assume, or add external knowledge."
                                    "3. Preserve key facts, definitions, steps, formulas, and conclusions."
                                    "4. Remove repetition and non-essential details."
                                    "5. If the document is long, produce a section-wise summary."
                                    "6. If information is missing or unclear, do not guess."
                                    " Accuracy and faithfulness to the source text are the top priority."

 
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=1,
                stream=False
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            st.error(f"Groq API Error: {str(e)}")
            return None
    
    def generate_stream(self, model, prompt, max_tokens=2048, temperature=0.7):
        """
        Generate text with streaming (for real-time display)
        
        Args:
            model (str): Model name to use
            prompt (str): Input prompt
            max_tokens (int): Maximum tokens to generate
            temperature (float): Sampling temperature
            
        Returns:
            generator: Stream of text chunks
        """
        try:
            stream = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at text summarization."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            st.error(f"Groq Streaming Error: {str(e)}")
            yield None


# Alternative: OpenAI Client (if you prefer OpenAI)
class OpenAIClient:
    """OpenAI Client (Alternative to Groq)"""
    
    def __init__(self, api_key=None):
        """Initialize OpenAI client"""
        from openai import OpenAI
        
        if api_key is None:
            try:
                api_key = st.secrets["OPENAI_API_KEY"]
            except:
                api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            raise ValueError("OpenAI API key not found")
        
        self.client = OpenAI(api_key=api_key)
        self.available_models = [
            "gpt-3.5-turbo",
            "gpt-4",
            "gpt-4-turbo-preview"
        ]
    
    def check_connection(self):
        """Check API connection"""
        try:
            self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            return True
        except:
            return False
    
    def list_models(self):
        """List available models"""
        return self.available_models
    
    def generate(self, model, prompt, max_tokens=2048, temperature=0.7):
        """Generate text"""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert summarizer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"OpenAI Error: {str(e)}")
            return None


# HuggingFace Client (Another Alternative)
class HuggingFaceClient:
    """HuggingFace Inference API Client"""
    
    def __init__(self, api_key=None):
        """Initialize HuggingFace client"""
        import requests
        
        if api_key is None:
            try:
                api_key = st.secrets["HUGGINGFACE_API_KEY"]
            except:
                api_key = os.getenv("HUGGINGFACE_API_KEY")
        
        if not api_key:
            raise ValueError("HuggingFace API key not found")
        
        self.api_key = api_key
        self.api_url = "https://api-inference.huggingface.co/models/"
        self.available_models = [
            "facebook/bart-large-cnn",
            "google/flan-t5-large",
            "mistralai/Mistral-7B-Instruct-v0.2"
        ]
    
    def check_connection(self):
        """Check API connection"""
        return True  # Simplified for HF
    
    def list_models(self):
        """List available models"""
        return self.available_models
    
    def generate(self, model, prompt, max_tokens=512):
        """Generate text using HuggingFace"""
        import requests
        
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            payload = {
                "inputs": prompt,
                "parameters": {"max_new_tokens": max_tokens}
            }
            
            response = requests.post(
                self.api_url + model,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list):
                    return result[0].get('generated_text', '')
                return result.get('generated_text', '')
            else:
                st.error(f"HuggingFace Error: {response.status_code}")
                return None
                
        except Exception as e:
            st.error(f"HuggingFace Error: {str(e)}")
            return None