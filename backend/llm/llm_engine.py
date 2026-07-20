"""
Modular LLM Engine Module for Gemma2 via Ollama with Rich Educational Fallback Synthesis.
"""

import os
import re
import time
from typing import Optional
from backend.config import LLM_MODEL_NAME, LLM_TEMPERATURE, OLLAMA_BASE_URL
from backend.utils.logger import get_logger

logger = get_logger()

class NCERTLLMEngine:
    """
    Modular wrapper for Gemma2 LLM runtime via Ollama with intelligent educational synthesis fallback.
    """
    def __init__(self, model_name: str = LLM_MODEL_NAME, temperature: float = LLM_TEMPERATURE):
        self.model_name = model_name
        self.temperature = temperature
        self.llm_instance = None
        self._initialize_llm()

    def _initialize_llm(self):
        try:
            from langchain_ollama import OllamaLLM
            self.llm_instance = OllamaLLM(
                model=self.model_name,
                temperature=self.temperature,
                base_url=OLLAMA_BASE_URL
            )
        except ImportError:
            try:
                from langchain_community.llms import Ollama
                self.llm_instance = Ollama(
                    model=self.model_name,
                    temperature=self.temperature,
                    base_url=OLLAMA_BASE_URL
                )
            except Exception as e:
                logger.warning(f"LangChain Ollama initialization deferred: {e}")
                self.llm_instance = None

    def generate_response(self, prompt: str) -> str:
        """
        Executes response generation using Ollama Gemma2 if available, or
        synthesizes a structured, step-by-step educational teacher response from retrieved NCERT context.
        """
        start_time = time.time()
        logger.info("Sending prompt to LLM engine...")

        # Strategy 1: Direct Ollama SDK
        try:
            import ollama
            client = ollama.Client(host=OLLAMA_BASE_URL)
            response = client.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            text_out = response.get("message", {}).get("content", "")
            if text_out:
                elapsed = time.time() - start_time
                logger.info(f"Ollama Gemma2 LLM response generated in {elapsed:.2f}s.")
                return text_out
        except Exception as e:
            logger.warning(f"Ollama chat API call unreachable ({e}). Attempting LangChain LLM invocation...")

        # Strategy 2: LangChain Ollama Instance
        if self.llm_instance:
            try:
                res = self.llm_instance.invoke(prompt)
                if res and str(res).strip():
                    elapsed = time.time() - start_time
                    logger.info(f"LangChain LLM response generated in {elapsed:.2f}s.")
                    return str(res)
            except Exception as e:
                logger.warning(f"LangChain Ollama invocation failed: {e}")

        # Strategy 3: High-Quality Educational Teacher Synthesis Engine (Offline / Cloud Ready)
        logger.info("Synthesizing step-by-step teacher explanation from retrieved NCERT context.")
        elapsed = time.time() - start_time
        return self._synthesize_educational_explanation(prompt)

    def _synthesize_educational_explanation(self, prompt: str) -> str:
        """
        Synthesizes a structured, step-by-step teacher response from the prompt's retrieved NCERT context.
        """
        # Extract Question
        question = "your question"
        if "Student Question:" in prompt:
            question = prompt.split("Student Question:")[1].split("Educational Explanation:")[0].strip()

        # Extract NCERT Context
        context_part = ""
        if "NCERT Context:" in prompt:
            context_part = prompt.split("NCERT Context:")[1].split("Student Question:")[0].strip()

        if not context_part or "NO RELEVANT NCERT TEXTBOOK CONTENT FOUND" in context_part:
            return "I could not find the answer in the provided NCERT textbook resources for your selected class and subject."

        # Clean up lines and extract key sentences
        raw_lines = [line.strip() for line in context_part.split("\n") if line.strip()]
        clean_sentences = []
        for line in raw_lines:
            if line.startswith("[Source"):
                continue
            # Split sentences cleanly
            parts = re.split(r'\.\s+', line)
            for p in parts:
                p_clean = p.strip(" •|-")
                if len(p_clean) > 20 and p_clean not in clean_sentences:
                    clean_sentences.append(p_clean)

        if not clean_sentences:
            return "I could not find clear explanatory details in the NCERT textbook content for this doubt."

        # Build clean Markdown response
        explanation_steps = clean_sentences[:5]
        steps_markdown = "\n".join([f"{idx+1}. **{step if step.endswith('.') else step + '.'}**" for idx, step in enumerate(explanation_steps)])

        response_text = (
            f"### 📘 NCERT Educational Explanation\n\n"
            f"Here is a step-by-step breakdown based directly on your **NCERT textbook content**:\n\n"
            f"{steps_markdown}\n\n"
            f"---\n"
            f"💡 **Teacher Tip:** Re-reading the corresponding chapter diagrams and exercises will help reinforce this concept!\n\n"
            f"*Note: To connect live interactive Gemma2 generative chat, start Ollama locally (`ollama run gemma2:2b`).*"
        )
        return response_text

def load_llm(model_name: str = LLM_MODEL_NAME, temperature: float = LLM_TEMPERATURE) -> NCERTLLMEngine:
    return NCERTLLMEngine(model_name=model_name, temperature=temperature)